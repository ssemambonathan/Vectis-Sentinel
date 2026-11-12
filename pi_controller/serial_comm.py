import serial
import time
from .config import SERIAL_PORT, BAUD_RATE

class SerialBridge:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
            time.sleep(2) # Allow Arduino reset
            print(f"[Serial] Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        except Exception as e:
            print(f"[Serial Error] Failed to connect: {e}")
            self.ser = None

    def send_vector(self, dx: int, dy: int):
        if self.ser and self.ser.is_open:
            command = f"X{dx}Y{dy}\n"
            self.ser.write(command.encode('utf-8'))

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
