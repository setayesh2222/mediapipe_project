import cv2
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
draw_utils = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    framRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            draw_utils.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            landmarks = hand.landmark
            finger_counter = 0

            if landmarks[8].y < landmarks[6].y:
                finger_counter += 1
            if landmarks[12].y < landmarks[10].y:
                finger_counter += 1
            if landmarks[16].y < landmarks[14].y:
                finger_counter += 1
            if landmarks[20].y < landmarks[18].y:
                finger_counter += 1
            if landmarks[4].x < landmarks[3].x:
                finger_counter += 1

            cv2.putText(frame, str(finger_counter), (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)

            if finger_counter == 3:
                volume.SetMasterVolumeLevelScalar(0.2, None)
            elif finger_counter == 1:
                volume.SetMasterVolumeLevelScalar(0.8, None)

    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()