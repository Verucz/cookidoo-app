import streamlit as st
import random

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# 1. Databáze s přímými odkazovými URL na konkrétní Cookidoo recepty
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {
                "nazev": "Ovesná kaše", 
                "kcal": 380, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r594505"
            },
            {
                "nazev": "Nadýchané lívance", 
                "kcal": 430, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r659068"
            },
            {
                "nazev": "Domácí granola", 
                "kcal": 390, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r263673"
            }
        ],
        "Svačina 1": [
            {
                "nazev": "Jablečné pyré", 
                "kcal": 200, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r594505"
            },
            {
                "nazev": "Ovocné smoothie", 
                "kcal": 220, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r263673"
            }
        ],
        "Oběd": [
            {
                "nazev": "Dýňová polévka", 
                "kcal": 350, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r82858"
            },
            {
                "nazev": "Hovězí guláš s knedlíky", 
                "kcal": 720, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r766768"
            },
            {
                "nazev": "Čočkovo-dýňová polévka", 
                "kcal": 450, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r263673"
            }
        ],
        "Svačina 2": [
            {
                "nazev": "Polévka z máslové dýně s kokosovým mlékem", 
                "kcal": 280, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r659068"
            }
        ],
        "Večeře": [
            {
                "nazev": "Dýňová polévka se smetanou", 
                "kcal": 410, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r594505"
            },
            {
                "nazev": "Hovězí guláš ze staršího pečiva", 
                "kcal": 680, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r644485"
            }
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

# 3. Formulář pro přikládání vlastních přesných receptů
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept z Cookidoo"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Název jídla")
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)
    novy_link = st.text_input("Přímý odkaz z Cookidoo", value="https://cookidoo.cz/recipes/recipe/cs/")
    
    if st.button("Uložit recept"):
        if novy_nazev and novy_link:
            st.session_state.recepty_db[novy_kat].append({
                "nazev": novy_nazev,
                "kcal": nove_kcal,
                "link": novy_link.strip()
            })
            st.success(f"Recept **{novy_nazev}** byl úspěšně přidán!")
        else:
            st.warning("Vyplňte prosím název i přesný odkaz.")

# 4. Hlavní zobrazení
if st.button("🎲 Vygenerovat nový týdenní plán"):
    st.rerun()

st.subheader("📅 Váš jídelníček na tento týden")

def zobraz_den(chody):
    for chod in chody:
        st.write(f"### {chod}")
        dostupne_recepty = st.session_state.recepty_db[chod]
        moznosti = random.sample(dostupne_recepty, min(3, len(dostupne_recepty)))
        cols = st.columns(len(moznosti))
        for i, recept in enumerate(moznosti):
            with cols[i]:
                st.info(f"**{recept['nazev']}**\n\n🔥 ~{recept['kcal']} kcal\n\n[📖 Otevřít recept v Cookidoo]({recept['link']})")

chody_dne = ["Snídaně", "Oběd", "Večeře"] if pocet_jidel == 3 else ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]

dny_v_tydnu = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
zalozky = st.tabs(dny_v_tydnu)

for idx, tab in enumerate(zalozky):
    with tab:
        st.write(f"#### Plán na {dny_v_tydnu[idx]}")
        zobraz_den(chody_dne)
