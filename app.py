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
        "delete_exercise_desc": "Warning: This will permanently remove the exercise from the list.",
        "delete_from_db": "Delete Exercise",
        "success_delete_db": "successfully deleted from the database!",
        "template_title": "📌 Template Settings",
        "how_many_sets": "How Many Sets?",
        "template_w": "Template Weight (kg)",
        "template_r": "Template Reps",
        "edit_sets": "📝 Edit Set Details",
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
        "cardio_details": "🏃‍♂️ Cardio Details",
        "save_cardio": "Save Cardio",
        "success_cardio": "cardio session successfully saved!",
        "delete_exercise_day": "🗑️ Delete Entire Exercise",
        "confirm_delete_exercise_day": "Are you sure you want to delete ALL sets of **{ex}** for this date?",
        "yes_delete": "✅ Yes, Delete",
        "success_delete_exercise_day": "and all its sets for this date were deleted.",
        "export_csv": "⬇️ Export This Day as CSV",
        "go_to_programs": "📋 Programs",
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
        "cardio_not_supported_in_program": "Cardio exercises aren't supported in programs.",
        "delete_exercise_from_program": "🗑️ Delete This Exercise",
        "confirm_delete_exercise_from_program": "Are you sure you want to delete ALL sets of **{ex}** from this program?",
        "success_delete_exercise_from_program": "removed from the program.",
        "save_all_changes": "💾 Save All Changes",
        "success_save_all_changes": "All changes saved!",
        "equipment_type": "Equipment Type",
        "equipment": "Equipment",
        "go_to_stats": "📊 Statistics",
        "stats_title": "📊 Personal & Group Statistics",
        "personal_summary": "👤 Personal Summary",
        "total_days": "Total Workout Days",
        "most_frequent": "Most Performed",
        "total_cardio": "Total Cardio",
        "weight_history": "📈 Exercise Weight History",
        "select_stat_ex": "Select an exercise to view weight progress",
        "group_comparison": "🏆 Group Comparison",
        "comp_days": "Workout Days by Member",
        "comp_cardio": "Total Cardio Duration (min) by Member",
        "nav_daily": "📝 Daily Log"
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
        "delete_exercise_desc": "Uyarı: Bu işlem hareketi listeden tamamen kaldırır. Geçmiş kayıtlar silinmez.",
        "delete_from_db": "Seçili Hareketi Sil",
        "success_delete_db": "veritabanından başarıyla silindi!",
        "template_title": "📌 Şablon Ayarları",
        "how_many_sets": "Kaç Set Yapılacak?",
        "template_w": "Şablon Ağırlık (kg)",
        "template_r": "Şablon Tekrar",
        "edit_sets": "📝 Set Detaylarını Düzenle",
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
        "no_chart_data": "Grafik için yeterli veri henüz yok.",
        "duration": "Süre (dk)",
        "calories": "Kalori (kcal)",
        "cardio_details": "🏃‍♂️ Kardiyo Detayları",
        "save_cardio": "Kardiyoyu Kaydet",
        "success_cardio": "kardiyo kaydı eklendi!",
        "delete_exercise_day": "🗑️ Hareketi Tamamen Sil",
        "confirm_delete_exercise_day": "Bu tarihteki **{ex}** hareketinin TÜM setlerini silmek istediğinize emin misiniz?",
        "yes_delete": "✅ Evet, Sil",
        "success_delete_exercise_day": "hareketinin bu tarihteki tüm setleri silindi.",
        "export_csv": "⬇️ Bu Günü CSV Aktar",
        "go_to_programs": "📋 Programlar",
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
        "target_sets": "Hedef Set",
        "target_weight": "Hedef Ağırlık (kg)",
        "target_reps": "Hedef Tekrar",
        "add_to_program": "Programa Ekle",
        "success_add_to_program": "programa eklendi!",
        "delete_program_panel": "🗑️ Bu Programı Sil",
        "delete_program_desc": "Uyarı: Programı ve içindeki tüm hareketleri siler.",
        "delete_program_btn": "Programı Sil",
        "success_delete_program": "Program başarıyla silindi.",
        "load_program_panel": "📥 Bugün İçin Bir Program Yükle",
        "select_program": "Program Seç",
        "program_preview": "Önizle ve Ayarla",
        "load_program_btn": "📥 Tüm Hareketleri Bugüne Yükle",
        "success_load_program": "bugünün kaydına yüklendi!",
        "cardio_not_supported_in_program": "Kardiyo hareketler programlarda desteklenmiyor.",
        "delete_exercise_from_program": "🗑️ Hareketi Programdan Sil",
        "confirm_delete_exercise_from_program": "Bu programdaki **{ex}** hareketinin TÜM setlerini silmek istediğinize emin misiniz?",
        "success_delete_exercise_from_program": "programdan kaldırıldı.",
        "save_all_changes": "💾 Tüm Değişiklikleri Kaydet",
        "success_save_all_changes": "Tüm değişiklikler kaydedildi!",
        "equipment_type": "Ekipman Tipi",
        "equipment": "Ekipman",
        "go_to_stats": "📊 İstatistikler",
        "stats_title": "📊 İstatistikler",
        "personal_summary": "👤 Kişisel Özet",
        "total_days": "Toplam Gün",
        "most_frequent": "En Sık Hareket",
        "total_cardio": "Toplam Kardiyo",
        "weight_history": "📈 Ağırlık Grafiği",
        "select_stat_ex": "Hareketi Seç",
        "group_comparison": "🏆 Grup İçi Karşılaştırma",
        "comp_days": "Üyelere Göre Antrenman Günleri",
        "comp_cardio": "Üyelere Göre Toplam Kardiyo (dk)",
        "nav_daily": "📝 Günlük"
    }
}

# --- KÜRESEL DEĞİŞKENLER ---
EKIPMAN_LISTESI = ["Barbell", "Dumbbell", "Machine", "Cable", "Bodyweight", "Band", "Smith Machine", "Kettlebell", "Other", "-"]

# --- SAYFA YAPILANDIRMASI & ÖZEL MOBİL CSS ---
st.set_page_config(page_title="Workout App", page_icon="💪", layout="centered", initial_sidebar_state="collapsed")

custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 800px;
    }
    div[data-testid="stButton"] > button {
        border-radius: 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 2px rgba(0,0,0,0.15);
    }
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    h1, h2, h3 {
        text-align: center;
    }
    input, select {
        border-radius: 10px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Dil seçeneğini ana ekranın en üstüne, küçük bir buton gibi ekliyoruz
dil_kolonu, bos_kolon = st.columns([1, 2])
with dil_kolonu:
    # Varsayılan dil Türkçe (index=0) yapıldı
    secilen_dil = st.selectbox("🌐 Dil", ["Türkçe", "English"], index=0, label_visibility="collapsed")
t = LANG[secilen_dil]

# --- OTURUM DEĞİŞKENLER ---
if 'sayfa' not in st.session_state: st.session_state.sayfa = 'ana_sayfa'
if 'secili_grup' not in st.session_state: st.session_state.secili_grup = None
if 'secili_kisi' not in st.session_state: st.session_state.secili_kisi = None
if 'onceki_hareket' not in st.session_state: st.session_state.onceki_hareket = ""
if 'sablon_w' not in st.session_state: st.session_state.sablon_w = 0.0
if 'sablon_r' not in st.session_state: st.session_state.sablon_r = 10
if 'grafik_gorunur' not in st.session_state: st.session_state.grafik_gorunur = None
if 'silme_onay_hareket' not in st.session_state: st.session_state.silme_onay_hareket = None
if 'secili_program' not in st.session_state: st.session_state.secili_program = None
if 'program_silme_onay_hareket' not in st.session_state: st.session_state.program_silme_onay_hareket = None
if 'p_onceki_hareket' not in st.session_state: st.session_state.p_onceki_hareket = ""
if 'p_sablon_w' not in st.session_state: st.session_state.p_sablon_w = 0.0
if 'p_sablon_r' not in st.session_state: st.session_state.p_sablon_r = 10

# --- GOOGLE SHEETS BAĞLANTISI ---
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=60)
def veri_getir(sekme_adi, kolonlar):
    try:
        df = conn.read(worksheet=sekme_adi)
        if df.empty: return pd.DataFrame(columns=kolonlar)
        df.fillna(0, inplace=True)
        return df.dropna(how='all')
    except:
        return pd.DataFrame(columns=kolonlar)

def sablon_guncelle():
    yeni_w = st.session_state.sablon_w
    yeni_r = st.session_state.sablon_r
    for key in list(st.session_state.keys()):
        if key.startswith("w_new_"): st.session_state[key] = yeni_w
        elif key.startswith("r_new_"): st.session_state[key] = yeni_r

# Ortak Navigasyon Barı
def render_top_nav():
    st.write("")
    n1, n2, n3, n4 = st.columns([1,1,1,1.5])
    with n1:
        if st.button("👥 " + t["back_to_groups"].split(" ")[-1], use_container_width=True):
            st.session_state.sayfa = 'grup_sayfasi'
            st.rerun()
    with n2:
        if st.button(t["nav_daily"], type="primary" if st.session_state.sayfa == 'kisi_sayfasi' else "secondary", use_container_width=True):
            st.session_state.sayfa = 'kisi_sayfasi'
            st.rerun()
    with n3:
        if st.button("📋 Prog", type="primary" if st.session_state.sayfa == 'program_sayfasi' else "secondary", use_container_width=True):
            st.session_state.sayfa = 'program_sayfasi'
            st.rerun()
    with n4:
        if st.button("📊 Stats", type="primary" if st.session_state.sayfa == 'istatistik_sayfasi' else "secondary", use_container_width=True):
            st.session_state.sayfa = 'istatistik_sayfasi'
            st.rerun()
    st.divider()

# --- SAYFA 1: ANA SAYFA (GRUPLAR) ---
if st.session_state.sayfa == 'ana_sayfa':
    df_gruplar = veri_getir("Gruplar", ["Grup Adı"])
    st.markdown(f"<h1>{t['groups_title']}</h1>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>{t['existing_groups']}</h3>", unsafe_allow_html=True)
        if not df_gruplar.empty:
            for index, row in df_gruplar.iterrows():
                if st.button(f"📁 {row['Grup Adı']}", use_container_width=True):
                    st.session_state.secili_grup = row['Grup Adı']
                    st.session_state.sayfa = 'grup_sayfasi'
                    st.rerun()
        else:
            st.info(t["no_group"])
            
    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>➕ {t['new_group']}</h3>", unsafe_allow_html=True)
        yeni_grup = st.text_input(t["new_group"], label_visibility="collapsed")
        if st.button(t["add_group"], type="primary", use_container_width=True):
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
    st.markdown(f"<h1>📁 {st.session_state.secili_grup}</h1>", unsafe_allow_html=True)
    
    if st.button(t["back_to_groups"], use_container_width=True):
        st.session_state.sayfa = 'ana_sayfa'
        st.rerun()
        
    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>{t['members']}</h3>", unsafe_allow_html=True)
        grup_uyeleri = df_kullanicilar[df_kullanicilar['Grup Adı'] == st.session_state.secili_grup]
        
        if not grup_uyeleri.empty:
            for index, row in grup_uyeleri.iterrows():
                if st.button(f"👤 {row['Kullanıcı Adı']}", use_container_width=True):
                    st.session_state.secili_kisi = row['Kullanıcı Adı']
                    st.session_state.sayfa = 'kisi_sayfasi'
                    st.rerun()
        else:
            st.info(t["no_member"])
            
    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>➕ {t['new_member']}</h3>", unsafe_allow_html=True)
        yeni_kisi = st.text_input(t["new_member"], label_visibility="collapsed")
        if st.button(t["add_member"], type="primary", use_container_width=True):
            if yeni_kisi:
                yeni_satir = pd.DataFrame([{"Grup Adı": st.session_state.secili_grup, "Kullanıcı Adı": yeni_kisi}])
                guncel_kullanicilar = pd.concat([df_kullanicilar, yeni_satir], ignore_index=True)
                conn.update(worksheet="Kullanicilar", data=guncel_kullanicilar)
                st.cache_data.clear()
                st.success(f"{yeni_kisi} {t['success_member']}")
                st.rerun()

# --- SAYFA 3: KİŞİ DETAYI (GÜNLÜK) ---
elif st.session_state.sayfa == 'kisi_sayfasi':
    render_top_nav()
    st.markdown(f"<h2>👤 {st.session_state.secili_kisi} - {t['daily_log']}</h2>", unsafe_allow_html=True)
    
    df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Süre (dk)", "Kalori", "Mekanik", "Ekipman"])
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik", "Ekipman"])
    df_programlar = veri_getir("Programlar", ["Kullanıcı", "Program Adı"])
    df_program_detay = veri_getir("ProgramDetay", ["Program Adı", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Ekipman"])
    
    def grafik_ciz(hareket_adi):
        gecmis_tum_setler = df_antrenmanlar[
            (df_antrenmanlar['Grup'] == st.session_state.secili_grup) &
            (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
            (df_antrenmanlar['Hareket'] == hareket_adi)
        ].copy()
        if not gecmis_tum_setler.empty:
            gecmis_tum_setler['Tarih'] = pd.to_datetime(gecmis_tum_setler['Tarih'])
            grafik_verisi = gecmis_tum_setler.groupby('Tarih')['Ağırlık'].max().reset_index().sort_values(by='Tarih')
            grafik_verisi['Tarih'] = grafik_verisi['Tarih'].dt.strftime('%d/%m/%Y')
            grafik_verisi.set_index('Tarih', inplace=True)
            st.line_chart(grafik_verisi['Ağırlık'].astype(float))
        else:
            st.info(t["no_chart_data"])

    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>📅 {t['date']}</h3>", unsafe_allow_html=True)
        secili_tarih = st.date_input("Tarih", value=date.today(), format="DD/MM/YYYY", label_visibility="collapsed")
        
        with st.expander(t["load_program_panel"]):
            kisi_programlari_yukle = df_programlar[df_programlar['Kullanıcı'] == st.session_state.secili_kisi]
            if kisi_programlari_yukle.empty:
                st.info(t["no_program"])
            else:
                secili_program_yukle = st.selectbox(t["select_program"], kisi_programlari_yukle['Program Adı'].unique(), key="program_yukle_secim")
                program_icerik_yukle = df_program_detay[(df_program_detay['Program Adı'] == secili_program_yukle) & (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi)].sort_values(by=["Hareket", "Set"])

                if program_icerik_yukle.empty:
                    st.info(t["no_program_content"])
                else:
                    st.write(f"**{t['program_preview']}**")
                    yuklenecek_setler_l = []
                    for hareket_l in program_icerik_yukle['Hareket'].unique():
                        hareket_setleri_l = program_icerik_yukle[program_icerik_yukle['Hareket'] == hareket_l]
                        kas_grubu_l = hareket_setleri_l.iloc[0]['Kas Grubu']
                        ekipman_l = hareket_setleri_l.iloc[0]['Ekipman'] if 'Ekipman' in hareket_setleri_l.columns else "-"
                        st.markdown(f"💪 **{ekipman_l} {kas_grubu_l} {hareket_l}**".replace("- ", "").strip())

                        for p_idx, p_row in hareket_setleri_l.iterrows():
                            cLabel, cW, cR = st.columns([1, 2, 2])
                            cLabel.markdown(f"<div style='margin-top: 8px;'>{t['set']} {int(p_row['Set'])}</div>", unsafe_allow_html=True)
                            w_key_l = f"load_w_{secili_program_yukle}_{p_idx}"
                            r_key_l = f"load_r_{secili_program_yukle}_{p_idx}"
                            if w_key_l not in st.session_state: st.session_state[w_key_l] = float(p_row['Ağırlık'])
                            if r_key_l not in st.session_state: st.session_state[r_key_l] = int(p_row['Tekrar'])
                            agirlik_l = cW.number_input(t["weight"], min_value=0.0, step=2.5, key=w_key_l, label_visibility="collapsed")
                            tekrar_l = cR.number_input(t["reps"], min_value=0, step=1, key=r_key_l, label_visibility="collapsed")
                            yuklenecek_setler_l.append({"Kas Grubu": kas_grubu_l, "Hareket": hareket_l, "Ağırlık": agirlik_l, "Tekrar": tekrar_l, "Ekipman": p_row['Ekipman'] if 'Ekipman' in p_row else "-"})

                    if st.button(t["load_program_btn"], type="primary", use_container_width=True):
                        hareket_mekanik_sozlugu = df_hareketler.set_index('Hareket Tipi')['Mekanik'].to_dict() if not df_hareketler.empty else {}
                        tum_yeni_setler = []
                        hareket_sayaclari = {}
                        for satir in yuklenecek_setler_l:
                            hareket_adi_l = satir["Hareket"]
                            if hareket_adi_l not in hareket_sayaclari:
                                hareket_sayaclari[hareket_adi_l] = len(df_antrenmanlar[(df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == hareket_adi_l)]) + 1
                            tum_yeni_setler.append({"Tarih": secili_tarih.strftime("%Y-%m-%d"), "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": satir["Kas Grubu"], "Hareket": hareket_adi_l, "Set": hareket_sayaclari[hareket_adi_l], "Ağırlık": satir["Ağırlık"], "Tekrar": satir["Tekrar"], "Süre (dk)": 0, "Kalori": 0, "Mekanik": hareket_mekanik_sozlugu.get(hareket_adi_l, "Compound"), "Ekipman": satir["Ekipman"]})
                            hareket_sayaclari[hareket_adi_l] += 1
                        conn.update(worksheet="Antrenmanlar", data=pd.concat([df_antrenmanlar, pd.DataFrame(tum_yeni_setler)], ignore_index=True))
                        st.cache_data.clear()
                        for key in list(st.session_state.keys()):
                            if key.startswith("load_w_") or key.startswith("load_r_"): del st.session_state[key]
                        st.success(f"{secili_program_yukle} {t['success_load_program']}")
                        st.rerun()

    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>➕ {t['add_new_set']}</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        mevcut_kas_gruplari = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Shoulder", "Biceps", "Triceps", "Legs", "Cardio"]
        with col1: secili_kas = st.selectbox(t["muscle_group"], mevcut_kas_gruplari)
        
        filtrelenmis_df = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]
        hareket_listesi = filtrelenmis_df['Hareket Tipi'].unique() if not filtrelenmis_df.empty else []
        with col2: secili_hareket = st.selectbox(t["exercise"], hareket_listesi)

        if secili_hareket:
            mekanik_degeri = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
            st.caption(f"{t['mechanic']}: **{mekanik_degeri}**") 
            
            veritabanindaki_ekipman = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Ekipman'].values[0] if 'Ekipman' in filtrelenmis_df.columns else "Barbell"
            secili_ekipman = st.selectbox(t["equipment"], EKIPMAN_LISTESI, index=EKIPMAN_LISTESI.index(veritabanindaki_ekipman) if veritabanindaki_ekipman in EKIPMAN_LISTESI else 0, key="gunluk_ekipman_sec")

            if st.session_state.onceki_hareket != secili_hareket:
                st.session_state.onceki_hareket = secili_hareket
                gecmis_hareket = df_antrenmanlar[(df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == secili_hareket) & (df_antrenmanlar['Mekanik'] != 'Kardiyo')]
                st.session_state.sablon_w = float(gecmis_hareket.sort_values(by="Tarih", ascending=False).iloc[0]['Ağırlık']) if not gecmis_hareket.empty else 0.0
                st.session_state.sablon_r = 10
                for key in list(st.session_state.keys()):
                    if key.startswith("w_new_") or key.startswith("r_new_"): del st.session_state[key]
            
            st.divider()
            
            if mekanik_degeri == "Kardiyo":
                st.write(f"**{t['cardio_details']}**")
                def kalori_hesapla(): st.session_state.kardiyo_kalori = int(st.session_state.kardiyo_sure * 10)
                if 'kardiyo_sure' not in st.session_state: st.session_state.kardiyo_sure = 30
                if 'kardiyo_kalori' not in st.session_state: st.session_state.kardiyo_kalori = 300
                c_sure, c_kalori = st.columns(2)
                kardiyo_sure = c_sure.number_input(t["duration"], min_value=1, value=st.session_state.kardiyo_sure, key="kardiyo_sure", step=1, on_change=kalori_hesapla)
                kardiyo_kalori = c_kalori.number_input(t["calories"], min_value=1, value=st.session_state.kardiyo_kalori, key="kardiyo_kalori", step=10)
                
                if st.button(t["save_cardio"], type="primary", use_container_width=True):
                    yeni_satir = pd.DataFrame([{"Tarih": secili_tarih.strftime("%Y-%m-%d"), "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": secili_kas, "Hareket": secili_hareket, "Set": 1, "Ağırlık": 0, "Tekrar": 0, "Süre (dk)": kardiyo_sure, "Kalori": kardiyo_kalori, "Mekanik": mekanik_degeri, "Ekipman": secili_ekipman}])
                    conn.update(worksheet="Antrenmanlar", data=pd.concat([df_antrenmanlar, yeni_satir], ignore_index=True))
                    st.cache_data.clear()
                    st.success(f"{secili_hareket} {t['success_cardio']}")
                    st.rerun()
            else:
                st.write(f"**{t['template_title']}**")
                set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1)
                c_hedef1, c_hedef2 = st.columns(2)
                c_hedef1.number_input(t["template_w"], step=2.5, key="sablon_w", on_change=sablon_guncelle)
                c_hedef2.number_input(t["template_r"], step=1, key="sablon_r", on_change=sablon_guncelle)
                
                st.write(f"**{t['edit_sets']}**")
                bugunku_setler = df_antrenmanlar[(df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == secili_hareket)]
                baslangic_seti = len(bugunku_setler) + 1
                eklenecek_setler = []
                
                for i in range(set_sayisi):
                    guncel_set_no = baslangic_seti + i
                    c_label, c_w, c_r = st.columns([1,2,2])
                    c_label.markdown(f"<div style='margin-top: 25px;'>**{t['set']} {guncel_set_no}**</div>", unsafe_allow_html=True)
                    w_key, r_key = f"w_new_{secili_hareket}_{guncel_set_no}", f"r_new_{secili_hareket}_{guncel_set_no}"
                    if w_key not in st.session_state: st.session_state[w_key] = st.session_state.sablon_w
                    if r_key not in st.session_state: st.session_state[r_key] = st.session_state.sablon_r
                    w = c_w.number_input(t["weight"], step=2.5, key=w_key, label_visibility="collapsed")
                    r = c_r.number_input(t["reps"], step=1, key=r_key, label_visibility="collapsed")
                    eklenecek_setler.append({"Tarih": secili_tarih.strftime("%Y-%m-%d"), "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": secili_kas, "Hareket": secili_hareket, "Set": guncel_set_no, "Ağırlık": w, "Tekrar": r, "Süre (dk)": 0, "Kalori": 0, "Mekanik": mekanik_degeri, "Ekipman": secili_ekipman})
                    
                if st.button(t["save_all"], type="primary", use_container_width=True):
                    conn.update(worksheet="Antrenmanlar", data=pd.concat([df_antrenmanlar, pd.DataFrame(eklenecek_setler)], ignore_index=True))
                    st.cache_data.clear()
                    for key in list(st.session_state.keys()):
                        if key.startswith("w_new_") or key.startswith("r_new_"): del st.session_state[key]
                    st.success(f"{secili_hareket}: {set_sayisi} {t['success_sets']}")
                    st.rerun()

        with st.expander(t["new_exercise_panel"]):
            st.caption(t["new_exercise_desc"])
            c_kas, c_har, c_mek, c_ekip = st.columns(4)
            yeni_kas = c_kas.selectbox(t["which_muscle"], mevcut_kas_gruplari, key="new_muscle")
            yeni_har = c_har.text_input(t["new_exercise_name"])
            yeni_mek = c_mek.selectbox(t["mechanic_type"], ["Compound", "Izole", "Kardiyo"])
            yeni_ekip = c_ekip.selectbox(t["equipment_type"], EKIPMAN_LISTESI) 
            if st.button(t["add_to_db"], type="secondary", use_container_width=True):
                if yeni_har:
                    conn.update(worksheet="Hareketler", data=pd.concat([df_hareketler, pd.DataFrame([{"Kas Grubu": yeni_kas, "Hareket Tipi": yeni_har, "Mekanik": yeni_mek, "Ekipman": yeni_ekip}])], ignore_index=True))
                    st.cache_data.clear()
                    st.rerun()
                else: st.warning(t["warn_name"])

    st.divider()
    st.markdown(f"<h2 style='font-size: 1.5rem;'>📋 {secili_tarih.strftime('%d/%m/%Y')} {t['workout_of'] if secilen_dil == 'English' else 'Tarihli ' + t['workout_of']}</h2>", unsafe_allow_html=True)
    
    gunluk_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d"))]

    if not gunluk_gecmis.empty:
        st.download_button(label=t["export_csv"], data=gunluk_gecmis.to_csv(index=False).encode('utf-8-sig'), file_name=f"antrenman_{st.session_state.secili_kisi}_{secili_tarih.strftime('%Y-%m-%d')}.csv", mime="text/csv", use_container_width=True)
        st.write("")

        for hareket in gunluk_gecmis['Hareket'].unique():
            hareket_setleri = gunluk_gecmis[gunluk_gecmis['Hareket'] == hareket].sort_values(by="Set")
            ilk = hareket_setleri.iloc[0]
            tam_adi = f"{ilk.get('Ekipman','-')} {ilk['Kas Grubu']} {hareket}".replace("- ", "").strip()
            
            if ilk['Mekanik'] == "Kardiyo":
                ozet = " | ".join([f"{row['Süre (dk)']} dk, {row['Kalori']} kcal" for _, row in hareket_setleri.iterrows()])
                baslik = f"🏃‍♂️ **{tam_adi}** 👉 {ozet}"
            else:
                ozet = " | ".join([f"{row['Ağırlık']}x{row['Tekrar']}" for _, row in hareket_setleri.iterrows()])
                baslik = f"💪 **{tam_adi}** ({len(hareket_setleri)} {t['set']}) 👉 {ozet}"
            
            with st.expander(baslik, key=f"exp_{hareket}_{secili_tarih}"):
                h_key = f"{hareket}_{secili_tarih}"
                c_grafik, c_sil = st.columns(2) if ilk['Mekanik'] != "Kardiyo" else (st.container(), st.columns(1)[0])
                
                if ilk['Mekanik'] != "Kardiyo":
                    with c_grafik:
                        if st.button(f"📈 {t['progress_chart']}", key=f"g_btn_{h_key}", use_container_width=True):
                            st.session_state.grafik_gorunur = None if st.session_state.grafik_gorunur == hareket else hareket
                with c_sil:
                    if st.button(t["delete_exercise_day"], key=f"del_btn_{h_key}", use_container_width=True):
                        st.session_state.silme_onay_hareket = None if st.session_state.silme_onay_hareket == h_key else h_key

                if st.session_state.silme_onay_hareket == h_key:
                    st.warning(t["confirm_delete_exercise_day"].format(ex=hareket))
                    co1, co2 = st.columns(2)
                    if co1.button(t["yes_delete"], key=f"y_del_{h_key}", type="primary", use_container_width=True):
                        conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar.drop(hareket_setleri.index))
                        st.cache_data.clear()
                        st.session_state.silme_onay_hareket, st.session_state.grafik_gorunur = None, None
                        st.rerun()
                    if co2.button(t["cancel"], key=f"c_del_{h_key}", use_container_width=True): st.session_state.silme_onay_hareket = None

                if ilk['Mekanik'] != "Kardiyo" and st.session_state.grafik_gorunur == hareket:
                    grafik_ciz(hareket)
                    st.divider()

                for idx, row in hareket_setleri.iterrows():
                    cL, c1, c2, cS = st.columns([0.8, 1.5, 1.5, 0.6])
                    if row['Mekanik'] == 'Kardiyo':
                        cL.markdown("<div style='margin-top: 8px;'>⏱️</div>", unsafe_allow_html=True)
                        c1.number_input(t["duration"], min_value=0, value=int(row['Süre (dk)']), step=1, key=f"ls_{idx}", label_visibility="collapsed")
                        c2.number_input(t["calories"], min_value=0, value=int(row['Kalori']), step=10, key=f"lk_{idx}", label_visibility="collapsed")
                    else:
                        cL.markdown(f"<div style='margin-top: 8px;'>{t['set']} {int(row['Set'])}</div>", unsafe_allow_html=True)
                        c1.number_input(t["weight"], min_value=0.0, value=float(row['Ağırlık']), step=2.5, key=f"lw_{idx}", label_visibility="collapsed")
                        c2.number_input(t["reps"], min_value=0, value=int(row['Tekrar']), step=1, key=f"lr_{idx}", label_visibility="collapsed")
                    if cS.button("❌", key=f"d_{idx}"):
                        conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar.drop(idx))
                        st.cache_data.clear()
                        st.rerun()

                if st.button(t["save_all_changes"], key=f"s_all_{h_key}", type="primary", use_container_width=True):
                    for idx, row in hareket_setleri.iterrows():
                        if row['Mekanik'] == 'Kardiyo':
                            df_antrenmanlar.at[idx, 'Süre (dk)'] = st.session_state[f"ls_{idx}"]
                            df_antrenmanlar.at[idx, 'Kalori'] = st.session_state[f"lk_{idx}"]
                        else:
                            df_antrenmanlar.at[idx, 'Ağırlık'] = st.session_state[f"lw_{idx}"]
                            df_antrenmanlar.at[idx, 'Tekrar'] = st.session_state[f"lr_{idx}"]
                    conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar)
                    st.cache_data.clear()
                    st.rerun()
    else:
        st.info(t["no_workout"])


# --- SAYFA 4: ANTRENMAN PROGRAMLARI ---
elif st.session_state.sayfa == 'program_sayfasi':
    render_top_nav()
    st.markdown(f"<h2>📋 {st.session_state.secili_kisi} - {t['programs_title']}</h2>", unsafe_allow_html=True)

    df_programlar = veri_getir("Programlar", ["Kullanıcı", "Program Adı"])
    df_program_detay = veri_getir("ProgramDetay", ["Program Adı", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Ekipman"])
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik", "Ekipman"])

    kisi_programlari = df_programlar[df_programlar['Kullanıcı'] == st.session_state.secili_kisi]

    if st.session_state.secili_program is None:
        with st.container(border=True):
            st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>{t['existing_programs']}</h3>", unsafe_allow_html=True)
            if not kisi_programlari.empty:
                for idx, row in kisi_programlari.iterrows():
                    if st.button(f"📁 {row['Program Adı']}", key=f"p_{idx}", use_container_width=True):
                        st.session_state.secili_program = row['Program Adı']
                        st.rerun()
            else:
                st.info(t["no_program"])
                
        with st.container(border=True):
            st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>➕ {t['create_program']}</h3>", unsafe_allow_html=True)
            yeni_prog = st.text_input(t["new_program_name"], label_visibility="collapsed")
            if st.button(t["create_program"], type="primary", use_container_width=True):
                if yeni_prog and yeni_prog not in kisi_programlari['Program Adı'].values:
                    conn.update(worksheet="Programlar", data=pd.concat([df_programlar, pd.DataFrame([{"Kullanıcı": st.session_state.secili_kisi, "Program Adı": yeni_prog}])], ignore_index=True))
                    st.cache_data.clear()
                    st.session_state.secili_program = yeni_prog
                    st.rerun()
                elif yeni_prog: st.warning(t["program_exists"])

    else:
        st.markdown(f"<h3>📁 {st.session_state.secili_program}</h3>", unsafe_allow_html=True)
        if st.button(t["back_to_programs"], use_container_width=True):
            st.session_state.secili_program = None
            st.rerun()

        program_icerik = df_program_detay[(df_program_detay['Program Adı'] == st.session_state.secili_program) & (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi)]

        st.write(f"**{t['program_content']}**")
        if not program_icerik.empty:
            for hareket_p in program_icerik['Hareket'].unique():
                h_set_p = program_icerik[program_icerik['Hareket'] == hareket_p].sort_values(by="Set")
                ilk_p = h_set_p.iloc[0]
                tam_adi = f"{ilk_p.get('Ekipman','-')} {ilk_p['Kas Grubu']} {hareket_p}".replace("- ", "").strip()
                ozet = " | ".join([f"{r['Ağırlık']}x{r['Tekrar']}" for _, r in h_set_p.iterrows()])
                
                with st.expander(f"💪 **{tam_adi}** 👉 {ozet}", key=f"e_{hareket_p}"):
                    p_key = f"{st.session_state.secili_program}_{hareket_p}"
                    if st.button(t["delete_exercise_from_program"], key=f"d_p_{p_key}", use_container_width=True):
                        st.session_state.program_silme_onay_hareket = None if st.session_state.program_silme_onay_hareket == p_key else p_key
                    if st.session_state.program_silme_onay_hareket == p_key:
                        st.warning(t["confirm_delete_exercise_from_program"].format(ex=hareket_p))
                        c1, c2 = st.columns(2)
                        if c1.button(t["yes_delete"], key=f"y_d_{p_key}", type="primary", use_container_width=True):
                            conn.update(worksheet="ProgramDetay", data=df_program_detay.drop(h_set_p.index))
                            st.cache_data.clear()
                            st.session_state.program_silme_onay_hareket = None
                            st.rerun()
                        if c2.button(t["cancel"], key=f"c_d_{p_key}", use_container_width=True): st.session_state.program_silme_onay_hareket = None

                    st.divider()
                    for idx, row in h_set_p.iterrows():
                        cL, cW, cR, cS = st.columns([0.8, 1.5, 1.5, 0.6])
                        cL.markdown(f"<div style='margin-top: 8px;'>{t['set']} {int(row['Set'])}</div>", unsafe_allow_html=True)
                        cW.number_input(t["weight"], min_value=0.0, value=float(row['Ağırlık']), step=2.5, key=f"pw_{idx}", label_visibility="collapsed")
                        cR.number_input(t["reps"], min_value=0, value=int(row['Tekrar']), step=1, key=f"pr_{idx}", label_visibility="collapsed")
                        if cS.button("❌", key=f"pd_{idx}"):
                            conn.update(worksheet="ProgramDetay", data=df_program_detay.drop(idx))
                            st.cache_data.clear()
                            st.rerun()
                    if st.button(t["save_all_changes"], key=f"psa_{p_key}", type="primary", use_container_width=True):
                        for idx, row in h_set_p.iterrows():
                            df_program_detay.at[idx, 'Ağırlık'] = st.session_state[f"pw_{idx}"]
                            df_program_detay.at[idx, 'Tekrar'] = st.session_state[f"pr_{idx}"]
                        conn.update(worksheet="ProgramDetay", data=df_program_detay)
                        st.cache_data.clear()
                        st.rerun()
        else:
            st.info(t["no_program_content"])

        with st.container(border=True):
            st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>➕ {t['add_exercise_to_program']}</h3>", unsafe_allow_html=True)
            pc1, pc2 = st.columns(2)
            mevcut_kas = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Legs"]
            p_kas = pc1.selectbox(t["muscle_group"], mevcut_kas, key="pkas")
            p_hareket_listesi = df_hareketler[df_hareketler['Kas Grubu'] == p_kas]['Hareket Tipi'].unique()
            p_hareket = pc2.selectbox(t["exercise"], p_hareket_listesi, key="phar")

            if p_hareket:
                p_ekip = df_hareketler[df_hareketler['Hareket Tipi'] == p_hareket]['Ekipman'].values[0] if 'Ekipman' in df_hareketler.columns else "Barbell"
                p_secili_ekipman = st.selectbox(t["equipment"], EKIPMAN_LISTESI, index=EKIPMAN_LISTESI.index(p_ekip) if p_ekip in EKIPMAN_LISTESI else 0, key="pekip")

                if st.session_state.p_onceki_hareket != p_hareket:
                    st.session_state.p_onceki_hareket = p_hareket
                    st.session_state.p_sablon_w, st.session_state.p_sablon_r = 0.0, 10
                    for key in list(st.session_state.keys()):
                        if key.startswith("p_w_new_") or key.startswith("p_r_new_"): del st.session_state[key]

                def p_sablon_guncelle():
                    for k in list(st.session_state.keys()):
                        if k.startswith("p_w_new_"): st.session_state[k] = st.session_state.p_sablon_w
                        elif k.startswith("p_r_new_"): st.session_state[k] = st.session_state.p_sablon_r

                if df_hareketler[df_hareketler['Hareket Tipi'] == p_hareket]['Mekanik'].values[0] == "Kardiyo":
                    st.warning(t["cardio_not_supported_in_program"])
                else:
                    p_set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1, key="psets")
                    pt1, pt2 = st.columns(2)
                    pt1.number_input(t["template_w"], step=2.5, key="p_sablon_w", on_change=p_sablon_guncelle)
                    pt2.number_input(t["template_r"], step=1, key="p_sablon_r", on_change=p_sablon_guncelle)
                    
                    st.divider()
                    mevcut_prog_set_har = program_icerik[program_icerik['Hareket'] == p_hareket]
                    p_bas_set = len(mevcut_prog_set_har) + 1
                    p_ekle_set = []

                    for i in range(p_set_sayisi):
                        g_set = p_bas_set + i
                        cl, cw, cr = st.columns([1, 2, 2])
                        cl.markdown(f"<div style='margin-top: 25px;'>**{t['set']} {g_set}**</div>", unsafe_allow_html=True)
                        kw, kr = f"p_w_new_{p_hareket}_{g_set}", f"p_r_new_{p_hareket}_{g_set}"
                        if kw not in st.session_state: st.session_state[kw] = st.session_state.p_sablon_w
                        if kr not in st.session_state: st.session_state[kr] = st.session_state.p_sablon_r
                        p_w = cw.number_input(t["weight"], step=2.5, key=kw, label_visibility="collapsed")
                        p_r = cr.number_input(t["reps"], step=1, key=kr, label_visibility="collapsed")
                        p_ekle_set.append({"Program Adı": st.session_state.secili_program, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": p_kas, "Hareket": p_hareket, "Set": g_set, "Ağırlık": p_w, "Tekrar": p_r, "Ekipman": p_secili_ekipman})

                    if st.button(t["add_to_program"], type="primary", use_container_width=True):
                        conn.update(worksheet="ProgramDetay", data=pd.concat([df_program_detay, pd.DataFrame(p_ekle_set)], ignore_index=True))
                        st.cache_data.clear()
                        for k in list(st.session_state.keys()):
                            if k.startswith("p_w_new_") or k.startswith("p_r_new_"): del st.session_state[k]
                        st.rerun()

        with st.expander(t["delete_program_panel"]):
            st.warning(t["delete_program_desc"])
            if st.button(t["delete_program_btn"], type="primary", use_container_width=True):
                conn.update(worksheet="Programlar", data=df_programlar[~((df_programlar['Program Adı'] == st.session_state.secili_program) & (df_programlar['Kullanıcı'] == st.session_state.secili_kisi))])
                conn.update(worksheet="ProgramDetay", data=df_program_detay[~((df_program_detay['Program Adı'] == st.session_state.secili_program) & (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi))])
                st.cache_data.clear()
                st.session_state.secili_program = None
                st.rerun()

# --- SAYFA 5: İSTATİSTİKLER (GÜNCELLENDİ) ---
elif st.session_state.sayfa == 'istatistik_sayfasi':
    render_top_nav()
    st.markdown(f"<h2>{t['stats_title']}</h2>", unsafe_allow_html=True)
    
    df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Süre (dk)", "Kalori", "Mekanik", "Ekipman"])
    
    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>{t['personal_summary']}</h3>", unsafe_allow_html=True)
        # copy() ile dataframe kopyası oluşturuyoruz, böylece yeni kolon eklerken hata (warning) almayız.
        kisi_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi)].copy()

        if kisi_gecmis.empty:
            st.info(t["no_chart_data"])
        else:
            # Tüm istatistikler için "Tam Hareket" ismini tek seferde oluşturuyoruz
            kisi_gecmis['Tam Hareket'] = kisi_gecmis.apply(
                lambda row: f"{row.get('Ekipman','-')} {row.get('Kas Grubu','')} {row.get('Hareket','')}".replace("- ", "").strip(), 
                axis=1
            )
            
            c1, c2, c3 = st.columns(3)
            c1.metric(t["total_days"], f"{kisi_gecmis['Tarih'].nunique()} Gün")
            c2.metric(t["most_frequent"], kisi_gecmis['Tam Hareket'].value_counts().idxmax() if not kisi_gecmis.empty else "-")
            c3.metric(t["total_cardio"], f"{int(pd.to_numeric(kisi_gecmis['Süre (dk)'], errors='coerce').fillna(0).sum())} dk")

    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>{t['weight_history']}</h3>", unsafe_allow_html=True)
        # Sadece ağırlık geçmişi olan hareketlerin "Tam İsimlerini" çekiyoruz
        agirlik_h = kisi_gecmis[kisi_gecmis['Mekanik'] != 'Kardiyo']['Tam Hareket'].unique() if not kisi_gecmis.empty else []
        
        if len(agirlik_h) > 0:
            sec_stat = st.selectbox(t["select_stat_ex"], agirlik_h, label_visibility="collapsed")
            if sec_stat:
                graf = kisi_gecmis[kisi_gecmis['Tam Hareket'] == sec_stat].copy()
                graf['Tarih'] = pd.to_datetime(graf['Tarih'])
                g = graf.groupby('Tarih')['Ağırlık'].max().reset_index().sort_values(by='Tarih')
                g['Tarih'] = g['Tarih'].dt.strftime('%d/%m/%Y')
                g.set_index('Tarih', inplace=True)
                st.line_chart(g['Ağırlık'].astype(float))
        else:
            st.info(t["no_chart_data"])
            
    with st.container(border=True):
        st.markdown(f"<h3 style='font-size: 1.2rem; color: #888;'>{t['group_comparison']}</h3>", unsafe_allow_html=True)
        grup_gecmisi = df_antrenmanlar[df_antrenmanlar['Grup'] == st.session_state.secili_grup].copy()

        if not grup_gecmisi.empty:
            st.markdown(f"**{t['comp_days']}**")
            gun_s = grup_gecmisi.groupby('Kullanıcı')['Tarih'].nunique().reset_index()
            gun_s.set_index('Kullanıcı', inplace=True)
            st.bar_chart(gun_s['Tarih'])

            st.markdown(f"**{t['comp_cardio']}**")
            grup_gecmisi['Süre (dk)'] = pd.to_numeric(grup_gecmisi['Süre (dk)'], errors='coerce').fillna(0)
            kard_s = grup_gecmisi.groupby('Kullanıcı')['Süre (dk)'].sum().reset_index()
            kard_s.set_index('Kullanıcı', inplace=True)
            st.bar_chart(kard_s['Süre (dk)'])
        else:
            st.info(t["no_chart_data"])
