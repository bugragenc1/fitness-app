import streamlit as st
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Antrenman Günlüğü", page_icon="💪", layout="centered")

# Veritabanını yükle
@st.cache_data
def load_data():
    return pd.read_csv("hareketler.csv")

df = load_data()

st.title("💪 Ortak Antrenman Günlüğü")

# Kullanıcı Seçimi
kullanici = st.selectbox("Kullanıcı Seç", ["Bugra", "Arkadaş 1", "Arkadaş 2"])

st.subheader("Yeni Set Ekle")

# Filtreleme için kolonlar
col1, col2, col3 = st.columns(3)

with col1:
    secili_kas = st.selectbox("Kas Grubu", df['Kas Grubu'].unique())

with col2:
    # Sadece seçili kas grubuna ait hareketleri ve mekanikleri getir
    filtrelenmis_df = df[df['Kas Grubu'] == secili_kas]
    secili_hareket = st.selectbox("Hareket", filtrelenmis_df['Hareket Tipi'].unique())

with col3:
    mekanik = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
    st.info(f"Mekanik: {mekanik}")

# Set detayları
col4, col5, col6 = st.columns(3)
with col4:
    agirlik = st.number_input("Ağırlık (kg)", min_value=0.0, step=2.5)
with col5:
    tekrar = st.number_input("Tekrar", min_value=1, step=1)
with col6:
    rpe = st.slider("RPE (Zorluk)", min_value=1, max_value=10, value=8)

if st.button("Kayıt Ekle"):
    # Burada veriyi kaydetme işlemi yapılacak
    st.success(f"{kullanici} için {secili_hareket} ({agirlik} kg x {tekrar} tekrar, RPE: {rpe}) eklendi!")
