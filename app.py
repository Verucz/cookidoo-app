import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# Pomocná funkce pro vygenerování přímého odkazu na vyhledání receptu na Cookidoo
def make_cookidoo_link(nazev_receptu):
    base_url = "https://cookidoo.cz/search/cs?"
    query = urllib.parse.urlencode({"context": "recipes", "query": nazev_receptu})
    return base_url + query

# 1. Databáze receptů s reálnými odkazy na vyhledání přímo daného jídla na Cookidoo
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {"nazev": "Ovesná kaše", "kcal": 380, "link": make_cookidoo_link("Ovesná kaše")},
            {"nazev": "Míchaná vajíčka", "kcal": 410, "link": make_cookidoo_link("Míchaná vajíčka")},
            {"nazev": "Smoothie bowl", "kcal": 350, "link": make_cookidoo_link("Smoothie bowl")},
            {"nazev": "Domácí granola", "kcal": 390, "link": make_cookidoo_link("Granola")},
            {"nazev": "Nadýchané lívance", "kcal": 430, "link": make_cookidoo_link("Lívance")},
        ],
        "Svačina 1": [
            {"nazev": "Jablečné pyré", "kcal": 200, "link": make_cookidoo_link("Jablečné pyré")},
            {"nazev": "Proteinový koktejl", "kcal": 220, "link": make_cookidoo_link("Proteinový koktejl")},
            {"nazev": "Mrkvový salát s jablkem", "kcal": 180, "link": make_cookidoo_link("Mrkvový salát s jablkem")},
        ],
        "Oběd": [
            {"nazev": "Dýňová krémová polévka", "kcal": 350, "link": make_cookidoo_link("Dýňová krémová polévka")},
            {"nazev": "Losos s brokolicí a bramborem", "kcal": 680, "link": make_cookidoo_link("Losos s brokolicí")},
            {"nazev": "Hovězí guláš", "kcal": 720, "link": make_cookidoo_link("Hovězí guláš")},
            {"nazev": "Rizoto s houbami", "kcal": 610, "link": make_cookidoo_link("Rizoto s houbami")},
            {"nazev": "Svíčková na smetaně", "kcal": 750, "link": make_cookidoo_link("Svíčková na smetaně")},
        ],
        "Svačina 2": [
            {"nazev": "Kefírové smoothie", "kcal": 190, "link": make_cookidoo_link("Kefírové smoothie")},
            {"nazev": "Hummus se zeleninou", "kcal": 230, "link": make_cookidoo_link("Hummus")},
        ],
        "Večeře": [
            {"nazev": "Zeleninový krém", "kcal": 450, "link": make_cookidoo_link("Zeleninový krém")},
            {"nazev": "Těstoviny s rajčatovou omáčkou", "kcal": 520, "link": make_cookidoo_link("Těstoviny s rajčatovou omáčkou")},
            {"nazev": "Salát s grilovaným sýrem Halloumi", "kcal": 490, "link": make_cookidoo_link("Halloumi salát")},
            {"nazev": "Pečená zelenina s tvarohem", "kcal": 430, "link": make_cookidoo_link("Pečená zelenina")},
        ]
    }

# 2. Postranní panel
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

# 3. Formulář pro přidání receptu
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept z Cookidoo"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Název jídla")
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)
    novy_link_vstup = st.text_input("Odkaz na Cookidoo (nepovinné)")
    
    if st.button("Uložit recept"):
        if novy_nazev:
            # Pokud uživatel nevloží přesný odkaz, vygeneruje se automaticky vyhledávací
            finilni_link = novy_link_vstup if novy_link_vstup.strip() else make_cookidoo_link(novy_nazev)
            
            st.session_state.recepty_db[novy_kat].append({
                "nazev": novy_nazev,
                "kcal": nove_kcal,
                "link": finilni_link
            })
            st.success(f"Recept **{novy_nazev}** byl přidán!")
        else:
            st.warning("Vyplňte prosím název jídla.")

# 4. Hlavní část
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
                st.info(f"**{recept['nazev']}**\n\n🔥 ~{recept['kcal']} kcal\n\n[📖 Otevřít v Cookidoo]({recept['link']})")

chody_dne = ["Snídaně", "Oběd", "Večeře"] if pocet_jidel == 3 else ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]

dny_v_tydnu = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
zalozky = st.tabs(dny_v_tydnu)

for idx, tab in enumerate(zalozky):
    with tab:
        st.write(f"#### Plán na {dny_v_tydnu[idx]}")
        zobraz_den(chody_dne)
