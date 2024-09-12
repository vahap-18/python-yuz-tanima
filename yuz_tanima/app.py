from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from flask_socketio import SocketIO, emit
import cv2
import os
import threading
import webbrowser
import glob
import numpy as np
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Kamera ve yüz algılayıcı başlatma
camera = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier("Cascade/haarcascade_frontalface_default.xml")
face_id = None
capture_images = False
log_file = 'log.txt'

# Profil isimlerini bir dizi olarak tanımlayın
names = ["mehmet", "vahap", "kadir", "deneme"]  # İsimleri burada tanımlayın

# İsimleri sayısal ID'lere eşle
id_map = {name: idx for idx, name in enumerate(names)}

def log_message(message):
    with open(log_file, 'a') as file:
        file.write(message + '\n')
    socketio.emit('log_update', {'message': message})

def capture_faces():
    global capture_images, face_id

    data_dir = os.path.join("data", face_id)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    count = 0
    directions = ["düz", "sağa", "sola", "yukarı", "aşağı"]

    for direction in directions:
        frames_captured = 0
        while frames_captured < 10:  # Her yön için 10 görüntü kaydedilecek
            ret, img = camera.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                x = max(x - 10, 0)
                y = max(y - 10, 0)
                w = min(w + 20, img.shape[1] - x)
                h = min(h + 20, img.shape[0] - y)

                face_img = gray[y:y + h, x:x + w]
                face_img = cv2.resize(face_img, (200, 200))

                count += 1
                frames_captured += 1
                filename = os.path.join(data_dir, str(count) + ".jpg")
                cv2.imwrite(filename, face_img)
                log_message(f"Görüntü kaydedildi: {filename}")

            if not capture_images:
                break

    capture_images = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    global capture_images, face_id

    data = request.get_json()
    face_id = data.get('name', None)
    if face_id is None:
        return jsonify({"status": "Geçersiz veya eksik isim."}), 400

    capture_images = True
    log_message(f"Fotoğraf çekimi başlatıldı. ID: {face_id}")

    threading.Thread(target=capture_faces).start()

    return jsonify({"status": "Fotoğraf çekimi başladı"})

@app.route('/train', methods=['POST'])
def train():
    trainer_path = 'trainer/trainer.yml'
    cascade_path = 'Cascade/haarcascade_frontalface_default.xml'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cascade_path)

    def getImagesAndLabels(path):
        faceSamples = []
        ids = []
        for folder_name in os.listdir(path):
            folder_path = os.path.join(path, folder_name)
            if os.path.isdir(folder_path):
                try:
                    imagePaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
                    for imagePath in imagePaths:
                        PIL_img = Image.open(imagePath).convert('L')
                        img_numpy = np.array(PIL_img, 'uint8')
                        faces = detector.detectMultiScale(img_numpy, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
                        for (x, y, w, h) in faces:
                            faceSamples.append(img_numpy[y:y + h, x:x + w])
                            ids.append(id_map.get(folder_name, -1))  # ID'yi id_map'den al
                except Exception as e:
                    log_message(f"Error processing folder {folder_path}: {e}")

        return faceSamples, ids

    faces, ids = getImagesAndLabels('data')
    if len(faces) > 0 and len(ids) > 0:
        recognizer.train(faces, np.array(ids, dtype=np.int32))
        if not os.path.exists('trainer'):
            os.makedirs('trainer')
        recognizer.write(trainer_path)
        log_message("Model başarıyla eğitildi ve kaydedildi.")
        return jsonify({"status": "Model başarıyla eğitildi ve kaydedildi."})
    else:
        log_message("Eğitim verisi yok. Yüzler veya ID'ler bulunamadı.")
        return jsonify({"status": "Eğitim verisi yok. Yüzler veya ID'ler bulunamadı."})

@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    return app.response_class(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_images', methods=['GET'])
def get_images():
    data_dir = os.path.join("data", face_id)
    if not os.path.exists(data_dir):
        return jsonify({"images": []})

    image_paths = glob.glob(os.path.join(data_dir, '*.jpg'))
    image_urls = [url_for('static', filename=os.path.basename(img)) for img in image_paths]
    return jsonify({"images": image_urls})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('data', filename)

@app.route('/start_recognition', methods=['POST'])
def start_recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    trainer_path = 'trainer/trainer.yml'
    if not os.path.exists(trainer_path):
        return jsonify({"status": "Eğitimli model bulunamadı."}), 500

    recognizer.read(trainer_path)
    detector = cv2.CascadeClassifier("Cascade/haarcascade_frontalface_default.xml")

    def recognize_faces():
        while True:
            ret, img = camera.read()
            if not ret:
                break
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                face_img = gray[y:y + h, x:x + w]
                face_img = cv2.resize(face_img, (200, 200))

                id, confidence = recognizer.predict(face_img)

                # ID'ye göre klasör ismini belirle
                folder_name = [name for name, index in id_map.items() if index == id]
                recognized_name = folder_name[0] if folder_name else "bilinmiyor"

                # Confidence değerini 100 - confidence olarak hesaplıyoruz
                confidence_percentage = 100 - confidence

                if confidence_percentage > 60:  # Güven oranı 60% ve üzerinde ise
                    log_message(f"Tanınan profil: {recognized_name}, Güven oranı: {confidence_percentage}% - Kapı açıldı")
                else:
                    log_message(f"Tanınan profil: {recognized_name}, Güven oranı: {confidence_percentage}% - Kapı açılmadı")

            # Tanıma işlemi tamamlandığında çıkış yapar
            break

    threading.Thread(target=recognize_faces).start()

    return jsonify({"status": "Profil tanıma başlatıldı."})


def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    socketio.run(app, debug=True)
