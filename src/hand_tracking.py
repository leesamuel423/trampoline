import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize hand tracking

        :param static_image_mode: whether to treat input images as video stream or independent images
        :param max_num_hands: max number of hands to detect
        :param min_detection_confidence: min confidence for hand detection
        :param min_tracking_confidence: min confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        """
        Detect hands in input frame and draw landmarks (optional)

        :param frame: input frame
        :param draw: whether to draw hand landmarks on frame
        :return: Frame with or without landmarks
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame

    def get_index_and_thumb(self, frame):
        """
        Get position of index fingertip and thumb tip on first detected hand

        :param frame: Input frame
        :return: Tuple (index_tip, thumb_tip) of positions or (None, None)
        """
        index_tip = thumb_tip = None
        frame_height, frame_width, _ = frame.shape

        if self.results.multi_hand_landmarks:
            # First hand detected
            hand = self.results.multi_hand_landmarks[0]

            # Index fingertip (landmark 8)
            index_tip = (
                int(hand.landmark[8].x * frame_width),
                int(hand.landmark[8].y * frame_height)
            )

            # Thumb fingertip (landmark 4)
            thumb_tip = (
                int(hand.landmark[4].x * frame_width),
                int(hand.landmark[4].y * frame_height)
            )

        return index_tip, thumb_tip
