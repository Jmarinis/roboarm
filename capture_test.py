import numpy as np
import cv2

cap = cv2.VideoCapture(0)
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

old_frame = None
old_gray = None
p0 = None

while True:
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if old_gray is None:
        old_gray = frame_gray
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    good_new = p1[st==1]
    good_old = p0[st==1]
    
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
        cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()