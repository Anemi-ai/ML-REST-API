from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.layers import DepthwiseConv2D
from google.cloud import firestore
import numpy as np
import cv2
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Menginisialisasi Firestore client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), "keys", "keyModel.json")
db = firestore.Client()

# Dictionary untuk label kelas dan informasi terkait
LABELS = {
    0: {
        'name': 'Normal',
        'description': 'Kadar hemoglobin darah berada dalam kisaran normal.',
        'symptoms': 'Sakit kepala, Mudah lelah, Pusing, Pucat, Detak jantung tidak teratur.'
    },
    1: {
        'name': 'Terindikasi Anemia!',
        'description': 'Jumlah sel darah merah dalam tubuh lebih rendah dari jumlah normal.',
        'symptoms': 'Sakit kepala, Mudah lelah, Pusing, Pucat, Detak jantung tidak teratur.'
    }
}

# Custom layer untuk menangani argumen tidak dikenal
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        if 'groups' in kwargs:
            del kwargs['groups']
        super(CustomDepthwiseConv2D, self).__init__(*args, **kwargs)

# Memuat model
try:
    model = load_model('Model_MobileNet.h5', custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D})
    print("Model Loaded Successfully")
except Exception as e:
    print("Failed to load model:", e)

# Load Haar Cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_eyes(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    return len(eyes) > 0  # Return True if eyes are detected, otherwise False

# Fungsi untuk memprediksi label
def predict_label(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 224.0
    img_array = img_array.reshape(1, 224, 224, 3)
    probs = model.predict(img_array)[0]
    predicted_class = np.argmax(probs)
    return predicted_class, LABELS[predicted_class], probs[predicted_class]

# Fungsi untuk menyimpan hasil prediksi ke Firestore
def save_to_firestore(prediction):
    doc_ref = db.collection('predictions').document()
    doc_ref.set(prediction)

# Endpoint untuk prediksi
@app.route("/predict", methods=['POST'])
def predict():
    if 'my_image' not in request.files or 'user_id' not in request.form:
        return jsonify({'error': 'Data tidak lengkap'}), 400
    
    img = request.files['my_image']
    user_id = request.form['user_id']  # Mengambil ID pengguna dari permintaan HTTP
    img_path = "static/" + img.filename
    img.save(img_path)
    
    if not detect_eyes(img_path):
        return jsonify({'error': 'Gambar tidak valid. Harap unggah gambar dengan jelas.'}), 400
    
    label_index, label_info, confidence = predict_label(img_path)
    accuracy = f"{confidence * 100:.2f}%"
    
    # Informasi tambahan berdasarkan kelas yang diprediksi
    additional_info = {
        'tindakan_saran': "Tidak ada tindakan khusus yang disarankan. Pertahankan gaya hidup sehat.",
        'pencegahan': "Anda dapat mencegah masalah kesehatan dengan menjaga pola makan seimbang, berolahraga secara teratur, dan tidur yang cukup.",
        'risiko_komplikasi': "Tidak ada risiko kesehatan yang signifikan terkait dengan kondisi ini.",
        'perawatan_medis': "Tidak memerlukan perawatan medis khusus. Tetap rutin periksa kesehatan secara berkala.",
        'gayahidup_sehat': "Anda dapat memelihara gaya hidup sehat dengan mengonsumsi makanan bergizi, berolahraga secara teratur, dan mengelola stres."
    } if label_index == 0 else {
        'tindakan_saran': "Disarankan berkonsultasi dengan dokter untuk evaluasi lebih lanjut dan penanganan yang sesuai.",
        'pencegahan': "Anda dapat mencegah anemia dengan mengonsumsi makanan yang kaya zat besi seperti daging merah, telur, dan sayuran berdaun hijau.",
        'risiko_komplikasi': "Komplikasi anemia bisa berupa kelelahan kronis, masalah jantung, dan penurunan kualitas hidup.",
        'perawatan_medis': "Perawatan medis untuk anemia tergantung pada jenis dan tingkat keparahan kondisi. Ini bisa mencakup suplemen zat besi atau transfusi darah.",
        'gayahidup_sehat': "Anda dapat membantu mengelola anemia dengan gaya hidup sehat, termasuk makan makanan bergizi, berolahraga secara teratur, dan mengelola stres."
    }
    
    prediction = {
        'id': user_id,
        'hasil': label_info['name'],
        'deskripsi': label_info['description'],
        'gejala': label_info['symptoms'],
        'akurasi': accuracy,
        'informasi_tambahan': additional_info
    }
    
    # Menyimpan hasil prediksi ke Firestore
    save_to_firestore(prediction)
    
    return jsonify(prediction)

# Endpoint untuk mengambil history prediksi dari Firestore
@app.route("/history", methods=['GET'])
def get_history():
    try:
        predictions_ref = db.collection('predictions')
        docs = predictions_ref.stream()
        history = []
        for doc in docs:
            history.append(doc.to_dict())
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fungsi untuk mengambil koleksi users
def get_users_collection():
    users_ref = db.collection('users')
    users = users_ref.get()
    return users

# Mengambil data ID dari setiap dokumen dalam koleksi "users"
users_collection = get_users_collection()
for user in users_collection:
    user_data = user.to_dict()
    user_id = user_data.get('id', 'N/A')
    print(f'User ID: {user_id}')
    
@app.route("/history/<user_id>", methods=['GET'])
def get_history_by_user_id(user_id):
    try:
        predictions_ref = db.collection('predictions')
        query = predictions_ref.where('id', '==', user_id)
        docs = query.stream()
        history = []
        for doc in docs:
            history.append(doc.to_dict())
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
