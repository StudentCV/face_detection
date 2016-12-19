import pypylon.pylon as py
import numpy as np
import cv2
import time

last_timestamp = 0
timestamp = 0

# Simply get the first available pylon device.
first_device = py.TlFactory.GetInstance().CreateFirstDevice()
instant_camera = py.InstantCamera(first_device)
instant_camera.Open()

# Optional if you set it in Pylon Viewer
instant_camera.PixelFormat = "RGB8"

instant_camera.StartGrabbing(py.GrabStrategy_LatestImages)

# Use haarcascade to detect faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    # Update current image in video window.
    # Grab one image.
    img = np.zeros((1, 1))
    if instant_camera.NumReadyBuffers:
        res = instant_camera.RetrieveResult(1000)
        if res:
            try:
                if res.GrabSucceeded():
                    currImg = res.Array
            finally:
                res.Release()

    faces = face_cascade.detectMultiScale(currImg, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(currImg, (x, y), (x + w, y + h), (255, 0, 0), 2)

    timestamp = time.time()
    if 0 == last_timestamp:
        last_timestamp = timestamp
    else:
        period = timestamp - last_timestamp
        last_timestamp = timestamp

        frame_rate = 1 / period
        frametime = period

        print(frame_rate)

    # Display new image in video window.
    cv2.imshow('Video', currImg)
    # Wait    1 ms.
    cv2.waitKey(1)