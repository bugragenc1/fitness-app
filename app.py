import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import calendar as cal_module
import html
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
        "export_all_csv": "📥 Export All Workouts as CSV",
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
        "nav_daily": "📝 Daily Log",
        "calendar_legend": "▪ Workout day · ■ Selected day",
        "legacy_add_panel": "📚 Add From Legacy List To Today",
        "legacy_add_desc": "Pick a common exercise from the curated legacy list and log it directly to today's workout. This does NOT add it to your personal exercise database.",
        "legacy_select_group": "Muscle Group",
        "legacy_empty": "Legacy exercise list is empty. Add exercises to the 'LegacyHareketler' sheet in Google Sheets first.",
        "legacy_add_program_panel": "📚 Add From Legacy List To This Program",
        "legacy_add_program_desc": "Pick a common exercise from the curated legacy list and add it directly to this program. This does NOT add it to your personal exercise database.",
        "legacy_manage_panel": "🛠️ Add / Remove Legacy Exercises",
        "legacy_manage_desc": "Manage the shared legacy exercise list used by the panels above.",
        "legacy_new_name": "New Legacy Exercise Name",
        "legacy_add_to_list": "Add to Legacy List",
        "legacy_add_to_list_success": "added to the legacy list!",
        "legacy_delete_select": "Select Legacy Exercise to Delete",
        "legacy_delete_btn": "Delete from Legacy List",
        "legacy_delete_success": "deleted from the legacy list!",
        "app_name": "Workout",
        "app_tagline": "Track · Plan · Progress",
        "home_eyebrow": "Welcome",
        "home_sub": "Pick a group to continue or create a new one.",
        "group_eyebrow": "Group",
        "group_sub": "Choose a member to open their log.",
        "nav_groups": "👥 Group",
        "nav_programs": "📋 Program",
        "nav_stats": "📊 Stats",
        "day_workout": "Workout of the Day",
        "tools": "Tools",
        "exercises_short": "Exercises",
        "sets_short": "Sets",
        "volume_short": "Volume",
        "days_unit": "days",
        "min_unit": "min",
        "program_eyebrow": "Program",
        "tab_add_set": "➕ Add Set",
        "nav_log": "📝 Log",
        "tab_program": "📥 Program",
        "tab_legacy": "📚 Legacy",
        "tab_manage": "🛠️ Manage",
        "today": "Today",
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
        "export_all_csv": "📥 Tüm Geçmişi CSV Aktar",
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
        "nav_daily": "📝 Günlük",
        "calendar_legend": "▪ Antrenman günü · ■ Seçili gün",
        "legacy_add_panel": "📚 Temel Hareketten Bugüne Ekle",
        "legacy_add_desc": "Hazır temel hareket listesinden seçip doğrudan bugünün antrenmanına ekleyin. Bu işlem hareketi kişisel veritabanınıza (Hareketler) EKLEMEZ.",
        "legacy_select_group": "Kas Grubu",
        "legacy_empty": "Temel hareket listesi boş. Önce Google Sheets'teki 'LegacyHareketler' sekmesine hareket ekleyin.",
        "legacy_add_program_panel": "📚 Temel Hareketten Programa Ekle",
        "legacy_add_program_desc": "Hazır temel hareket listesinden seçip doğrudan bu programa ekleyin. Bu işlem hareketi kişisel veritabanınıza (Hareketler) EKLEMEZ.",
        "legacy_manage_panel": "🛠️ Temel Hareket Ekle / Sil",
        "legacy_manage_desc": "Yukarıdaki panellerde kullanılan ortak temel hareket listesine ekleme/çıkarma yapabilirsiniz.",
        "legacy_new_name": "Yeni Temel Hareketin Adı",
        "legacy_add_to_list": "Listeye Ekle",
        "legacy_add_to_list_success": "temel hareket listesine eklendi!",
        "legacy_delete_select": "Silinecek Temel Hareketi Seçin",
        "legacy_delete_btn": "Listeden Sil",
        "legacy_delete_success": "temel hareket listesinden silindi!",
        "app_name": "Workout",
        "app_tagline": "Takip · Plan · Gelişim",
        "home_eyebrow": "Hoş geldin",
        "home_sub": "Devam etmek için bir grup seç ya da yenisini oluştur.",
        "group_eyebrow": "Grup",
        "group_sub": "Günlüğünü açmak için bir üye seç.",
        "nav_groups": "👥 Grup",
        "nav_programs": "📋 Program",
        "nav_stats": "📊 İstatistik",
        "day_workout": "Günün Antrenmanı",
        "tools": "Araçlar",
        "exercises_short": "Hareket",
        "sets_short": "Set",
        "volume_short": "Hacim",
        "days_unit": "gün",
        "min_unit": "dk",
        "program_eyebrow": "Program",
        "tab_add_set": "➕ Set Ekle",
        "nav_log": "📝 Günlük",
        "tab_program": "📥 Program",
        "tab_legacy": "📚 Temel",
        "tab_manage": "🛠️ Yönet",
        "today": "Bugün",
    }
}

# --- KÜRESEL DEĞİŞKENLER ---
EKIPMAN_LISTESI = ["Barbell", "Dumbbell", "Machine", "Cable", "Bodyweight", "Band", "Smith Machine", "Kettlebell", "Plate Loaded", "Other", "-"]

# --- SAYFA YAPILANDIRMASI & ÖZEL MOBİL CSS ---
st.set_page_config(page_title="Workout App", page_icon="💪", layout="centered", initial_sidebar_state="collapsed")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500;600;700;800;900&display=swap');

    /* ===== TASARIM DEĞİŞKENLERİ — "Gym Poster" teması ===== */
    :root {
        --acc: #C8FF2E;          /* neon lime */
        --acc-dim: #9FD11A;
        --acc-soft: rgba(200, 255, 46, 0.12);
        --on-acc: #0A0A0B;
        --hot: #FF4D2E;          /* kardiyo / uyarı */
        --hot-soft: rgba(255, 77, 46, 0.14);
        --bg: #0A0A0B;
        --card: #121214;
        --card-2: #1A1A1D;
        --line: #26262B;
        --line-2: #35353C;
        --txt: #F4F4F0;
        --muted: #8C8C94;
        --danger: #FF4D5E;
        --r: 6px;
        --display: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif;
        --body: 'Archivo', 'Segoe UI', system-ui, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        font-family: var(--body);
        color: var(--txt);
        background-color: var(--bg);
        background-image:
            linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
        background-size: 28px 28px;
    }
    .stApp p, .stApp label, .stApp input, .stApp button, .stApp summary { font-family: var(--body); }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 7.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 760px;
    }
    hr { border-color: var(--line) !important; margin: 1.2rem 0 !important; }
    div[data-testid="stElementContainer"]:has(> div > div > style),
    div[data-testid="stElementContainer"]:has(iframe[title="streamlit.components.v1.html"]) { margin-bottom: -1rem; }

    /* Mobilde kolonlar alt alta düşmesin */
    div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.5rem !important; }
    div[data-testid="stColumn"] { min-width: 0 !important; }

    /* ===== ÜST BAR ===== */
    .brand { display: flex; align-items: center; gap: 10px; padding-top: 4px; }
    .brand-logo {
        width: 36px; height: 36px; border-radius: var(--r);
        display: grid; place-items: center; font-size: 1.1rem;
        background: var(--acc); transform: skewX(-8deg);
    }
    .brand-txt { font-family: var(--display); font-size: 1.45rem; letter-spacing: 0.04em; text-transform: uppercase; line-height: 1; }
    .brand-txt small { display: block; font-family: var(--body); font-size: 0.66rem; font-weight: 700; letter-spacing: 0.14em; color: var(--acc); margin-top: 3px; }

    /* ===== SAYFA BAŞLIKLARI ===== */
    .page-head { margin: 1rem 0 1.2rem 0; position: relative; }
    .page-head .ph-eyebrow {
        display: inline-block; font-size: 0.7rem; font-weight: 800; letter-spacing: 0.16em; text-transform: uppercase;
        color: var(--on-acc); background: var(--acc); padding: 3px 8px; border-radius: 3px; margin-bottom: 8px;
    }
    .page-head .ph-title {
        font-family: var(--display); font-weight: 400; text-transform: uppercase;
        font-size: 2.6rem; line-height: 1.02; letter-spacing: 0.01em; padding-top: 2px; color: var(--txt); word-break: break-word;
    }
    .page-head .ph-sub { font-size: 0.88rem; color: var(--muted); margin-top: 8px; font-weight: 500; }
    .page-head .ph-icon { display: none; }
    .page-head.small .ph-title { font-size: 1.9rem; }

    .section-label {
        display: flex; align-items: center; gap: 8px;
        font-size: 0.72rem; font-weight: 800; letter-spacing: 0.16em; text-transform: uppercase;
        color: var(--muted); margin: 0.1rem 0 0.5rem 0;
    }
    .section-label::before { content: ""; width: 14px; height: 3px; background: var(--acc); }
    .section-label .count { color: var(--acc); letter-spacing: 0; font-size: 0.8rem; }
    .subhead { font-weight: 800; font-size: 0.95rem; margin: 0.5rem 0 0.4rem 0; color: var(--txt); }

    /* ===== KARTLAR ===== */
    div[class*="st-key-card_"] {
        background: var(--card) !important;
        border: 1px solid var(--line) !important;
        border-radius: var(--r) !important;
    }

    /* ===== BUTONLAR ===== */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        min-height: 48px; border-radius: var(--r); font-weight: 800;
        transition: transform 0.12s ease, background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
    }
    div[data-testid="stButton"] > button p,
    div[data-testid="stDownloadButton"] > button p { white-space: normal; overflow: visible; text-overflow: clip; line-height: 1.25; }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--acc); border: none; color: var(--on-acc);
    }
    div[data-testid="stButton"] > button[kind="primary"] p { text-transform: uppercase; letter-spacing: 0.06em; }
    div[data-testid="stButton"] > button[kind="primary"]:hover { background: #D8FF66; color: var(--on-acc); }
    div[data-testid="stButton"] > button[kind="secondary"],
    div[data-testid="stDownloadButton"] > button {
        background: var(--card-2); border: 1px solid var(--line-2); color: var(--txt);
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover,
    div[data-testid="stDownloadButton"] > button:hover { border-color: var(--acc); color: var(--acc); }
    div[data-testid="stButton"] > button:active,
    div[data-testid="stDownloadButton"] > button:active { transform: scale(0.97); }

    /* Grup / üye kutucukları */
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button {
        min-height: 108px; align-items: flex-end; justify-content: flex-start;
        padding: 14px; text-align: left; position: relative; overflow: hidden;
        background: var(--card-2); border: 1px solid var(--line-2);
    }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button > div { justify-content: flex-start; width: 100%; }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button p {
        font-family: var(--display); font-weight: 400; font-size: 1.35rem; text-transform: uppercase; letter-spacing: 0.02em; line-height: 1.05; text-align: left;
    }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button::before {
        content: "↗"; position: absolute; top: 10px; right: 12px; font-size: 1.1rem; color: var(--muted);
    }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button::after {
        content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--acc); opacity: 0; transition: opacity .15s;
    }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button:hover { border-color: var(--acc); color: var(--txt); }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button:hover::after { opacity: 1; }
    div[class*="st-key-card_tiles"] div[data-testid="stButton"] > button:hover::before { color: var(--acc); }

    /* Program listesi satırları */
    div[class*="st-key-card_list"] div[data-testid="stButton"] > button {
        min-height: 58px; justify-content: flex-start; text-align: left; padding: 0 16px; position: relative;
    }
    div[class*="st-key-card_list"] div[data-testid="stButton"] > button > div { justify-content: flex-start; width: 100%; }
    div[class*="st-key-card_list"] div[data-testid="stButton"] > button p { font-size: 1rem; font-weight: 700; }
    div[class*="st-key-card_list"] div[data-testid="stButton"] > button::after {
        content: "→"; position: absolute; right: 16px; top: 50%; transform: translateY(-50%); color: var(--muted);
    }

    /* Geri butonları */
    div[class*="st-key-back_"] { margin-top: 8px; }
    div[class*="st-key-back_"] div[data-testid="stButton"] > button {
        min-height: 36px; width: auto !important; padding: 0 12px;
        background: transparent; border: 1px solid var(--line-2); color: var(--muted); font-weight: 700;
    }
    div[class*="st-key-back_"] div[data-testid="stButton"] > button p { font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.08em; }

    /* Satır silme (✕) */
    div[class*="st-key-d_"] button, div[class*="st-key-pd_"] button {
        min-height: 40px !important; padding: 0 !important; width: 100%;
        background: transparent !important; border: 1px solid var(--line-2) !important; color: var(--danger) !important;
    }
    div[class*="st-key-d_"] button:hover, div[class*="st-key-pd_"] button:hover { background: rgba(255,77,94,0.12) !important; border-color: var(--danger) !important; }
    div[class*="st-key-del_btn_"] button, div[class*="st-key-d_p_"] button {
        color: var(--danger) !important; border-color: rgba(255,77,94,0.4) !important; background: transparent !important;
    }

    /* ===== ALT SABİT MENÜ ===== */
    div.st-key-topnav {
        position: fixed; left: 0; right: 0; bottom: 0; z-index: 999;
        padding: 8px max(10px, calc((100vw - 760px) / 2 + 10px)) calc(8px + env(safe-area-inset-bottom));
        background: rgba(10, 10, 11, 0.92);
        backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
        border-top: 1px solid var(--line-2);
    }
    div.st-key-topnav div[data-testid="stHorizontalBlock"] { gap: 6px !important; }
    div.st-key-topnav div[data-testid="stButton"] > button {
        min-height: 52px; padding: 4px 2px; background: transparent; border: none; box-shadow: none !important; color: var(--muted);
    }
    div.st-key-topnav div[data-testid="stButton"] > button p { font-size: 0.74rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; white-space: normal; }
    div.st-key-topnav div[data-testid="stButton"] > button[kind="primary"] { background: var(--acc); color: var(--on-acc); }
    div.st-key-topnav div[data-testid="stButton"] > button[kind="secondary"]:hover { color: var(--txt); }

    /* ===== TARİH KARTI ===== */
    div.st-key-card_date {
        background: var(--acc) !important; border: none !important; border-radius: var(--r) !important;
        padding: 14px 16px 12px 16px; color: var(--on-acc);
    }
    .date-hero { display: flex; align-items: center; gap: 14px; }
    .date-hero .dh-day { font-family: var(--display); font-size: 4.2rem; line-height: 0.9; color: var(--on-acc); }
    .date-hero .dh-week { font-weight: 900; font-size: 1.05rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--on-acc); display: flex; align-items: center; gap: 8px; }
    .date-hero .dh-month { font-weight: 600; font-size: 0.9rem; color: rgba(10,10,11,0.7); }
    .today-tag { background: var(--on-acc); color: var(--acc); font-size: 0.62rem; padding: 2px 6px; border-radius: 3px; letter-spacing: 0.1em; }
    div.st-key-card_date [data-testid="stDateInput"] div[data-baseweb="input"],
    div.st-key-card_date [data-testid="stDateInput"] input {
        background: var(--on-acc) !important; color: var(--acc) !important; font-weight: 800; border-color: var(--on-acc) !important;
    }
    div.st-key-card_date [data-testid="stCaptionContainer"], div.st-key-card_date [data-testid="stCaptionContainer"] p { color: rgba(10,10,11,0.75) !important; font-weight: 600; }
    .day-chip {
        display: inline-grid; place-items: center; min-width: 32px; height: 32px; padding: 0 6px;
        margin: 3px 3px 0 0; border-radius: 4px; font-size: 0.85rem; font-weight: 800;
        background: rgba(10,10,11,0.14); color: var(--on-acc);
    }
    .day-chip.sel { background: var(--on-acc); color: var(--acc); }

    /* ===== SEKMELER ===== */
    div.st-key-tools_wrap { margin-top: 0.4rem; }
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 6px; border-bottom: none !important; overflow-x: auto; scrollbar-width: none; padding-bottom: 2px;
    }
    div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar { display: none; }
    div[data-testid="stTabs"] [role="tab"] {
        flex: 0 0 auto; height: 40px; padding: 0 14px !important; border-radius: var(--r);
        background: var(--card-2); border: 1px solid var(--line-2); margin: 0 !important;
    }
    div[data-testid="stTabs"] [role="tab"] p { font-weight: 800 !important; font-size: 0.85rem !important; }
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"] { background: var(--txt); border-color: var(--txt); }
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"] p { color: var(--on-acc) !important; }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"], div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }
    div[data-testid="stTabs"] [role="tabpanel"] {
        background: var(--card); border: 1px solid var(--line); border-radius: var(--r); padding: 14px 14px 16px 14px; margin-top: 8px;
    }

    /* ===== EXPANDER (antrenman kartları) ===== */
    div[data-testid="stExpander"] details {
        background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--acc);
        border-radius: var(--r); overflow: hidden;
    }
    div[data-testid="stExpander"] details[open] { border-color: var(--line-2); border-left-color: var(--acc); }
    div[data-testid="stExpander"] summary { padding: 0.9rem 1rem; font-weight: 600; }
    div[data-testid="stExpander"] summary:hover { color: var(--acc); }
    div[data-testid="stExpander"] summary p { font-size: 0.95rem; }
    div[data-testid="stExpander"] summary strong { font-weight: 900; color: var(--acc); }
    div[class*="st-key-card_"] div[data-testid="stExpander"] details { background: var(--card-2); }

    /* ===== FORM ===== */
    input, select { border-radius: var(--r) !important; }
    div[data-baseweb="input"], div[data-testid="stNumberInputContainer"] { border-radius: var(--r) !important; }
    div[data-testid="stNumberInput"] input { font-weight: 800; font-variant-numeric: tabular-nums; }
    label[data-testid="stWidgetLabel"] p { font-size: 0.72rem !important; color: var(--muted) !important; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }

    .set-pill {
        height: 40px; border-radius: var(--r); display: grid; place-items: center;
        background: var(--txt); color: var(--on-acc);
        font-family: var(--display); font-size: 1.15rem;
    }
    .set-pill.cardio { background: var(--hot); color: #fff; font-family: var(--body); }
    div[data-testid="stMarkdownContainer"]:has(.set-pill),
    div[data-testid="stMarkdownContainer"]:has(.col-head) { margin-bottom: 0 !important; }
    .col-head { font-size: 0.66rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); text-align: center; }

    .chip { display: inline-flex; align-items: center; gap: 6px; padding: 3px 9px; border-radius: 3px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }
    .chip.acc { background: var(--acc-soft); color: var(--acc); }
    .chip.ok { background: var(--hot-soft); color: var(--hot); }
    .chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0 6px 0; }

    /* ===== İSTATİSTİK KARTLARI ===== */
    .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin: 4px 0 12px 0; }
    .stat { background: var(--card-2); border: 1px solid var(--line-2); border-radius: var(--r); padding: 12px 14px; min-width: 0; }
    .stat .s-label { font-size: 0.66rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); }
    .stat .s-value { font-family: var(--display); font-size: 2.2rem; line-height: 1; margin-top: 6px; word-break: break-word; }
    .stat .s-value.small { font-family: var(--body); font-size: 1rem; font-weight: 900; text-transform: uppercase; line-height: 1.25; }
    .stat .s-unit { font-family: var(--body); font-size: 0.8rem; font-weight: 700; color: var(--muted); margin-left: 4px; }
    .stat.hl { background: var(--acc); border-color: var(--acc); }
    .stat.hl .s-label, .stat.hl .s-unit { color: rgba(10,10,11,0.65); }
    .stat.hl .s-value { color: var(--on-acc); }
    .summary-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 0 0 12px 0; }
    .summary-strip .s-value { font-size: 1.9rem; }

    div[data-testid="stAlert"] { border-radius: var(--r); }
    div[data-testid="stCaptionContainer"] { color: var(--muted); }

    @media (min-width: 700px) {
        .page-head .ph-title { font-size: 3.4rem; }
        .block-container { padding-top: 1.5rem; }
    }

    /* Dropdown / Selectbox'larda klavye ile serbest yazmayı ve mobil sanal klavyeyi engelleme */
    div[data-testid="stSelectbox"] input,
    .stSelectbox input,
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
        -webkit-user-select: none !important;
        user-select: none !important;
    }
    div[data-testid="stSelectbox"],
    .stSelectbox,
    div[data-baseweb="select"] {
        cursor: pointer !important;
    }
    iframe[title="streamlit.components.v1.html"] {
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        border: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Dropdown (selectbox) elemanlarında dokunulduğu an menüyü gecikmesiz açan, klavyeyi engelleyen hafif JS
components.html(
    """
    <script>
    function fixSelectboxesFast() {
        try {
            const parentDoc = window.parent.document;
            if (!parentDoc) return;
            const selectInputs = parentDoc.querySelectorAll('div[data-testid="stSelectbox"] input, .stSelectbox input, div[data-baseweb="select"] input');
            for (let i = 0; i < selectInputs.length; i++) {
                const input = selectInputs[i];
                if (input.getAttribute('inputmode') !== 'none') {
                    input.setAttribute('inputmode', 'none');
                    input.style.caretColor = 'transparent';
                    input.style.cursor = 'pointer';
                    // Bilgisayarda harf yazmayı engelle, yön tuşları/Enter/Tab/Esc serbest kalsın
                    input.addEventListener('keydown', function(e) {
                        if (!['Tab', 'Escape', 'ArrowDown', 'ArrowUp', 'Enter'].includes(e.key)) {
                            e.preventDefault();
                        }
                    });
                }
            }
        } catch (e) {}
    }

    fixSelectboxesFast();

    try {
        const parentDoc = window.parent.document;
        if (parentDoc && !window.selectObserverInitialized) {
            window.selectObserverInitialized = true;
            
            // Dokunma/odak anında gecikmesiz klavye engeli
            parentDoc.addEventListener('focusin', function(e) {
                if (e.target && e.target.matches && e.target.matches('div[data-testid="stSelectbox"] input, .stSelectbox input, div[data-baseweb="select"] input')) {
                    if (e.target.getAttribute('inputmode') !== 'none') {
                        e.target.setAttribute('inputmode', 'none');
                    }
                }
            }, true);

            const observer = new MutationObserver(() => {
                fixSelectboxesFast();
            });
            observer.observe(parentDoc.body, { childList: true, subtree: true });
        }
    } catch (e) {}
    </script>
    """,
    height=0,
    width=0,
)

# Üst bar: solda uygulama logosu, sağda küçük dil seçici
bos_kolon, dil_kolonu = st.columns([2.2, 1], vertical_alignment="center")
with dil_kolonu:
    secilen_dil = st.selectbox("🌐 Dil", ["Türkçe", "English"], index=1, label_visibility="collapsed")
t = LANG[secilen_dil]
with bos_kolon:
    st.markdown(
        f"<div class='brand'><div class='brand-logo'>💪</div><div class='brand-txt'>{t['app_name']}<small>{t['app_tagline']}</small></div></div>",
        unsafe_allow_html=True,
    )

# --- ARAYÜZ YARDIMCILARI (sadece görünüm) ---
def _e(x):
    return html.escape(str(x))

def buyuk(x):
    # Türkçe uyumlu büyük harf (i -> İ, ı -> I)
    x = str(x)
    if secilen_dil == "Türkçe":
        x = x.replace("i", "İ").replace("ı", "I")
    return x.upper()

def page_header(title, icon="", subtitle=None, eyebrow=None, soft=False):
    icon_html = f"<div class='ph-icon{' soft' if soft else ''}'>{icon}</div>" if icon else ""
    eyebrow_html = f"<div class='ph-eyebrow'>{_e(eyebrow)}</div>" if eyebrow else ""
    sub_html = f"<div class='ph-sub'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"<div class='page-head'>{icon_html}<div>{eyebrow_html}<div class='ph-title'>{_e(buyuk(title))}</div>{sub_html}</div></div>", unsafe_allow_html=True)

def section_label(text, count=None):
    count_html = f"<span class='count'>{count}</span>" if count is not None else ""
    st.markdown(f"<div class='section-label'>{text}{count_html}</div>", unsafe_allow_html=True)

def subhead(text):
    st.markdown(f"<div class='subhead'>{text}</div>", unsafe_allow_html=True)

def set_pill(col, n, cardio=False):
    col.markdown(f"<div class='set-pill{' cardio' if cardio else ''}'>{n}</div>", unsafe_allow_html=True)

def set_table_header(ratios, labels):
    cols = st.columns(ratios)
    for c, lbl in zip(cols, labels):
        c.markdown(f"<div class='col-head'>{lbl}</div>", unsafe_allow_html=True)

def mechanic_chip(mekanik):
    cls = "ok" if mekanik == "Kardiyo" else "acc"
    st.markdown(f"<div class='chip-row'><span class='chip {cls}'>{t['mechanic']}: {_e(mekanik)}</span></div>", unsafe_allow_html=True)

def initials(name):
    parts = str(name).split()
    return _e("".join(p[0] for p in parts[:2]).upper() or "?")

GRAFIK_RENGI = "#C8FF2E"

def date_hero(d):
    gunler_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    aylar_tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gun_adi = gunler_tr[d.weekday()] if secilen_dil == "Türkçe" else cal_module.day_name[d.weekday()]
    ay_adi = aylar_tr[d.month - 1] if secilen_dil == "Türkçe" else cal_module.month_name[d.month]
    bugun = f"<span class='today-tag'>{t['today']}</span>" if d == date.today() else ""
    st.markdown(
        f"<div class='date-hero'><div class='dh-day'>{d.day:02d}</div>"
        f"<div class='dh-meta'><div class='dh-week'>{gun_adi} {bugun}</div><div class='dh-month'>{ay_adi} {d.year}</div></div></div>",
        unsafe_allow_html=True,
    )

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
if 'secili_tarih_widget' not in st.session_state: st.session_state.secili_tarih_widget = date.today()
if 'leg_onceki_hareket' not in st.session_state: st.session_state.leg_onceki_hareket = ""
if 'leg_sablon_w' not in st.session_state: st.session_state.leg_sablon_w = 0.0
if 'leg_sablon_r' not in st.session_state: st.session_state.leg_sablon_r = 10
if 'pleg_onceki_hareket' not in st.session_state: st.session_state.pleg_onceki_hareket = ""
if 'pleg_sablon_w' not in st.session_state: st.session_state.pleg_sablon_w = 0.0
if 'pleg_sablon_r' not in st.session_state: st.session_state.pleg_sablon_r = 10

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

def leg_sablon_guncelle():
    yeni_w = st.session_state.leg_sablon_w
    yeni_r = st.session_state.leg_sablon_r
    for key in list(st.session_state.keys()):
        if key.startswith("leg_w_new_"): st.session_state[key] = yeni_w
        elif key.startswith("leg_r_new_"): st.session_state[key] = yeni_r

def pleg_sablon_guncelle():
    yeni_w = st.session_state.pleg_sablon_w
    yeni_r = st.session_state.pleg_sablon_r
    for key in list(st.session_state.keys()):
        if key.startswith("pleg_w_new_"): st.session_state[key] = yeni_w
        elif key.startswith("pleg_r_new_"): st.session_state[key] = yeni_r

# Ortak Navigasyon Barı (mobilde ekranın altına sabitlenen tab bar)
def render_top_nav():
    with st.container(key="topnav"):
        n1, n2, n3, n4 = st.columns(4)
        with n1:
            if st.button(t["nav_groups"], key="nav_groups_btn", use_container_width=True):
                st.session_state.sayfa = 'grup_sayfasi'
                st.rerun()
        with n2:
            if st.button(t["nav_log"], key="nav_daily_btn", type="primary" if st.session_state.sayfa == 'kisi_sayfasi' else "secondary", use_container_width=True):
                st.session_state.sayfa = 'kisi_sayfasi'
                st.rerun()
        with n3:
            if st.button(t["nav_programs"], key="nav_prog_btn", type="primary" if st.session_state.sayfa == 'program_sayfasi' else "secondary", use_container_width=True):
                st.session_state.sayfa = 'program_sayfasi'
                st.rerun()
        with n4:
            if st.button(t["nav_stats"], key="nav_stats_btn", type="primary" if st.session_state.sayfa == 'istatistik_sayfasi' else "secondary", use_container_width=True):
                st.session_state.sayfa = 'istatistik_sayfasi'
                st.rerun()

# Antrenman Günlerini İşaretleyen Takvim Widget'ı
# NOT: Özel buton-grid takvimi mobilde bazı cihaz/tarayıcılarda hâlâ büyük/dikey
# görünebiliyordu. Bunun yerine tarayıcının kendi native date picker'ını (st.date_input)
# kullanıyoruz — bu, mobilde garanti şekilde kompakt bir popup olarak açılır.
# Antrenman yapılan günler ise altında küçük bir etiket listesi halinde gösteriliyor.
def antrenman_takvimi_ciz(df_antrenmanlar, kullanici, grup):
    kisi_df = df_antrenmanlar[(df_antrenmanlar['Kullanıcı'] == kullanici) & (df_antrenmanlar['Grup'] == grup)].copy()
    kisi_df['Tarih'] = pd.to_datetime(kisi_df['Tarih'], errors='coerce')
    antrenman_gunleri = set(kisi_df['Tarih'].dt.date.dropna())

    secili = st.session_state["secili_tarih_widget"]

    yeni_tarih = st.date_input(
        t["date"],
        value=secili,
        format="DD/MM/YYYY",
        key="takvim_date_input",
        label_visibility="collapsed",
    )
    if yeni_tarih != secili:
        st.session_state["secili_tarih_widget"] = yeni_tarih
        st.rerun()

    ay_isimleri_tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    ay_adi = ay_isimleri_tr[yeni_tarih.month - 1] if secilen_dil == "Türkçe" else cal_module.month_name[yeni_tarih.month]

    ay_gunleri = sorted(g.day for g in antrenman_gunleri if g.year == yeni_tarih.year and g.month == yeni_tarih.month)
    if ay_gunleri:
        gun_etiketleri = "".join(
            f"<span class='day-chip{' sel' if g == yeni_tarih.day else ''}'>{g}</span>"
            for g in ay_gunleri
        )
        st.markdown(f"<div style='margin-top:6px;'>{gun_etiketleri}</div>", unsafe_allow_html=True)
    st.caption(f"{ay_adi} {yeni_tarih.year} · {t['calendar_legend']}")

    return yeni_tarih


# --- SAYFA 1: ANA SAYFA (GRUPLAR) ---
if st.session_state.sayfa == 'ana_sayfa':
    df_gruplar = veri_getir("Gruplar", ["Grup Adı"])
    page_header(t['groups_title'].replace("🏋️‍♂️", "").strip(), icon="🏋️", subtitle=t['home_sub'], eyebrow=t['home_eyebrow'])
    
    with st.container(border=True, key="card_tiles_groups"):
        section_label(t['existing_groups'], len(df_gruplar) if not df_gruplar.empty else None)
        if not df_gruplar.empty:
            _grid = st.columns(2)
            for _i, (index, row) in enumerate(df_gruplar.iterrows()):
                with _grid[_i % 2]:
                    if st.button(buyuk(row['Grup Adı']), key=f"grp_tile_{index}", use_container_width=True):
                        st.session_state.secili_grup = row['Grup Adı']
                        st.session_state.sayfa = 'grup_sayfasi'
                        st.rerun()
        else:
            st.info(t["no_group"])
            
    with st.container(border=True, key="card_new_group"):
        section_label(f"➕ {t['new_group']}")
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
    with st.container(key="back_groups"):
        if st.button(t["back_to_groups"], use_container_width=True):
            st.session_state.sayfa = 'ana_sayfa'
            st.rerun()
    page_header(st.session_state.secili_grup, icon="👥", subtitle=t['group_sub'], eyebrow=t['group_eyebrow'])
        
    with st.container(border=True, key="card_tiles_members"):
        grup_uyeleri = df_kullanicilar[df_kullanicilar['Grup Adı'] == st.session_state.secili_grup]
        section_label(t['members'], len(grup_uyeleri) if not grup_uyeleri.empty else None)
        
        if not grup_uyeleri.empty:
            _grid = st.columns(2)
            for _i, (index, row) in enumerate(grup_uyeleri.iterrows()):
                with _grid[_i % 2]:
                    if st.button(buyuk(row['Kullanıcı Adı']), key=f"usr_tile_{index}", use_container_width=True):
                        st.session_state.secili_kisi = row['Kullanıcı Adı']
                        st.session_state.sayfa = 'kisi_sayfasi'
                        st.rerun()
        else:
            st.info(t["no_member"])
            
    with st.container(border=True, key="card_new_member"):
        section_label(f"➕ {t['new_member']}")
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
    page_header(st.session_state.secili_kisi, icon=initials(st.session_state.secili_kisi), subtitle=f"👥 {_e(st.session_state.secili_grup)}", eyebrow=t['daily_log'])
    
    df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Süre (dk)", "Kalori", "Mekanik", "Ekipman"])
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik", "Ekipman"])
    df_programlar = veri_getir("Programlar", ["Kullanıcı", "Program Adı"])
    df_program_detay = veri_getir("ProgramDetay", ["Program Adı", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Ekipman"])
    df_legacy = veri_getir("LegacyHareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik", "Ekipman"])
    
    # NOT: Aynı hareket ismi farklı ekipmanlarla ayrı kayıtlar olarak değerlendirilsin diye
    # grafik fonksiyonu artık ekipman bilgisini de dikkate alıyor.
    def grafik_ciz(hareket_adi, ekipman_adi=None):
        gecmis_tum_setler = df_antrenmanlar[
            (df_antrenmanlar['Grup'] == st.session_state.secili_grup) &
            (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) &
            (df_antrenmanlar['Hareket'] == hareket_adi)
        ].copy()
        if ekipman_adi is not None and 'Ekipman' in gecmis_tum_setler.columns:
            gecmis_tum_setler = gecmis_tum_setler[gecmis_tum_setler['Ekipman'] == ekipman_adi]
        if not gecmis_tum_setler.empty:
            gecmis_tum_setler['Tarih'] = pd.to_datetime(gecmis_tum_setler['Tarih'])
            grafik_verisi = gecmis_tum_setler.groupby('Tarih')['Ağırlık'].max().reset_index().sort_values(by='Tarih')
            grafik_verisi['Tarih'] = grafik_verisi['Tarih'].dt.strftime('%d/%m/%Y')
            grafik_verisi.set_index('Tarih', inplace=True)
            st.line_chart(grafik_verisi['Ağırlık'].astype(float), color=GRAFIK_RENGI)
        else:
            st.info(t["no_chart_data"])

    # Tarih kartı: büyük tarih göstergesi + tarih seçici her zaman görünür
    with st.container(key="card_date"):
        date_hero(st.session_state["secili_tarih_widget"])
        antrenman_takvimi_ciz(df_antrenmanlar, st.session_state.secili_kisi, st.session_state.secili_grup)
    secili_tarih = st.session_state["secili_tarih_widget"]

    # Eski açılır paneller yerine sekmeli araç kutusu
    with st.container(key="tools_wrap"):
        tab_set, tab_prog, tab_leg, tab_mng = st.tabs([t["tab_add_set"], t["tab_program"], t["tab_legacy"], t["tab_manage"]])

        with tab_prog:
            subhead(t["load_program_panel"])
            kisi_programlari_yukle = df_programlar[df_programlar['Kullanıcı'] == st.session_state.secili_kisi]
            if kisi_programlari_yukle.empty:
                st.info(t["no_program"])
            else:
                secili_program_yukle = st.selectbox(t["select_program"], kisi_programlari_yukle['Program Adı'].unique(), key="program_yukle_secim")
                program_icerik_yukle = df_program_detay[(df_program_detay['Program Adı'] == secili_program_yukle) & (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi)].sort_values(by=["Hareket", "Set"])

                if program_icerik_yukle.empty:
                    st.info(t["no_program_content"])
                else:
                    subhead(t['program_preview'])
                    yuklenecek_setler_l = []
                    # Program içeriğini artık (Hareket, Ekipman) ikilisine göre gruplandırıyoruz
                    program_icerik_yukle = program_icerik_yukle.copy()
                    program_icerik_yukle['_grp_l'] = list(zip(program_icerik_yukle['Hareket'], program_icerik_yukle.get('Ekipman', '-')))
                    for grp_l in program_icerik_yukle['_grp_l'].unique():
                        hareket_l, ekipman_grp_l = grp_l
                        hareket_setleri_l = program_icerik_yukle[program_icerik_yukle['_grp_l'] == grp_l]
                        kas_grubu_l = hareket_setleri_l.iloc[0]['Kas Grubu']
                        ekipman_l = hareket_setleri_l.iloc[0]['Ekipman'] if 'Ekipman' in hareket_setleri_l.columns else "-"
                        st.markdown(f"💪 **{ekipman_l} {kas_grubu_l} {hareket_l}**".replace("- ", "").strip())
                        set_table_header([0.7, 2, 2], [t["set"], "kg", t["reps"]])

                        for p_idx, p_row in hareket_setleri_l.iterrows():
                            cLabel, cW, cR = st.columns([0.7, 2, 2], vertical_alignment="center")
                            set_pill(cLabel, int(p_row['Set']))
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
                        # Set numaralandırma artık (Hareket, Ekipman) ikilisine göre yapılıyor
                        hareket_sayaclari = {}
                        for satir in yuklenecek_setler_l:
                            hareket_adi_l = satir["Hareket"]
                            ekipman_l2 = satir["Ekipman"]
                            anahtar_l = (hareket_adi_l, ekipman_l2)
                            if anahtar_l not in hareket_sayaclari:
                                hareket_sayaclari[anahtar_l] = len(df_antrenmanlar[(df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == hareket_adi_l) & (df_antrenmanlar['Ekipman'] == ekipman_l2)]) + 1
                            tum_yeni_setler.append({"Tarih": secili_tarih.strftime("%Y-%m-%d"), "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": satir["Kas Grubu"], "Hareket": hareket_adi_l, "Set": hareket_sayaclari[anahtar_l], "Ağırlık": satir["Ağırlık"], "Tekrar": satir["Tekrar"], "Süre (dk)": 0, "Kalori": 0, "Mekanik": hareket_mekanik_sozlugu.get(hareket_adi_l, "Compound"), "Ekipman": ekipman_l2})
                            hareket_sayaclari[anahtar_l] += 1
                        conn.update(worksheet="Antrenmanlar", data=pd.concat([df_antrenmanlar, pd.DataFrame(tum_yeni_setler)], ignore_index=True))
                        st.cache_data.clear()
                        for key in list(st.session_state.keys()):
                            if key.startswith("load_w_") or key.startswith("load_r_"): del st.session_state[key]
                        st.success(f"{secili_program_yukle} {t['success_load_program']}")
                        st.rerun()

        # --- LEGACY HAREKETTEN BUGÜNE DİREKT EKLE ---
        with tab_leg:
            subhead(t["legacy_add_panel"])
            st.caption(t["legacy_add_desc"])
            if df_legacy.empty:
                st.info(t["legacy_empty"])
            else:
                leg_kas = st.selectbox(t["legacy_select_group"], df_legacy['Kas Grubu'].unique(), key="leg_kas_sec")
                leg_liste = df_legacy[df_legacy['Kas Grubu'] == leg_kas]['Hareket Tipi'].unique()
                leg_hareket = st.selectbox(t["exercise"], leg_liste, key="leg_hareket_sec")

                if leg_hareket:
                    leg_row = df_legacy[(df_legacy['Kas Grubu'] == leg_kas) & (df_legacy['Hareket Tipi'] == leg_hareket)].iloc[0]
                    leg_mekanik = leg_row['Mekanik']
                    mechanic_chip(leg_mekanik)

                    leg_varsayilan_ekip = leg_row['Ekipman'] if 'Ekipman' in leg_row else "Barbell"
                    if st.session_state.get("_aktif_leg_hareket") != leg_hareket:
                        st.session_state["_aktif_leg_hareket"] = leg_hareket
                        if leg_varsayilan_ekip in EKIPMAN_LISTESI:
                            st.session_state["leg_ekip_sec"] = leg_varsayilan_ekip
                    leg_ekipman = st.selectbox(t["equipment"], EKIPMAN_LISTESI, index=EKIPMAN_LISTESI.index(leg_varsayilan_ekip) if leg_varsayilan_ekip in EKIPMAN_LISTESI else 0, key="leg_ekip_sec")

                    # Şablon/önceki ağırlık takibi Hareket+Ekipman ikilisine göre tetikleniyor
                    leg_onceki_anahtar = f"{leg_hareket}||{leg_ekipman}"
                    if st.session_state.leg_onceki_hareket != leg_onceki_anahtar:
                        st.session_state.leg_onceki_hareket = leg_onceki_anahtar
                        leg_gecmis = df_antrenmanlar[(df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == leg_hareket) & (df_antrenmanlar['Ekipman'] == leg_ekipman) & (df_antrenmanlar['Mekanik'] != 'Kardiyo')]
                        st.session_state.leg_sablon_w = float(leg_gecmis.sort_values(by="Tarih", ascending=False).iloc[0]['Ağırlık']) if not leg_gecmis.empty else 0.0
                        st.session_state.leg_sablon_r = 10
                        for key in list(st.session_state.keys()):
                            if key.startswith("leg_w_new_") or key.startswith("leg_r_new_"): del st.session_state[key]

                    st.divider()

                    if leg_mekanik == "Kardiyo":
                        subhead(t['cardio_details'])
                        def leg_kalori_hesapla(): st.session_state.leg_kardiyo_kalori = int(st.session_state.leg_kardiyo_sure * 10)
                        if 'leg_kardiyo_sure' not in st.session_state: st.session_state.leg_kardiyo_sure = 30
                        if 'leg_kardiyo_kalori' not in st.session_state: st.session_state.leg_kardiyo_kalori = 300
                        lc_sure, lc_kalori = st.columns(2)
                        leg_kardiyo_sure = lc_sure.number_input(t["duration"], min_value=1, value=st.session_state.leg_kardiyo_sure, key="leg_kardiyo_sure", step=1, on_change=leg_kalori_hesapla)
                        leg_kardiyo_kalori = lc_kalori.number_input(t["calories"], min_value=1, value=st.session_state.leg_kardiyo_kalori, key="leg_kardiyo_kalori", step=10)

                        if st.button(t["save_cardio"], type="primary", use_container_width=True, key="leg_save_cardio_btn"):
                            leg_yeni_satir = pd.DataFrame([{"Tarih": secili_tarih.strftime("%Y-%m-%d"), "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": leg_kas, "Hareket": leg_hareket, "Set": 1, "Ağırlık": 0, "Tekrar": 0, "Süre (dk)": leg_kardiyo_sure, "Kalori": leg_kardiyo_kalori, "Mekanik": leg_mekanik, "Ekipman": leg_ekipman}])
                            conn.update(worksheet="Antrenmanlar", data=pd.concat([df_antrenmanlar, leg_yeni_satir], ignore_index=True))
                            st.cache_data.clear()
                            st.success(f"{leg_hareket} {t['success_cardio']}")
                            st.rerun()
                    else:
                        subhead(t['template_title'])
                        leg_set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1, key="leg_set_sayisi")
                        lc_hedef1, lc_hedef2 = st.columns(2)
                        lc_hedef1.number_input(t["template_w"], step=2.5, key="leg_sablon_w", on_change=leg_sablon_guncelle)
                        lc_hedef2.number_input(t["template_r"], step=1, key="leg_sablon_r", on_change=leg_sablon_guncelle)

                        subhead(t['edit_sets'])
                        set_table_header([0.7, 2, 2], [t["set"], "kg", t["reps"]])
                        leg_bugunku_setler = df_antrenmanlar[(df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == leg_hareket) & (df_antrenmanlar['Ekipman'] == leg_ekipman)]
                        leg_baslangic_seti = len(leg_bugunku_setler) + 1
                        leg_eklenecek_setler = []

                        for i in range(leg_set_sayisi):
                            leg_guncel_set_no = leg_baslangic_seti + i
                            lc_label, lc_w, lc_r = st.columns([0.7, 2, 2], vertical_alignment="center")
                            set_pill(lc_label, leg_guncel_set_no)
                            leg_w_key, leg_r_key = f"leg_w_new_{leg_hareket}_{leg_ekipman}_{leg_guncel_set_no}", f"leg_r_new_{leg_hareket}_{leg_ekipman}_{leg_guncel_set_no}"
                            if leg_w_key not in st.session_state: st.session_state[leg_w_key] = st.session_state.leg_sablon_w
                            if leg_r_key not in st.session_state: st.session_state[leg_r_key] = st.session_state.leg_sablon_r
                            leg_w = lc_w.number_input(t["weight"], step=2.5, key=leg_w_key, label_visibility="collapsed")
                            leg_r = lc_r.number_input(t["reps"], step=1, key=leg_r_key, label_visibility="collapsed")
                            leg_eklenecek_setler.append({"Tarih": secili_tarih.strftime("%Y-%m-%d"), "Grup": st.session_state.secili_grup, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": leg_kas, "Hareket": leg_hareket, "Set": leg_guncel_set_no, "Ağırlık": leg_w, "Tekrar": leg_r, "Süre (dk)": 0, "Kalori": 0, "Mekanik": leg_mekanik, "Ekipman": leg_ekipman})

                        if st.button(t["save_all"], type="primary", use_container_width=True, key="leg_save_all_btn"):
                            conn.update(worksheet="Antrenmanlar", data=pd.concat([df_antrenmanlar, pd.DataFrame(leg_eklenecek_setler)], ignore_index=True))
                            st.cache_data.clear()
                            for key in list(st.session_state.keys()):
                                if key.startswith("leg_w_new_") or key.startswith("leg_r_new_"): del st.session_state[key]
                            st.success(f"{leg_hareket}: {leg_set_sayisi} {t['success_sets']}")
                            st.rerun()

        # --- TEMEL HAREKET LİSTESİNİ YÖNET (EKLE/SİL) ---
        with tab_mng:
            subhead(t["legacy_manage_panel"])
            st.caption(t["legacy_manage_desc"])
            mevcut_kas_gruplari_legacy = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Shoulder", "Biceps", "Triceps", "Legs", "Cardio"]
            lc_kas, lc_har = st.columns(2)
            lc_mek, lc_ekip = st.columns(2)
            lc_yeni_kas = lc_kas.selectbox(t["which_muscle"], mevcut_kas_gruplari_legacy, key="legacy_new_muscle")
            lc_yeni_har = lc_har.text_input(t["legacy_new_name"], key="legacy_new_name_input")
            lc_yeni_mek = lc_mek.selectbox(t["mechanic_type"], ["Compound", "Izole", "Kardiyo"], key="legacy_new_mek")
            lc_yeni_ekip = lc_ekip.selectbox(t["equipment_type"], EKIPMAN_LISTESI, key="legacy_new_ekip")
            if st.button(t["legacy_add_to_list"], type="secondary", use_container_width=True, key="legacy_add_list_btn"):
                if lc_yeni_har:
                    conn.update(worksheet="LegacyHareketler", data=pd.concat([df_legacy, pd.DataFrame([{"Kas Grubu": lc_yeni_kas, "Hareket Tipi": lc_yeni_har, "Mekanik": lc_yeni_mek, "Ekipman": lc_yeni_ekip}])], ignore_index=True))
                    st.cache_data.clear()
                    st.success(f"{lc_yeni_har} {t['legacy_add_to_list_success']}")
                    st.rerun()
                else:
                    st.warning(t["warn_name"])

            if not df_legacy.empty:
                st.divider()
                lc_sil_secim = st.selectbox(t["legacy_delete_select"], df_legacy['Hareket Tipi'].unique(), key="legacy_sil_sec")
                if st.button(t["legacy_delete_btn"], type="secondary", use_container_width=True, key="legacy_del_btn"):
                    conn.update(worksheet="LegacyHareketler", data=df_legacy[df_legacy['Hareket Tipi'] != lc_sil_secim])
                    st.cache_data.clear()
                    st.success(f"{lc_sil_secim} {t['legacy_delete_success']}")
                    st.rerun()

    with tab_set:
        col1, col2 = st.columns(2)
        mevcut_kas_gruplari = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Shoulder", "Biceps", "Triceps", "Legs", "Cardio"]
        with col1: secili_kas = st.selectbox(t["muscle_group"], mevcut_kas_gruplari)
        
        filtrelenmis_df = df_hareketler[df_hareketler['Kas Grubu'] == secili_kas]
        hareket_listesi = filtrelenmis_df['Hareket Tipi'].unique() if not filtrelenmis_df.empty else []
        with col2: secili_hareket = st.selectbox(t["exercise"], hareket_listesi)

        if secili_hareket:
            mekanik_degeri = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Mekanik'].values[0]
            mechanic_chip(mekanik_degeri)
            
            veritabanindaki_ekipman = filtrelenmis_df[filtrelenmis_df['Hareket Tipi'] == secili_hareket]['Ekipman'].values[0] if 'Ekipman' in filtrelenmis_df.columns else "Barbell"
            if st.session_state.get("_aktif_gunluk_hareket") != secili_hareket:
                st.session_state["_aktif_gunluk_hareket"] = secili_hareket
                if veritabanindaki_ekipman in EKIPMAN_LISTESI:
                    st.session_state["gunluk_ekipman_sec"] = veritabanindaki_ekipman
            secili_ekipman = st.selectbox(t["equipment"], EKIPMAN_LISTESI, index=EKIPMAN_LISTESI.index(veritabanindaki_ekipman) if veritabanindaki_ekipman in EKIPMAN_LISTESI else 0, key="gunluk_ekipman_sec")

            # Şablon/önceki ağırlık takibi artık Hareket+Ekipman ikilisine göre tetikleniyor,
            # böylece aynı hareketi farklı ekipmanla seçtiğinizde önceki ağırlık o ekipmana ait olan gelir.
            onceki_anahtar = f"{secili_hareket}||{secili_ekipman}"
            if st.session_state.onceki_hareket != onceki_anahtar:
                st.session_state.onceki_hareket = onceki_anahtar
                gecmis_hareket = df_antrenmanlar[(df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == secili_hareket) & (df_antrenmanlar['Ekipman'] == secili_ekipman) & (df_antrenmanlar['Mekanik'] != 'Kardiyo')]
                st.session_state.sablon_w = float(gecmis_hareket.sort_values(by="Tarih", ascending=False).iloc[0]['Ağırlık']) if not gecmis_hareket.empty else 0.0
                st.session_state.sablon_r = 10
                for key in list(st.session_state.keys()):
                    if key.startswith("w_new_") or key.startswith("r_new_"): del st.session_state[key]
            
            st.divider()
            
            if mekanik_degeri == "Kardiyo":
                subhead(t['cardio_details'])
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
                subhead(t['template_title'])
                set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1)
                c_hedef1, c_hedef2 = st.columns(2)
                c_hedef1.number_input(t["template_w"], step=2.5, key="sablon_w", on_change=sablon_guncelle)
                c_hedef2.number_input(t["template_r"], step=1, key="sablon_r", on_change=sablon_guncelle)
                
                subhead(t['edit_sets'])
                set_table_header([0.7, 2, 2], [t["set"], "kg", t["reps"]])
                # Bugünkü set sayısı artık Hareket+Ekipman ikilisine göre hesaplanıyor
                bugunku_setler = df_antrenmanlar[(df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d")) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Hareket'] == secili_hareket) & (df_antrenmanlar['Ekipman'] == secili_ekipman)]
                baslangic_seti = len(bugunku_setler) + 1
                eklenecek_setler = []
                
                for i in range(set_sayisi):
                    guncel_set_no = baslangic_seti + i
                    c_label, c_w, c_r = st.columns([0.7, 2, 2], vertical_alignment="center")
                    set_pill(c_label, guncel_set_no)
                    w_key, r_key = f"w_new_{secili_hareket}_{secili_ekipman}_{guncel_set_no}", f"r_new_{secili_hareket}_{secili_ekipman}_{guncel_set_no}"
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

        if 'yeni_hareket_panel_acik' not in st.session_state: st.session_state.yeni_hareket_panel_acik = False
        with st.container(border=True):
            hcol1, hcol2 = st.columns([5, 1])
            hcol1.markdown(f"**{t['new_exercise_panel']}**")
            if hcol2.button("🔽" if not st.session_state.yeni_hareket_panel_acik else "🔼", key="toggle_yeni_hareket", use_container_width=True):
                st.session_state.yeni_hareket_panel_acik = not st.session_state.yeni_hareket_panel_acik
                st.rerun()
            if st.session_state.yeni_hareket_panel_acik:
                st.caption(t["new_exercise_desc"])
                c_kas, c_har = st.columns(2)
                c_mek, c_ekip = st.columns(2)
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
    page_header(t['day_workout'], icon="📋", subtitle=f"📅 {secili_tarih.strftime('%d/%m/%Y')}", soft=True)
    
    gunluk_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi) & (df_antrenmanlar['Tarih'] == secili_tarih.strftime("%Y-%m-%d"))]
    kisi_tum_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi)].copy()
    if not kisi_tum_gecmis.empty:
        kisi_tum_gecmis['Tarih_sirala'] = pd.to_datetime(kisi_tum_gecmis['Tarih'], errors='coerce')
        kisi_tum_gecmis = kisi_tum_gecmis.sort_values(by=['Tarih_sirala', 'Set'], ascending=[False, True]).drop(columns=['Tarih_sirala'], errors='ignore')

    if not gunluk_gecmis.empty:
        # CSV verisi kartlar çizilmeden önce hazırlanır (indirme butonları sayfanın altında gösterilir)
        gunluk_csv_verisi = gunluk_gecmis.to_csv(index=False).encode('utf-8-sig')

        # Günün kısa özeti (sadece görüntüleme)
        _ozet_df = gunluk_gecmis[gunluk_gecmis['Mekanik'] != 'Kardiyo']
        _hacim = float((pd.to_numeric(_ozet_df['Ağırlık'], errors='coerce').fillna(0) * pd.to_numeric(_ozet_df['Tekrar'], errors='coerce').fillna(0)).sum())
        _hareket_sayisi = len(set(zip(gunluk_gecmis['Hareket'], gunluk_gecmis.get('Ekipman', '-'))))
        st.markdown(
            f"<div class='summary-strip'>"
            f"<div class='stat'><div class='s-label'>{t['exercises_short']}</div><div class='s-value'>{_hareket_sayisi}</div></div>"
            f"<div class='stat'><div class='s-label'>{t['sets_short']}</div><div class='s-value'>{len(_ozet_df)}</div></div>"
            f"<div class='stat hl'><div class='s-label'>{t['volume_short']}</div><div class='s-value'>{_hacim:,.0f}<span class='s-unit'>kg</span></div></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Günlük kayıtları artık (Hareket, Ekipman) ikilisine göre gruplandırıyoruz.
        # Bu sayede "Barbell Horizontal Press" ile "Dumbbell Horizontal Press" ayrı kartlarda görünür.
        gunluk_gecmis = gunluk_gecmis.copy()
        gunluk_gecmis['_grp'] = list(zip(gunluk_gecmis['Hareket'], gunluk_gecmis.get('Ekipman', '-')))

        for grp_key in gunluk_gecmis['_grp'].unique():
            hareket, ekipman_grp = grp_key
            hareket_setleri = gunluk_gecmis[gunluk_gecmis['_grp'] == grp_key].sort_values(by="Set")
            ilk = hareket_setleri.iloc[0]
            tam_adi = f"{ilk.get('Ekipman','-')} {ilk['Kas Grubu']} {hareket}".replace("- ", "").strip()
            
            if ilk['Mekanik'] == "Kardiyo":
                ozet = " · ".join([f"{row['Süre (dk)']} dk, {row['Kalori']} kcal" for _, row in hareket_setleri.iterrows()])
                baslik = f"🏃‍♂️ **{tam_adi}** — {ozet}"
            else:
                ozet = " · ".join([f"{row['Ağırlık']}×{row['Tekrar']}" for _, row in hareket_setleri.iterrows()])
                baslik = f"💪 **{tam_adi}** — {len(hareket_setleri)} {t['set']} · {ozet}"
            
            with st.expander(baslik, key=f"exp_{hareket}_{ekipman_grp}_{secili_tarih}"):
                h_key = f"{hareket}_{ekipman_grp}_{secili_tarih}"
                c_grafik, c_sil = st.columns(2) if ilk['Mekanik'] != "Kardiyo" else (st.container(), st.columns(1)[0])
                
                if ilk['Mekanik'] != "Kardiyo":
                    with c_grafik:
                        if st.button(f"📈 {t['progress_chart']}", key=f"g_btn_{h_key}", use_container_width=True):
                            st.session_state.grafik_gorunur = None if st.session_state.grafik_gorunur == h_key else h_key
                with c_sil:
                    if st.button(t["delete_exercise_day"], key=f"del_btn_{h_key}", use_container_width=True):
                        st.session_state.silme_onay_hareket = None if st.session_state.silme_onay_hareket == h_key else h_key

                if st.session_state.silme_onay_hareket == h_key:
                    st.warning(t["confirm_delete_exercise_day"].format(ex=tam_adi))
                    co1, co2 = st.columns(2)
                    if co1.button(t["yes_delete"], key=f"y_del_{h_key}", type="primary", use_container_width=True):
                        conn.update(worksheet="Antrenmanlar", data=df_antrenmanlar.drop(hareket_setleri.index))
                        st.cache_data.clear()
                        st.session_state.silme_onay_hareket, st.session_state.grafik_gorunur = None, None
                        st.rerun()
                    if co2.button(t["cancel"], key=f"c_del_{h_key}", use_container_width=True): st.session_state.silme_onay_hareket = None

                if ilk['Mekanik'] != "Kardiyo" and st.session_state.grafik_gorunur == h_key:
                    grafik_ciz(hareket, ekipman_grp)
                    st.divider()

                if ilk['Mekanik'] == 'Kardiyo':
                    set_table_header([0.7, 2, 2, 0.6], ["", t["min_unit"], "kcal", ""])
                else:
                    set_table_header([0.7, 2, 2, 0.6], [t["set"], "kg", t["reps"], ""])
                for idx, row in hareket_setleri.iterrows():
                    cL, c1, c2, cS = st.columns([0.7, 2, 2, 0.6], vertical_alignment="center")
                    if row['Mekanik'] == 'Kardiyo':
                        set_pill(cL, "⏱", cardio=True)
                        c1.number_input(t["duration"], min_value=0, value=int(row['Süre (dk)']), step=1, key=f"ls_{idx}", label_visibility="collapsed")
                        c2.number_input(t["calories"], min_value=0, value=int(row['Kalori']), step=10, key=f"lk_{idx}", label_visibility="collapsed")
                    else:
                        set_pill(cL, int(row['Set']))
                        c1.number_input(t["weight"], min_value=0.0, value=float(row['Ağırlık']), step=2.5, key=f"lw_{idx}", label_visibility="collapsed")
                        c2.number_input(t["reps"], min_value=0, value=int(row['Tekrar']), step=1, key=f"lr_{idx}", label_visibility="collapsed")
                    if cS.button("✕", key=f"d_{idx}"):
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

        st.write("")
        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            st.download_button(label=t["export_csv"], data=gunluk_csv_verisi, file_name=f"antrenman_{st.session_state.secili_kisi}_{secili_tarih.strftime('%Y-%m-%d')}.csv", mime="text/csv", use_container_width=True, key="gunluk_export_csv")
        with c_exp2:
            if not kisi_tum_gecmis.empty:
                st.download_button(label=t["export_all_csv"], data=kisi_tum_gecmis.to_csv(index=False).encode('utf-8-sig'), file_name=f"tum_antrenmanlar_{st.session_state.secili_kisi}.csv", mime="text/csv", use_container_width=True, key="gunluk_export_all_csv")
    else:
        st.info(t["no_workout"])
        if not kisi_tum_gecmis.empty:
            st.download_button(label=t["export_all_csv"], data=kisi_tum_gecmis.to_csv(index=False).encode('utf-8-sig'), file_name=f"tum_antrenmanlar_{st.session_state.secili_kisi}.csv", mime="text/csv", use_container_width=True, key="bos_gun_export_all_csv")


# --- SAYFA 4: ANTRENMAN PROGRAMLARI ---
elif st.session_state.sayfa == 'program_sayfasi':
    render_top_nav()
    page_header(t['programs_title'], icon="📋", subtitle=f"👤 {_e(st.session_state.secili_kisi)}")

    df_programlar = veri_getir("Programlar", ["Kullanıcı", "Program Adı"])
    df_program_detay = veri_getir("ProgramDetay", ["Program Adı", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Ekipman"])
    df_hareketler = veri_getir("Hareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik", "Ekipman"])
    df_legacy_prog = veri_getir("LegacyHareketler", ["Kas Grubu", "Hareket Tipi", "Mekanik", "Ekipman"])

    kisi_programlari = df_programlar[df_programlar['Kullanıcı'] == st.session_state.secili_kisi]

    if st.session_state.secili_program is None:
        with st.container(border=True, key="card_list_programs"):
            section_label(t['existing_programs'], len(kisi_programlari) if not kisi_programlari.empty else None)
            if not kisi_programlari.empty:
                for idx, row in kisi_programlari.iterrows():
                    if st.button(f"📁 {row['Program Adı']}", key=f"p_{idx}", use_container_width=True):
                        st.session_state.secili_program = row['Program Adı']
                        st.rerun()
            else:
                st.info(t["no_program"])
                
        with st.container(border=True, key="card_new_program"):
            section_label(t['create_program'])
            yeni_prog = st.text_input(t["new_program_name"], label_visibility="collapsed")
            if st.button(t["create_program"], type="primary", use_container_width=True):
                if yeni_prog and yeni_prog not in kisi_programlari['Program Adı'].values:
                    conn.update(worksheet="Programlar", data=pd.concat([df_programlar, pd.DataFrame([{"Kullanıcı": st.session_state.secili_kisi, "Program Adı": yeni_prog}])], ignore_index=True))
                    st.cache_data.clear()
                    st.session_state.secili_program = yeni_prog
                    st.rerun()
                elif yeni_prog: st.warning(t["program_exists"])

    else:
        with st.container(key="back_programs"):
            if st.button(t["back_to_programs"], use_container_width=True):
                st.session_state.secili_program = None
                st.rerun()
        section_label(f"📁 {t['program_eyebrow']}")
        st.markdown(f"<div style='font-family:var(--display);font-size:2rem;line-height:1.05;margin:-2px 0 12px 0;'>{_e(buyuk(st.session_state.secili_program))}</div>", unsafe_allow_html=True)

        program_icerik = df_program_detay[(df_program_detay['Program Adı'] == st.session_state.secili_program) & (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi)]

        section_label(t['program_content'])
        if not program_icerik.empty:
            # Program içeriği de (Hareket, Ekipman) ikilisine göre gruplandırılıyor
            program_icerik = program_icerik.copy()
            program_icerik['_grp'] = list(zip(program_icerik['Hareket'], program_icerik.get('Ekipman', '-')))
            for grp_key in program_icerik['_grp'].unique():
                hareket_p, ekipman_p_grp = grp_key
                h_set_p = program_icerik[program_icerik['_grp'] == grp_key].sort_values(by="Set")
                ilk_p = h_set_p.iloc[0]
                tam_adi = f"{ilk_p.get('Ekipman','-')} {ilk_p['Kas Grubu']} {hareket_p}".replace("- ", "").strip()
                ozet = " · ".join([f"{r['Ağırlık']}×{r['Tekrar']}" for _, r in h_set_p.iterrows()])
                
                with st.expander(f"💪 **{tam_adi}** — {len(h_set_p)} {t['set']} · {ozet}", key=f"e_{hareket_p}_{ekipman_p_grp}"):
                    p_key = f"{st.session_state.secili_program}_{hareket_p}_{ekipman_p_grp}"
                    if st.button(t["delete_exercise_from_program"], key=f"d_p_{p_key}", use_container_width=True):
                        st.session_state.program_silme_onay_hareket = None if st.session_state.program_silme_onay_hareket == p_key else p_key
                    if st.session_state.program_silme_onay_hareket == p_key:
                        st.warning(t["confirm_delete_exercise_from_program"].format(ex=tam_adi))
                        c1, c2 = st.columns(2)
                        if c1.button(t["yes_delete"], key=f"y_d_{p_key}", type="primary", use_container_width=True):
                            conn.update(worksheet="ProgramDetay", data=df_program_detay.drop(h_set_p.index))
                            st.cache_data.clear()
                            st.session_state.program_silme_onay_hareket = None
                            st.rerun()
                        if c2.button(t["cancel"], key=f"c_d_{p_key}", use_container_width=True): st.session_state.program_silme_onay_hareket = None

                    st.divider()
                    set_table_header([0.7, 2, 2, 0.6], [t["set"], "kg", t["reps"], ""])
                    for idx, row in h_set_p.iterrows():
                        cL, cW, cR, cS = st.columns([0.7, 2, 2, 0.6], vertical_alignment="center")
                        set_pill(cL, int(row['Set']))
                        cW.number_input(t["weight"], min_value=0.0, value=float(row['Ağırlık']), step=2.5, key=f"pw_{idx}", label_visibility="collapsed")
                        cR.number_input(t["reps"], min_value=0, value=int(row['Tekrar']), step=1, key=f"pr_{idx}", label_visibility="collapsed")
                        if cS.button("✕", key=f"pd_{idx}"):
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

        with st.container(border=True, key="card_add_to_program"):
            section_label(t['add_exercise_to_program'])
            pc1, pc2 = st.columns(2)
            mevcut_kas = df_hareketler['Kas Grubu'].unique() if not df_hareketler.empty else ["Chest", "Back", "Legs"]
            p_kas = pc1.selectbox(t["muscle_group"], mevcut_kas, key="pkas")
            p_hareket_listesi = df_hareketler[df_hareketler['Kas Grubu'] == p_kas]['Hareket Tipi'].unique()
            p_hareket = pc2.selectbox(t["exercise"], p_hareket_listesi, key="phar")

            if p_hareket:
                p_ekip = df_hareketler[df_hareketler['Hareket Tipi'] == p_hareket]['Ekipman'].values[0] if 'Ekipman' in df_hareketler.columns else "Barbell"
                if st.session_state.get("_aktif_p_hareket") != p_hareket:
                    st.session_state["_aktif_p_hareket"] = p_hareket
                    if p_ekip in EKIPMAN_LISTESI:
                        st.session_state["pekip"] = p_ekip
                p_secili_ekipman = st.selectbox(t["equipment"], EKIPMAN_LISTESI, index=EKIPMAN_LISTESI.index(p_ekip) if p_ekip in EKIPMAN_LISTESI else 0, key="pekip")

                # Şablon takibi artık Hareket+Ekipman ikilisine göre tetikleniyor
                p_onceki_anahtar = f"{p_hareket}||{p_secili_ekipman}"
                if st.session_state.p_onceki_hareket != p_onceki_anahtar:
                    st.session_state.p_onceki_hareket = p_onceki_anahtar
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
                    # Programdaki mevcut set sayısı artık Hareket+Ekipman ikilisine göre hesaplanıyor
                    mevcut_prog_set_har = program_icerik[(program_icerik['Hareket'] == p_hareket) & (program_icerik['Ekipman'] == p_secili_ekipman)]
                    p_bas_set = len(mevcut_prog_set_har) + 1
                    p_ekle_set = []
                    set_table_header([0.7, 2, 2], [t["set"], "kg", t["reps"]])

                    for i in range(p_set_sayisi):
                        g_set = p_bas_set + i
                        cl, cw, cr = st.columns([0.7, 2, 2], vertical_alignment="center")
                        set_pill(cl, g_set)
                        kw, kr = f"p_w_new_{p_hareket}_{p_secili_ekipman}_{g_set}", f"p_r_new_{p_hareket}_{p_secili_ekipman}_{g_set}"
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

        # --- LEGACY HAREKETTEN PROGRAMA DİREKT EKLE ---
        with st.expander(t["legacy_add_program_panel"]):
            st.caption(t["legacy_add_program_desc"])
            if df_legacy_prog.empty:
                st.info(t["legacy_empty"])
            else:
                pleg_kas = st.selectbox(t["legacy_select_group"], df_legacy_prog['Kas Grubu'].unique(), key="pleg_kas_sec")
                pleg_liste = df_legacy_prog[df_legacy_prog['Kas Grubu'] == pleg_kas]['Hareket Tipi'].unique()
                pleg_hareket = st.selectbox(t["exercise"], pleg_liste, key="pleg_hareket_sec")

                if pleg_hareket:
                    pleg_row = df_legacy_prog[(df_legacy_prog['Kas Grubu'] == pleg_kas) & (df_legacy_prog['Hareket Tipi'] == pleg_hareket)].iloc[0]
                    pleg_mekanik = pleg_row['Mekanik']
                    mechanic_chip(pleg_mekanik)

                    if pleg_mekanik == "Kardiyo":
                        st.warning(t["cardio_not_supported_in_program"])
                    else:
                        pleg_varsayilan_ekip = pleg_row['Ekipman'] if 'Ekipman' in pleg_row else "Barbell"
                        if st.session_state.get("_aktif_pleg_hareket") != pleg_hareket:
                            st.session_state["_aktif_pleg_hareket"] = pleg_hareket
                            if pleg_varsayilan_ekip in EKIPMAN_LISTESI:
                                st.session_state["pleg_ekip_sec"] = pleg_varsayilan_ekip
                        pleg_ekipman = st.selectbox(t["equipment"], EKIPMAN_LISTESI, index=EKIPMAN_LISTESI.index(pleg_varsayilan_ekip) if pleg_varsayilan_ekip in EKIPMAN_LISTESI else 0, key="pleg_ekip_sec")

                        # Şablon takibi Hareket+Ekipman ikilisine göre tetikleniyor
                        pleg_onceki_anahtar = f"{pleg_hareket}||{pleg_ekipman}"
                        if st.session_state.pleg_onceki_hareket != pleg_onceki_anahtar:
                            st.session_state.pleg_onceki_hareket = pleg_onceki_anahtar
                            st.session_state.pleg_sablon_w, st.session_state.pleg_sablon_r = 0.0, 10
                            for key in list(st.session_state.keys()):
                                if key.startswith("pleg_w_new_") or key.startswith("pleg_r_new_"): del st.session_state[key]

                        pleg_set_sayisi = st.number_input(t["how_many_sets"], min_value=1, max_value=10, value=3, step=1, key="pleg_set_sayisi")
                        plc1, plc2 = st.columns(2)
                        plc1.number_input(t["template_w"], step=2.5, key="pleg_sablon_w", on_change=pleg_sablon_guncelle)
                        plc2.number_input(t["template_r"], step=1, key="pleg_sablon_r", on_change=pleg_sablon_guncelle)

                        st.divider()
                        pleg_mevcut_setler = program_icerik[(program_icerik['Hareket'] == pleg_hareket) & (program_icerik['Ekipman'] == pleg_ekipman)]
                        pleg_bas_set = len(pleg_mevcut_setler) + 1
                        pleg_ekle_set = []
                        set_table_header([0.7, 2, 2], [t["set"], "kg", t["reps"]])

                        for i in range(pleg_set_sayisi):
                            pleg_g_set = pleg_bas_set + i
                            plcl, plcw, plcr = st.columns([0.7, 2, 2], vertical_alignment="center")
                            set_pill(plcl, pleg_g_set)
                            pleg_w_key, pleg_r_key = f"pleg_w_new_{pleg_hareket}_{pleg_ekipman}_{pleg_g_set}", f"pleg_r_new_{pleg_hareket}_{pleg_ekipman}_{pleg_g_set}"
                            if pleg_w_key not in st.session_state: st.session_state[pleg_w_key] = st.session_state.pleg_sablon_w
                            if pleg_r_key not in st.session_state: st.session_state[pleg_r_key] = st.session_state.pleg_sablon_r
                            pleg_w = plcw.number_input(t["weight"], step=2.5, key=pleg_w_key, label_visibility="collapsed")
                            pleg_r = plcr.number_input(t["reps"], step=1, key=pleg_r_key, label_visibility="collapsed")
                            pleg_ekle_set.append({"Program Adı": st.session_state.secili_program, "Kullanıcı": st.session_state.secili_kisi, "Kas Grubu": pleg_kas, "Hareket": pleg_hareket, "Set": pleg_g_set, "Ağırlık": pleg_w, "Tekrar": pleg_r, "Ekipman": pleg_ekipman})

                        if st.button(t["add_to_program"], type="primary", use_container_width=True, key="pleg_add_btn"):
                            conn.update(worksheet="ProgramDetay", data=pd.concat([df_program_detay, pd.DataFrame(pleg_ekle_set)], ignore_index=True))
                            st.cache_data.clear()
                            for key in list(st.session_state.keys()):
                                if key.startswith("pleg_w_new_") or key.startswith("pleg_r_new_"): del st.session_state[key]
                            st.success(f"{pleg_hareket} {t['success_add_to_program']}")
                            st.rerun()

        with st.expander(t["delete_program_panel"]):
            st.warning(t["delete_program_desc"])
            if st.button(t["delete_program_btn"], type="primary", use_container_width=True):
                conn.update(worksheet="Programlar", data=df_programlar[~((df_programlar['Program Adı'] == st.session_state.secili_program) & (df_programlar['Kullanıcı'] == st.session_state.secili_kisi))])
                conn.update(worksheet="ProgramDetay", data=df_program_detay[~((df_program_detay['Program Adı'] == st.session_state.secili_program) & (df_program_detay['Kullanıcı'] == st.session_state.secili_kisi))])
                st.cache_data.clear()
                st.session_state.secili_program = None
                st.rerun()

# --- SAYFA 5: İSTATİSTİKLER ---
elif st.session_state.sayfa == 'istatistik_sayfasi':
    render_top_nav()
    page_header(t['stats_title'].replace("📊", "").strip(), icon="📊", subtitle=f"👤 {_e(st.session_state.secili_kisi)} · 👥 {_e(st.session_state.secili_grup)}")
    
    df_antrenmanlar = veri_getir("Antrenmanlar", ["Tarih", "Grup", "Kullanıcı", "Kas Grubu", "Hareket", "Set", "Ağırlık", "Tekrar", "Süre (dk)", "Kalori", "Mekanik", "Ekipman"])
    
    with st.container(border=True, key="card_stat_summary"):
        section_label(t['personal_summary'])
        kisi_gecmis = df_antrenmanlar[(df_antrenmanlar['Grup'] == st.session_state.secili_grup) & (df_antrenmanlar['Kullanıcı'] == st.session_state.secili_kisi)].copy()

        if kisi_gecmis.empty:
            st.info(t["no_chart_data"])
        else:
            # Tam Hareket ismi zaten Ekipman'ı da içeriyor, bu yüzden istatistiklerde
            # farklı ekipmanlarla yapılan aynı isimli hareketler doğru şekilde ayrışıyor.
            kisi_gecmis['Tam Hareket'] = kisi_gecmis.apply(
                lambda row: f"{row.get('Ekipman','-')} {row.get('Kas Grubu','')} {row.get('Hareket','')}".replace("- ", "").strip(), 
                axis=1
            )
            
            _toplam_gun = kisi_gecmis['Tarih'].nunique()
            _en_sik = kisi_gecmis['Tam Hareket'].value_counts().idxmax() if not kisi_gecmis.empty else "-"
            _toplam_kardiyo = int(pd.to_numeric(kisi_gecmis['Süre (dk)'], errors='coerce').fillna(0).sum())
            st.markdown(
                f"<div class='stat-grid'>"
                f"<div class='stat hl'><div class='s-label'>{t['total_days']}</div><div class='s-value'>{_toplam_gun}<span class='s-unit'>{t['days_unit']}</span></div></div>"
                f"<div class='stat'><div class='s-label'>{t['total_cardio']}</div><div class='s-value'>{_toplam_kardiyo}<span class='s-unit'>{t['min_unit']}</span></div></div>"
                f"<div class='stat' style='grid-column: 1 / -1;'><div class='s-label'>{t['most_frequent']}</div><div class='s-value small'>{_e(_en_sik)}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            stat_export = kisi_gecmis.drop(columns=['Tam Hareket'], errors='ignore').copy()
            stat_export['Tarih_sirala'] = pd.to_datetime(stat_export['Tarih'], errors='coerce')
            stat_export = stat_export.sort_values(by=['Tarih_sirala', 'Set'], ascending=[False, True]).drop(columns=['Tarih_sirala'], errors='ignore')
            st.download_button(label=t["export_all_csv"], data=stat_export.to_csv(index=False).encode('utf-8-sig'), file_name=f"tum_antrenmanlar_{st.session_state.secili_kisi}.csv", mime="text/csv", use_container_width=True, key="stat_export_all_csv")

    with st.container(border=True, key="card_stat_weight"):
        section_label(t['weight_history'])
        agirlik_h = kisi_gecmis[kisi_gecmis['Mekanik'] != 'Kardiyo']['Tam Hareket'].unique() if not kisi_gecmis.empty else []
        
        if len(agirlik_h) > 0:
            sec_stat = st.selectbox(t["select_stat_ex"], agirlik_h, label_visibility="collapsed")
            if sec_stat:
                graf = kisi_gecmis[kisi_gecmis['Tam Hareket'] == sec_stat].copy()
                graf['Tarih'] = pd.to_datetime(graf['Tarih'])
                g = graf.groupby('Tarih')['Ağırlık'].max().reset_index().sort_values(by='Tarih')
                g['Tarih'] = g['Tarih'].dt.strftime('%d/%m/%Y')
                g.set_index('Tarih', inplace=True)
                st.line_chart(g['Ağırlık'].astype(float), color=GRAFIK_RENGI)
        else:
            st.info(t["no_chart_data"])
            
    with st.container(border=True, key="card_stat_group"):
        section_label(t['group_comparison'])
        grup_gecmisi = df_antrenmanlar[df_antrenmanlar['Grup'] == st.session_state.secili_grup].copy()

        if not grup_gecmisi.empty:
            subhead(t['comp_days'])
            gun_s = grup_gecmisi.groupby('Kullanıcı')['Tarih'].nunique().reset_index()
            gun_s.set_index('Kullanıcı', inplace=True)
            st.bar_chart(gun_s['Tarih'], color=GRAFIK_RENGI)

            subhead(t['comp_cardio'])
            grup_gecmisi['Süre (dk)'] = pd.to_numeric(grup_gecmisi['Süre (dk)'], errors='coerce').fillna(0)
            kard_s = grup_gecmisi.groupby('Kullanıcı')['Süre (dk)'].sum().reset_index()
            kard_s.set_index('Kullanıcı', inplace=True)
            st.bar_chart(kard_s['Süre (dk)'], color="#FF4D2E")
        else:
            st.info(t["no_chart_data"])
