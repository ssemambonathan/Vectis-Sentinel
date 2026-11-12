import cv2
import numpy as np
from .config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, DEADZONE, SCALE_X, SCALE_Y
from .serial_comm import SerialBridge

def run_tracker():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    bridge = SerialBridge()
    
    # Background subtractor for motion detection
    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=False)

    print("[Tracker] Starting video stream loop. Press 'q' to exit.")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Flip for mirror view if needed, convert to gray/blur
            frame = cv2.flip(frame, 1)
            fgmask = fgbg.apply(frame)

            # Remove noise via morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

            # Find contours of moving objects
            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            frame_center_x = FRAME_WIDTH // 2
            frame_center_y = FRAME_HEIGHT // 2

            # Draw center crosshair
            cv2.line(frame, (frame_center_x - 10, frame_center_y), (frame_center_x + 10, frame_center_y), (0, 255, 0), 2)
            cv2.line(frame, (frame_center_x, frame_center_y - 10), (frame_center_x, frame_center_y + 10), (0, 255, 0), 2)

            target_found = False
            if contours:
                # Find largest moving contour
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                if area > 100:  # Minimum threshold area filter
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    target_x = x + w // 2
                    target_y = y + h // 2
                    target_found = True

                    # Draw bounding box and tracking point
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.circle(frame, (target_x, target_y), 5, (255, 0, 0), -1)

                    # Compute offset relative to screen center
                    error_x = target_x - frame_center_x
                    error_y = target_y - frame_center_y

                    # Apply deadzone filtering
                    dx = int(error_x * SCALE_X) if abs(error_x) > DEADZONE else 0
                    dy = int(error_y * SCALE_Y) if abs(error_y) > DEADZONE else 0

                    # Transmit motor command vector via Serial
                    bridge.send_vector(dx, dy)

            cv2.imshow("Vectis-Sentinel Tracking Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        bridge.close()
        print("[Tracker] Shutdown complete.")

if __name__ == "__main__":
    run_tracker()
