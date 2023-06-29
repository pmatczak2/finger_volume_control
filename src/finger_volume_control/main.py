import cv2
import mediapipe as mp
import subprocess
# import cv2: Imports the OpenCV library, which provides computer vision and image processing functions.
#
# import mediapipe as mp: Imports the Mediapipe library, which is used for various computer vision tasks, including
# hand tracking.
#
# import subprocess: Imports the subprocess module, which allows executing external commands.


cap = cv2.VideoCapture(0)
#  cap = cv2.VideoCapture(0): Creates a VideoCapture object to capture video from the default camera (index 0).

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
#  mp_hands = mp.solutions.hands: Assigns the mp.solutions.hands module to the variable mp_hands.
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5,
# min_tracking_confidence=0.5): Creates an instance of the Hands class from the mp_hands module. It configures the
# hand tracking parameters, such as enabling real-time video processing (static_image_mode=False), setting the maximum
# number of hands to track (max_num_hands=1), and defining the minimum confidence thresholds for hand detection
# and tracking.

mp_drawing = mp.solutions.drawing_utils
#  mp_drawing = mp.solutions.drawing_utils: Assigns the mp.solutions.drawing_utils module to the variable mp_drawing,
#  which provides utilities for drawing landmarks and connections on the image.
while True:
    ret, img = cap.read()
    if not ret:
        break
# while True:: Starts an infinite loop for continuously capturing frames and processing them.
    #
    # ret, img = cap.read(): Reads a frame from the video capture object (cap). The return value ret indicates whether
    # the frame was successfully read, and img stores the captured frame.
    #
    # if not ret: Checks if the frame was not successfully read. If so, it breaks the loop and ends the program.
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB): Converts the color space of the captured image from BGR
    # (Blue-Green-Red) to RGB (Red-Green-Blue) format. Mediapipe requires RGB images as input.
    results = hands.process(image_rgb)
    # results = hands.process(image_rgb): Processes the RGB image using the hand tracking model (hands).
    # It detects and tracks hands in the image and returns the results.
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
    # if results.multi_hand_landmarks:: Checks if hand landmarks were detected in the image. If there are detected
            # landmarks, it proceeds to the next block of code.

        # for handLms in results.multi_hand_landmarks:: Iterates over each detected hand landmark.

            # mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS): Draws landmarks and connections on
            # the image (img) using the detected hand landmarks (handLms) and predefined hand connections provided by
            # mp_hands.HAND_CONNECTIONS. This visualizes the hand tracking results on the image.
            index_finger_y = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_finger_y = handLms.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            # index_finger_y = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y: Retrieves the y-coordinate
            # of the index finger tip landmark from handLms.

            # thumb_finger_y = handLms.landmark[mp_hands.HandLandmark.THUMB_TIP].y: Retrieves the y-coordinate
            # of the thumb finger tip landmark from handLms.
            if index_finger_y < thumb_finger_y:
                hand_gesture = 'pointing up'
            elif index_finger_y > thumb_finger_y:
                hand_gesture = 'pointing down'
            else:
                hand_gesture = 'not pointing'
            # Determines the hand gesture based on the relative position of the index finger tip and thumb tip. If the
            # index finger is positioned higher than the thumb, it is considered as "pointing up." If the index finger
            # is positioned lower than the thumb, it is considered as "pointing down." Otherwise, it is considered
            # as "not pointing."
            if hand_gesture == 'pointing up':
                subprocess.call(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) '
                                                    '+ 10)'])
            elif hand_gesture == 'pointing down':
                subprocess.call(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) '
                                 '- 10)'])
                # If the hand gesture is "pointing up," it uses the subprocess.call() function to execute an AppleScript
                # command (osascript) to increase the volume by 10 using the set volume output volume command.
                #
                # If the hand gesture is "pointing down," it uses the subprocess.call() function to execute an
                # AppleScript command (osascript) to decrease the volume by 10 using the set volume output volume
                # command.


            cv2.imshow('Hand Gesture', img)
            # cv2.imshow('Hand Gesture', img): Displays the image with hand landmarks and connections in a window
            # titled "Hand Gesture."
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # if cv2.waitKey(1) & 0xFF == ord('q'):: Checks if the 'q' key is pressed while the window is active.
            # If so, it breaks the loop and ends the program.
cap.release()
cv2.destroyAllWindows()
# cap.release(): Releases the video capture object, allowing the camera or video source to be used by other applications.
# cv2.destroyAllWindows(): Closes all the OpenCV windows created during the program execution.
#
# Overall, this code captures video frames, performs hand tracking using the Mediapipe library, detects hand
# gestures based on the relative position of the index finger and thumb, and adjusts the system volume accordingly.