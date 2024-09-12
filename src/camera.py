import cv2

class Camera:
    def __init__(self, camera_index=0):
        """
        Initialize camera

        : param camera_index: Index of camera to use (default 0 for first available camera)
        """
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise ValueError(f"Unable to open camera with index {camera_index}. Check if the camera is connected and not in use by another application.")
        
        # Get default frame width and height
        self.frame_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera initialized with dimensions: {self.frame_width}x{self.frame_height}")

    def __del__(self):
        """
        Destructor to release camera when object deleted
        """
        if hasattr(self, 'camera'):
            self.camera.release()
            print("Camera released")

    def get_frame(self):
        """
        Capture and return frame from camera

        : return: numpy array representing captured frame
        """
        if not self.camera.isOpened():
            raise RuntimeError("Camera is not opened. It might have been released or disconnected.")
        
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture frame. The camera might be disconnected or in use by another application.")
        return frame

    def get_frame_dimensions(self):
        """
        Get dimensions of camera frame

        : return: Tuple (width, height) of frame dimensions
        """
        return (self.frame_width, self.frame_height)

# Run module as script to test
if __name__ == "__main__":
    try:
        cam = Camera()
        print("Press 'q' to quit")
        while True:
            frame = cam.get_frame()
            cv2.imshow("Camera Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()
