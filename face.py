import cv2

cascade = cv2.CascadeClassifier("face.xml")
cap = cv2.VideoCapture(1)
while cap.isOpened():
    _, frame = cap.read()
    faces = cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imshow("image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
