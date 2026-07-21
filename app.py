import streamlit as st
import random

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# 1. Databáze receptů s přímými funkčními URL adresami na konkrétní Cookidoo recepty
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {
                "nazev": "Ovesná kaše s jablky", 
                "kcal": 380, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55273"
            },
            {
                "nazev": "Nadýchané lívance", 
                "kcal": 430, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55281"
            },
            {
                "nazev": "Domácí granola", 
                "kcal": 390, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r128392"
            },
            {
                "nazev": "Míchaná vajíčka", 
                "kcal": 410, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55272"
            }
        ],
        "Svačina 1": [
            {
                "nazev": "Jablečné pyré", 
                "kcal": 200, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55270"
            },
            {
                "nazev": "Ovocné smoothie", 
                "kcal": 220, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55269"
            },
            {
                "nazev": "Mrkvový salát s jablkem", 
                "kcal": 180, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55268"
            }
        ],
        "Oběd": [
            {
                "nazev": "Dýňová krémová polévka", 
                "kcal": 350, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55284"
            },
            {
                "nazev": "Svíčková na smetaně", 
                "kcal": 750, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160751"
            },
            {
                "nazev": "Losos s parní zeleninou a bramborem (Varoma)", 
                "kcal": 680, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160742"
            },
            {
                "nazev": "Hovězí guláš", 
                "kcal": 720, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160750"
            },
            {
                "nazev": "Rizoto s houbami", 
                "kcal": 610, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160748"
            }
        ],
        "Svačina 2": [
            {
                "nazev": "Hummus", 
                "kcal": 230, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55280"
            },
            {
                "nazev": "Tvarohová pomazánka", 
                "kcal": 190, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55279"
            }
        ],
        "Večeře": [
            {
                "nazev": "Zeleninový krém", 
                "kcal": 450, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55283"
            },
            {
                "nazev": "Těstoviny s rajčatovou omáčkou", 
                "kcal": 520, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160745"
            },
            {
                "nazev": "Pečená zelenina s tvarohem", 
                "kcal": 430, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55282"
            }
        ]
    }

# 2. Postranní panel - Výpočet kalorií
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

# 3. Formulář pro přikládání konkrétních odkazů
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
                "link": novy_link
            })
            st.success(f"Recept **{novy_nazev}** byl úspěšně přidán!")
        else:
            st.warning("Vyplňte prosím název i odkaz.")

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
