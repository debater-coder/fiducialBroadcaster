import asyncio
import json
import pickle

import cv2 as cv
import numpy as np
import websockets

input_video = cv.VideoCapture(1)

detector_params = cv.aruco.DetectorParameters()
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
aruco_detector = cv.aruco.ArucoDetector(dictionary, detector_params)

# Calibrated with https://github.com/niconielsen32/CameraCalibration
with open("calibration.pkl", "rb") as f:
    camera_matrix, dist = pickle.load(f)


def get_marker_transform():
    if not input_video.grab():
        return None

    ret, image = input_video.read()

    corners, ids, rejected = aruco_detector.detectMarkers(image)

    if ids is None:
        return None

    ret, rvec, tvec = cv.solvePnP(np.array([
        (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)
    ], dtype="double"), corners[0], camera_matrix, dist)

    image = cv.aruco.drawDetectedMarkers(image, corners, ids)

    cv.imshow("image", image)

    return rvec.tolist(), tvec.tolist()


async def handler(websocket):
    while True:
        marker_transform = get_marker_transform()
        await websocket.send(json.dumps(marker_transform))
        await asyncio.sleep(0)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        input_video.release()
