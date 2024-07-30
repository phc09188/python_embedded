#!/usr/bin/env python3
"""
Modbus Server
used by ems application test

"""
import asyncio
import threading
import time

from pymodbus.client import ModbusTcpClient
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.server import StartAsyncTcpServer, StartAsyncSerialServer


class CallbackDataBlock(ModbusSequentialDataBlock):
    """A datablock that stores the new value in memory,.

    and passes the operation to a message queue for further processing.
    """

    def __init__(self, queue, addr, values):
        """Initialize."""
        self.queue = queue
        self.val = 0
        super().__init__(addr, values)

    def setValues(self, address, value):
        """Set the requested values of the datastore."""
        super().setValues(address, value)
        #txt = f"Callback from setValues with address {address}, value {value}"
        #_logger.debug(txt)

    def getValues(self, address, count=1):
        """Return the requested values from the datastore."""
        result = super().getValues(address, count=count)
        #txt = f"Callback from getValues with address {address}, count {count}, data {result}"
        #_logger.debug(txt)
        self.setValues(1, self.val)
        self.val += 1
        print(self.val)
        return result

    def validate(self, address, count=1):
        """Check to see if the request is in range."""
        result = super().validate(address, count=count)
        #txt = f"Callback from validate with address {address}, count {count}, data {result}"
        #_logger.debug(txt)
        return result


class ModbusServer:
    def __init__(self,port):
        queue = asyncio.Queue()
        self.context = ModbusSlaveContext(di=CallbackDataBlock(queue, 0x00, [0] * 65535), co=CallbackDataBlock(queue, 0x00, [0] * 65535),
                                          hr=CallbackDataBlock(queue, 0x00, [0] * 65535), ir=CallbackDataBlock(queue, 0x00, [0] * 65535))
        self.port = port
        thread = threading.Thread(
            target=self.startModbusServer, name="modbusServer")
        thread.daemon = True  # True면 Main이 끝나면 자동 종료
        thread.start()

    async def runAsyncServer(self):
        msContext = ModbusServerContext(slaves=self.context, single=True)
        svr = await StartAsyncSerialServer(msContext, port=self.port, baudrate=9600)
        # 포트가 1024보다 작을 경우는 root 권한 필요.
        return svr

    def startModbusServer(self):
        global stat
        modServer = self.runAsyncServer()
        asyncio.run(modServer, debug=False)

    def writeReg(self, fc_code,addr, val):
        global stat
        self.context.setValues(fc_code, addr, [val])

    def readRegs(self,fc_code, addr, cnt):
        data = self.context.getValues(fc_code, addr, count=cnt)
        # print("===== read ")
        # print(data)
        return data

