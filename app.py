import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Sayfa Yapılandırması
st.set_page_config(page_title="Antrenman Günlüğü", page_icon="💪", layout="centered")

# Oturum (Session State) Değişkenlerini Başlat
if 'sayfa' not in st.session_state:
    st.session_state.sayfa = 'ana_sayfa'
if 'secili_grup' not in st.session_state:
    st.session_state.secili_grup = None
if 'secili_kisi' not in st.session_state:
    st.session_state.secili_kisi = None

# Google Sheets Bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# --- VERİ OKUMA FONKSİYONLARI ---
def veri_getir(sekme_adi, kolonlar):
    try:
        df = conn.read(worksheet=sekme_adi, ttl=0)
        if df.empty:
            return pd.DataFrame(columns=kolonlar)
        return df.dropna(how='all')
    except:
        return pd.DataFrame(columns=kolonlar)

df_gruplar = veri_getir("Gruplar", ["Grup Adı"])
df_kullanicilar = veri_getir("Kullanicilar", ["Grup Adı", "Kullanıcı Adı"])
df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Ağırlık", "Tekrar", "RPE"])
df_hareketler = pd.read_csv("hareketler.csv")

# --- SAYFA 1: ANA SAYFA (GRUPLAR) ---
if st.session_state.sayfa == 'ana_sayfa':
    st.title("🏋️‍♂️ Antrenman Grupları")
    
    # Mevcut Grupları Listele
    st.subheader("Mevcut Gruplar")
    if not df_gruplar.empty:
        for index, row in df_gruplar.iterrows():
            grup_adi = row['Grup Adı']
            if st.button(f"📁 {grup_adi}", use_container_width=True):
                st.session_state.secili_grup = grup_adi
                st.session_state.sayfa = 'grup_sayfasi'
                st.rerun()
    else:
        st.info("Henüz kayıtlı bir grup yok.")
        
    st.divider()
    
    # Yeni Grup Ekle
    yeni_grup = st.text_input("Yeni Grup Oluştur (Örn: Ataşehir Spor Kulübü)")
    if st.button("Grup Ekle", type="primary"):
        if yeni_grup:
            yeni_satir = pd.DataFrame([{"Grup Adı": yeni_grup}])
            guncel_gruplar = pd.concat([df_gruplar, yeni_satir], ignore_index=True)
            conn.update(worksheet="Gruplar", data=guncel_gruplar)
            st.success(f"{yeni_grup} başarıyla oluşturuldu!")
            st.rerun()

# --- SAYFA 2: GRUP İÇİ (KİŞİLER) ---
elif st.session_state.sayfa == 'grup_sayfasi':
    st.title(f"📁 {st.session_state.secili_grup}")
    
    if st.button("⬅️ Gruplara Dön"):
        st.session_state.sayfa = 'ana_sayfa'
        st.rerun()
        
    st.subheader("Üyeler")
    grup_uyeleri = df_kullanicilar[df_kullanicilar['Grup Adı'] == st.session_state.secili_grup]
    
    if not grup_uyeleri.empty:
        for index, row in grup_uyeleri.iterrows():
            kisi_adi = row['Kullanıcı Adı']
            if st.button(f"👤 {kisi_adi}", use_container_width=True):
                st.session_state.secili_kisi = kisi_adi
                st.session_state.sayfa = 'kisi_sayfasi'
                st.rerun()
    else:
        st.info("Bu gruba henüz kimse eklenmemiş.")
        
    st.divider()
    
    # Yeni Kişi Ekle
    yeni_kisi = st.text_input("Bu gruba yeni kişi ekle")
    if st.button("Kişi Ekle", type="primary"):
        if yeni_kisi:
            yeni_satir = pd.DataFrame([{"Grup Adı": st.session_state.secili_grup, "Kullanıcı Adı": yeni_kisi}])
            guncel_kullanicilar = pd.concat([df_kullanicilar, yeni_satir], ignore_index=True)
            conn.update(worksheet="Kullanicilar", data=guncel_kullanicilar)
            st.success(f"{yeni_kisi} gruba eklendi!")
            st.rerun()

# --- SAYFA 3: KİŞİ DETAYI VE HAREKET EKLEME ---
elif st.session_state.sayfa == 'kisi_sayfasi':
    st.title(f"👤 {st.session_state.secili_kisi} - Antrenman Günlüğü")
    
    if st.button("⬅️ Üyelere Dön"):
        st.session_state.sayfa = 'grup_sayfasi'
        st.rerun()
        
    st.subheader("Yeni Set Ekle")
    
    # Takvimden Tarih Seçimi
    secili_tarih = st.date_input("Antrenman Tarihi", value=date.today())
    
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

    if st.button("Kayıt Ekle", type="primary"):
        yeni_satir = pd.DataFrame([{
            "Tarih": secili_tarih.strftime("%Y-%m-%d"),
            "Grup": st.session_state.secili_grup,
            "Kullanıcı": st.session_state.secili_kisi,
            "Kas Grubu": secili_kas,
            "Hareket": secili_hareket,
            "Ağırlık": agirlik,
            "Tekrar": tekrar,
            "RPE": rpe
        }])
        
        guncel_antrenmanlar = pd.concat([df_antrenmanlar, yeni_satir], ignore_index=True)
        conn.update(worksheet="Antrenmanlar", data=guncel_antrenmanlar)
        st.success("Set başarıyla buluta kaydedildi!")
        st.rerun()

    st.divider()
    
    # Kişiye Özel Geçmiş
    st.subheader("📋 Kişisel Antrenman Geçmişi")
    kisisel_gecmis = df_antrenmanlar[
        (df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
        (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi)
    ]
    
    if not kisisel_gecmis.empty:
        st.dataframe(kisisel_gecmis.sort_values(by="Tarih", ascending=False).drop(columns=["Grup", "Kullanıcı"]), use_container_width=True)
    else:
        st.info("Henüz bu kişiye ait bir antrenman kaydı yok.")
