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
    
if 'sablon_w' not in st.session_state:
    st.session_state.sablon_w = 0.0
if 'sablon_r' not in st.session_state:
    st.session_state.sablon_r = 10

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

def sablon_guncelle():
    yeni_w = st.session_state.sablon_w
    yeni_r = st.session_state.sablon_r
    for key in list(st.session_state.keys()):
        if key.startswith("w_new_"):
            st.session_state[key] = yeni_w
        elif key.startswith("r_new_"):
            st.session_state[key] = yeni_r

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
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik"])
    
    st.title(f"👤 {st.session_state.secili_kisi} - Günlük")
    
    if st.button("⬅️ Üyelere Dön"):
        st.session_state.sayfa = 'grup_sayfasi'
        st.rerun()
        
    st.subheader("Yeni Set Ekle")
    secili_tarih = st.date_input("Antrenman Tarihi", value=date.today())
    
    col1, col2 = st.columns(2)
    with col1:
        mevcut_kas_gruplari = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Shoulder", "Biceps", "Triceps", "Legs", "Glutes", "Calves", "Abs", "Forearm", "Neck", "Cardio"]
        secili_kas = st.selectbox("Kas Grubu", mevcut_kas_gruplari)
    with col2:
        filtrelenmis_df = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]
        hareket_listesi = filtrelenmis_df['Hareket Tipi'].unique() if not filtrelenmis_df.empty else []
        secili_hareket = st.selectbox("Hareket", hareket_listesi)

    if secili_hareket:
        mekanik_degeri = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
        st.info(f"Mekanik: **{mekanik_degeri}**")

        if st.session_state.onceki_hareket != secili_hareket:
            st.session_state.onceki_hareket = secili_hareket
            
            gecmis_hareket = df_antrenmanlar[
                (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & 
                (df_antrenmanlar['Hareket'] == secili_hareket)
            ]
            
            if not gecmis_hareket.empty:
                son_agirlik = float(gecmis_hareket.sort_values(by="Tarih", ascending=False).iloc[0]['Ağırlık'])
                st.session_state.sablon_w = son_agirlik
            else:
                st.session_state.sablon_w = 0.0
                
            st.session_state.sablon_r = 10
            
            for key in list(st.session_state.keys()):
                if key.startswith("w_new_") or key.startswith("r_new_"):
                    del st.session_state[key]

    with st.expander("➕ Listede Olmayan Yeni Bir Hareket Ekle"):
        st.write("Veritabanına kalıcı olarak yeni bir hareket ekleyebilirsiniz.")
        c_kas_yeni, c_har_yeni, c_mek_yeni = st.columns(3)
        yeni_kas_grubu = c_kas_yeni.selectbox("Hangi Kas Grubuna?", mevcut_kas_gruplari)
        yeni_hareket_adi = c_har_yeni.text_input("Yeni Hareketin Adı")
        yeni_mekanik = c_mek_yeni.selectbox("Mekanik Tipi", ["Compound", "Izole", "Kardiyo"])
        
        if st.button("Veritabanına Ekle", type="secondary"):
            if yeni_hareket_adi:
                yeni_hareket_satiri = pd.DataFrame([{
                    "Kas Grubu": yeni_kas_grubu, 
                    "Hareket Tipi": yeni_hareket_adi, 
                    "Mekanik": yeni_mekanik
                }])
                guncel_hareketler = pd.concat([df_hareketler, yeni_hareket_satiri], ignore_index=True)
                conn.update(worksheet="Hareketler", data=guncel_hareketler)
                st.cache_data.clear()
                st.success(f"**{yeni_hareket_adi}** başarıyla veritabanına eklendi!")
                st.rerun()
            else:
                st.warning("Lütfen hareket adını girin.")

    st.divider()
    
    if secili_hareket:
        st.write("📌 **Şablon Ayarları (Alttaki setlere otomatik dolar)**")
        
        set_sayisi = st.number_input("Kaç Set Yapılacak?", min_value=1, max_value=10, value=3, step=1)
        
        c_hedef1, c_hedef2 = st.columns(2)
        c_hedef1.number_input("Şablon Ağırlık (kg)", step=2.5, key="sablon_w", on_change=sablon_guncelle)
        c_hedef2.number_input("Şablon Tekrar", step=1, key="sablon_r", on_change=sablon_guncelle)
        
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
            
            w_key = f"w_new_{secili_hareket}_{guncel_set_no}"
            r_key = f"r_new_{secili_hareket}_{guncel_set_no}"
            
            if w_key not in st.session_state:
                st.session_state[w_key] = st.session_state.sablon_w
            if r_key not in st.session_state:
                st.session_state[r_key] = st.session_state.sablon_r
            
            w = c_w.number_input("Ağırlık", step=2.5, key=w_key)
            r = c_r.number_input("Tekrar", step=1, key=r_key)
            
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
            
            for key in list(st.session_state.keys()):
                if key.startswith("w_new_") or key.startswith("r_new_"):
                    del st.session_state[key]
                    
            st.success(f"{secili_hareket} için {set_sayisi} set başarıyla kaydedildi!")
            st.rerun()

    st.divider()
    
    # --- GÜNLÜK ANTRENMAN LİSTESİ (GRUPLANDIRILMIŞ GÖRÜNÜM) ---
    st.subheader(f"📋 {secili_tarih.strftime('%d.%m.%Y')} Antrenmanı")
    
    gunluk_gecmis = df_antrenmanlar[
        (df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
        (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
        (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d"))
    ]
    
    if not gunluk_gecmis.empty:
        # Hareketlere göre benzersiz bir liste oluştur
        yapilan_hareketler = gunluk_gecmis['Hareket'].unique()
        
        for hareket in yapilan_hareketler:
            # Sadece bu harekete ait setleri çek ve set numarasına göre sırala
            hareket_setleri = gunluk_gecmis[gunluk_gecmis['Hareket'] == hareket].sort_values(by="Set")
            toplam_set = len(hareket_setleri)
            
            # Başlık için özet metni oluştur (Örn: 80kgx10 | 82.5kgx8 | 85kgx6)
            ozet_listesi = [f"{row['Ağırlık']}x{row['Tekrar']}" for _, row in hareket_setleri.iterrows()]
            ozet_metni = " | ".join(ozet_listesi)
            
            # Expander (Genişleyebilir Panel) Oluştur
            with st.expander(f"💪 **{hareket}** ({toplam_set} Set) 👉 {ozet_metni}"):
                
                # Panel içindeki her bir seti listele
                for idx, row in hareket_setleri.iterrows():
                    # Düzenleme modu
                    if st.session_state.duzenlenen_idx == idx:
                        st.write(f"**Set {row['Set']} Düzenleniyor**")
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
                    
                    # Normal görünüm (Panel içi okuma/silme)
                    else:
                        col_metin, col_edit, col_sil = st.columns([5, 1, 1])
                        with col_metin:
                            st.write(f"Set {row['Set']}: **{row['Ağırlık']}kg** x {row['Tekrar']} tekrar")
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
