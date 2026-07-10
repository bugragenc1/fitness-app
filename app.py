import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import calendar as cal_module
from datetime import date
import time

# --- SAYFA YAPILANDIRMASI & ÖZEL CSS (B15: Görsel Kimlik) ---
st.set_page_config(page_title="Workout App", page_icon="💪", layout="centered", initial_sidebar_state="collapsed")

custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    :root {
        --primary-color: #ff4b4b;
        --bg-color: #0e1117;
        --card-bg: rgba(255, 255, 255, 0.05);
    }
    .block-container {
        padding: 1.5rem 1rem 2rem 1rem;
        max-width: 800px;
    }
    div[data-testid="stButton"] > button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.2);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(0);
    }
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        background-color: transparent !important;
    }
    input, select {
        border-radius: 8px !important;
    }
    /* Toast mesajlarını belirginleştir */
    div[data-testid="stToast"] {
        border-radius: 10px;
        background-color: #2b2b2b;
        color: white;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- GOOGLE SHEETS BAĞLANTISI ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- A5 & A2 ÇÖZÜMÜ: Hedefli Cache Temizliği ve Hata Yakalama ---
@st.cache_data(ttl=60)
def veri_getir(sekme_adi):
    try:
        df = conn.read(worksheet=sekme_adi)
        if df is None or df.empty:
            return pd.DataFrame()
        df.fillna(0, inplace=True)
        return df.dropna(how='all')
    except Exception as e:
        # A2: Hata gizleme çözüldü
        st.error(f"Veri bağlantı hatası ({sekme_adi}): Lütfen internet bağlantınızı kontrol edin.")
        return pd.DataFrame()

# --- A1 ÇÖZÜMÜ: Eşzamanlı Kullanım (Optimistic Fetch) ---
def guvenli_veri_yaz(sekme_adi, yeni_df, degisim_tipi="ekle"):
    try:
        if degisim_tipi == "ekle":
            # Yazmadan hemen önce en güncel veriyi zorla çek (Cache atla)
            veri_getir.clear(sekme_adi)
            guncel_df = veri_getir(sekme_adi)
            yazilacak_df = pd.concat([guncel_df, yeni_df], ignore_index=True)
        else:
            # Silme/Güncelleme için direkt üzerine yaz
            yazilacak_df = yeni_df
            
        conn.update(worksheet=sekme_adi, data=yazilacak_df)
        veri_getir.clear(sekme_adi) # Sadece ilgili sekmenin cache'ini temizle
        return True
    except Exception as e:
        st.error(f"Kayıt işlemi başarısız: {e}")
        return False

# --- OTURUM DEĞİŞKENLERİ ---
varsayilan_state = {
    'sayfa': 'ana_sayfa', 'secili_grup': None, 'secili_kisi': None, 
    'secili_tarih_widget': date.today(), 'takvim_yil': date.today().year, 'takvim_ay': date.today().month,
    'sablon_w': 0.0, 'sablon_r': 10, 'toast_msg': None, 'toast_icon': None, 'toast_balloons': False
}
for k, v in varsayilan_state.items():
    if k not in st.session_state:
        st.session_state[k] = v

EKIPMAN_LISTESI = ["Barbell", "Dumbbell", "Machine", "Cable", "Bodyweight", "Band", "Smith Machine", "Kettlebell", "Other", "-"]

# --- A3 ÇÖZÜMÜ: Başarı Mesajı Yöneticisi ---
def mesaj_goster():
    if st.session_state.toast_msg:
        st.toast(st.session_state.toast_msg, icon=st.session_state.toast_icon)
        if st.session_state.toast_balloons:
            st.balloons()
        st.session_state.toast_msg = None
        st.session_state.toast_balloons = False

# --- B9 ÇÖZÜMÜ: Modal Diyaloglar ---
@st.dialog("🗑️ Kayıt Silme Onayı")
def silme_onay_modal(hareket_adi, silinecek_index_listesi):
    st.warning(f"**{hareket_adi}** hareketine ait tüm setleri bu tarihten silmek üzeresiniz. Emin misiniz?")
    c1, c2 = st.columns(2)
    if c1.button("✅ Evet, Sil", type="primary", use_container_width=True):
        df_ant = veri_getir("Antrenmanlar")
        yeni_df = df_ant.drop(silinecek_index_listesi)
        if guvenli_veri_yaz("Antrenmanlar", yeni_df, degisim_tipi="guncelle"):
            st.session_state.toast_msg = f"{hareket_adi} silindi."
            st.session_state.toast_icon = "🗑️"
            st.rerun()
    if c2.button("İptal", use_container_width=True):
        st.rerun()

# Ortak Navigasyon Barı
def render_top_nav():
    st.write("")
    n1, n2, n3 = st.columns([1,1,1])
    with n1:
        if st.button("📝 Günlük", type="primary" if st.session_state.sayfa == 'kisi_sayfasi' else "secondary", use_container_width=True):
            st.session_state.sayfa = 'kisi_sayfasi'; st.rerun()
    with n2:
        if st.button("⚖️ Vücut", type="primary" if st.session_state.sayfa == 'vucut_sayfasi' else "secondary", use_container_width=True):
            st.session_state.sayfa = 'vucut_sayfasi'; st.rerun()
    with n3:
        if st.button("📊 İstatistik", type="primary" if st.session_state.sayfa == 'istatistik_sayfasi' else "secondary", use_container_width=True):
            st.session_state.sayfa = 'istatistik_sayfasi'; st.rerun()
    st.divider()

# --- UYGULAMA AKIŞI ---
mesaj_goster()

# A8: Tarih Formatlama Fonksiyonu
def format_date(d):
    return pd.to_datetime(d).strftime("%Y-%m-%d")

# --- SAYFA 1: ANA SAYFA (GRUPLAR) ---
if st.session_state.sayfa == 'ana_sayfa':
    df_gruplar = veri_getir("Gruplar")
    if 'Grup Adı' not in df_gruplar.columns: df_gruplar = pd.DataFrame(columns=['Grup Adı'])
    
    st.markdown("<h1>🏋️‍♂️ Antrenman Grupları</h1>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<h3>📁 Mevcut Gruplar</h3>", unsafe_allow_html=True)
        for index, row in df_gruplar.iterrows():
            if st.button(f"📁 {row['Grup Adı']}", use_container_width=True):
                st.session_state.secili_grup = row['Grup Adı']
                st.session_state.sayfa = 'grup_sayfasi'
                st.rerun()
                
    with st.container(border=True):
        yeni_grup = st.text_input("➕ Yeni Grup Oluştur", label_visibility="collapsed", placeholder="Grup Adı...")
        if st.button("Oluştur", type="primary", use_container_width=True) and yeni_grup:
            yeni_satir = pd.DataFrame([{"Grup Adı": yeni_grup}])
            if guvenli_veri_yaz("Gruplar", yeni_satir, "ekle"):
                st.session_state.toast_msg = f"{yeni_grup} başarıyla oluşturuldu!"
                st.session_state.toast_icon = "✅"
                st.rerun()

# --- SAYFA 2: GRUP İÇİ (KİŞİLER) ---
elif st.session_state.sayfa == 'grup_sayfasi':
    df_kullanicilar = veri_getir("Kullanicilar")
    if 'Kullanıcı Adı' not in df_kullanicilar.columns: df_kullanicilar = pd.DataFrame(columns=['Grup Adı', 'Kullanıcı Adı'])
    
    if st.button("⬅️ Gruplara Dön"):
        st.session_state.sayfa = 'ana_sayfa'; st.rerun()
        
    st.markdown(f"<h1>📁 {st.session_state.secili_grup}</h1>", unsafe_allow_html=True)
    
    with st.container(border=True):
        grup_uyeleri = df_kullanicilar[df_kullanicilar['Grup Adı'] == st.session_state.secili_grup]
        for index, row in grup_uyeleri.iterrows():
            if st.button(f"👤 {row['Kullanıcı Adı']}", use_container_width=True):
                st.session_state.secili_kisi = row['Kullanıcı Adı']
                st.session_state.sayfa = 'kisi_sayfasi'
                st.rerun()
                
    with st.container(border=True):
        yeni_kisi = st.text_input("➕ Yeni Kişi Ekle", label_visibility="collapsed", placeholder="Kullanıcı Adı...")
        if st.button("Ekle", type="primary", use_container_width=True) and yeni_kisi:
            yeni_satir = pd.DataFrame([{"Grup Adı": st.session_state.secili_grup, "Kullanıcı Adı": yeni_kisi}])
            if guvenli_veri_yaz("Kullanicilar", yeni_satir, "ekle"):
                st.session_state.toast_msg = f"{yeni_kisi} eklendi!"
                st.session_state.toast_icon = "✅"
                st.rerun()

# --- SAYFA 3: GÜNLÜK ANTRENMAN LOGU ---
elif st.session_state.sayfa == 'kisi_sayfasi':
    if st.button("⬅️ Üyelere Dön"):
        st.session_state.sayfa = 'grup_sayfasi'; st.rerun()
        
    render_top_nav()
    st.markdown(f"<h2>👤 {st.session_state.secili_kisi}</h2>", unsafe_allow_html=True)
    
    df_antrenmanlar = veri_getir("Antrenmanlar")
    df_hareketler = veri_getir("Hareketler")
    
    # Tarih Formatı Garantisi
    secili_tarih_str = st.session_state["secili_tarih_widget"].strftime("%Y-%m-%d")
    
    # Tarih Seçici Widget (Basitleştirilmiş Streamlit Native Date Input)
    st.session_state["secili_tarih_widget"] = st.date_input("📅 Tarih Seç", st.session_state["secili_tarih_widget"])
    
    with st.container(border=True):
        st.markdown("### ➕ Yeni Set Ekle")
        mevcut_kas_gruplari = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Legs"]
        c1, c2 = st.columns(2)
        secili_kas = c1.selectbox("Kas Grubu", mevcut_kas_gruplari)
        hareket_listesi = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]['Hareket Tipi'].unique() if not df_hareketler.empty else []
        secili_hareket = c2.selectbox("Hareket", hareket_listesi)

        if secili_hareket:
            mekanik = df_hareketler[df_hareketler['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
            ekipman = df_hareketler[df_hareketler['Hareket Tipi'] == secili_hareket].get('Ekipman', pd.Series(["Barbell"])).values[0]
            
            cW, cR, cBtn = st.columns([1,1,1])
            w = cW.number_input("Ağırlık (kg)", min_value=0.0, step=2.5, value=st.session_state.sablon_w)
            r = cR.number_input("Tekrar", min_value=0, step=1, value=st.session_state.sablon_r)
            
            if cBtn.button("Ekle", type="primary", use_container_width=True):
                st.session_state.sablon_w = w
                st.session_state.sablon_r = r
                
                # B3 ÇÖZÜMÜ: PR (Personal Record) Kontrolü
                if not df_antrenmanlar.empty:
                    gecmis = df_antrenmanlar[(df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == secili_hareket)]
                    if not gecmis.empty:
                        max_w = pd.to_numeric(gecmis['Ağırlık'], errors='coerce').max()
                        if float(w) > float(max_w) and float(w) > 0:
                            st.session_state.toast_balloons = True
                            st.session_state.toast_msg = f"🎉 YENİ REKOR! {secili_hareket}: {w} kg!"
                            st.session_state.toast_icon = "🔥"
                
                # Yeni set no hesapla
                bugun_bu_hareket = df_antrenmanlar[(pd.to_datetime(df_antrenmanlar['Tarih']).dt.strftime("%Y-%m-%d") == secili_tarih_str) & 
                                                   (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & 
                                                   (df_antrenmanlar['Hareket'] == secili_hareket)]
                yeni_set_no = len(bugun_bu_hareket) + 1
                
                yeni_satir = pd.DataFrame([{
                    "Tarih": secili_tarih_str, "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi,
                    "Kas Grubu": secili_kas, "Hareket": secili_hareket, "Set": yeni_set_no, "Ağırlık": w, "Tekrar": r,
                    "Süre (dk)": 0, "Kalori": 0, "Mekanik": mekanik, "Ekipman": ekipman
                }])
                
                if guvenli_veri_yaz("Antrenmanlar", yeni_satir, "ekle"):
                    if not st.session_state.toast_msg:
                        st.session_state.toast_msg = "Set Eklendi"
                        st.session_state.toast_icon = "✅"
                    st.rerun()

    st.divider()
    st.markdown(f"### 📋 {secili_tarih_str} Logu")
    
    if df_antrenmanlar.empty:
        st.info("Kayıt yok.")
    else:
        df_antrenmanlar['Formatted_Tarih'] = pd.to_datetime(df_antrenmanlar['Tarih']).dt.strftime("%Y-%m-%d")
        gunluk_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
                                        (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & 
                                        (df_antrenmanlar['Formatted_Tarih'] == secili_tarih_str)]
                                        
        if gunluk_gecmis.empty:
            st.info("Bu tarihte antrenman kaydı yok.")
        else:
            for hareket in gunluk_gecmis['Hareket'].unique():
                h_setleri = gunluk_gecmis[gunluk_gecmis['Hareket'] == hareket].sort_values(by="Set")
                ozet = " | ".join([f"{row['Ağırlık']}x{row['Tekrar']}" for _, row in h_setleri.iterrows()])
                
                with st.expander(f"💪 {hareket} 👉 {ozet}"):
                    c1, c2 = st.columns([4,1])
                    if c2.button("🗑️ Sil", key=f"del_{hareket}", use_container_width=True):
                        silme_onay_modal(hareket, h_setleri.index.tolist())
                    
                    # A4 ÇÖZÜMÜ: State-Value uyumsuzluğunu gidermek için index bazlı iteration ve doğrudan update
                    for idx, row in h_setleri.iterrows():
                        cC, cW, cR = st.columns([1,2,2])
                        cC.markdown(f"**Set {int(row['Set'])}**")
                        # State içinde key tanımlayıp value'yu state'e devrediyoruz
                        k_w, k_r = f"w_{idx}", f"r_{idx}"
                        if k_w not in st.session_state: st.session_state[k_w] = float(row['Ağırlık'])
                        if k_r not in st.session_state: st.session_state[k_r] = int(row['Tekrar'])
                        
                        yeni_w = cW.number_input("Ağırlık", min_value=0.0, step=2.5, key=k_w, label_visibility="collapsed")
                        yeni_r = cR.number_input("Tekrar", min_value=0, step=1, key=k_r, label_visibility="collapsed")
                        
                        if yeni_w != float(row['Ağırlık']) or yeni_r != int(row['Tekrar']):
                            df_antrenmanlar.at[idx, 'Ağırlık'] = st.session_state[k_w]
                            df_antrenmanlar.at[idx, 'Tekrar'] = st.session_state[k_r]
                            if guvenli_veri_yaz("Antrenmanlar", df_antrenmanlar, "guncelle"):
                                st.session_state.toast_msg = "Güncellendi!"
                                st.session_state.toast_icon = "💾"

# --- B5 ÇÖZÜMÜ: SAYFA 4: VÜCUT ÖLÇÜLERİ ---
elif st.session_state.sayfa == 'vucut_sayfasi':
    render_top_nav()
    st.markdown("<h2>⚖️ Vücut Takibi</h2>", unsafe_allow_html=True)
    
    df_vucut = veri_getir("VucutOlculeri")
    if 'Kullanıcı' not in df_vucut.columns: df_vucut = pd.DataFrame(columns=['Tarih', 'Kullanıcı', 'Kilo', 'Yağ Oranı'])
    
    with st.container(border=True):
        st.markdown("### ➕ Yeni Ölçüm Ekle")
        c1, c2 = st.columns(2)
        kilo = c1.number_input("Kilo (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
        yag = c2.number_input("Yağ Oranı (%)", min_value=1.0, max_value=50.0, value=15.0, step=0.1)
        tarih_sec = st.date_input("Tarih", date.today())
        
        if st.button("Kaydet", type="primary", use_container_width=True):
            yeni_satir = pd.DataFrame([{"Tarih": format_date(tarih_sec), "Kullanıcı": st.session_state.secili_kisi, "Kilo": kilo, "Yağ Oranı": yag}])
            if guvenli_veri_yaz("VucutOlculeri", yeni_satir, "ekle"):
                st.session_state.toast_msg = "Ölçüm eklendi!"
                st.session_state.toast_icon = "✅"
                st.rerun()
                
    st.divider()
    kisi_vucut = df_vucut[df_vucut['Kullanıcı'] == st.session_state.secili_kisi]
    if not kisi_vucut.empty:
        kisi_vucut['Tarih'] = pd.to_datetime(kisi_vucut['Tarih'])
        g_kilo = kisi_vucut.sort_values(by="Tarih").set_index('Tarih')['Kilo']
        st.markdown("### 📈 Kilo Grafiği")
        st.line_chart(g_kilo)
    else:
        st.info("Henüz vücut ölçüm kaydı yok.")

# --- SAYFA 5: İSTATİSTİKLER VE ARAMA (B12 ÇÖZÜMÜ) ---
elif st.session_state.sayfa == 'istatistik_sayfasi':
    render_top_nav()
    st.markdown("<h2>📊 İstatistikler</h2>", unsafe_allow_html=True)
    
    df_antrenmanlar = veri_getir("Antrenmanlar")
    if not df_antrenmanlar.empty:
        df_antrenmanlar['Formatted_Tarih'] = pd.to_datetime(df_antrenmanlar['Tarih']).dt.strftime("%Y-%m-%d")
        kisi_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
                                      (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi)].copy()
        
        # B12 ÇÖZÜMÜ: Arama Modülü
        with st.container(border=True):
            st.markdown("### 🔍 Geçmişte Ara")
            arama_kelimesi = st.text_input("Hareket veya Kas Grubu Ara", placeholder="Örn: Bench Press, Chest...")
            if arama_kelimesi:
                sonuclar = kisi_gecmis[kisi_gecmis['Hareket'].str.contains(arama_kelimesi, case=False, na=False) | 
                                       kisi_gecmis['Kas Grubu'].str.contains(arama_kelimesi, case=False, na=False)]
                if not sonuclar.empty:
                    st.dataframe(sonuclar[['Formatted_Tarih', 'Hareket', 'Set', 'Ağırlık', 'Tekrar']].sort_values(by="Formatted_Tarih", ascending=False), hide_index=True)
                else:
                    st.warning("Kayıt bulunamadı.")
        
        st.divider()
        
        # Grafik
        st.markdown("### 📈 Maksimum Ağırlık Grafiği")
        agirlik_h = kisi_gecmis['Hareket'].unique()
        if len(agirlik_h) > 0:
            sec_stat = st.selectbox("Hareketi Seç", agirlik_h)
            graf = kisi_gecmis[kisi_gecmis['Hareket'] == sec_stat].copy()
            graf['Tarih_DT'] = pd.to_datetime(graf['Tarih'])
            g = graf.groupby('Tarih_DT')['Ağırlık'].max().reset_index().sort_values(by='Tarih_DT')
            g.set_index('Tarih_DT', inplace=True)
            st.line_chart(g['Ağırlık'].astype(float))
    else:
        st.info("İstatistik gösterilecek veri yok.")
