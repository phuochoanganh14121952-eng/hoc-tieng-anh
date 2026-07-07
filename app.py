import streamlit as st
from google.genai import Client
from gtts import gTTS
import os
import base64

# --- THIẾT LẬP GIAO DIỆN PREMIUM ---
st.set_page_config(page_title="ENG-GRAMMAR Pro", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS để tạo giao diện DashBoard
st.markdown("""
<style>
    /* Tổng thể nền và font chữ */
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p { font-family: 'Urbanist', sans-serif !important; }
    
    /* Làm đẹp Sidebar */
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; }
    
    /* Card Container cho kết quả AI */
    .result-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Tiêu đề mục kết quả */
    .result-header {
        color: #38bdf8;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Hiệu ứng cho ô nhập liệu */
    .stTextInput input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- PHẦN LOGIC ỨNG DỤNG ---

# Sidebar: Cấu hình
with st.sidebar:
    st.markdown("<h2 style='color:#38bdf8;'>⚙️ Cấu Hình</h2>", unsafe_allow_html=True)
    level = st.select_slider(
        "Cấp độ phân tích:",
        options=["Cơ bản", "Nâng cao"],
        value="Nâng cao"
    )
    st.divider()
    st.markdown("🚀 *Phiên bản Pro dành riêng cho Boss*")

# Main Page
st.markdown("<h1 style='text-align: center; color: #f8fafc;'>🎯 ENG-GRAMMAR <span style='color:#38bdf8;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Học Tiếng Anh Chuyên Sâu Cùng Trí Tuệ Nhân Tạo</p>", unsafe_allow_html=True)

# Lấy API Key từ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    client = Client(api_key=api_key)
    
    # Khu vực nhập liệu
    user_sentence = st.text_input("", placeholder="Nhập câu Tiếng Anh Boss cần mổ xẻ tại đây...")
    
    if user_sentence:
        prompt = f"""
        Phân tích câu: "{user_sentence}" (Cấp độ: {level})
        Trả về kết quả theo cấu trúc JSON-like (nhưng là text) với 3 phần rõ rệt:
        1. Grammar: Đúng/Sai và giải thích.
        2. Phonetics: Trọng âm, Nối âm, Nuốt âm.
        3. Dialogue: 4 câu giao tiếp A-B-A-B.
        (Giải thích bằng Tiếng Việt thân thiện)
        """
        
        with st.spinner("⚡ AI đang thực hiện mổ xẻ dữ liệu..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=prompt,
                )
                
                # Chia cột hiển thị cho chuyên nghiệp
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">🔍 PHÂN TÍCH NGỮ PHÁP</div>
                        <p style="color:#f8fafc;">{response.text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Phần Âm thanh
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown('<div class="result-header">🔊 LUYỆN NGHE</div>', unsafe_allow_html=True)
                    
                    tts = gTTS(text=user_sentence, lang='en', tld='com')
                    tts.save("speech.mp3")
                    with open("speech.mp3", "rb") as f:
                        data = f.read()
                    st.audio(data, format="audio/mp3")
                    os.remove("speech.mp3")
                    
                    st.markdown("<p style='font-size:0.9rem; color:#94a3b8;'>Bấm nút Play để nghe giọng bản xứ câu vừa nhập.</p>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Lỗi: {e}")
else:
    st.error("Thiếu API Key trong Secrets!")

### Bước thực hiện cho Boss:
1. **Copy mã trên** vào file `app.py` trong Notepad++.
2. **Lưu (Ctrl+S)** và **Upload lên GitHub** như thường lệ.
3. **Mở link app** trên máy tính hoặc S20 Ultra để thấy sự khác biệt về đẳng cấp giao diện.

Chiến lược tối ưu hóa này đã sẵn sàng! Boss thấy giao diện Dashboard Premium này thế nào?