# 🏀 BasketCoach-AI

**BasketCoach-AI** adalah asisten pelatih bola basket cerdas berbasis AI yang dikembangkan menggunakan **Google Gemini LLM** dan arsitektur **RAG (Retrieval-Augmented Generation)**. Sistem ini memungkinkan pengguna untuk bertanya tentang aturan teknik, strategi, dan sejarah basket secara interaktif melalui antarmuka Streamlit.

![Streamlit App Demo]()
<img width="2547" height="1334" alt="Screenshot 2026-05-10 033712" src="https://github.com/user-attachments/assets/29bab19c-0392-4475-a90c-9987ac6fbc6e" />



## 🚀 Fitur Utama
- **RAG-Powered:** Jawaban akurat berdasarkan dokumen resmi basket (PDF) yang diproses menggunakan FAISS.
- **Streaming Responses:** Pengalaman chat yang responsif dengan teks yang mengalir kata demi kata.
- **Smart Welcome Cards:** Saran pertanyaan populer untuk memudahkan pengguna.
- **Session History & Search:** Simpan sesi chat dan cari kembali riwayat percakapan dengan mudah.
- **Visual Aids:** Mendukung penampilan gambar teknis (seperti dimensi lapangan) secara otomatis.

## 🏗️ Alur Kerja (Project Flow)

Proyek ini bekerja dengan dua tahap utama: Ingesti Data dan Chatbot Interface.



1.  **Ingestion Phase (`ingest.py`):**
    - Membaca dokumen PDF dari folder `data/`.
    - Memecah teks menjadi potongan kecil (*chunking*).
    - Mengubah teks menjadi vektor (embedding) menggunakan `gemini-embedding-2`.
    - Menyimpan vektor tersebut ke dalam database lokal **FAISS**.

2.  **Retrieval & Generation Phase (`app.py`):**
    - Pengguna memberikan input melalui Streamlit.
    - Sistem mencari potongan teks paling relevan dari database FAISS.
    - Konteks teks tersebut dikirim ke Gemini LLM bersama dengan pertanyaan pengguna.
    - Gemini memberikan jawaban yang akurat dan santun layaknya seorang pelatih.

## 🛠️ Persiapan Lingkungan (Setup)

### 1. Prasyarat
Pastikan Anda sudah menginstal Python 3.9+ dan memiliki **Gemini API Key**.

### 2. Instalasi Library
Clone repositori ini dan instal semua library yang dibutuhkan:
```bash
git clone [https://github.com/username/BasketCoach-AI.git](https://github.com/username/BasketCoach-AI.git)
cd BasketCoach-AI
pip install -r requirements.txt
