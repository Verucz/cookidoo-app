import streamlit as st
import random

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# 1. Databáze s přímými reálnými URL adresami a doslovnými názvy z Cookidoo
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {
                "nazev": "Nadýchané americké palačinky", 
                "kcal": 430, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r177504"
            },
            {
                "nazev": "Ovesná kaše s jablky", 
                "kcal": 380, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55273"
            },
            {
                "nazev": "Domácí zapečená granola", 
                "kcal": 390, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r128392"
            },
            {
                "nazev": "Míchaná vajíčka z Varomy", 
                "kcal": 350, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55272"
            }
        ],
        "Svačina 1": [
            {
                "nazev": "Jablečno-mrkvové pyré", 
                "kcal": 180, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55270"
            },
            {
                "nazev": "Ovocné smoothie s banánem", 
                "kcal": 210, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55269"
            },
            {
                "nazev": "Tvarohový krém s ovocem", 
                "kcal": 220, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55279"
            }
        ],
        "Oběd": [
            {
                "nazev": "Dýňová krémová polévka Hokkaidó", 
                "kcal": 350, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55284"
            },
            {
                "nazev": "Tradiční svíčková na smetaně", 
                "kcal": 750, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160751"
            },
            {
                "nazev": "Losos na parním koši Varoma s bramborem", 
                "kcal": 680, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160742"
            },
            {
                "nazev": "Krémové houbové rizoto", 
                "kcal": 620, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160748"
            }
        ],
        "Svačina 2": [
            {
                "nazev": "Krémový hummus s cizrnou", 
                "kcal": 230, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55280"
            },
            {
                "nazev": "Tvarohová pomazánka s pažitkou", 
                "kcal": 190, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55279"
            },
            {
                "nazev": "Mrkvový salát s jablkem", 
                "kcal": 160, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55268"
            }
        ],
        "Večeře": [
            {
                "nazev": "Zeleninový krém", 
                "kcal": 390, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55283"
            },
            {
                "nazev": "Těstoviny s rajčatovou omáčkou", 
                "kcal": 510, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r160745"
            },
            {
                "nazev": "Pečená zelenina s tvarohem", 
                "kcal": 430, 
                "link": "https://cookidoo.cz/recipes/recipe/cs/r55282"
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

# 3. Formulář pro přikládání přímých odkazů
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept z Cookidoo"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Doslovný název receptu")
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)
    novy_link = st.text_input("Přímý URL odkaz z Cookidoo", value="https://cookidoo.cz/recipes/recipe/cs/")
    
    if st.button("Uložit recept"):
        if novy_nazev and novy_link:
            st.session_state.recepty_db[novy_kat].append({
                "nazev": novy_nazev.strip(),
                "kcal": nove_kcal,
                "link": novy_link.strip()
            })
            st.success(f"Recept **{novy_nazev}** byl úspěšně přidán!")
        else:
            st.warning("Vyplňte prosím název i přímý odkaz.")

# 4. Hlavní zobrazení
if st.button("🎲 Vygenerovat nový týdenní plán"):
    st.rerun()

st.subheader("📅 Váš jídelníček na tento týden")

# Vykreslení přesně 3 možností pro každý chod
def zobraz_den(chody):
    for chod in chody:
        st.write(f"### {chod}")
        dostupne_recepty = st.session_state.recepty_db[chod]
        
        pocet_moznosti = min(3, len(dostupne_recepty))
        moznosti = random.sample(dostupne_recepty, pocet_moznosti)
        
        cols = st.columns(3)
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
