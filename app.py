
import streamlit as st
from news_api import get_top_headlines, get_custom_news
from pdf_generator import create_newsletter_pdf
from send_email import send_email_with_pdf
import os
import base64
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# --- LOGIN SECTION ---
st.set_page_config(page_title="Newsletter Generator", page_icon="📰", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("🔐 Login to Access Newsletter App")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == os.getenv("APP_USERNAME") and password == os.getenv("APP_PASSWORD"):
            st.session_state.authenticated = True
            st.success("✅ Login successful! Loading app...")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

if not st.session_state.authenticated:
    login()
    st.stop()


def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)

set_bg_from_local("bg.jpg")  # Add your image in project folder



# Streamlit UI
st.title("🗞️ AI Newsletter Generator")

st.write("Generate a newsletter PDF and email it to up to 4 people!")

# Country and category selection
country = st.selectbox("🌍 Select Country", ["USA", "INDIA", "gb", "AUSTRALIA", "ca"])
language = st.selectbox("🌎 Select Language", ["ENGLISH", "HINDI", "FRANCE", "es", "de"])
category = st.selectbox("📚 Select News Category", [
    "business", "entertainment", "general", "health", "science", "sports", "technology"])

# Optional keyword searchS
keyword = st.text_input("🔎 Optional: Search by keyword (e.g., AI, Olympics, Bitcoin)")

# Show warning if keyword is being used
if keyword:
    st.warning("⚠️ Country & category selections will be ignored when searching by keyword.")

# Select number of recipients
num_recipients = st.selectbox("📬 Number of Recipients", [1, 2, 3, 4])

# Email input fields
emails = []
for i in range(num_recipients):
    email = st.text_input(f"Enter email address #{i+1}", key=f"email_{i}")
    if email:
        emails.append(email)

# Schedule toggle (just for UI)
schedule_daily = st.toggle("🕒 Schedule Daily (UI only, no backend)")

# Generate and send button
if st.button("🚀 Generate Newsletter & Send Email"):
    if len(emails) != num_recipients:
        st.error("Please fill all recipient email addresses.")
    else:
        st.info("Fetching news articles...")

        if keyword:
            articles = get_custom_news(query=keyword, language=language)
        else:
            articles = get_top_headlines(category=category, country=country)

        if articles:
            st.success(f"Fetched {len(articles)} articles. Generating PDF...")
            pdf_file = create_newsletter_pdf(articles, category.capitalize() if not keyword else keyword.capitalize())

            st.success(f"PDF created: {pdf_file}")

            for email in emails:
                send_email_with_pdf(pdf_file, receivers=[email])

            st.success("✅ Emails sent successfully!")  
            st.balloons()
            st.markdown("### 🎉 Woohoo! All emails are flying out successfully! 🎉")

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📥 Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_file),
                    mime="application/pdf"
                )
        else:
            st.error("No articles found for this category and country.")
