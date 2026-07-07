import streamlit as st
from google.genai import Client
from gtts import gTTS
import os
import re

# --- THIẾT LẬP GIAO DIỆN PREMIUM ---
st.set_page_config(page_title="ENG-GRAMMAR Text Pro", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS để tạo giao diện DashBoard màu tối cao cấp
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

    /* Hiệu ứng cho ô nhập văn bản lớn */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- PHẦN LOGIC ỨNG DỤNG ---

# Sidebar: Cấu hình cấp độ học tập
with st.sidebar:
    st.markdown("<h2 style='color:#38bdf8;'>⚙️ Cấu Hình</h2>", unsafe_allow_html=True)
    level = st.select_slider(
        "Cấp độ phân tích:",
        options=["Cơ bản", "Nâng cao"],
        value="Nâng cao"
    )
    st.divider()
    st.markdown("🚀 *Phiên bản Xử lý Văn bản dài dành cho Boss*")

# Giao diện Trang chính
st.markdown("<h1 style='text-align: center; color: #f8fafc;'>🎯 ENG-GRAMMAR <span style='color:#38bdf8;'>TEXT PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Tự Động Tách Câu & Phân Tích Văn Bản Dài</p>", unsafe_allow_html=True)

# Tự động lấy API Key từ hệ thống Secrets bảo mật
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    client = Client(api_key=api_key)
    
    # Khung nhập văn bản lớn thay thế cho ô nhập câu đơn
    user_text = st.text_area("", placeholder="Dán đoạn văn bản dài hoặc các đoạn hội thoại, bài báo Tiếng Anh của Boss vào đây...", height=150)
    
    if user_text:
        # Sử dụng RegEx để tách đoạn văn thành danh sách các câu dựa vào dấu chấm, dấu chấm hỏi, dấu chấm than
        sentences = re.split(r'(?<=[.!?])\s+', user_text.strip())
        sentences = [s for s in sentences if s] # Loại bỏ khoảng trống thừa
        
        st.markdown(f"### 📋 Hệ thống phát hiện: **{len(sentences)} câu đơn**. Chọn câu để mổ xẻ:")
        
        # Cho Boss chọn câu cụ thể muốn học sâu để tránh tràn màn hình S20 Ultra
        selected_sentence = st.selectbox("Bấm vào đây để chọn câu:", sentences)
        
        if selected_sentence:
            prompt = f"""
            Phân tích câu sau trích từ đoạn văn: "{selected_sentence}" (Cấp độ: {level})
            Trả về kết quả bằng Tiếng Việt theo cấu trúc chuẩn sau:
            
            ### 1. KIỂM TRA NGỮ PHÁP (GRAMMAR CHECK)
            - Trạng thái: [Đúng hay Sai]
            - Giải thích cấu trúc của câu, các cụm từ quan trọng trong ngữ cảnh này.
            
            ### 2. PHÂN TÍCH NGỮ ÂM CHUYÊN SÂU (PHONETICS & TRUNCATION)
            - Chỉ rõ trọng âm câu.
            - Liệt kê chi tiết các vị trí cần Nối âm (Linking sounds).
            - Liệt kê các vị trí cần Nuốt âm/Chặn âm (Glottal stop) để nói trôi chảy toàn văn.
            
            ### 3. KỊCH BẢN HỘI THOẠI MẪU 4 CÂU (INTERACTIVE DIALOGUE)
            Tạo đoạn hội thoại thực tế ngắn 4 câu (A-B-A-B) mở rộng từ câu trên (Kèm dịch nghĩa).
            """
            
            with st.spinner("⚡ AI đang thực hiện bóc tách và mổ xẻ chuyên sâu câu được chọn..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-pro',
                        contents=prompt,
                    )
                    
                    # Chia 2 cột hiển thị kiểu Dashboard Premium
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-header">🔍 PHÂN TÍCH CHI TIẾT CÂU ĐÃ CHỌN</div>
                            <p style="color:#f8fafc; white-space: pre-wrap;">{response.text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Khối trình phát âm thanh riêng cho câu được chọn
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown('<div class="result-header">🔊 LUYỆN NGHE CÂU ĐƠN</div>', unsafe_allow_html=True)
                        
                        tts = gTTS(text=selected_sentence, lang='en', tld='com')
                        tts.save("speech_text.mp3")
                        with open("speech_text.mp3", "rb") as f:
                            data = f.read()
                        st.audio(data, format="audio/mp3")
                        os.remove("speech_text.mp3")
                        
                        st.markdown("<p style='font-size:0.9rem; color:#94a3b8;'>Hệ thống đã tự động ngắt và tạo file nghe riêng cho câu này để Boss luyện tập lặp đi lặp lại dễ dàng.</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Lỗi xử lý hệ thống: {e}")
else:
    st.error("Thiếu mã API Key trong mục Secrets trực tuyến của Streamlit!")