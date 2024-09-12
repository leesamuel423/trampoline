import cv2
from camera import Camera
from hand_tracking import HandTracker
from ball import Ball
import math

def main():
    """
    Main function to run game
    """
    try:
        cam = Camera()
        hand_tracker = HandTracker()
        frame_width, frame_height = cam.get_frame_dimensions()

        ball = Ball(frame_width // 2, frame_height // 2)
        print("Camera initialized successfully")
        print("Press 'q' to quit")

        while True:
            try:
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

                    if ball.check_trampoline_collision(thumb_tip, index_tip):
                        print("Ball bounced on the trampoline!")

                ball.move()
                ball.check_boundary(frame_width, frame_height)
                ball.draw(frame)
                
                # Display ball velocity and cooldown status (check stuttering)
                cv2.putText(frame, f"Velocity: ({ball.velocity[0]:.2f}, {ball.velocity[1]:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cooldown_status = "Active" if ball.get_collision_cooldown_status() else "Ready"
                cooldown_color = (0, 0, 255) if cooldown_status == "Active" else (0, 255, 0)
                cv2.putText(frame, f"Cooldown: {cooldown_status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cooldown_color, 2)

                # Display processed frame
                cv2.imshow("Trampoline", frame)
                
                # Check for 'q' key press to quit game
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    print("Restarting game")
                    ball = Ball(frame_width // 2, frame_height // 2)
            except Exception as e:
                print(f"An error occurred in game loop: {e}")
                print(f"Ball position: ({ball.x}, {ball.y})")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always close display window
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
