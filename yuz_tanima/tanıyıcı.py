import cv2
import numpy as np

# Yüz tanıyıcıyı yükleyin
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Yüz algılayıcıyı yükleyin
faceCascade = cv2.CascadeClassifier("Cascade/haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX

# Tanınan kişilerin isimleri
names = ['dogan','bebek']  # Tanıdık isimlerinizi buraya ekleyin

# Kamera açılır
cam = cv2.VideoCapture(0)
cam.set(3, 1000)  # Genişlik
cam.set(4, 720)   # Yükseklik

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Yüzleri algıla
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # ID'nin geçerli olup olmadığını kontrol edin
        if id < len(names):
            name = names[id]
        else:
            name = "bilinmiyor"

        if confidence < 60:
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            name = "bilinmiyor"
            confidence = "  {0}%".format(round(100 - confidence))

        # İsim ve güvenilirlik oranını ekrana yazdır
        cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    # Kamera görüntüsünü göster
    cv2.imshow('Person Profil', img)

    # ESC tuşuna basılınca çık
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Kamera kapatılır
cam.release()
cv2.destroyAllWindows()