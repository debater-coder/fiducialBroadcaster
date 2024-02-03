import cv2 as cv
import numpy as np

print("ArUco marker generator utility")

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
border_bits = 1

marker_id = int(input("Enter marker id: "))

if marker_id < 0 or marker_id > 250:
    print("Invalid marker")

marker_image = cv.aruco.generateImageMarker(dictionary, marker_id, 200, np.zeros((200, 200), dtype=np.uint8), border_bits)

filename = f'aruco{marker_id}.png'

cv.imwrite(filename, marker_image)


print(f"Generated marker image at {filename}")
print("Dictionary: DICT_6X6_250")
print("Border bits: ", border_bits)


