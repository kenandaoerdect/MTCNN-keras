import cv2
from mtcnn import mtcnn
import time


model = mtcnn()
threshold = [0.5,0.6,0.7]
capture = cv2.VideoCapture(0)
fps = 0.0

while(True):
    t1 = time.time()
    ref, frame = capture.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    rectangles = model.detectFace(img, threshold)
    draw = img.copy()

    for rectangle in rectangles:
        if rectangle is not None:
            W = -int(rectangle[0]) + int(rectangle[2])
            H = -int(rectangle[1]) + int(rectangle[3])
            paddingH = 0.01 * W
            paddingW = 0.02 * H
            crop_img = img[int(rectangle[1]+paddingH):int(rectangle[3]-paddingH), int(rectangle[0]-paddingW):int(rectangle[2]+paddingW)]
            if crop_img is None:
                continue
            if crop_img.shape[0] < 0 or crop_img.shape[1] < 0:
                continue
            cv2.rectangle(draw, (int(rectangle[0]), int(rectangle[1])), (int(rectangle[2]), int(rectangle[3])), (255, 0, 0), 1)

            for i in range(5, 15, 2):
                cv2.circle(draw, (int(rectangle[i + 0]), int(rectangle[i + 1])), 2, (0, 255, 0))

    draw = cv2.cvtColor(draw, cv2.COLOR_RGB2BGR)
    fps = (fps + (1. / (time.time() - t1))) / 2
    print("fps= %.2f" % (fps))
    draw = cv2.putText(draw, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("video", draw)
    c = cv2.waitKey(30) & 0xff
    if c == 27:
        capture.release()
        break