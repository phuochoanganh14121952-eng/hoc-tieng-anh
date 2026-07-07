import streamlit as st
from google.genai import Client

# Khởi tạo giao diện
st.title("English Learning Assistant for Boss")
st.write("Nhập một câu Tiếng Anh để AI kiểm tra ngữ pháp và giải thích.")

# Tự động lấy API Key từ hệ thống cấu hình bảo mật Secrets của Streamlit
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Nhập Gemini API Key của Boss:", type="password")

if api_key:
    client = Client(api_key=api_key)
    
    # Ô nhập liệu câu tiếng Anh
    user_sentence = st.text_input("Nhập câu Tiếng Anh tại đây:")
    
    if user_sentence:
        prompt = f"""
        Bạn là một giáo viên Tiếng Anh bản xứ dạy cho người Việt. 
        Hãy kiểm tra câu sau: "{user_sentence}"
        1. Chỉ ra câu này đúng hay sai ngữ pháp. Nếu sai, sửa lại cho đúng và giải thích lý do ngắn gọn.
        2. Cung cấp 2 câu ví dụ tương tự để luyện tập giao tiếp.
        """
        
        with st.spinner("AI đang phân tích câu..."):
            try:
                # Sử dụng mô hình thế hệ mới gemini-2.5-pro
                response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=prompt,
                )
                st.subheader("Kết quả phản hồi từ AI:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
else:
    st.warning("Vui lòng cấu hình API Key để kích hoạt trợ lý AI.")