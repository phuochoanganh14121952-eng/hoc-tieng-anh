import streamlit as st
from google.genai import Client

# Khởi tạo giao diện trang web
st.set_page_config(page_title="ENG-GRAMMAR Pro", layout="wide")

st.title("🎯 English Learning Assistant for Boss (Pro Version)")
st.write("Trợ lý phân tích ngữ pháp, phát âm chuyên sâu và luyện giao tiếp phản xạ.")

# Thanh cấu hình ở cột bên trái (Sidebar)
with st.sidebar:
    st.header("⚙️ Cấu hình học tập")
    # Tính năng 4: Thanh chọn cấp độ giải thích
    level = st.select_slider(
        "Chọn cấp độ phân tích của AI:",
        options=["Cơ bản (Ngắn gọn)", "Nâng cao (Phân tích sâu)"],
        value="Nâng cao (Phân tích sâu)"
    )
    st.info(f"Chế độ hiện tại: {level}")

# Tự động lấy API Key từ cấu hình Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Nhập Gemini API Key của Boss:", type="password")

if api_key:
    client = Client(api_key=api_key)
    
    # Ô nhập liệu câu tiếng Anh
    user_sentence = st.text_input("✍️ Nhập câu Tiếng Anh của Boss cần mổ xẻ tại đây:")
    
    if user_sentence:
        # Xây dựng cấu trúc prompt ép AI trả về định dạng rõ ràng
        prompt = f"""
        Bạn là một chuyên gia ngôn ngữ và giáo viên Tiếng Anh bản xứ dạy cho người Việt. 
        Hãy phân tích câu sau: "{user_sentence}" với tiêu chí {level}.
        
        Yêu cầu cấu trúc đầu ra bắt buộc phải có các mục sau:
        
        ### 1. KIỂM TRA NGỮ PHÁP (GRAMMAR CHECK)
        - Trạng thái: [Đúng hay Sai]
        - Giải thích chi tiết cấu trúc, lỗi sai (nếu có) và cách sửa.
        
        ### 2. PHÂN TÍCH NGỮ ÂM CHUYÊN SÂU (PHONETICS & TRUNCATION)
        - Chỉ rõ các từ có trọng âm chính trong câu.
        - Liệt kê chi tiết các vị trí cần Nối âm (Linking sounds).
        - Liệt kê các vị trí cần Nuốt âm/Chặn âm (Glottal stop / Truncation) để nói tự nhiên.
        
        ### 3. KỊCH BẢN HỘI THOẠI MẪU 4 CÂU (INTERACTIVE DIALOGUE)
        Tạo một đoạn hội thoại ngắn 4 câu (A - B - A - B) thực tế hàng ngày chứa câu trên:
        - Câu A1 (Tiếng Anh) + Dịch nghĩa
        - Câu B1 (Tiếng Anh) + Dịch nghĩa
        - Câu A2 (Tiếng Anh) + Dịch nghĩa
        - Câu B2 (Tiếng Anh) + Dịch nghĩa
        """
        
        with st.spinner("AI đang mổ xẻ chuyên sâu ngữ pháp và ngữ âm..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=prompt,
                )
                
                # Hiển thị kết quả phân tích
                st.markdown("---")
                st.subheader("📊 Kết quả phân tích chi tiết cho Boss:")
                st.write(response.text)
                
                # Tính năng 3: Tích hợp nút phát âm mẫu cho câu vừa nhập
                st.markdown("---")
                st.subheader("🔊 Luyện nghe phát âm câu gốc:")
                # Sử dụng tính năng Text-to-Speech cơ bản bằng HTML5 của trình duyệt
                tts_html = f"""
                <audio controls autoplay src="https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={user_sentence.replace(' ', '%20')}">
                Trình duyệt của bạn không hỗ trợ phát âm thanh.
                </audio>
                """
                st.components.v1.html(tts_html, height=50)
                
            except Exception as e:
                st.error(f"Lỗi kết nối hoặc xử lý: {e}")
else:
    st.warning("Vui lòng cấu hình API Key trong mục Secrets của Streamlit để kích hoạt.")