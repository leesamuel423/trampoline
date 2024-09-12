import cv2
from camera import Camera
from hand_tracking import HandTracker

def main():
    """
    Main function to run game
    """
    try:
        cam = Camera()
        hand_tracker = HandTracker()
        print("Camera initialized successfully")
        print("Press 'q' to quit")

        while True:
            frame = cam.get_frame()
            frame = hand_tracker.find_hands(frame, draw=False)

            # Get the positions of index finger and thumb tips
            index_tip, thumb_tip = hand_tracker.get_index_and_thumb(frame)
            
            # Draw circles at the fingertip positions
            if index_tip and thumb_tip:
                cv2.circle(frame, index_tip, 10, (0, 255, 0), cv2.FILLED)  # Green
                cv2.circle(frame, thumb_tip, 10, (0, 255, 0), cv2.FILLED)  # Green
                
                # Draw a line between index and thumb
                cv2.line(frame, index_tip, thumb_tip, (255, 255, 0), 2) # Yellow

            # TODO: Implement game logic
            # TODO: Render game elements on frame

            # Display processed frame
            cv2.imshow("Trampoline", frame)
            
            # Check for 'q' key press to quit game
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always close display window
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
