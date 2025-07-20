import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Apply custom HTML + CSS
st.markdown("""
    <style>
        body {
            background-color: #f4f6f9;
        }
        .main {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f77b4;
            font-family: 'Segoe UI', sans-serif;
        }
        .stTextInput>div>div>input {
            background-color: #eef6fb;
        }
        .css-1n76uvr {
            color: #5b5b5b;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)

# Title and description
st.title("E-commerce Product Dashboard")
st.write("Enter a demo e-commerce URL to fetch product data with a interface.")

# Input
url = st.text_input("Enter E-commerce URL", "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")

# Scrape function
@st.cache_data(ttl=300)
def scrape_products(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []
    for p in soup.select('.thumbnail'):
        title = p.select_one('.title').get('title')
        price = p.select_one('.price').get_text(strip=True)
        desc = p.select_one('.description').get_text(strip=True)
        data.append({'Title': title, 'Price': price, 'Description': desc})
    return pd.DataFrame(data)

# Show data
if st.button("Scrape Products"):
    try:
        df = scrape_products(url)
        st.success("Products scraped successfully!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "products.csv", "text/csv")
    except Exception as e:
        st.error(f"Error: {e}")

# Close custom layout div
