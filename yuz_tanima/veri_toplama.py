import cv2
import os

# Kamerayı başlat
cam = cv2.VideoCapture(0)

# Kamera çözünürlüğünü yüksek ayarla
cam.set(3, 720)  # Genişlik
cam.set(4, 480)  # Yükseklik

# Yüz algılayıcıyı yükle
face_detector = cv2.CascadeClassifier("Cascade/haarcascade_frontalface_default.xml")

# Kullanıcıdan bir isim al
face_id = input('\n Bir isim giriniz ==>  ')

# İsimle aynı adı taşıyan bir klasör oluştur
data_dir = "data/" + face_id
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

print("\n [Bilgi] Yüz yakalama başlatılıyor. Lütfen yüzünüzü farklı yönlere çevirin...")

count = 0
directions = ["düz", "sağa", "sola", "yukarı", "aşağı"]

for direction in directions:
    print(f"\n [Bilgi] Lütfen yüzünüzü {direction} çevirin ve birkaç saniye bekleyin...")
    frames_captured = 0  # Her yön için yakalanan kare sayısını takip eder
    while frames_captured < 10:  # Her yön için 10 görüntü kaydedilecek
        ret, img = cam.read()

        if not ret:
            print("Kamera görüntüsü alınamadı.")
            break

        # Görüntüyü yatay olarak çevir (kamerada ayna etkisi için)
        img = cv2.flip(img, 1)

        # Görüntüyü gri tonlamaya çevir
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Yüzleri algıla
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            # Çerçeveyi biraz ayarlayarak yüzü daha iyi ortala
            x = max(x - 10, 0)
            y = max(y - 10, 0)
            w = min(w + 20, img.shape[1] - x)
            h = min(h + 20, img.shape[0] - y)

            # Yüzün etrafına dikdörtgen çiz
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Yüzün iç kısmını kesin
            face_img = gray[y:y + h, x:x + w]

            # Yüzün boyutlarını yeniden ayarla
            face_img = cv2.resize(face_img, (200, 200))

            # Yakalanan yüzü kaydedin
            count += 1
            frames_captured += 1
            cv2.imwrite(os.path.join(data_dir, str(count) + ".jpg"), face_img)

        # Görüntüyü sürekli göster
        cv2.imshow('image', img)

        # 0.3 saniye bekle
        cv2.waitKey(500)  # 500ms bekle

        # 'Esc' tuşuna basıldığında döngüyü kır
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

# Kamerayı serbest bırak ve tüm pencereleri kapat
cam.release()
cv2.destroyAllWindows()

print("\n [Bilgi] Yüz yakalama tamamlandı, {} görüntü kaydedildi.".format(count))
