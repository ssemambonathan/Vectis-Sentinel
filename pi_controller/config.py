"""
Configuration parameters for camera resolution, serial ports, and PID/step scaling.
"""

SERIAL_PORT = "/dev/ttyUSB0"  # Update to your Arduino port (e.g., /dev/ttyACM0)
BAUD_RATE = 115200

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Control scaling factors to map pixel offset to motor steps
SCALE_X = 0.05
SCALE_Y = 0.05

# Deadzone bounds to prevent jitter around target center
DEADZONE = 10
