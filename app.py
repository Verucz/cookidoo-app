import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# Pomocná funkce – vytvoří bezpečný odkaz, který otevře Cookidoo přímo na daném receptu
def získej_cookidoo_odkaz(nazev):
    presny_nazev = f'"{nazev}"'
    encoded = urllib.parse.quote(presny_nazev)
    return f"https://cookidoo.cz/search/cs?context=recipes&query={encoded}"

# 1. Databáze s přesnými doslovnými názvy receptů z českého Cookidoo
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {"nazev": "Nadýchané americké palačinky", "kcal": 430},
            {"nazev": "Ovesná kaše", "kcal": 380},
            {"nazev": "Domácí granola", "kcal": 390},
            {"nazev": "Míchaná vajíčka", "kcal": 350}
        ],
        "Svačina 1": [
            {"nazev": "Jablečné pyré", "kcal": 180},
            {"nazev": "Ovocné smoothie", "kcal": 210},
            {"nazev": "Tvarohový krém s ovocem", "kcal": 220},
            {"nazev": "Mrkvový salát s jablkem", "kcal": 160}
        ],
        "Oběd": [
            {"nazev": "Dýňová krémová polévka", "kcal": 350},
            {"nazev": "Svíčková na smetaně", "kcal": 750},
            {"nazev": "Losos s parní zeleninou a bramborem", "kcal": 680},
            {"nazev": "Krémové houbové rizoto", "kcal": 620},
            {"nazev": "Hovězí guláš", "kcal": 710}
        ],
        "Svačina 2": [
            {"nazev": "Hummus", "kcal": 230},
            {"nazev": "Tvarohová pomazánka s pažitkou", "kcal": 190},
            {"nazev": "Kefírové smoothie s borůvkami", "kcal": 180}
        ],
        "Večeře": [
            {"nazev": "Zeleninový krém", "kcal": 390},
            {"nazev": "Těstoviny s rajčatovou omáčkou", "kcal": 510},
            {"nazev": "Pečená zelenina s tvarohem", "kcal": 430},
            {"nazev": "Houbový Stroganoff", "kcal": 490}
        ]
    }

# 2. Postranní panel - Výpočet BMR a TDEE
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

if pohlavi == "Muž":
    bmr = 10 * vaha + 6.25 * vyska - 5 * vek + 5
else:
    bmr = 10 * vaha + 6.25 * vyska - 5 * vek - 161

tdee = round(bmr * aktivity_dict[aktivita])

st.sidebar.markdown("---")
st.sidebar.metric("Váš denní cílový příjem", f"{tdee} kcal")

# 3. Formulář pro přikládání receptů podle doslovného názvu
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept z Cookidoo"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Doslovný název receptu z Cookidoo")
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)
    
    if st.button("Uložit recept"):
        if novy_nazev:
            st.session_state.recepty_db[novy_kat].append({
                "nazev": novy_nazev.strip(),
                "kcal": nove_kcal
            })
            st.success(f"Recept **{novy_nazev}** byl úspěšně přidán!")
        else:
            st.warning("Vyplňte prosím název jídla.")

# 4. Hlavní zobrazení
if st.button("🎲 Vygenerovat nový týdenní plán"):
    st.rerun()

st.subheader("📅 Váš jídelníček na tento týden")

# Zobrazení VŽDY 3 možností pro každý chod
def zobraz_den(chody):
    for chod in chody:
        st.write(f"### {chod}")
        dostupne_recepty = st.session_state.recepty_db[chod]
        
        pocet_moznosti = min(3, len(dostupne_recepty))
        moznosti = random.sample(dostupne_recepty, pocet_moznosti)
        
        cols = st.columns(3)
        for i, recept in enumerate(moznosti):
            odkaz = získej_cookidoo_odkaz(recept['nazev'])
            with cols[i]:
                st.info(f"**{recept['nazev']}**\n\n🔥 ~{recept['kcal']} kcal\n\n[📖 Otevřít recept na Cookidoo]({odkaz})")

chody_dne = ["Snídaně", "Oběd", "Večeře"] if pocet_jidel == 3 else ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]

dny_v_tydnu = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
zalozky = st.tabs(dny_v_tydnu)

for idx, tab in enumerate(zalozky):
    with tab:
        st.write(f"#### Plán na {dny_v_tydnu[idx]}")
        zobraz_den(chody_dne)
