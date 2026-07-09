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
        "success_cardio": "cardio session successfully saved!",
        "delete_exercise_day": "🗑️ Delete Entire Exercise",
        "confirm_delete_exercise_day": "Are you sure you want to delete ALL sets of **{ex}** for this date? This cannot be undone.",
        "yes_delete": "✅ Yes, Delete",
        "success_delete_exercise_day": "and all its sets for this date were deleted.",
        "export_csv": "⬇️ Export This Day as CSV",
        "go_to_programs": "📋 Workout Programs",
        "programs_title": "Workout Programs",
        "back_to_person": "⬅️ Back",
        "existing_programs": "Existing Programs",
        "no_program": "No programs created yet.",
        "new_program_name": "New Program Name",
        "create_program": "➕ Create Program",
        "success_program": "successfully created!",
        "program_exists": "A program with this name already exists.",
        "back_to_programs": "⬅️ Back to Programs",
        "program_content": "📝 Program Content",
        "no_program_content": "No exercises added to this program yet.",
        "add_exercise_to_program": "➕ Add Exercise to Program",
        "target_sets": "Target Sets",
        "target_weight": "Target Weight (kg)",
        "target_reps": "Target Reps",
        "add_to_program": "Add to Program",
        "success_add_to_program": "added to the program!",
        "delete_program_panel": "🗑️ Delete This Program",
        "delete_program_desc": "Warning: This will permanently delete the program and all its exercises.",
        "delete_program_btn": "Delete Program",
        "success_delete_program": "Program successfully deleted.",
        "load_program_panel": "📥 Load a Program for Today",
        "select_program": "Select Program",
        "program_preview": "Preview & Adjust (optional)",
        "load_program_btn": "📥 Load All Exercises for Today",
        "success_load_program": "loaded into today's log!",
        "cardio_not_supported_in_program": "Cardio exercises aren't supported in programs — only weight-based exercises can be added.",
        "delete_exercise_from_program": "🗑️ Delete This Exercise from Program",
        "confirm_delete_exercise_from_program": "Are you sure you want to delete ALL sets of **{ex}** from this program? This cannot be undone.",
        "success_delete_exercise_from_program": "removed from the program."
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
        "success_cardio": "kardiyo kaydı başarıyla eklendi!",
        "delete_exercise_day": "🗑️ Hareketi Tamamen Sil",
        "confirm_delete_exercise_day": "Bu tarihteki **{ex}** hareketinin TÜM setlerini silmek istediğinize emin misiniz? Bu işlem geri alınamaz.",
        "yes_delete": "✅ Evet, Sil",
        "success_delete_exercise_day": "hareketinin bu tarihteki tüm setleri silindi.",
        "export_csv": "⬇️ Bu Günü CSV Olarak Dışa Aktar",
        "go_to_programs": "📋 Antrenman Programları",
        "programs_title": "Antrenman Programları",
        "back_to_person": "⬅️ Geri Dön",
        "existing_programs": "Mevcut Programlar",
        "no_program": "Henüz oluşturulmuş bir program yok.",
        "new_program_name": "Yeni Program Adı",
        "create_program": "➕ Program Oluştur",
        "success_program": "başarıyla oluşturuldu!",
        "program_exists": "Bu isimde bir program zaten var.",
        "back_to_programs": "⬅️ Programlara Dön",
        "program_content": "📝 Program İçeriği",
        "no_program_content": "Bu programa henüz hareket eklenmemiş.",
        "add_exercise_to_program": "➕ Programa Hareket Ekle",
        "target_sets": "Hedef Set Sayısı",
        "target_weight": "Hedef Ağırlık (kg)",
        "target_reps": "Hedef Tekrar",
        "add_to_program": "Programa Ekle",
        "success_add_to_program": "programa eklendi!",
        "delete_program_panel": "🗑️ Bu Programı Sil",
        "delete_program_desc": "Uyarı: Bu işlem programı ve içindeki tüm hareketleri kalıcı olarak siler.",
        "delete_program_btn": "Programı Sil",
        "success_delete_program": "Program başarıyla silindi.",
        "load_program_panel": "📥 Bugün İçin Bir Program Yükle",
        "select_program": "Program Seç",
        "program_preview": "Önizle ve Ayarla (isteğe bağlı)",
        "load_program_btn": "📥 Tüm Hareketleri Bugüne Yükle",
        "success_load_program": "bugünün kaydına yüklendi!",
        "cardio_not_supported_in_program": "Kardiyo hareketler programlarda desteklenmiyor — sadece ağırlık hareketleri eklenebilir.",
        "delete_exercise_from_program": "🗑️ Bu Hareketi Programdan Sil",
        "confirm_delete_exercise_from_program": "Bu programdaki **{ex}** hareketinin TÜM setlerini silmek istediğinize emin misiniz? Bu işlem geri alınamaz.",
        "success_delete_exercise_from_program": "programdan kaldırıldı."
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
if 'grafik_gorunur' not in st.session_state: st.session_state.grafik_gorunur = None  # YENİ: hangi hareketin grafiği açık
if 'silme_onay_hareket' not in st.session_state: st.session_state.silme_onay_hareket = None  # YENİ: onay bekleyen toplu silme
if 'secili_program' not in st.session_state: st.session_state.secili_program = None  # YENİ: seçili antrenman programı
if 'program_duzenlenen_idx' not in st.session_state: st.session_state.program_duzenlenen_idx = None  # YENİ: düzenlenen program satırı
if 'program_silme_onay_hareket' not in st.session_state: st.session_state.program_silme_onay_hareket = None  # YENİ: programdan hareket silme onayı
if 'p_onceki_hareket' not in st.session_state: st.session_state.p_onceki_hareket = ""  # YENİ: programa hareket eklerken şablon takibi
if 'p_sablon_w' not in st.session_state: st.session_state.p_sablon_w = 0.0
if 'p_sablon_r' not in st.session_state: st.session_state.p_sablon_r = 10

# --- GOOGLE SHEETS BAĞLANTISI ---
conn = st.connection("gsheets", type=GSheetsConnection)

def veri_getir(sekme_adi, kolonlar):
    try:
        # ttl artırıldı: 5sn yerine 60sn önbellek. Kayıt/silme/güncelleme
        # sonrasında zaten st.cache_data.clear() ile manuel temizleniyor,
        # bu yüzden veri bayatlama riski yok; ama her tıklamada Sheets'e
        # gidilmesi engellenmiş olur (asıl gecikme kaynağı buydu).
        df = conn.read(worksheet=sekme_adi, ttl=60)
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
    df_programlar = veri_getir("Programlar", ["Kullanıcı", "Program Adı"])
    df_program_detay = veri_getir("ProgramDetay", ["Program Adı", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar"])
    
    st.title(f"👤 {st.session_state.secili_kisi} - {t['daily_log']}")
    
    if st.button(t["back_to_members"]):
        st.session_state.sayfa = 'grup_sayfasi'
        st.rerun()

    if st.button(t["go_to_programs"], use_container_width=True):
        st.session_state.sayfa = 'program_sayfasi'
        st.rerun()

    # --- YENİ: Herhangi bir hareketin geçmiş ağırlık grafiğini çizen yardımcı fonksiyon ---
    def grafik_ciz(hareket_adi):
        gecmis_tum_setler = df_antrenmanlar[
            (df_antrenmanlar['Grup'] == st.session_state.secili_grup) &
            (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
            (df_antrenmanlar['Hareket'] == hareket_adi)
        ].copy()

        if not gecmis_tum_setler.empty:
            gecmis_tum_setler['Tarih'] = pd.to_datetime(gecmis_tum_setler['Tarih'])
            grafik_verisi = gecmis_tum_setler.groupby('Tarih')['Ağırlık'].max().reset_index()
            grafik_verisi = grafik_verisi.sort_values(by='Tarih')
            # Tarihi saat bilgisi olmayan bir metne çeviriyoruz (örn. "09/07/2026"),
            # aksi halde grafik ekseni tarihi "zaman" tipi sanıp saat bazlı etiketler gösteriyordu.
            grafik_verisi['Tarih'] = grafik_verisi['Tarih'].dt.strftime('%d/%m/%Y')
            grafik_verisi.set_index('Tarih', inplace=True)
            grafik_verisi['Ağırlık'] = grafik_verisi['Ağırlık'].astype(float)
            st.line_chart(grafik_verisi['Ağırlık'])
        else:
            st.info(t["no_chart_data"])

    st.subheader(t["add_new_set"])
    secili_tarih = st.date_input(t["date"], value=date.today(), format="DD/MM/YYYY")

    # --- YENİ: Kayıtlı bir programı seçili tarihe tek tıkla yükleme ---
    with st.expander(t["load_program_panel"]):
        kisi_programlari_yukle = df_programlar[df_programlar['Kullanıcı'] == st.session_state.secili_kisi]
        if kisi_programlari_yukle.empty:
            st.info(t["no_program"])
        else:
            secili_program_yukle = st.selectbox(
                t["select_program"], kisi_programlari_yukle['Program Adı'].unique(), key="program_yukle_secim"
            )
            program_icerik_yukle = df_program_detay[
                (df_program_detay['Program Adı'] == secili_program_yukle) &
                (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi)
            ].sort_values(by=["Hareket", "Set"])

            if program_icerik_yukle.empty:
                st.info(t["no_program_content"])
            else:
                st.write(f"**{t['program_preview']}**")
                yuklenecek_setler_l = []
                yukleme_hareketleri = program_icerik_yukle['Hareket'].unique()

                for hareket_l in yukleme_hareketleri:
                    st.markdown(f"💪 **{hareket_l}**")
                    hareket_setleri_l = program_icerik_yukle[program_icerik_yukle['Hareket'] == hareket_l]
                    kas_grubu_l = hareket_setleri_l.iloc[0]['Kas Grubu']

                    for p_idx, p_row in hareket_setleri_l.iterrows():
                        cLabel, cW, cR = st.columns([1, 2, 2])
                        cLabel.markdown(f"<div style='margin-top: 8px;'>{t['set']} {int(p_row['Set'])}</div>", unsafe_allow_html=True)

                        w_key_l = f"load_w_{secili_program_yukle}_{p_idx}"
                        r_key_l = f"load_r_{secili_program_yukle}_{p_idx}"
                        if w_key_l not in st.session_state: st.session_state[w_key_l] = float(p_row['Ağırlık'])
                        if r_key_l not in st.session_state: st.session_state[r_key_l] = int(p_row['Tekrar'])

                        agirlik_l = cW.number_input(t["weight"], min_value=0.0, step=2.5, key=w_key_l)
                        tekrar_l = cR.number_input(t["reps"], min_value=0, step=1, key=r_key_l)

                        yuklenecek_setler_l.append({
                            "Kas Grubu": kas_grubu_l,
                            "Hareket": hareket_l,
                            "Ağırlık": agirlik_l,
                            "Tekrar": tekrar_l
                        })
                    st.write("")

                if st.button(t["load_program_btn"], type="primary", use_container_width=True):
                    hareket_mekanik_sozlugu = df_hareketler.set_index('Hareket Tipi')['Mekanik'].to_dict() if not df_hareketler.empty else {}
                    tum_yeni_setler = []
                    hareket_sayaclari = {}

                    for satir in yuklenecek_setler_l:
                        hareket_adi_l = satir["Hareket"]
                        if hareket_adi_l not in hareket_sayaclari:
                            mevcut_setler_l = df_antrenmanlar[
                                (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) &
                                (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
                                (df_antrenmanlar['Hareket'] == hareket_adi_l)
                            ]
                            hareket_sayaclari[hareket_adi_l] = len(mevcut_setler_l) + 1

                        mekanik_l = hareket_mekanik_sozlugu.get(hareket_adi_l, "Compound")
                        tum_yeni_setler.append({
                            "Tarih": secili_tarih.strftime("%Y-%m-%d"),
                            "Grup": st.session_state.secili_grup,
                            "Kullanıcı": st.session_state.secili_kisi,
                            "Kas Grubu": satir["Kas Grubu"],
                            "Hareket": hareket_adi_l,
                            "Set": hareket_sayaclari[hareket_adi_l],
                            "Ağırlık": satir["Ağırlık"],
                            "Tekrar": satir["Tekrar"],
                            "Süre (dk)": 0,
                            "Kalori": 0,
                            "Mekanik": mekanik_l
                        })
                        hareket_sayaclari[hareket_adi_l] += 1

                    yeni_df_l = pd.DataFrame(tum_yeni_setler)
                    guncel_antrenmanlar_l = pd.concat([df_antrenmanlar, yeni_df_l], ignore_index=True)
                    conn.update(worksheet="Antrenmanlar", data=guncel_antrenmanlar_l)
                    st.cache_data.clear()

                    for key in list(st.session_state.keys()):
                        if key.startswith("load_w_") or key.startswith("load_r_"):
                            del st.session_state[key]

                    st.success(f"{secili_program_yukle} {t['success_load_program']}")
                    st.rerun()
    
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
            
            # Kalori hesaplama tetikleyicisi
            def kalori_hesapla():
                # Dakikada ortalama 10 kalori yakıldığını varsayan basit bir algoritma
                st.session_state.kardiyo_kalori = int(st.session_state.kardiyo_sure * 10)

            # Session state'e değişkenleri atıyoruz
            if 'kardiyo_sure' not in st.session_state: st.session_state.kardiyo_sure = 30
            if 'kardiyo_kalori' not in st.session_state: st.session_state.kardiyo_kalori = 300

            c_sure, c_kalori = st.columns(2)
            # Süre değiştiğinde 'kalori_hesapla' fonksiyonu tetiklenir
            kardiyo_sure = c_sure.number_input(t["duration"], min_value=1, value=st.session_state.kardiyo_sure, 
                                               key="kardiyo_sure", step=1, on_change=kalori_hesapla)
            
            # Kalori kutusu kendi değerini session_state'den alır
            kardiyo_kalori = c_kalori.number_input(t["calories"], min_value=1, value=st.session_state.kardiyo_kalori, 
                                                 key="kardiyo_kalori", step=10)
            
            if st.button(t["save_cardio"], type="primary", use_container_width=True):
                yeni_satir = pd.DataFrame([{
                    "Tarih": secili_tarih.strftime("%Y-%m-%d"),
                    "Grup": st.session_state.secili_grup,
                    "Kullanıcı": st.session_state.secili_kisi,
                    "Kas Grubu": secili_kas,
                    "Hareket": secili_hareket,
                    "Set": 1,
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

    # --- YENİ: Seçili günün antrenmanını CSV olarak dışa aktarma ---
    if not gunluk_gecmis.empty:
        csv_verisi = gunluk_gecmis.to_csv(index=False).encode('utf-8-sig')  # utf-8-sig: Excel'de Türkçe karakterler bozulmasın
        st.download_button(
            label=t["export_csv"],
            data=csv_verisi,
            file_name=f"antrenman_{st.session_state.secili_kisi}_{secili_tarih.strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
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

                # --- YENİ: Grafik göster/gizle ve hareketi komple silme butonları ---
                hareket_silme_anahtari = f"{hareket}_{secili_tarih}"

                if mekanik_kontrol != "Kardiyo":
                    c_grafik, c_sil_hareket = st.columns(2)
                else:
                    c_sil_hareket = st.container()

                if mekanik_kontrol != "Kardiyo":
                    with c_grafik:
                        if st.button(f"📈 {t['progress_chart']}", key=f"grafik_btn_{hareket}_{secili_tarih}", use_container_width=True):
                            if st.session_state.grafik_gorunur == hareket:
                                st.session_state.grafik_gorunur = None
                            else:
                                st.session_state.grafik_gorunur = hareket
                            # Not: st.rerun() burada kasıtlı olarak kaldırıldı.
                            # st.button zaten tıklamada otomatik rerun tetikliyor;
                            # ek çağrı sayfayı iki kere baştan çalıştırıp gecikme yaratıyordu.

                with c_sil_hareket:
                    if st.button(t["delete_exercise_day"], key=f"sil_hareket_btn_{hareket_silme_anahtari}", use_container_width=True):
                        if st.session_state.silme_onay_hareket == hareket_silme_anahtari:
                            st.session_state.silme_onay_hareket = None
                        else:
                            st.session_state.silme_onay_hareket = hareket_silme_anahtari

                # Onay kutusu: kullanıcı gerçekten silmek istediğini teyit etmeden hiçbir şey silinmez
                if st.session_state.silme_onay_hareket == hareket_silme_anahtari:
                    st.warning(t["confirm_delete_exercise_day"].format(ex=hareket))
                    c_onay, c_vazgec = st.columns(2)
                    if c_onay.button(t["yes_delete"], key=f"onay_sil_{hareket_silme_anahtari}", type="primary", use_container_width=True):
                        df_antrenmanlar = df_antrenmanlar.drop(hareket_setleri.index)
                        conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar)
                        st.cache_data.clear()
                        st.session_state.silme_onay_hareket = None
                        if st.session_state.grafik_gorunur == hareket:
                            st.session_state.grafik_gorunur = None
                        st.success(f"**{hareket}** {t['success_delete_exercise_day']}")
                        st.rerun()
                    if c_vazgec.button(t["cancel"], key=f"vazgec_sil_{hareket_silme_anahtari}", use_container_width=True):
                        st.session_state.silme_onay_hareket = None

                if mekanik_kontrol != "Kardiyo" and st.session_state.grafik_gorunur == hareket:
                    grafik_ciz(hareket)
                    st.divider()

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

# --- SAYFA 4: ANTRENMAN PROGRAMLARI ---
elif st.session_state.sayfa == 'program_sayfasi':
    df_programlar = veri_getir("Programlar", ["Kullanıcı", "Program Adı"])
    df_program_detay = veri_getir("ProgramDetay", ["Program Adı", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar"])
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik"])

    st.title(f"📋 {st.session_state.secili_kisi} - {t['programs_title']}")

    if st.button(t["back_to_person"]):
        st.session_state.sayfa = 'kisi_sayfasi'
        st.session_state.secili_program = None
        st.rerun()

    kisi_programlari = df_programlar[df_programlar['Kullanıcı'] == st.session_state.secili_kisi]

    # --- PROGRAM LİSTESİ GÖRÜNÜMÜ ---
    if st.session_state.secili_program is None:
        st.subheader(t["existing_programs"])
        if not kisi_programlari.empty:
            for idx, row in kisi_programlari.iterrows():
                if st.button(f"📁 {row['Program Adı']}", key=f"prog_sec_{idx}", use_container_width=True):
                    st.session_state.secili_program = row['Program Adı']
                    st.rerun()
        else:
            st.info(t["no_program"])

        st.divider()
        yeni_program_adi = st.text_input(t["new_program_name"])
        if st.button(t["create_program"], type="primary"):
            if yeni_program_adi:
                if not kisi_programlari.empty and yeni_program_adi in kisi_programlari['Program Adı'].values:
                    st.warning(t["program_exists"])
                else:
                    yeni_satir = pd.DataFrame([{"Kullanıcı": st.session_state.secili_kisi, "Program Adı": yeni_program_adi}])
                    guncel_programlar = pd.concat([df_programlar, yeni_satir], ignore_index=True)
                    conn.update(worksheet="Programlar", data=guncel_programlar)
                    st.cache_data.clear()
                    st.session_state.secili_program = yeni_program_adi
                    st.success(f"{yeni_program_adi} {t['success_program']}")
                    st.rerun()

    # --- PROGRAM DÜZENLEME GÖRÜNÜMÜ ---
    else:
        st.subheader(f"📁 {st.session_state.secili_program}")
        if st.button(t["back_to_programs"]):
            st.session_state.secili_program = None
            st.session_state.program_duzenlenen_idx = None
            st.session_state.program_silme_onay_hareket = None
            st.rerun()

        program_icerik = df_program_detay[
            (df_program_detay['Program Adı'] == st.session_state.secili_program) &
            (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi)
        ]

        st.write(f"**{t['program_content']}**")
        if not program_icerik.empty:
            program_hareketleri = program_icerik['Hareket'].unique()

            for hareket_p in program_hareketleri:
                hareket_setleri_p = program_icerik[program_icerik['Hareket'] == hareket_p].sort_values(by="Set")
                toplam_set_p = len(hareket_setleri_p)
                ozet_listesi_p = [f"{row['Ağırlık']}x{row['Tekrar']}" for _, row in hareket_setleri_p.iterrows()]
                ozet_metni_p = " | ".join(ozet_listesi_p)
                expander_baslik_p = f"💪 **{hareket_p}** ({toplam_set_p} {t['set']}) 👉 {ozet_metni_p}"

                with st.expander(expander_baslik_p):
                    # --- Hareketi programdan komple silme (onaylı) ---
                    hareket_silme_anahtari_p = f"{st.session_state.secili_program}_{hareket_p}"
                    if st.button(t["delete_exercise_from_program"], key=f"p_sil_hareket_btn_{hareket_silme_anahtari_p}", use_container_width=True):
                        if st.session_state.program_silme_onay_hareket == hareket_silme_anahtari_p:
                            st.session_state.program_silme_onay_hareket = None
                        else:
                            st.session_state.program_silme_onay_hareket = hareket_silme_anahtari_p

                    if st.session_state.program_silme_onay_hareket == hareket_silme_anahtari_p:
                        st.warning(t["confirm_delete_exercise_from_program"].format(ex=hareket_p))
                        c_onay_p, c_vazgec_p = st.columns(2)
                        if c_onay_p.button(t["yes_delete"], key=f"p_onay_sil_{hareket_silme_anahtari_p}", type="primary", use_container_width=True):
                            df_program_detay = df_program_detay.drop(hareket_setleri_p.index)
                            conn.update(worksheet="ProgramDetay", data=df_program_detay)
                            st.cache_data.clear()
                            st.session_state.program_silme_onay_hareket = None
                            st.success(f"**{hareket_p}** {t['success_delete_exercise_from_program']}")
                            st.rerun()
                        if c_vazgec_p.button(t["cancel"], key=f"p_vazgec_sil_{hareket_silme_anahtari_p}", use_container_width=True):
                            st.session_state.program_silme_onay_hareket = None

                    st.divider()

                    # --- Her seti ayrı ayrı göster / düzenle / sil (günlük listedeki gibi) ---
                    for idx, row in hareket_setleri_p.iterrows():
                        if st.session_state.program_duzenlenen_idx == idx:
                            d1, d2, d3, d4 = st.columns(4)
                            yeni_agirlik = d1.number_input(t["weight"], min_value=0.0, value=float(row['Ağırlık']), step=2.5, key=f"pe_w_{idx}")
                            yeni_tekrar = d2.number_input(t["reps"], min_value=0, value=int(row['Tekrar']), step=1, key=f"pe_r_{idx}")
                            if d3.button(t["save"], key=f"pe_save_{idx}"):
                                df_program_detay.at[idx, 'Ağırlık'] = yeni_agirlik
                                df_program_detay.at[idx, 'Tekrar'] = yeni_tekrar
                                conn.update(worksheet="ProgramDetay", data=df_program_detay)
                                st.cache_data.clear()
                                st.session_state.program_duzenlenen_idx = None
                                st.rerun()
                            if d4.button(t["cancel"], key=f"pe_cancel_{idx}"):
                                st.session_state.program_duzenlenen_idx = None
                                st.rerun()
                        else:
                            col_metin_p, col_edit_p, col_sil_p = st.columns([5, 1, 1])
                            with col_metin_p:
                                st.write(f"{t['set']} {int(row['Set'])}: **{row['Ağırlık']}kg** x {int(row['Tekrar'])}")
                            with col_edit_p:
                                if st.button("✏️", key=f"pe_editbtn_{idx}"):
                                    st.session_state.program_duzenlenen_idx = idx
                                    st.rerun()
                            with col_sil_p:
                                if st.button("❌", key=f"pe_delbtn_{idx}"):
                                    df_program_detay = df_program_detay.drop(idx)
                                    conn.update(worksheet="ProgramDetay", data=df_program_detay)
                                    st.cache_data.clear()
                                    st.rerun()
        else:
            st.info(t["no_program_content"])

        st.divider()
        st.write(f"**{t['add_exercise_to_program']}**")

        pc1, pc2 = st.columns(2)
        mevcut_kas_gruplari_p = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Shoulder", "Biceps", "Triceps", "Legs", "Glutes", "Calves", "Abs", "Forearm", "Neck"]
        p_kas = pc1.selectbox(t["muscle_group"], mevcut_kas_gruplari_p, key="p_kas_sec")
        p_filtrelenmis = df_hareketler[df_hareketler['Kas Grubu'] == p_kas]
        p_hareket_listesi = p_filtrelenmis['Hareket Tipi'].unique() if not p_filtrelenmis.empty else []
        p_hareket = pc2.selectbox(t["exercise"], p_hareket_listesi, key="p_hareket_sec")

        if p_hareket and st.session_state.p_onceki_hareket != p_hareket:
            st.session_state.p_onceki_hareket = p_hareket
            st.session_state.p_sablon_w = 0.0
            st.session_state.p_sablon_r = 10
            for key in list(st.session_state.keys()):
                if key.startswith("p_w_new_") or key.startswith("p_r_new_"):
                    del st.session_state[key]

        def p_sablon_guncelle():
            yeni_w = st.session_state.p_sablon_w
            yeni_r = st.session_state.p_sablon_r
            for key in list(st.session_state.keys()):
                if key.startswith("p_w_new_"):
                    st.session_state[key] = yeni_w
                elif key.startswith("p_r_new_"):
                    st.session_state[key] = yeni_r

        if p_hareket:
            p_mekanik_kontrol = p_filtrelenmis[p_filtrelenmis['Hareket Tipi'] == p_hareket]['Mekanik'].values[0]

            if p_mekanik_kontrol == "Kardiyo":
                st.warning(t["cardio_not_supported_in_program"])
            else:
                st.write(t["template_title"])
                p_set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1, key="p_set_sayisi_input")

                pt1, pt2 = st.columns(2)
                pt1.number_input(t["template_w"], step=2.5, key="p_sablon_w", on_change=p_sablon_guncelle)
                pt2.number_input(t["template_r"], step=1, key="p_sablon_r", on_change=p_sablon_guncelle)

                st.write("---")
                st.write(t["edit_sets"])

                mevcut_program_setleri_bu_hareket = program_icerik[program_icerik['Hareket'] == p_hareket] if not program_icerik.empty else pd.DataFrame()
                p_baslangic_seti = len(mevcut_program_setleri_bu_hareket) + 1
                p_eklenecek_setler = []

                for i in range(p_set_sayisi):
                    p_guncel_set_no = p_baslangic_seti + i
                    pc_label, pc_w, pc_r = st.columns([1, 2, 2])
                    pc_label.markdown(f"<div style='margin-top: 25px;'>**{t['set']} {p_guncel_set_no}**</div>", unsafe_allow_html=True)

                    p_w_key = f"p_w_new_{p_hareket}_{p_guncel_set_no}"
                    p_r_key = f"p_r_new_{p_hareket}_{p_guncel_set_no}"

                    if p_w_key not in st.session_state: st.session_state[p_w_key] = st.session_state.p_sablon_w
                    if p_r_key not in st.session_state: st.session_state[p_r_key] = st.session_state.p_sablon_r

                    p_w = pc_w.number_input(t["weight"], step=2.5, key=p_w_key)
                    p_r = pc_r.number_input(t["reps"], step=1, key=p_r_key)

                    p_eklenecek_setler.append({
                        "Program Adı": st.session_state.secili_program,
                        "Kullanıcı": st.session_state.secili_kisi,
                        "Kas Grubu": p_kas,
                        "Hareket": p_hareket,
                        "Set": p_guncel_set_no,
                        "Ağırlık": p_w,
                        "Tekrar": p_r
                    })

                if st.button(t["add_to_program"], type="primary", use_container_width=True):
                    p_yeni_satirlar = pd.DataFrame(p_eklenecek_setler)
                    guncel_program_detay = pd.concat([df_program_detay, p_yeni_satirlar], ignore_index=True)
                    conn.update(worksheet="ProgramDetay", data=guncel_program_detay)
                    st.cache_data.clear()

                    for key in list(st.session_state.keys()):
                        if key.startswith("p_w_new_") or key.startswith("p_r_new_"):
                            del st.session_state[key]

                    st.success(f"{p_hareket}: {p_set_sayisi} {t['success_add_to_program']}")
                    st.rerun()

        st.divider()
        with st.expander(t["delete_program_panel"]):
            st.warning(t["delete_program_desc"])
            if st.button(t["delete_program_btn"], type="primary"):
                guncel_programlar = df_programlar[
                    ~((df_programlar['Program Adı'] == st.session_state.secili_program) &
                      (df_programlar['Kullanıcı'] == st.session_state.secili_kisi))
                ]
                guncel_program_detay_kalan = df_program_detay[
                    ~((df_program_detay['Program Adı'] == st.session_state.secili_program) &
                      (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi))
                ]
                conn.update(worksheet="Programlar", data=guncel_programlar)
                conn.update(worksheet="ProgramDetay", data=guncel_program_detay_kalan)
                st.cache_data.clear()
                silinen_program_adi = st.session_state.secili_program
                st.session_state.secili_program = None
                st.success(f"**{silinen_program_adi}** {t['success_delete_program']}")
                st.rerun()
