import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands.Hands()
draw_utils = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
finger_counter = 0
finger_tips = [8, 12, 16, 20]
while True :
    finger_counter = 0
    success , frame =cap.read()
    if not success:
        break
    
    framRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(framRGB)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            #draw_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmark = hand.landmark
            
            for tip in finger_tips:
                if landmark[tip].y < landmark[tip-2].y:
                    finger_counter += 1
            if landmark[4].x < landmark[3].x:
                finger_counter += 1        
    cv2.putText(frame, str(finger_counter), (50,100), cv2.FONT_HERSHEY_COMPLEX, 3, (0,0,255), 3)
    
    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()    