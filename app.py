import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Antrenman Günlüğü", page_icon="💪", layout="centered")

# Google Sheets Bağlantısı (Ayarları Secrets'tan alacak)
conn = st.connection("gsheets", type=GSheetsConnection)

# Mevcut verileri canlı olarak oku
try:
    existing_data = conn.read(worksheet="Sheet1", ttl=0)  # ttl=0 önbelleği kapatır, her yenilemede güncel veriyi çeker
except Exception:
    existing_data = pd.DataFrame(columns=["Tarih", "Kullanıcı", "Kas Grubu", "Hareket", "Ağırlık", "Tekrar", "RPE"])

# Yerel hareket listesini oku
df_hareketler = pd.read_csv("hareketler.csv")

st.title("💪 Ortak Antrenman Günlüğü")

# Kullanıcı Seçimi
kullanici = st.selectbox("Kullanıcı Seç", ["Bugra", "Arkadaş 1", "Arkadaş 2"])

st.subheader("Yeni Set Ekle")
col1, col2 = st.columns(2)

with col1:
    secili_kas = st.selectbox("Kas Grubu", df_hareketler['Kas Grubu'].unique())

with col2:
    filtrelenmis_df = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]
    secili_hareket = st.selectbox("Hareket", filtrelenmis_df['Hareket Tipi'].unique())

col3, col4, col5 = st.columns(3)
with col3:
    agirlik = st.number_input("Ağırlık (kg)", min_value=0.0, step=2.5)
with col4:
    tekrar = st.number_input("Tekrar", min_value=1, step=1)
with col5:
    rpe = st.slider("RPE (Zorluk)", min_value=1, max_value=10, value=8)

if st.button("Kayıt Ekle"):
    # Yeni veri satırını oluştur
    new_row = pd.DataFrame([{
        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Kullanıcı": kullanici,
        "Kas Grubu": secili_kas,
        "Hareket": secili_hareket,
        "Ağırlık": agirlik,
        "Tekrar": tekrar,
        "RPE": rpe
    }])
    
    # Eski veriyle yeni veriyi birleştir
    if existing_data.empty:
        updated_df = new_row
    else:
        # Boş sütun veya eşleşme hatasını önlemek için sıralı birleştirme
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    
    # Google Sheets'e veriyi gönder
    conn.update(worksheet="Sheet1", data=updated_df)
    st.success("Set başarıyla buluta kaydedildi!")
    st.rerun()

# Antrenman Geçmişini Tablo Olarak Göster
st.subheader("📋 Antrenman Geçmişi")
if not existing_data.empty:
    # Boş satırları temizle ve tarihe göre tersten sırala
    display_df = existing_data.dropna(how='all')
    st.dataframe(display_df.sort_values(by="Tarih", ascending=False), use_container_width=True)
else:
    st.info("Henüz kayıtlı antrenman bulunmuyor. İlk seti yukarıdan ekleyebilirsin!")
