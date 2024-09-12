import cv2
import numpy as np
from PIL import Image
import os

# Yolu ve dosya adlarını tanımla
data_path = 'data'
trainer_path = 'trainer/trainer.yml'
cascade_path = 'Cascade/haarcascade_frontalface_default.xml'

# Yüz tanıma ve yüz algılayıcı oluştur
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cascade_path)

def getImagesAndLabels(path):
    faceSamples = []
    ids = []
    
    # Klasörler arasından geç
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        
        if os.path.isdir(folder_path):
            # ID olarak klasör adını kullan
            id = folder_name
            
            try:
                imagePaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
                
                for imagePath in imagePaths:
                    try:
                        # Resmi gri tonlamaya çevir
                        PIL_img = Image.open(imagePath).convert('L')
                        img_numpy = np.array(PIL_img, 'uint8')
                        
                        # Yüzleri tespit et
                        faces = detector.detectMultiScale(img_numpy, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

                        for (x, y, w, h) in faces:
                            faceSamples.append(img_numpy[y:y + h, x:x + w])
                            ids.append(id)  # ID'yi ekle
                    except Exception as e:
                        print(f"Error processing image {imagePath}: {e}")
            
            except Exception as e:
                print(f"Error processing folder {folder_path}: {e}")

    return faceSamples, ids

def train_model():
    if not os.path.exists('trainer'):
        os.makedirs('trainer')

    print("\nYüzler taranıyor. Birkaç saniye sürecek, bekleyin...")
    faces, ids = getImagesAndLabels(data_path)

    if len(faces) > 0 and len(ids) > 0:
        try:
            # IDs dizisini numerik türüne dönüştür
            # Kişi isimleri ile ID'ler arasında bir eşleme yapmamız gerekiyor
            unique_ids = list(set(ids))
            id_map = {name: idx for idx, name in enumerate(unique_ids)}
            numeric_ids = np.array([id_map[name] for name in ids], dtype=np.int32)

            recognizer.train(faces, numeric_ids)
            recognizer.write(trainer_path)
            print(f"Model başarıyla '{trainer_path}' dosyasına yazıldı.")
        except cv2.error as e:
            print(f"OpenCV hata: {e}")
        except Exception as e:
            print(f"Genel hata: {e}")
    else:
        print("Eğitim verisi yok. Yüzler veya ID'ler bulunamadı.")

train_model()
