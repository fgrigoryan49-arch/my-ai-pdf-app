import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. Կարգավորում ենք էջի տեսքը
st.set_page_config(page_title="Իմ AI Օգնական", page_icon="🤖")
st.title("🤖 Իմ AI Օգնական")
st.write("Բեռնիր PDF ֆայլը և տուր քո հարցը:")

# 2. Միացնում ենք Gemini API-ն (Քո բանալին դիր այստեղ)
genai.configure(api_key="YOUR_GEMINI_API_K")
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Ֆայլի բեռնման դաշտ
uploaded_file = st.file_uploader("Ընտրիր PDF ֆայլը", type="pdf")

# 4. Հարցի դաշտը դնում ենք այստեղ, որ միշտ երևա
user_question = st.text_input("Գրիր քո հարցը այստեղ...")

if uploaded_file is not None:
    try:
        # Կարդում ենք PDF-ը
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        st.success(f"Ֆայլը բեռնվեց! Էջերի քանակը: {len(reader.pages)}")

        # Եթե հարցը գրված է և սեղմում են կոճակը
        if st.button("Հարցրու AI-ին") and user_question:
            with st.spinner('AI-ն մտածում է...'):
                # Ուղարկում ենք տեքստը և հարցը Gemini-ին
                prompt = f"Հիմնվելով հետևյալ տեքստի վրա՝ {text[:30000]}... Պատասխանիր հարցին: {user_question + "\n\n Context: " + text[:20000]}"
                response = model.generate_content(prompt)
                
                st.subheader("Պատասխան:")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Տեղի է ունեցել սխալ: {e}")
else:

    st.info("Խնդրում եմ բեռնել PDF ֆայլ՝ հարցեր տալու համար:")
