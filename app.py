import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# --- DİL (LANGUAGE) SÖZLÜĞÜ ---
LANG = {
    "English": {
        "groups_title": "🏋️‍♂️ Workout Groups",
        "existing_groups": "Existing Groups",
        "no_group": "No groups registered yet.",
        "new_group": "Create New Group",
        "add_group": "Add Group",
        "success_group": "successfully created!",
        "back_to_groups": "⬅️ Back to Groups",
        "members": "Members",
        "no_member": "No members in this group yet.",
        "new_member": "Add new member to this group",
        "add_member": "Add Member",
        "success_member": "added to the group!",
        "back_to_members": "⬅️ Back to Members",
        "daily_log": "Daily Log",
        "add_new_set": "Add New Set",
        "date": "Workout Date",
        "muscle_group": "Muscle Group",
        "exercise": "Exercise",
        "mechanic": "Mechanic",
        "new_exercise_panel": "➕ Add a New Exercise to Database",
        "new_exercise_desc": "You can permanently add a new exercise to the database.",
        "which_muscle": "Which Muscle Group?",
        "new_exercise_name": "New Exercise Name",
        "mechanic_type": "Mechanic Type",
        "add_to_db": "Add to Database",
        "success_db": "successfully added to the database!",
        "warn_name": "Please enter an exercise name.",
        "delete_exercise_panel": "🗑️ Delete Selected Exercise",
        "delete_exercise_desc": "Warning: This will permanently remove the exercise from the list. Past workout logs will not be deleted.",
        "delete_from_db": "Delete Exercise from Database",
        "success_delete_db": "successfully deleted from the database!",
        "template_title": "📌 **Template Settings (Autofills sets below)**",
        "how_many_sets": "How Many Sets?",
        "template_w": "Template Weight (kg)",
        "template_r": "Template Reps",
        "edit_sets": "📝 **Edit Set Details (Optional)**",
        "set": "Set",
        "weight": "Weight",
        "reps": "Reps",
        "save_all": "Save All Sets",
        "success_sets": "sets successfully saved for",
        "workout_of": "Workout",
        "editing": "Editing",
        "save": "💾 Save",
        "cancel": "Cancel",
        "no_workout": "No workout records for this date yet.",
        "progress_chart": "Progress Chart",
        "no_chart_data": "Not enough data to display a chart for this exercise yet.",
        "duration": "Duration (min)",
        "calories": "Calories (kcal)",
        "cardio_details": "🏃‍♂️ **Cardio Details**",
        "save_cardio": "Save Cardio",
        "success_cardio": "cardio session successfully saved!"
    },
    "Türkçe": {
        "groups_title": "🏋️‍♂️ Antrenman Grupları",
        "existing_groups": "Mevcut Gruplar",
        "no_group": "Henüz kayıtlı bir grup yok.",
        "new_group": "Yeni Grup Oluştur",
        "add_group": "Grup Ekle",
        "success_group": "başarıyla oluşturuldu!",
        "back_to_groups": "⬅️ Gruplara Dön",
        "members": "Üyeler",
        "no_member": "Bu gruba henüz kimse eklenmemiş.",
        "new_member": "Bu gruba yeni kişi ekle",
        "add_member": "Kişi Ekle",
        "success_member": "gruba eklendi!",
        "back_to_members": "⬅️ Üyelere Dön",
        "daily_log": "Günlük",
        "add_new_set": "Yeni Set Ekle",
        "date": "Antrenman Tarihi",
        "muscle_group": "Kas Grubu",
        "exercise": "Hareket",
        "mechanic": "Mekanik",
        "new_exercise_panel": "➕ Listede Olmayan Yeni Bir Hareket Ekle",
        "new_exercise_desc": "Veritabanına kalıcı olarak yeni bir hareket ekleyebilirsiniz.",
        "which_muscle": "Hangi Kas Grubuna?",
        "new_exercise_name": "Yeni Hareketin Adı",
        "mechanic_type": "Mekanik Tipi",
        "add_to_db": "Veritabanına Ekle",
        "success_db": "başarıyla veritabanına eklendi!",
        "warn_name": "Lütfen hareket adını girin.",
        "delete_exercise_panel": "🗑️ Seçili Hareketi Veritabanından Sil",
        "delete_exercise_desc": "Uyarı: Bu işlem hareketi listeden tamamen kaldırır. Geçmiş antrenman kayıtlarınız silinmez.",
        "delete_from_db": "Seçili Hareketi Sil",
        "success_delete_db": "veritabanından başarıyla silindi!",
        "template_title": "📌 **Şablon Ayarları (Alttaki setlere otomatik dolar)**",
        "how_many_sets": "Kaç Set Yapılacak?",
        "template_w": "Şablon Ağırlık (kg)",
        "template_r": "Şablon Tekrar",
        "edit_sets": "📝 **Set Detaylarını Düzenle (İsteğe Bağlı)**",
        "set": "Set",
        "weight": "Ağırlık",
        "reps": "Tekrar",
        "save_all": "Tüm Setleri Kaydet",
        "success_sets": "set başarıyla kaydedildi!",
        "workout_of": "Antrenmanı",
        "editing": "Düzenleniyor",
        "save": "💾 Kaydet",
        "cancel": "İptal",
        "no_workout": "Bu tarihte henüz bir antrenman kaydı yok.",
        "progress_chart": "Gelişim Grafiği",
        "no_chart_data": "Bu hareket için grafiği oluşturacak yeterli veri henüz yok.",
        "duration": "Süre (dk)",
        "calories": "Kalori (kcal)",
        "cardio_details": "🏃‍♂️ **Kardiyo Detayları**",
        "save_cardio": "Kardiyoyu Kaydet",
        "success_cardio": "kardiyo kaydı başarıyla eklendi!"
    }
}

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Workout App", page_icon="💪", layout="centered")

secilen_dil = st.sidebar.selectbox("🌐 Language / Dil", ["English", "Türkçe"], index=0)
t = LANG[secilen_dil]

# --- OTURUM DEĞİŞKENLERİ ---
if 'sayfa' not in st.session_state: st.session_state.sayfa = 'ana_sayfa'
if 'secili_grup' not in st.session_state: st.session_state.secili_grup = None
if 'secili_kisi' not in st.session_state: st.session_state.secili_kisi = None
if 'duzenlenen_idx' not in st.session_state: st.session_state.duzenlenen_idx = None
if 'onceki_hareket' not in st.session_state: st.session_state.onceki_hareket = ""
if 'sablon_w' not in st.session_state: st.session_state.sablon_w = 0.0
if 'sablon_r' not in st.session_state: st.session_state.sablon_r = 10

# --- GOOGLE SHEETS BAĞLANTISI ---
conn = st.connection("gsheets", type=GSheetsConnection)

def veri_getir(sekme_adi, kolonlar):
    try:
        df = conn.read(worksheet=sekme_adi, ttl=5)
        if df.empty:
            return pd.DataFrame(columns=kolonlar)
        # NaN değerleri 0 ile dolduruyoruz (Eski kayıtlarda Süre/Kalori hatası vermemesi için)
        df.fillna(0, inplace=True)
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
    st.title(t["groups_title"])
    st.subheader(t["existing_groups"])
    if not df_gruplar.empty:
        for index, row in df_gruplar.iterrows():
            grup_adi = row['Grup Adı']
            if st.button(f"📁 {grup_adi}", use_container_width=True):
                st.session_state.secili_grup = grup_adi
                st.session_state.sayfa = 'grup_sayfasi'
                st.rerun()
    else:
        st.info(t["no_group"])
        
    st.divider()
    yeni_grup = st.text_input(t["new_group"])
    if st.button(t["add_group"], type="primary"):
        if yeni_grup:
            yeni_satir = pd.DataFrame([{"Grup Adı": yeni_grup}])
            guncel_gruplar = pd.concat([df_gruplar, yeni_satir], ignore_index=True)
            conn.update(worksheet="Gruplar", data=guncel_gruplar)
            st.cache_data.clear() 
            st.success(f"{yeni_grup} {t['success_group']}")
            st.rerun()

# --- SAYFA 2: GRUP İÇİ (KİŞİLER) ---
elif st.session_state.sayfa == 'grup_sayfasi':
    df_kullanicilar = veri_getir("Kullanicilar", ["Grup Adı", "Kullanıcı Adı"])
    st.title(f"📁 {st.session_state.secili_grup}")
    
    if st.button(t["back_to_groups"]):
        st.session_state.sayfa = 'ana_sayfa'
        st.rerun()
        
    st.subheader(t["members"])
    grup_uyeleri = df_kullanicilar[df_kullanicilar['Grup Adı'] == st.session_state.secili_grup]
    
    if not grup_uyeleri.empty:
        for index, row in grup_uyeleri.iterrows():
            kisi_adi = row['Kullanıcı Adı']
            if st.button(f"👤 {kisi_adi}", use_container_width=True):
                st.session_state.secili_kisi = kisi_adi
                st.session_state.sayfa = 'kisi_sayfasi'
                st.rerun()
    else:
        st.info(t["no_member"])
        
    st.divider()
    yeni_kisi = st.text_input(t["new_member"])
    if st.button(t["add_member"], type="primary"):
        if yeni_kisi:
            yeni_satir = pd.DataFrame([{"Grup Adı": st.session_state.secili_grup, "Kullanıcı Adı": yeni_kisi}])
            guncel_kullanicilar = pd.concat([df_kullanicilar, yeni_satir], ignore_index=True)
            conn.update(worksheet="Kullanicilar", data=guncel_kullanicilar)
            st.cache_data.clear()
            st.success(f"{yeni_kisi} {t['success_member']}")
            st.rerun()

# --- SAYFA 3: KİŞİ DETAYI VE HAREKET EKLEME ---
elif st.session_state.sayfa == 'kisi_sayfasi':
    df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Süre (dk)", "Kalori", "Mekanik"])
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik"])
    
    st.title(f"👤 {st.session_state.secili_kisi} - {t['daily_log']}")
    
    if st.button(t["back_to_members"]):
        st.session_state.sayfa = 'grup_sayfasi'
        st.rerun()
        
    st.subheader(t["add_new_set"])
    secili_tarih = st.date_input(t["date"], value=date.today(), format="DD/MM/YYYY")
    
    col1, col2 = st.columns(2)
    with col1:
        mevcut_kas_gruplari = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Shoulder", "Biceps", "Triceps", "Legs", "Glutes", "Calves", "Abs", "Forearm", "Neck", "Cardio"]
        secili_kas = st.selectbox(t["muscle_group"], mevcut_kas_gruplari)
    with col2:
        filtrelenmis_df = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]
        hareket_listesi = filtrelenmis_df['Hareket Tipi'].unique() if not filtrelenmis_df.empty else []
        secili_hareket = st.selectbox(t["exercise"], hareket_listesi)

    if secili_hareket:
        mekanik_degeri = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
        st.info(f"{t['mechanic']}: **{mekanik_degeri}**")

        if st.session_state.onceki_hareket != secili_hareket:
            st.session_state.onceki_hareket = secili_hareket
            gecmis_hareket = df_antrenmanlar[
                (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & 
                (df_antrenmanlar['Hareket'] == secili_hareket) &
                (df_antrenmanlar['Mekanik'] != 'Kardiyo') # Sadece ağırlık idmanlarının geçmişini şablona al
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

    with st.expander(t["new_exercise_panel"]):
        st.write(t["new_exercise_desc"])
        c_kas_yeni, c_har_yeni, c_mek_yeni = st.columns(3)
        yeni_kas_grubu = c_kas_yeni.selectbox(t["which_muscle"], mevcut_kas_gruplari)
        yeni_hareket_adi = c_har_yeni.text_input(t["new_exercise_name"])
        yeni_mekanik = c_mek_yeni.selectbox(t["mechanic_type"], ["Compound", "Izole", "Kardiyo"])
        
        if st.button(t["add_to_db"], type="secondary"):
            if yeni_hareket_adi:
                yeni_hareket_satiri = pd.DataFrame([{"Kas Grubu": yeni_kas_grubu, "Hareket Tipi": yeni_hareket_adi, "Mekanik": yeni_mekanik}])
                guncel_hareketler = pd.concat([df_hareketler, yeni_hareket_satiri], ignore_index=True)
                conn.update(worksheet="Hareketler", data=guncel_hareketler)
                st.cache_data.clear()
                st.success(f"**{yeni_hareket_adi}** {t['success_db']}")
                st.rerun()
            else:
                st.warning(t["warn_name"])
                
    if secili_hareket:
        with st.expander(t["delete_exercise_panel"]):
            st.warning(t["delete_exercise_desc"])
            st.write(f"**{secili_hareket}**")
            if st.button(t["delete_from_db"], type="primary"):
                guncel_hareketler = df_hareketler[df_hareketler['Hareket Tipi'] != secili_hareket]
                conn.update(worksheet="Hareketler", data=guncel_hareketler)
                st.cache_data.clear()
                if st.session_state.onceki_hareket == secili_hareket:
                    st.session_state.onceki_hareket = ""
                st.success(f"**{secili_hareket}** {t['success_delete_db']}")
                st.rerun()

    st.divider()
    
    # --- KARDİYO VE AĞIRLIK İÇİN AKILLI FORM YAPISI ---
    if secili_hareket:
        
        # EĞER SEÇİLEN HAREKET KARDİYO İSE
        if mekanik_degeri == "Kardiyo":
            st.write(t["cardio_details"])
            
            c_sure, c_kalori = st.columns(2)
            kardiyo_sure = c_sure.number_input(t["duration"], min_value=1, value=30, step=1)
            kardiyo_kalori = c_kalori.number_input(t["calories"], min_value=1, value=300, step=10)
            
            if st.button(t["save_cardio"], type="primary", use_container_width=True):
                yeni_satir = pd.DataFrame([{
                    "Tarih": secili_tarih.strftime("%Y-%m-%d"),
                    "Grup": st.session_state.secili_grup,
                    "Kullanıcı": st.session_state.secili_kisi,
                    "Kas Grubu": secili_kas,
                    "Hareket": secili_hareket,
                    "Set": 1, # Kardiyo genelde tek set kaydedilir
                    "Ağırlık": 0,
                    "Tekrar": 0,
                    "Süre (dk)": kardiyo_sure,
                    "Kalori": kardiyo_kalori,
                    "Mekanik": mekanik_degeri
                }])
                guncel_antrenmanlar = pd.concat([df_antrenmanlar, yeni_satir], ignore_index=True)
                conn.update(worksheet="Antrenmanlar", data=guncel_antrenmanlar)
                st.cache_data.clear()
                st.success(f"{secili_hareket} {t['success_cardio']}")
                st.rerun()

        # EĞER SEÇİLEN HAREKET AĞIRLIK (COMPOUND/İZOLE) İSE
        else:
            st.write(t["template_title"])
            set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1)
            
            c_hedef1, c_hedef2 = st.columns(2)
            c_hedef1.number_input(t["template_w"], step=2.5, key="sablon_w", on_change=sablon_guncelle)
            c_hedef2.number_input(t["template_r"], step=1, key="sablon_r", on_change=sablon_guncelle)
            
            st.write("---")
            st.write(t["edit_sets"])
            
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
                c_label.markdown(f"<div style='margin-top: 25px;'>**{t['set']} {guncel_set_no}**</div>", unsafe_allow_html=True)
                
                w_key = f"w_new_{secili_hareket}_{guncel_set_no}"
                r_key = f"r_new_{secili_hareket}_{guncel_set_no}"
                
                if w_key not in st.session_state: st.session_state[w_key] = st.session_state.sablon_w
                if r_key not in st.session_state: st.session_state[r_key] = st.session_state.sablon_r
                
                w = c_w.number_input(t["weight"], step=2.5, key=w_key)
                r = c_r.number_input(t["reps"], step=1, key=r_key)
                
                eklenecek_setler.append({
                    "Tarih": secili_tarih.strftime("%Y-%m-%d"),
                    "Grup": st.session_state.secili_grup,
                    "Kullanıcı": st.session_state.secili_kisi,
                    "Kas Grubu": secili_kas,
                    "Hareket": secili_hareket,
                    "Set": guncel_set_no,
                    "Ağırlık": w,
                    "Tekrar": r,
                    "Süre (dk)": 0,
                    "Kalori": 0,
                    "Mekanik": mekanik_degeri
                })
                
            if st.button(t["save_all"], type="primary", use_container_width=True):
                yeni_satirlar = pd.DataFrame(eklenecek_setler)
                guncel_antrenmanlar = pd.concat([df_antrenmanlar, yeni_satirlar], ignore_index=True)
                conn.update(worksheet="Antrenmanlar", data=guncel_antrenmanlar)
                st.cache_data.clear()
                
                for key in list(st.session_state.keys()):
                    if key.startswith("w_new_") or key.startswith("r_new_"):
                        del st.session_state[key]
                        
                st.success(f"{secili_hareket}: {set_sayisi} {t['success_sets']}")
                st.rerun()

    st.divider()
    
    # --- GÜNLÜK ANTRENMAN LİSTESİ ---
    if secilen_dil == "English":
        st.subheader(f"📋 {secili_tarih.strftime('%d/%m/%Y')} {t['workout_of']}")
    else:
        st.subheader(f"📋 {secili_tarih.strftime('%d/%m/%Y')} Tarihli {t['workout_of']}")
    
    gunluk_gecmis = df_antrenmanlar[
        (df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
        (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
        (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d"))
    ]
    
    if not gunluk_gecmis.empty:
        yapilan_hareketler = gunluk_gecmis['Hareket'].unique()
        
        for hareket in yapilan_hareketler:
            hareket_setleri = gunluk_gecmis[gunluk_gecmis['Hareket'] == hareket].sort_values(by="Set")
            toplam_set = len(hareket_setleri)
            
            # Başlıktaki özet metni Kardiyo ve Ağırlık için ayrı ayarlıyoruz
            mekanik_kontrol = hareket_setleri.iloc[0]['Mekanik']
            
            if mekanik_kontrol == "Kardiyo":
                ozet_listesi = [f"{row['Süre (dk)']} dk, {row['Kalori']} kcal" for _, row in hareket_setleri.iterrows()]
                ozet_metni = " | ".join(ozet_listesi)
                expander_baslik = f"🏃‍♂️ **{hareket}** 👉 {ozet_metni}"
            else:
                ozet_listesi = [f"{row['Ağırlık']}x{row['Tekrar']}" for _, row in hareket_setleri.iterrows()]
                ozet_metni = " | ".join(ozet_listesi)
                expander_baslik = f"💪 **{hareket}** ({toplam_set} {t['set']}) 👉 {ozet_metni}"
            
            with st.expander(expander_baslik):
                
                for idx, row in hareket_setleri.iterrows():
                    
                    if st.session_state.duzenlenen_idx == idx:
                        st.write(f"**{t['editing']}**")
                        d1, d2, d3, d4 = st.columns(4)
                        
                        if row['Mekanik'] == 'Kardiyo':
                            yeni_sure = d1.number_input(t["duration"], value=int(row['Süre (dk)']), step=1, key=f"edit_s_{idx}")
                            yeni_kalori = d2.number_input(t["calories"], value=int(row['Kalori']), step=10, key=f"edit_k_{idx}")
                        else:
                            yeni_agirlik = d1.number_input(t["weight"], value=float(row['Ağırlık']), step=2.5, key=f"edit_w_{idx}")
                            yeni_tekrar = d2.number_input(t["reps"], value=int(row['Tekrar']), step=1, key=f"edit_r_{idx}")
                        
                        if d3.button(t["save"], key=f"save_{idx}"):
                            if row['Mekanik'] == 'Kardiyo':
                                df_antrenmanlar.at[idx, 'Süre (dk)'] = yeni_sure
                                df_antrenmanlar.at[idx, 'Kalori'] = yeni_kalori
                            else:
                                df_antrenmanlar.at[idx, 'Ağırlık'] = yeni_agirlik
                                df_antrenmanlar.at[idx, 'Tekrar'] = yeni_tekrar
                                
                            conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar)
                            st.session_state.duzenlenen_idx = None
                            st.cache_data.clear()
                            st.rerun()
                            
                        if d4.button(t["cancel"], key=f"cancel_{idx}"):
                            st.session_state.duzenlenen_idx = None
                            st.rerun()
                    else:
                        col_metin, col_edit, col_sil = st.columns([5, 1, 1])
                        with col_metin:
                            if row['Mekanik'] == 'Kardiyo':
                                st.write(f"⏱️ **{row['Süre (dk)']} dk** | 🔥 {row['Kalori']} kcal")
                            else:
                                st.write(f"{t['set']} {row['Set']}: **{row['Ağırlık']}kg** x {row['Tekrar']}")
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
        st.info(t["no_workout"])

    # --- GELİŞİM GRAFİĞİ (SADECE AĞIRLIK İDMANLARI İÇİN) ---
    st.divider()
    
    if secili_hareket and mekanik_degeri != "Kardiyo":
        st.subheader(f"📈 {secili_hareket} - {t['progress_chart']}")
        
        gecmis_tum_setler = df_antrenmanlar[
            (df_antrenmanlar['Grup'] == st.session_state.secili_grup) & 
            (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
            (df_antrenmanlar['Hareket'] == secili_hareket)
        ].copy()
        
        if not gecmis_tum_setler.empty and len(gecmis_tum_setler) > 0:
            gecmis_tum_setler['Tarih'] = pd.to_datetime(gecmis_tum_setler['Tarih'])
            grafik_verisi = gecmis_tum_setler.groupby('Tarih')['Ağırlık'].max().reset_index()
            grafik_verisi = grafik_verisi.sort_values(by='Tarih')
            grafik_verisi.set_index('Tarih', inplace=True)
            grafik_verisi['Ağırlık'] = grafik_verisi['Ağırlık'].astype(float)
            st.line_chart(grafik_verisi['Ağırlık'])
        else:
            st.info(t["no_chart_data"])
