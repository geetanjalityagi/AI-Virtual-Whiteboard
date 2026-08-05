import cv2
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, num_hands = 2, detection_conf = 0.5, tracking_conf = 0.5):

        self.mode = mode
        self.num_hands = num_hands
        self.detection_conf = detection_conf
        self.tracking_conf = tracking_conf

        self.mpDraw = mp.solutions.drawing_utils
        self.mphands = mp.solutions.hands
        self.hand = self.mphands.Hands(static_image_mode=self.mode,
                                      max_num_hands=self.num_hands,
                                      min_detection_confidence=self.detection_conf,
                                      min_tracking_confidence=self.tracking_conf)

    def findhands(self, frame, draw = True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hand.process(frameRGB)
        
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mphands.HAND_CONNECTIONS)

        return frame

    def findpoints(self, frame):
        lmlist = []
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                for id, lms in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lms.x * w), int(lms.y * h)

                    lmlist.append([id, cx, cy])

        return lmlist
