
### 1. Predict Endpoint

- **Endpoint:** `/predict`  
- **Method:** POST  
- **Deskripsi:** Endpoint ini digunakan untuk memprediksi kondisi berdasarkan gambar yang diunggah.  
- **Request Body:**
  - Form Data:
    - `my_image`: File gambar yang akan diprediksi.
    - `user_id`: ID pengguna yang mengunggah gambar.
  
- **Response:**
  - **Status Code:** 200 OK
  - **Data:**
    ```json
    {
      "id": "user_id",
      "hasil": "Label Hasil Prediksi",
      "deskripsi": "Deskripsi hasil prediksi",
      "gejala": "Gejala yang terkait dengan hasil prediksi",
      "akurasi": "Akurasi prediksi",
      "informasi_tambahan": {
        "tindakan_saran": "Saran atau tindakan yang dianjurkan",
        "pencegahan": "Langkah-langkah pencegahan yang disarankan",
        "risiko_komplikasi": "Risiko komplikasi terkait dengan kondisi",
        "perawatan_medis": "Perawatan medis yang mungkin diperlukan",
        "gayahidup_sehat": "Gaya hidup sehat yang dianjurkan"
      }
      "waktu_prediksi": "2024-06-13 00:13:35"
    }
    ```
  - **Status Code:** 400 Bad Request
  - **Data:**
    ```json
    {
      "error": "Harap isi data yang sesuai, image dan ID tidak boleh kosong!"
    }
    ```
  - **Status Code:** 400 Bad Request
  - **Data:**
    ```json
    {
      "error": "Gambar tidak valid. Harap unggah gambar dengan jelas."
    }
    ```

### 2. History Endpoint

- **Endpoint:** `/history`  
- **Method:** GET  
- **Deskripsi:** Endpoint ini digunakan untuk mengambil riwayat prediksi dari Firestore.  
- **Response:**
  - **Status Code:** 200 OK
  - **Data:** Array of Prediction Objects
    ```json
    {
      "id": "user_id",
      "hasil": "Label Hasil Prediksi",
      "deskripsi": "Deskripsi hasil prediksi",
      "gejala": "Gejala yang terkait dengan hasil prediksi",
      "akurasi": "Akurasi prediksi",
      "informasi_tambahan": {
        "tindakan_saran": "Saran atau tindakan yang dianjurkan",
        "pencegahan": "Langkah-langkah pencegahan yang disarankan",
        "risiko_komplikasi": "Risiko komplikasi terkait dengan kondisi",
        "perawatan_medis": "Perawatan medis yang mungkin diperlukan",
        "gayahidup_sehat": "Gaya hidup sehat yang dianjurkan"
      }
      "waktu_prediksi": "2024-06-13 00:13:35"
    }
    // Dan seterusnya

  - **Status Code:** 404 Not Found
  - **Data:**
    ```json
    {
      "error": "Data kosong tidak ditemukan"
    }
    ```

### 3. History by User ID Endpoint

- **Endpoint:** `/history/<user_id>`  
- **Method:** GET  
- **Deskripsi:** Endpoint ini digunakan untuk mengambil riwayat prediksi berdasarkan ID pengguna dari Firestore.  
- **Response:**
  - **Status Code:** 200 OK
  - **Data:** Array of Prediction Objects
    ```json
    {
      "id": "user_id",
      "hasil": "Label Hasil Prediksi",
      "deskripsi": "Deskripsi hasil prediksi",
      "gejala": "Gejala yang terkait dengan hasil prediksi",
      "akurasi": "Akurasi prediksi",
      "informasi_tambahan": {
        "tindakan_saran": "Saran atau tindakan yang dianjurkan",
        "pencegahan": "Langkah-langkah pencegahan yang disarankan",
        "risiko_komplikasi": "Risiko komplikasi terkait dengan kondisi",
        "perawatan_medis": "Perawatan medis yang mungkin diperlukan",
        "gayahidup_sehat": "Gaya hidup sehat yang dianjurkan"
      }
      "waktu_prediksi": "2024-06-13 00:13:35"
    }

  - **Status Code:** 404 Not Found
  - **Data:**
    ```json
    {
      "error": "User dengan ID yang dicari tidak ditemukan!"
    }
    ```
