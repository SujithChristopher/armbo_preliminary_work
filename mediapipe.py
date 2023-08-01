import cv2
import mediapipe as mp

def main():
    # Initialize mediapipe pose module
    # mp_pose = mp.solutions.holistic.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    mp_holistic = mp.solutions.pose
    holistic_model = mp_holistic.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.9
    )
    
    # Initialize webcam feed
    cap = cv2.VideoCapture(2)

    while True:
        # Read a frame from the webcam
        ret, image = cap.read()
        
        # Convert the image from BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and get pose landmarks
        results = holistic_model.process(image_rgb)
        
        if results.pose_landmarks:
            # Draw pose landmarks on the image
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, holistic_model.POSE_CONNECTIONS)
        
        # Display the image with pose landmarks
        cv2.imshow('Pose Tracking', image)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
