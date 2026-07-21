import streamlit as st
import random

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# 1. Databáze receptů (Uložená ve st.session_state, aby do ní šlo přidávat za chodu)
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {"nazev": "Ovesná kaše s jablky a skořicí", "kcal": 380, "link": "https://cookidoo.cz"},
            {"nazev": "Míchaná vajíčka z Varomy", "kcal": 410, "link": "https://cookidoo.cz"},
            {"nazev": "Smoothie bowl s lesním ovocem", "kcal": 350, "link": "https://cookidoo.cz"},
            {"nazev": "Domácí granola s řeckým jogurtem", "kcal": 390, "link": "https://cookidoo.cz"},
            {"nazev": "Nadýchané lívance z Thermomixu", "kcal": 430, "link": "https://cookidoo.cz"},
        ],
        "Svačina 1": [
            {"nazev": "Jablečné pyré s ořechy", "kcal": 200, "link": "https://cookidoo.cz"},
            {"nazev": "Proteinový koktejl s banánem", "kcal": 220, "link": "https://cookidoo.cz"},
            {"nazev": "Mrkvový salát s jablkem", "kcal": 180, "link": "https://cookidoo.cz"},
        ],
        "Oběd": [
            {"nazev": "Dýňová krémová polévka + Kuřecí prsa v pari", "kcal": 650, "link": "https://cookidoo.cz"},
            {"nazev": "Losos s brokolicí a bramborem z Varomy", "kcal": 680, "link": "https://cookidoo.cz"},
            {"nazev": "Hovězí guláš z Thermomixu", "kcal": 720, "link": "https://cookidoo.cz"},
            {"nazev": "Rizoto s houbami a parmazánem", "kcal": 610, "link": "https://cookidoo.cz"},
        ],
        "Svačina 2": [
            {"nazev": "Kefírové smoothie s borůvkami", "kcal": 190, "link": "https://cookidoo.cz"},
            {"nazev": "Krájená zelenina s hummusem", "kcal": 230, "link": "https://cookidoo.cz"},
        ],
        "Večeře": [
            {"nazev": "Zeleninový krém s krutony", "kcal": 450, "link": "https://cookidoo.cz"},
            {"nazev": "Těstoviny s rajčatovou omáčkou a bazalkou", "kcal": 520, "link": "https://cookidoo.cz"},
            {"nazev": "Salát s grilovaným sýrem Halloumi", "kcal": 490, "link": "https://cookidoo.cz"},
            {"nazev": "Pečená zelenina s tvarohem", "kcal": 430, "link": "https://cookidoo.cz"},
        ]
    }

# 2. Postranní panel - Vstupy od uživatele
st.sidebar.header("⚙️ Vaše parametry")

pohlavi = st.sidebar.selectbox("Pohlaví", ["Žena", "Muž"])
vek = st.sidebar.number_input("Věk", min_value=15, max_value=100, value=30)
vaha = st.sidebar.number_input("Váha (kg)", min_value=40.0, max_value=200.0, value=65.0)
vyska = st.sidebar.number_input("Výška (cm)", min_value=130, max_value=220, value=170)

aktivity_dict = {
    "Sedavé zaměstnání (minimální pohyb)": 1.2,
    "Lehká aktivita (1-3x týdně cvičení)": 1.375,
    "Střední aktivita (3-5x týdně cvičení)": 1.55,
    "Vysoká aktivita (6-7x týdně náročný sport)": 1.725
}

aktivita = st.sidebar.selectbox("Úroveň aktivity", list(aktivity_dict.keys()))
pocet_jidel = st.sidebar.radio("Počet jídel denně", [3, 5], index=0)

# Výpočet BMR a TDEE
if pohlavi == "Muž":
    bmr = 10 * vaha + 6.25 * vyska - 5 * vek + 5
else:
    bmr = 10 * vaha + 6.25 * vyska - 5 * vek - 161

tdee = round(bmr * aktivity_dict[aktivita])

st.sidebar.markdown("---")
st.sidebar.metric("Váš denní cílový příjem", f"{tdee} kcal")

# 3. Formulář pro přidání nového receptu do databáze přímo v aplikaci
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept z Cookidoo"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Název jídla")
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)
    novy_link = st.text_input("Odkaz na Cookidoo", value="https://cookidoo.cz")
    
    if st.button("Uložit recept"):
        if novy_nazev:
            st.session_state.recepty_db[novy_kat].append({
                "nazev": novy_nazev,
                "kcal": nove_kcal,
                "link": novy_link
            })
            st.success(f"Recept **{novy_nazev}** byl přidán!")
        else:
            st.warning("Vyplňte prosím název jídla.")

# 4. Hlavní část - Tlačítko pro nový výběr a Týdenní záložky
if st.button("🎲 Vygenerovat nový týdenní plán"):
    st.rerun()

st.subheader("📅 Váš jídelníček na tento týden")

# Pomocná funkce pro zobrazení jednoho dne
def zobraz_den(chody):
    for chod in chody:
        st.write(f"### {chod}")
        dostupne_recepty = st.session_state.recepty_db[chod]
        moznosti = random.sample(dostupne_recepty, min(3, len(dostupne_recepty)))
        cols = st.columns(len(moznosti))
        for i, recept in enumerate(moznosti):
            with cols[i]:
                st.info(f"**{recept['nazev']}**\n\n🔥 ~{recept['kcal']} kcal\n\n[📖 Otevřít v Cookidoo]({recept['link']})")

# Definice chodů
chody_dne = ["Snídaně", "Oběd", "Večeře"] if pocet_jidel == 3 else ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]

# Tvorba týdenních záložek (Tabs)
dny_v_tydnu = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
zalozky = st.tabs(dny_v_tydnu)

for idx, tab in enumerate(zalozky):
    with tab:
        st.write(f"#### Plán na {dny_v_tydnu[idx]}")
        zobraz_den(chody_dne)
