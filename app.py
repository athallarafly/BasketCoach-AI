import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from google.api_core import client_options
import time

# CONFIGURATION

def setup_page():
    st.set_page_config(page_title="Asisten Pelatih Basket", page_icon="🏀")
    st.header("🏀 Chatbot Asisten Pelatih Basket")
    
    # --- SIDEBAR STRUCTURE ---
    st.sidebar.header("🏀 Menu Pelatih", divider='rainbow')

    # 1. TOMBOL NEW CHAT (PALING ATAS)
    if st.sidebar.button("➕ Simpan & Mulai Baru", use_container_width=True, type="primary"):
        if st.session_state.get("messages"):
            # Ambil pesan pertama user sebagai judul preview
            preview_text = st.session_state["messages"][0]["content"][:25]
            st.session_state["history_archives"].append({
                "preview": preview_text,
                "chats": list(st.session_state["messages"])
            })
        st.session_state["messages"] = []
        st.rerun()

    st.sidebar.write("") # Memberi sedikit spasi visual

    # 2. SEARCH BAR (TENGAH)
    st.sidebar.subheader("Cari Percakapan")
    search_query = st.sidebar.text_input(
        "Cari", 
        placeholder="Cari topik (ex: Layup)", 
        label_visibility="collapsed"
    )

    st.sidebar.divider()

    # 3. RECENT HISTORY (PALING BAWAH)
    st.sidebar.subheader("Riwayat Terakhir")
    
    if "history_archives" not in st.session_state:
        st.session_state["history_archives"] = []

    if st.session_state["history_archives"]:
        # Filter berdasarkan pencarian
        filtered_archives = [
            (i, arch) for i, arch in enumerate(st.session_state["history_archives"])
            if search_query.lower() in arch['preview'].lower()
        ]

        if filtered_archives:
            # Urutkan dari yang terbaru (paling atas)
            for i, archive in reversed(filtered_archives):
                if st.sidebar.button(f"💬 {archive['preview']}...", key=f"arch_{i}", use_container_width=True):
                    st.session_state["messages"] = list(archive["chats"])
                    st.rerun()
        else:
            st.sidebar.caption("Tidak ada riwayat yang cocok.")
    else:
        st.sidebar.caption("Belum ada riwayat percakapan.")


# Jalankan setup UI
setup_page()

# --- LOAD API KEY DARI .ENV ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- 1. SETUP MODEL & DB (DI-CACHE AGAR CEPAT) ---
@st.cache_resource
def load_chatbot():
    if not api_key:
        st.error("API Key tidak ditemukan! Pastikan file .env sudah benar.")
        st.stop()

    #inisialisasi embedding
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        task_type="retrieval_document",
        google_api_key = api_key
    )

    # 2. Muat database dari folder lokal
    print("Memuat database rules basket dari folder lokal...")
    vector_db = FAISS.load_local(
        "faiss_index_basket", 
        embeddings_model, 
        allow_dangerous_deserialization=True
    )

    template = """
    Kamu adalah asisten pelatih basket yang ramah. 
    1. Gunakan 'Konteks Aturan' di bawah ini sebagai sumber utama untuk menjawab pertanyaan teknis.
    2. Hanya jawab pertanyaan yang berhubungan dengan BASKET.
    3. Jika pertanyaan bersifat umum tentang basket (seperti pemain terkenal atau sejarah) dan tidak ada di konteks, kamu boleh menggunakan pengetahuan umummu sebagai asisten pelatih.
    4. Jika pertanyaan di luar topik basket (seperti sepakbola, memasak, politik, dll), jawablah dengan sopan bahwa kamu hanya ahli dalam bidang basket dan tidak bisa membantu topik lain.

    Konteks Aturan: {context}
    Pertanyaan: {question}

    Jawaban Pelatih:"""

    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

    llm = ChatGoogleGenerativeAI(
            # Gunakan alias 'gemini-flash-latest' agar otomatis memilih yang paling stabil
            model="gemini-flash-latest", 
            google_api_key=api_key,
            temperature=0.1,
            max_retries=0, # Tetap 0 agar tidak buang token kalau error
            # Tambahkan transport agar tidak tersesat ke v1beta
            transport="rest",
            client_options={"api_endpoint": "generativelanguage.googleapis.com"}
        )

    # Buat ulang bot-nya dengan objek 'llm' yang baru saja kita perbaiki
    qa_bot = RetrievalQA.from_chain_type(
        llm=llm, # Objek LLM baru (Flash)
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}), # Mengambil 3 potongan teks terdekat
        chain_type_kwargs={"prompt": PROMPT} # INI KUNCINYA# Pastikan vector_db sudah siap
    )
    return qa_bot

# Inisialisasi bot
bot = load_chatbot()


# 1. Inisialisasi Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 2. LOGIKA TOMBOL (Welcome Cards)
if not st.session_state["messages"]:
    st.subheader("Selamat Datang, Player! 🏀")
    st.write("Coach siap bantu. Coba tanya hal-hal berikut:")
    
    col1, col2 = st.columns(2)
    prompt_to_trigger = None # Variabel bantuan

    with col1:
        if st.button("📏 Dimensi Lapangan"):
            prompt_to_trigger = "Berapa ukuran lapangan basket standar FIBA?"
        if st.button("🏃 Teknik Layup"):
            prompt_to_trigger = "Bagaimana langkah melakukan layup yang benar?"
        if st.button("🏃 All-time Points Leader NBA"):
            prompt_to_trigger = "Siapa pencetak Point terbanyak di NBA?"
    with col2:
        if st.button("⏱️ Aturan 24 Detik"):
            prompt_to_trigger = "Apa itu shot clock 24 detik?"
        if st.button("⛹️ Posisi Pemain"):
            prompt_to_trigger = "Jelaskan peran Point Guard dan Center"
        if st.button("⛹️ Jenis Pelanggaran"):
            prompt_to_trigger = "Jelaskan jenis - jenis pelanggaran di basket"

    # Jika tombol diklik, masukkan ke session state
    if prompt_to_trigger:
        st.session_state["messages"].append({"role": "user", "content": prompt_to_trigger})
        # Jangan pakai st.rerun() di sini agar script lanjut ke bawah dan memproses pesan

# 3. Tampilkan riwayat chat
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Ambil input dari Chat Input (jika ada)
chat_input_val = st.chat_input("Tanya tentang basket")

# 5. LOGIKA PEMROSESAN (Gabungan Chat Input + Tombol)
# Cek apakah ada input baru dari keyboard ATAU ada pesan terakhir yang belum dijawab bot
if chat_input_val:
    current_prompt = chat_input_val
    st.session_state["messages"].append({"role": "user", "content": current_prompt})
    with st.chat_message("user"):
        st.markdown(current_prompt)
    process_response = True
elif st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "user":
    # Ini menangani kasus pesan dari tombol
    current_prompt = st.session_state["messages"][-1]["content"]
    process_response = True
else:
    process_response = False

# 6. JALANKAN RESPONS BOT
if process_response:
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        with st.spinner("Coach sedang membaca buku panduan..."):
            try:
                for chunk in bot.stream({"query": current_prompt}):
                    content = chunk.get("result", "") if isinstance(chunk, dict) else str(chunk)
                    full_response += content
                    placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                
                placeholder.markdown(full_response)
                st.session_state["messages"].append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error("Maaf, Coach sedang sibuk.")