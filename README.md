# Vectis-Sentinel
High-precision, dual-tier computer vision tracking and gimbal positioning framework leveraging a Raspberry Pi for real-time OpenCV motion vector extraction and an Arduino microcontroller for low-level stepper motor kinematics.
# Vectis-Sentinel 🛡️⚡

`Vectis-Sentinel` is an open-source, dual-architecture hardware-software prototype designed to track moving targets in real time using computer vision and direct the precise alignment of a motorized gimbal system via serial communication.

## System Architecture
* **Vision & Processing Unit (Master):** Raspberry Pi running Python & OpenCV. Captures video frames, performs background subtraction and contour tracking, calculates spatial offset deltas ($dX, dY$), and transmits movement commands.
* **Actuation Unit (Slave):** Arduino microcontroller parsing serial vectors and driving high-resolution stepper motors via step/direction drivers.

---

## Setup & Installation

### 1. Raspberry Pi Environment
Clone the repository and install dependencies:
```bash
git clone [https://github.com/yourusername/Vectis-Sentinel.git](https://github.com/yourusername/Vectis-Sentinel.git)
cd Vectis-Sentinel
pip install -r requirements.txt
