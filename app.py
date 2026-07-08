import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# --- DİL SÖZLÜĞÜ ---
LANG = {
    "English": {
        "groups_title": "🏋️‍♂️ Workout Groups", "existing_groups": "Existing Groups", "no_group": "No groups registered yet.",
        "new_group": "Create New Group", "add_group": "Add Group", "success_group": "successfully created!",
        "back_to_groups": "⬅️ Back to Groups", "members": "Members", "no_member": "No members yet.",
        "new_member": "Add new member", "add_member": "Add Member", "success_member": "added to the group!",
        "back_to_members": "⬅️ Back to Members", "daily_log": "Daily Log", "add_new_set": "Add New Set",
        "date": "Date", "exercise": "Exercise", "weight": "Weight", "reps": "Reps",
        "save_all": "Save All Sets", "progress_chart": "Progress Chart", "no_chart_data": "Not enough data.",
        "duration": "Duration (min)", "calories": "Calories (kcal)", "save_cardio": "Save Cardio", "success_cardio": "saved!",
        "set": "Set", "editing": "Editing", "save": "💾 Save", "cancel": "Cancel", "no_workout": "No records."
    },
    "Türkçe": {
        "groups_title": "🏋️‍♂️ Antrenman Grupları", "existing_groups": "Mevcut Gruplar", "no_group": "Grup yok.",
        "new_group": "Yeni Grup Oluştur", "add_group": "Grup Ekle", "success_group": "oluşturuldu!",
        "back_to_groups": "⬅️ Gruplara Dön", "members": "Üyeler", "no_member": "Üye yok.",
        "new_member": "Yeni kişi ekle", "add_member": "Kişi Ekle", "success_member": "gruba eklendi!",
        "back_to_members": "⬅️ Üyelere Dön", "daily_log": "Günlük", "add_new_set": "Yeni Set Ekle",
        "date": "Tarih", "exercise": "Hareket", "weight": "Ağırlık", "reps": "Tekrar",
        "save_all": "Tüm Setleri Kaydet", "progress_chart": "Gelişim Grafiği", "no_chart_data": "Yeterli veri yok.",
        "duration": "Süre (dk)", "calories": "Kalori (kcal)", "save_cardio": "Kardiyoyu Kaydet", "success_cardio": "kaydedildi!",
        "set": "Set", "editing": "Düzenleniyor", "save": "💾 Kaydet", "cancel": "İptal", "no_workout": "Kayıt yok."
    }
}

st.set_page_config(page_title="Workout App", layout="centered")
secilen_dil = st.sidebar.selectbox("🌐 Language", ["English", "Türkçe"], index=1)
t = LANG[secilen_dil]

if 'sayfa' not in st.session_state: st.session_state.sayfa = 'ana_sayfa'
if 'secili_grup' not in st.session_state: st.session_state.secili_grup = None
if 'secili_kisi' not in st.session_state: st.session_state.secili_kisi = None
if 'edit_idx' not in st.session_state: st.session_state.edit_idx = None

conn = st.connection("gsheets", type=GSheetsConnection)

def veri_getir(s, k):
    df = conn.read(worksheet=s, ttl=5)
    return df.fillna(0).dropna(how='all') if not df.empty else pd.DataFrame(columns=k)

# --- SAYFA MANTIĞI ---
if st.session_state.sayfa == 'ana_sayfa':
    df_g = veri_getir("Gruplar", ["Grup Adı"])
    st.title(t["groups_title"])
    for _, r in df_g.iterrows():
        if st.button(f"📁 {r['Grup Adı']}", use_container_width=True):
            st.session_state.secili_grup = r['Grup Adı']; st.session_state.sayfa = 'grup_sayfasi'; st.rerun()
    yeni_g = st.text_input(t["new_group"])
    if st.button(t["add_group"]) and yeni_g:
        conn.update("Gruplar", pd.concat([df_g, pd.DataFrame([{"Grup Adı": yeni_g}])])); st.rerun()

elif st.session_state.sayfa == 'grup_sayfasi':
    if st.button(t["back_to_groups"]): st.session_state.sayfa = 'ana_sayfa'; st.rerun()
    df_k = veri_getir("Kullanicilar", ["Grup Adı", "Kullanıcı Adı"])
    st.title(f"📁 {st.session_state.secili_grup}")
    for _, r in df_k[df_k['Grup Adı'] == st.session_state.secili_grup].iterrows():
        if st.button(f"👤 {r['Kullanıcı Adı']}", use_container_width=True):
            st.session_state.secili_kisi = r['Kullanıcı Adı']; st.session_state.sayfa = 'kisi_sayfasi'; st.rerun()

elif st.session_state.sayfa == 'kisi_sayfasi':
    if st.button(t["back_to_members"]): st.session_state.sayfa = 'grup_sayfasi'; st.rerun()
    df_ant = veri_getir("Antrenmanlar", ["Tarih", "Kullanıcı", "Hareket", "Ağırlık", "Süre (dk)", "Kalori", "Mekanik", "Set", "Tekrar"])
    df_har = veri_getir("Hareketler", ["Hareket Tipi", "Mekanik"])
    
    tarih = st.date_input(t["date"], value=date.today())
    h = st.selectbox(t["exercise"], df_har['Hareket Tipi'].unique())
    mekanik = df_har[df_har['Hareket Tipi'] == h]['Mekanik'].values[0]
    
    # FORMLAR
    if mekanik == "Kardiyo":
        sure = st.number_input(t["duration"], value=30)
        kal = st.number_input(t["calories"], value=sure * 10)
        if st.button(t["save_cardio"]):
            conn.update("Antrenmanlar", pd.concat([df_ant, pd.DataFrame([{"Tarih": tarih.strftime("%Y-%m-%d"), "Kullanıcı": st.session_state.secili_kisi, "Hareket": h, "Süre (dk)": sure, "Kalori": kal, "Mekanik": "Kardiyo", "Set": 1}])])); st.rerun()
    else:
        set_s = st.number_input("Set", 1, 10, 3)
        cols = st.columns(2)
        w = cols[0].number_input(t["weight"], 0.0, 200.0, 20.0, 2.5)
        r = cols[1].number_input(t["reps"], 1, 30, 10)
        if st.button(t["save_all"]):
            yeni = [ {"Tarih": tarih.strftime("%Y-%m-%d"), "Kullanıcı": st.session_state.secili_kisi, "Hareket": h, "Ağırlık": w, "Tekrar": r, "Mekanik": mekanik, "Set": i+1} for i in range(set_s)]
            conn.update("Antrenmanlar", pd.concat([df_ant, pd.DataFrame(yeni)])); st.rerun()

    # LİSTELEME
    st.divider()
    gunluk = df_ant[(df_ant['Tarih'] == tarih.strftime("%Y-%m-%d")) & (df_ant['Kullanıcı'] == st.session_state.secili_kisi)]
    for mov in gunluk['Hareket'].unique():
        with st.expander(f"💪 {mov}"):
            with st.popover("📈 " + t["progress_chart"]):
                g = df_ant[(df_ant['Kullanıcı'] == st.session_state.secili_kisi) & (df_ant['Hareket'] == mov)]
                st.line_chart(g.groupby('Tarih')['Ağırlık'].max())
            for idx, row in gunluk[gunluk['Hareket'] == mov].iterrows():
                if st.session_state.edit_idx == idx:
                    w_n = st.number_input(t["weight"], value=float(row['Ağırlık']), key=f"w{idx}")
                    r_n = st.number_input(t["reps"], value=int(row['Tekrar']), key=f"r{idx}")
                    if st.button(t["save"], key=f"s{idx}"):
                        df_ant.at[idx, 'Ağırlık'] = w_n; df_ant.at[idx, 'Tekrar'] = r_n; conn.update("Antrenmanlar", df_ant); st.session_state.edit_idx=None; st.rerun()
                else:
                    c1, c2, c3 = st.columns([4,1,1])
                    c1.write(f"Set {row['Set']}: {row['Ağırlık']}kg x {row['Tekrar']}")
                    if c2.button("✏️", key=f"e{idx}"): st.session_state.edit_idx = idx; st.rerun()
                    if c3.button("❌", key=f"d{idx}"): conn.update("Antrenmanlar", df_ant.drop(idx)); st.rerun()
