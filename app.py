import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Antrenman Günlüğü", page_icon="💪", layout="centered")

# --- OTURUM (SESSION STATE) DEĞİŞKENLERİ ---
if 'sayfa' not in st.session_state:
    st.session_state.sayfa = 'ana_sayfa'
if 'secili_grup' not in st.session_state:
    st.session_state.secili_grup = None
if 'secili_kisi' not in st.session_state:
    st.session_state.secili_kisi = None
if 'duzenlenen_idx' not in st.session_state:
    st.session_state.duzenlenen_idx = None
if 'onceki_hareket' not in st.session_state:
    st.session_state.onceki_hareket = ""
if 'hareket_agirlik' not in st.session_state:
    st.session_state.hareket_agirlik = 0.0

# --- GOOGLE SHEETS BAĞLANTISI ---
conn = st.connection("gsheets", type=GSheetsConnection)

def veri_getir(sekme_adi, kolonlar):
    try:
        df = conn.read(worksheet=sekme_adi, ttl=5)
        if df.empty:
            return pd.DataFrame(columns=kolonlar)
        return df.dropna(how='all')
    except:
        return pd.DataFrame(columns=kolonlar)

@st.cache_data
def hareketleri_getir():
    return pd.read_csv("hareketler.csv")

# Şablon değiştiğinde alt setlerin hafızasını silen fonksiyon
def alt_setleri_sifirla():
    for key in list(st.session_state.keys()):
        if key.startswith("w_new_") or key.startswith("r_new_"):
            del st.session_state[key]

# --- SAYFA 1: ANA SAYFA (GRUPLAR) ---
if st.session_state.sayfa == 'ana_sayfa':
    df_gruplar = veri_getir("Gruplar", ["Grup Adı"])
    st.title("🏋️‍♂️ Antrenman Grupları")
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
    yeni_grup = st.text_input("Yeni Grup Oluştur")
    if st.button("Grup Ekle", type="primary"):
        if yeni_grup:
            yeni_satir = pd.DataFrame([{"Grup Adı": yeni_grup}])
            guncel_gruplar = pd.concat([df_gruplar, yeni_satir], ignore_index=True)
            conn.update(worksheet="Gruplar", data=guncel_gruplar)
            st.cache_data.clear() 
            st.success(f"{yeni_grup} başarıyla oluşturuldu!")
            st.rerun()

# --- SAYFA 2: GRUP İÇİ (KİŞİLER) ---
elif st.session_state.sayfa == 'grup_sayfasi':
    df_kullanicilar = veri_getir("Kullanicilar", ["Grup Adı", "Kullanıcı Adı"])
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
    yeni_kisi = st.text_input("Bu gruba yeni kişi ekle")
    if st.button("Kişi Ekle", type="primary"):
        if yeni_kisi:
            yeni_satir = pd.DataFrame([{"Grup Adı": st.session_state.secili_grup, "Kullanıcı Adı": yeni_kisi}])
            guncel_kullanicilar = pd.concat([df_kullanicilar, yeni_satir], ignore_index=True)
            conn.update(worksheet="Kullanicilar", data=guncel_kullanicilar)
            st.cache_data.clear()
            st.success(f"{yeni_kisi} gruba eklendi!")
            st.rerun()

# --- SAYFA 3: KİŞİ DETAYI VE HAREKET EKLEME ---
elif st.session_state.sayfa == 'kisi_sayfasi':
    df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Mekanik"])
    df_hareketler = hareketleri_getir()
    
    st.title(f"👤 {st.session_state.secili_kisi} - Günlük")
    
    if st.button("⬅️ Üyelere Dön"):
        st.session_state.sayfa = 'grup_sayfasi'
        st.rerun()
        
    st.subheader("Yeni Set Ekle")
    secili_tarih = st.date_input("Antrenman Tarihi", value=date.today())
    
    col1, col2 = st.columns(2)
    with col1:
        secili_kas = st.selectbox("Kas Grubu", df_hareketler['Kas Grubu'].unique())
    with col2:
        filtrelenmis_df = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]
        secili_hareket = st.selectbox("Hareket", filtrelenmis_df['Hareket Tipi'].unique())

    mekanik_degeri = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
    st.info(f"Mekanik: **{mekanik_degeri}**")

    # --- GEÇMİŞ AĞIRLIĞI BULMA VE SIFIRLAMA ---
    if st.session_state.onceki_hareket != secili_hareket:
        st.session_state.onceki_hareket = secili_hareket
        alt_setleri_sifirla() # Yeni harekete geçildiğinde alt formları temizle
        
        gecmis_hareket = df_antrenmanlar[
            (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & 
            (df_antrenmanlar['Hareket'] == secili_hareket)
        ]
        if not gecmis_hareket.empty:
            son_agirlik = gecmis_hareket.sort_values(by="Tarih", ascending=False).iloc[0]['Ağırlık']
            st.session_state.hareket_agirlik = float(son_agirlik)
        else:
            st.session_state.hareket_agirlik = 0.0

    st.divider()
    
    # --- TOPLU SET EKLEME ALANI ---
    st.write("📌 **Şablon Ayarları (Alttaki setlere otomatik dolar)**")
    
    # on_change tetikleyicileri eklendi. Değer değiştiği an alt_setleri_sifirla fonksiyonu çalışır.
    set_sayisi = st.number_input("Kaç Set Yapılacak?", min_value=1, max_value=10, value=3, step=1, on_change=alt_setleri_sifirla)
    
    c_hedef1, c_hedef2 = st.columns(2)
    hedef_agirlik = c_hedef1.number_input("Şablon Ağırlık (kg)", value=float(st.session_state.hareket_agirlik), step=2.5, on_change=alt_setleri_sifirla)
    hedef_tekrar = c_hedef2.number_input("Şablon Tekrar", value=10, step=1, on_change=alt_setleri_sifirla)
    
    st.write("---")
    st.write("📝 **Set Detaylarını Düzenle (İsteğe Bağlı)**")
    
    bugunku_setler = df_antrenmanlar[
        (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) &
        (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
        (df_antrenmanlar['Hareket'] == secili_hareket)
    ]
    baslangic_seti = len(bugunku_setler) + 1
    
    eklenecek_setler = []
    
    for i in range(set_sayisi):
        guncel_set_no = baslangic_seti + i
        c_label, c_w, c_r = st.columns([1,2,2])
        c_label.markdown(f"<div style='margin-top: 25px;'>**Set {guncel_set_no}**</div>", unsafe_allow_html=True)
        
        # Benzersiz anahtarlar (key) hareket adını da içerir
        w = c_w.number_input("Ağırlık", value=float(hedef_agirlik), step=2.5, key=f"w_new_{secili_hareket}_{guncel_set_no}")
        r = c_r.number_input("Tekrar", value=int(hedef_tekrar), step=1, key=f"r_new_{secili_hareket}_{guncel_set_no}")
        
        eklenecek_setler.append({
            "Tarih": secili_tarih.strftime("%Y-%m-%d"),
            "Grup": st.session_state.secili_grup,
            "Kullanıcı": st.session_state.secili_kisi,
            "Kas Grubu": secili_kas,
            "Hareket": secili_hareket,
            "Set": guncel_set_no,
            "Ağırlık": w,
            "Tekrar": r,
            "Mekanik": mekanik_degeri
        })
        
    if st.button("Tüm Setleri Kaydet", type="primary", use_container_width=True):
        yeni_satirlar = pd.DataFrame(eklenecek_setler)
        guncel_antrenmanlar = pd.concat([df_antrenmanlar, yeni_satirlar], ignore_index=True)
        
        conn.update(worksheet="Antrenmanlar", data=guncel_antrenmanlar)
        st.cache_data.clear()
        
        # Başarıyla kaydedildikten sonra da set formlarını temizliyoruz
        alt_setleri_sifirla()
        
        st.success(f"{secili_hareket} için {set_sayisi} set başarıyla kaydedildi!")
        st.rerun()

    st.divider()
    
    # --- GÜNLÜK ANTRENMAN LİSTESİ ---
    st.subheader(f"📋 {secili_tarih.strftime('%d.%m.%Y')} Antrenmanı")
    
    gunluk_gecmis = df_antrenmanlar[
        (df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
        (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
        (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d"))
    ]
    
    if not gunluk_gecmis.empty:
        for idx, row in gunluk_gecmis.iterrows():
            if st.session_state.duzenlenen_idx == idx:
                st.write(f"**{row['Hareket']} - Set {row['Set']} Düzenleniyor**")
                d1, d2, d3, d4 = st.columns(4)
                yeni_agirlik = d1.number_input("Ağırlık", value=float(row['Ağırlık']), step=2.5, key=f"edit_w_{idx}")
                yeni_tekrar = d2.number_input("Tekrar", value=int(row['Tekrar']), step=1, key=f"edit_r_{idx}")
                
                if d3.button("💾 Kaydet", key=f"save_{idx}"):
                    df_antrenmanlar.at[idx, 'Ağırlık'] = yeni_agirlik
                    df_antrenmanlar.at[idx, 'Tekrar'] = yeni_tekrar
                    conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar)
                    st.session_state.duzenlenen_idx = None
                    st.cache_data.clear()
                    st.rerun()
                    
                if d4.button("İptal", key=f"cancel_{idx}"):
                    st.session_state.duzenlenen_idx = None
                    st.rerun()
            else:
                col_metin, col_edit, col_sil = st.columns([5, 1, 1])
                with col_metin:
                    st.write(f"💪 **{row['Hareket']}** (Set {row['Set']}) | {row['Ağırlık']}kg x {row['Tekrar']} tekrar")
                with col_edit:
                    if st.button("✏️", key=f"edit_btn_{idx}"):
                        st.session_state.duzenlenen_idx = idx
                        st.rerun()
                with col_sil:
                    if st.button("❌", key=f"sil_btn_{idx}"):
                        df_antrenmanlar = df_antrenmanlar.drop(idx)
                        conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar)
                        st.cache_data.clear()
                        st.rerun()
    else:
        st.info("Bu tarihte henüz bir antrenman kaydı yok.")
