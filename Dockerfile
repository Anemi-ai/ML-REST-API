# Gunakan image dasar python
FROM python:3.8-slim

# Set lingkungan kerja di dalam container
WORKDIR /app

# Salin requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Atur variabel lingkungan untuk menyimpan path file kunci Google Cloud
ENV GOOGLE_APPLICATION_CREDENTIALS=keys/keyModel.json

# Expose port 8080
EXPOSE 8080

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
