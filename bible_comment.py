import streamlit as st
import google.generativeai as genai

# Gemini 설정 및 해설 생성 함수
def ask_bible_explanation(book, chapter, verse, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")  # 사용자 설정 반영

    prompt = f"""
    아래에 입력된 성경 구절({book} {chapter}:{verse})을 한국어로 설명해 주세요.

    - 구절의 원뜻과 문맥, 배경을 설명해 주세요.
    - 신학적 의미, 교훈, 현대적 적용까지 간단히 요약해 주세요.
    - 너무 전문적이지 않게, 다양한 연령대가 이해할 수 있도록 설명해 주세요.
    - 해당 본문은 NIV 또는 개역개정 버전 중 하나라고 가정해 주세요.

    성경 구절: {book} {chapter}:{verse}
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit 앱 메인 함수
def main():
    st.set_page_config(page_title="📖 성경 구절 해설 앱")
    st.title("📖 성경 말씀 해설기")

    if "GEMINI_API" not in st.session_state:
        st.session_state["GEMINI_API"] = ""

    with st.sidebar:
        api_key = "AIzaSyD2vnmS8q_xWhnn6zSsnPs1LpzydRzfyAA"  ## st.text_input("🔑 Gemini API Key", type="password")
        if api_key:
            st.session_state["GEMINI_API"] = api_key
        st.markdown("---")

    # 사용자 입력: 성경 장절
    book = st.text_input("📘 성경 책 이름", placeholder="예: 요한복음")
    chapter = st.text_input("🔢 장 (Chapter)", placeholder="예: 3")
    verse = st.text_input("🔢 절 (Verse)", placeholder="예: 16")

    if st.button("🔍 해설 보기"):
        if book and chapter and verse:
            try:
                result = ask_bible_explanation(book, chapter, verse, st.session_state["GEMINI_API"])
                st.subheader(f"📜 {book} {chapter}:{verse} 해설")
                st.success(result)
            except Exception as e:
                st.error(f"오류 발생: {e}")
        else:
            st.warning("책 이름, 장, 절을 모두 입력해 주세요.")

if __name__ == "__main__":
    main()
