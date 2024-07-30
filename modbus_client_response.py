from pymodbus.client import ModbusTcpClient
import time
import signal
import sys

# Modbus Client 연결 테스트 코드

clients = ModbusTcpClient('localhost', port=1502)


# Handle interrupt signals
def signal_handler(sig, frame):
    print("\nInterrupt received, stopping client read loop.")
    # Close all clients gracefully
    client.close()
    sys.exit(0)

# Register signal handlers for graceful termination
signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signals

# Periodically read data from the clients
try:
    while True:
        response = clients.read_input_registers(100,10)
        print(response.registers)
        time.sleep(0.5)
except Exception as e:
    print(f"An error occurred: {e}")
    # Close all clients in case of an error
    client.close()
    sys.exit(1)