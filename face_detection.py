import pypylon.pylon as py
import cv2

# Simply get the first available pylon device.
first_device = py.TlFactory.GetInstance().CreateFirstDevice()
instant_camera = py.InstantCamera(first_device)
instant_camera.Open()

# Optional if you set it in Pylon Viewer
instant_camera.PixelFormat = "RGB8"

# Grab a single  camera image
grab_result = instant_camera.GrabOne(400)
image = grab_result.Array

# Alternatively you can try loading an image from file
# image = cv2.imread(r'/path/to/image.jpg')

# Use haarcascade to detect faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Detect faces and draw rectangles around them
faces = face_cascade.detectMultiScale(image, 1.3, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Show the image in a new window
cv2.imshow("face detection", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
cv2.waitKey()
