import cv2
from camera import Camera

def main():
    """
    Main function to run game

    Initialize camera, continuously capture frames, and implement game logic + rendering

    """
    try:
        # Init camera
        cam = Camera()
        print("Camera initialized successfully")
        print("Press 'q' to quit")

        while True:
            frame = cam.get_frame()

            # TODO: Implement hand tracking
            # TODO: Implement game logic
            # TODO: Render game elements on frame

            # Just show raw frame for now
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
