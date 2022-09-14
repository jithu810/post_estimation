import cv2
import numpy as np


class Object:
    def __init__(self, start_x=100, start_y=100, size=50):

        self.logo_org = cv2.imread('e.jpeg')
        self.size = size
        self.logo = cv2.resize(self.logo_org, (size, size))
        img2gray = cv2.cvtColor(self.logo, cv2.COLOR_BGR2GRAY)
        _, logo_mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        self.logo_mask = logo_mask
        self.x = start_x
        self.y = start_y
        self.on_mask = False

    def insert_object(self, frame):
        roi = frame[self.y:self.y + self.size, self.x:self.x + self.size]
        roi[np.where(self.logo_mask)] = 0
        roi += self.logo

    def update_position(self, mask):
        height, width = mask.shape
        roi = mask[self.y:self.y + self.size, self.x:self.x + self.size]
        check = np.any(roi[np.where(self.logo_mask)])
        if check:
            best_delta_x = 0
            best_delta_y = 0
            best_fit = np.inf
            for _ in range(8):
                delta_x = np.random.randint(-15, 15)
                delta_y = np.random.randint(-15, 15)
                if self.y + self.size + delta_y > height or self.y + delta_y < 0 or \
                        self.x + self.size + delta_x > width or self.x + delta_x < 0:
                    continue
                roi = mask[self.y + delta_y:self.y + delta_y + self.size, self.x + delta_x:self.x + delta_x + self.size]
                check = np.count_nonzero(roi[np.where(self.logo_mask)])
                if check == 0:
                    self.x += delta_x
                    self.y += delta_y
                    return
                elif check < best_fit:
                    best_fit = check
                    best_delta_x = delta_x
                    best_delta_y = delta_y
            if best_fit < np.inf:
                self.x += best_delta_x
                self.y += best_delta_y
                return

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
background_subtractor = cv2.createBackgroundSubtractorMOG2()
obj = Object()

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    fg_mask = background_subtractor.apply(frame)
    _, fg_mask = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
    
    obj.update_position(fg_mask)
    obj.insert_object(frame)
    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()