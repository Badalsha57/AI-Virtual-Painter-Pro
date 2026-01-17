import cv2
import numpy as np
import mediapipe as mp
import time

# 1. Mediapipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(model_complexity=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# 2. Canvas aur Resolution
wCam, hCam = 1280, 720
canvas = np.zeros((hCam, wCam, 3), dtype=np.uint8)

# --- SMOOTHING VARIABLES ---
px, py = 0, 0  # Purane points
curr_x, curr_y = 0, 0  # Filtered current points
smooth_factor = 0.25  # 0 se 1 ke beech (Jitna kam, utni smooth line)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

while cap.isOpened():
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            lm = hand_lms.landmark

            # Fingers Check
            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y

            # Raw Coordinates
            rx, ry = int(lm[8].x * wCam), int(lm[8].y * hCam)

            # --- EMA FILTER (SHAKING CONTROL) ---
            # Yeh line shaking ko khatam karti hai
            if curr_x == 0 and curr_y == 0:
                curr_x, curr_y = rx, ry
            else:
                curr_x = int(curr_x + smooth_factor * (rx - curr_x))
                curr_y = int(curr_y + smooth_factor * (ry - curr_y))

            # --- MODE SELECTION ---

            # 1. ERASER: Index + Middle Finger
            if index_up and middle_up:
                px, py = 0, 0
                cv2.circle(img, (curr_x, curr_y), 40, (255, 255, 255), cv2.FILLED)
                cv2.circle(canvas, (curr_x, curr_y), 80, (0, 0, 0), cv2.FILLED)
                cv2.putText(img, "ERASER", (curr_x - 40, curr_y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 2. DRAWING: Only Index Finger
            elif index_up:
                cv2.circle(img, (curr_x, curr_y), 10, (255, 0, 255), cv2.FILLED)

                if px == 0 and py == 0:
                    px, py = curr_x, curr_y

                # Jitter Protection: Sirf tab likho jab ungli 2 pixel se zyada hile
                dist = np.hypot(curr_x - px, curr_y - py)
                if 2 < dist < 80:
                    cv2.line(canvas, (px, py), (curr_x, curr_y), (255, 0, 255), 10, cv2.LINE_AA)
                    px, py = curr_x, curr_y

            else:
                px, py = 0, 0
                curr_x, curr_y = 0, 0  # Reset filter when finger is down

    # Final Merging
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    cv2.imshow("Ultra Smooth Painter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()