import random
import time
import cv2
import mediapipe as mp

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)


random.seed(1234)

def is_finger_up(fingername: str):
    # Get landmark coordinates

    i_tip, i_pip, i_mcp = -1, -1, -1

    if fingername=="index":
        i_tip = 8
        i_pip = 6
        i_mcp = 5
    elif fingername=="thumb":
        i_tip = 4
        i_pip = 3
        i_mcp = 2
    elif fingername=="middle":
        i_tip = 12
        i_pip = 10
        i_mcp = 9
    elif fingername=="ring":
        i_tip = 16
        i_pip = 14
        i_mcp = 13
    elif fingername=="pinky":
        i_tip = 20
        i_pip = 18
        i_mcp = 17
    else:
        print("error")

    index_tip = hand_landmarks.landmark[i_tip]   # Index Finger Tip
    index_pip = hand_landmarks.landmark[i_pip]   # Index Finger PIP
    index_mcp = hand_landmarks.landmark[i_mcp]   # Index Finger MCP

    # Convert normalized coordinates to pixel values
    h, w, _ = frame.shape
    index_tip_y = int(index_tip.y * h)
    index_pip_y = int(index_pip.y * h)
    index_mcp_y = int(index_mcp.y * h)

    tolerance = 0.01

    # Check if the index finger is upd
    if fingername=="thumb":
        return  index_tip.x*w > index_pip.x*w and index_pip.x*w > index_mcp.x*w
    else:
        return index_tip_y < index_pip_y and index_tip_y < index_mcp_y


def return_number():
    ans = -1
    if is_finger_up('thumb'):
        ans = 6
        if is_finger_up('index'): ans = 7
        if is_finger_up('middle'): ans = 8
        if is_finger_up('ring'): ans = 9
        if is_finger_up('pinky'): ans = 5
    else:
        if is_finger_up('index'): ans = 1
        if is_finger_up('middle'): ans = 2
        if is_finger_up('ring'): ans = 3
        if is_finger_up('pinky'): ans = 4
    return ans

def play_system():
    return random.choice([i for i in range(1,6)])

def toss_winner():
    res = toss_system_num + toss_user_num
    print('toss res: ', res)
    if res%2==0:
        if toss=='odd': return 'system'
        else: return 'user'
    else:
        if toss=='odd': return 'user'
        else: return 'system'

toss = input('odd or even? ')
toss_system_num = play_system()
batting = ''
bowling = ''

# Timer Variables
start_time = time.time()
timer_duration = 5  # Countdown from 5 to 1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    countdown = max(5 - int(elapsed_time), 0)

    # Show countdown on the SAME frame
    cv2.putText(frame, str(countdown), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame with the countdown
    cv2.imshow('Hand Tracking', frame)
    
    # Wait for 1ms to allow the display to update
    key = cv2.waitKey(1) & 0xFF

    # If countdown has finished, continue with hand tracking
    if countdown == 0:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            print("yes")
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            toss_user_num = return_number()
            #cv2.tex
            cv2.putText(frame, 'user choice: ' + str(toss_user_num), (50, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, 'system choice: ' + str(toss_system_num), (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Hand Tracking', frame)
            cv2.waitKey(500)

            print('user choice: ', str(toss_user_num))
            print('system choice:', str(toss_system_num))

            if toss_winner() == 'system':
                bat_bowl_choice = random.choice(['bat', 'bowl'])
                print('System wins! chooses to', bat_bowl_choice)
                batting, bowling = ('system', 'user') if bat_bowl_choice == 'bat' else ('user', 'system')
            else:
                print('User wins! Choose bat (b) or bowl (v):')
                while True:
                    key = cv2.waitKey(0) & 0xFF  # Wait for key press instead of blocking `input()`
                    if key == ord('b'):
                        batting, bowling = 'system', 'user'
                        break
                    elif key == ord('v'):  # Example key for batting
                        batting, bowling = 'user', 'system'
                        break
            print(f'{batting} bats and {bowling} bowls...(press any key to close)')

        # Display the frame after processing
        cv2.imshow('Hand Tracking', frame)
        cv2.waitKey(0)  # Allow display refresh
        break

    # Press 'q' to exit
    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

score = 0

cap = cv2.VideoCapture(0)
start_time = time.time()
timer_duration = 3  # Countdown from 5 to 1
out = False

while True:
    start_time = time.time()  # Start countdown
    while True:
        elapsed_time = time.time() - start_time
        countdown = max(3 - int(elapsed_time), 0)

        ret, frame = cap.read()
        if not ret:
            break

        # Display countdown on frame
        cv2.putText(frame, str(countdown), (100, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow(f'{batting} batting', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

        if countdown == 0:
            break  # Exit countdown loop

    # Capture frame and detect hand
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get user and system numbers
        toss_user_num = return_number()
        toss_system_num = play_system()

        # Check if user and system numbers match
        if toss_user_num == toss_system_num:
            out = True
        else:
            if batting == 'system': 
                score += toss_system_num
            else: 
                score += toss_user_num
        
        # Display both numbers
        cv2.putText(frame, f'User: {toss_user_num}', (50, 85), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'System: {toss_system_num}', (50, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.putText(frame, f'{batting}\'s score: {score}', (50, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow(f'{batting} batting', frame)
        cv2.waitKey(500)  # Half-second delay before restarting countdown

        if out:
            print(f'batter-{batting} got out!') 
            break

cap.release()
cv2.destroyAllWindows()

print(f'final batting score of {batting}: {score}')

batting, bowling = bowling, batting
target = score+1
print(f'target: {target}')

print(f'Now, {batting} bats and {bowling} bowls')

score = 0
out = False

cap = cv2.VideoCapture(0)
start_time = time.time()
timer_duration = 3  # Countdown from 5 to 1

while True:
    start_time = time.time()  # Start countdown
    while True:
        elapsed_time = time.time() - start_time
        countdown = max(3 - int(elapsed_time), 0)

        ret, frame = cap.read()
        if not ret:
            break

        # Display countdown on frame
        cv2.putText(frame, str(countdown), (100, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow(f'{batting} batting', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

        if countdown == 0:
            break  # Exit countdown loop

    # Capture frame and detect hand
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get user and system numbers
        toss_user_num = return_number()
        toss_system_num = play_system()

        # Display both numbers
        cv2.putText(frame, f'User: {toss_user_num}', (50, 85), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'System: {toss_system_num}', (50, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow(f'{batting} batting', frame)
        cv2.waitKey(500)  # Half-second delay before restarting countdown

        # Check if user and system numbers match
        if toss_user_num == toss_system_num:
            print(f"batter-{batting} got out!\n\n{bowling} wins!!!")
            break  # Exit loop
        else:
            if batting == 'system': 
                score += toss_system_num
            else: 
                score += toss_user_num
            if score > target: 
                print(f'batter-{batting} beat the target!\n\n{batting} wins!!!')
                break

cap.release()
cv2.destroyAllWindows()









    



