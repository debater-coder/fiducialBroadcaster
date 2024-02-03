import pickle

import cv2 as cv
import numpy as np

input_video = cv.VideoCapture(1)

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
aruco_detector = cv.aruco.ArucoDetector(dictionary, detector_params)

with open("calibration.pkl", "rb") as f:
    camera_matrix, dist = pickle.load(f)

while input_video.grab():
    ret, image = input_video.read()

    corners, ids, rejected = aruco_detector.detectMarkers(image)

    if ids is not None:
        ret, rvec, tvec = cv.solvePnP(np.array([
            (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)
        ], dtype="double"), corners[0], camera_matrix, dist)

        image = cv.aruco.drawDetectedMarkers(image, corners, ids)

        image = cv.drawFrameAxes(image, camera_matrix, dist, rvec, tvec, 1)

        cv.imshow("detected markers", image)

    if cv.waitKey(1) == ord('q'):
        break

input_video.release()
cv.destroyAllWindows()