import csv
import threading

from pymodbus.client import ModbusTcpClient, ModbusSerialClient
import time
import signal
import sys

# Modbus Client 클래스 코드



class ModbusClient:
    def __init__(self, device_name, port):
        self.isConnected = False
        self.device_name = device_name
        self.port = port
        try:
            self.client = ModbusTcpClient(host='127.0.0.1', port=self.port)
            self.isConnected = True
        except Exception as e:
            print(f"An error occurred: {e}")

    def callback(self):
        while self.isConnected:
            self.read_data()
        print("finished {}".format(threading.current_thread().name))

    def read_data(self):
        if self.isConnected:
            # Example read: Reading holding registers from address 0, count 1
            response = self.client.read_input_registers(100, 10 ,slave=1)
            if not response.isError():
                print(f"Server on port {self.port}: {response.registers}")
            else:
                print(f"Error reading from server on port {self.port}")
            self.client.close()
        else:
            print(f"Unable to connect to server on port {self.port}")
    def write_data(self):
        if self.isConnected:
            result = self.client.write_registers(100,[20,0,0,0], skip_encode=False, slave=1)
            if result.isError():
                print("error")
    def stop_client(self):
        self.client.close()

