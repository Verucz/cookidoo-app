import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# Pomocná funkce – vyhledá na Cookidoo přesný název receptu v uvozovkách
def získej_cookidoo_odkaz(nazev):
    presny_nazev = f'"{nazev}"'
    encoded = urllib.parse.quote(presny_nazev)
    return f"https://cookidoo.cz/search/cs?context=recipes&query={encoded}"

# 1. Databáze se 100% reálnými recepty z českého Cookidoo
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {"nazev": "Ovesná kaše", "kcal": 380},
            {"nazev": "Nadýchané lívance", "kcal": 430},
            {"nazev": "Domácí granola", "kcal": 390},
            {"nazev": "Míchaná vajíčka", "kcal": 350}
        ],
        "Svačina 1": [
            {"nazev": "Jablečné pyré", "kcal": 180},
            {"nazev": "Ovocné smoothie", "kcal": 210},
            {"nazev": "Těstovinový salát Caprese", "kcal": 290},
            {"nazev": "Mrkvový salát s jablkem", "kcal": 160}
        ],
        "Oběd": [
            {"nazev": "Svíčková na smetaně", "kcal": 750},
            {"nazev": "Slaný koláč Quiche Lorraine", "kcal": 620},
            {"nazev": "Špagety Carbonara", "kcal": 680},
            {"nazev": "Chilli con carne s bílými fazolemi", "kcal": 610},
            {"nazev": "Rizoto s uzeným lososem a pórkem", "kcal": 590}
        ],
        "Svačina 2": [
            {"nazev": "Bramborovo - zeleninové pyré", "kcal": 220},
            {"nazev": "Avokádo plněné tuňákem", "kcal": 260},
            {"nazev": "Bílé fazole se zakysanou smetanou a pórkem", "kcal": 240}
        ],
        "Večeře": [
            {"nazev": "Houbový Stroganoff", "kcal": 490},
            {"nazev": "Cuketové špagety s boloňskou omáčkou z hlívy ústřičné", "kcal": 420},
            {"nazev": "Kuřecí stehenní řízky s brokolicí, žampióny a těstovinami", "kcal": 540},
            {"nazev": "Kokosový Dhal", "kcal": 450}
        ]
    }

# 2. Postranní panel – Parametry a výpočty TDEE
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

# 3. Přidání nového receptu
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Přesný název receptu podle Cookidoo")
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

# 4. Zobrazení týdenního jídelníčku
if st.button("🎲 Vygenerovat nový týdenní plán"):
    st.rerun()

st.subheader("📅 Váš jídelníček na tento týden")

# Funkce pro vykreslení 3 možností na chod
def zobraz_den(chody):
    for chod in chody:
        st.write(f"### {chod}")
        dostupne_recepty = st.session_state.recepty_db[chod]
        
        # Výběr 3 možností z databáze
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
