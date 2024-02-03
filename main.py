import cv2 as cv
import numpy as np

input_video = cv.VideoCapture(1)

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
aruco_detector = cv.aruco.ArucoDetector(dictionary, detector_params)

while input_video.grab():
    ret, image = input_video.read()

    corners, ids, rejected = aruco_detector.detectMarkers(image)

    if ids is not None:
        image_detected = cv.aruco.drawDetectedMarkers(image, corners, ids)
        cv.imshow("detected markers", image_detected)

    if cv.waitKey(1) == ord('q'):
        break

input_video.release()
cv.destroyAllWindows()