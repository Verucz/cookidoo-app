import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# Pomocná funkce pro vyhledávání na Cookidoo (fallback, pokud recept nemá přímý odkaz)
def cookidoo_search(dotaz):
    encoded = urllib.parse.quote(dotaz)
    return f"https://cookidoo.cz/search/cs?context=recipes&query={encoded}"

# 1. Velká databáze receptů - nyní s přímými odkazy na konkrétní recepty na Cookidoo
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = {
        "Snídaně": [
            {"nazev": "Nadýchané americké palačinky (Pancakes)", "kcal": 430, "link": "https://cookidoo.cz/recipes/recipe/cs/r88410"},
            {"nazev": "Palačinky (Crêpes)", "kcal": 380, "link": "https://cookidoo.cz/recipes/recipe/cs/r54963"},
            {"nazev": "Palačinky s tvarohem", "kcal": 400, "link": "https://cookidoo.cz/recipes/recipe/cs/r52523"},
            {"nazev": "Čokoládové palačinky", "kcal": 420, "link": "https://cookidoo.cz/recipes/recipe/cs/r73428"},
            {"nazev": "Palačinky z ovesných otrub a tvarohu", "kcal": 360, "link": "https://cookidoo.cz/recipes/recipe/cs/r178395"},
            {"nazev": "Crêpes Suzette (palačinky podle Suzette)", "kcal": 410, "link": "https://cookidoo.cz/recipes/recipe/cs/r178389"},
            {"nazev": "Krupicová kaše pro děti", "kcal": 340, "link": "https://cookidoo.cz/recipes/recipe/cs/r73541"},
            {"nazev": "Bílý a kokosový jogurt", "kcal": 200, "link": "https://cookidoo.cz/recipes/recipe/cs/r6875"},
            {"nazev": "Jogurtovo-citrónové muffiny", "kcal": 207, "link": "https://cookidoo.cz/recipes/recipe/cs/r93006"},
            {"nazev": "Pomerančovo-brusinkové muffiny", "kcal": 250, "link": "https://cookidoo.cz/recipes/recipe/cs/r93011"},
            {"nazev": "Rýžová kaše s jablky a tvarohem", "kcal": 350, "link": cookidoo_search("Rýžová kaše s jablky a tvarohem")},
            {"nazev": "Shakshuka", "kcal": 380, "link": cookidoo_search("Shakshuka")},
            {"nazev": "Avokádový toast s vejcem", "kcal": 410, "link": cookidoo_search("Avokádový toast s vejcem")}
        ],
        "Svačina 1": [
            {"nazev": "Kozí jogurt", "kcal": 150, "link": "https://cookidoo.cz/recipes/recipe/cs/r539669"},
            {"nazev": "Kokosový jogurt (veganský)", "kcal": 190, "link": "https://cookidoo.cz/recipes/recipe/cs/r539672"},
            {"nazev": "Jahodovo-jogurtové smoothie s chia semínky", "kcal": 210, "link": "https://cookidoo.cz/recipes/recipe/cs/r177507"},
            {"nazev": "Banánové smoothie s arašídy a jogurtem", "kcal": 368, "link": "https://cookidoo.cz/recipes/recipe/cs/r122391"},
            {"nazev": "Banánovo-čokoládové muffiny", "kcal": 280, "link": "https://cookidoo.cz/recipes/recipe/cs/r812011"},
            {"nazev": "Muffiny s čokoládovými kousky", "kcal": 270, "link": "https://cookidoo.cz/recipes/recipe/cs/r54988"},
            {"nazev": "Pečená jablka s ořechy", "kcal": 200, "link": cookidoo_search("Pečená jablka s ořechy")},
            {"nazev": "Chia pudink s ovocem", "kcal": 230, "link": cookidoo_search("Chia pudink s ovocem")}
        ],
        "Oběd": [
            {"nazev": "Drůbeží guláš s knedlíkem", "kcal": 620, "link": "https://cookidoo.cz/recipes/recipe/cs/r58189"},
            {"nazev": "Bramborový guláš", "kcal": 351, "link": "https://cookidoo.cz/recipes/recipe/cs/r365840"},
            {"nazev": "Guláš z vepřové panenky", "kcal": 640, "link": "https://cookidoo.cz/recipes/recipe/cs/r710014"},
            {"nazev": "Guláš se středozemní zeleninou", "kcal": 480, "link": "https://cookidoo.cz/recipes/recipe/cs/r134669"},
            {"nazev": "Zabijačkový guláš s knedlíkem", "kcal": 700, "link": "https://cookidoo.cz/recipes/recipe/cs/r73546"},
            {"nazev": "Čočkový guláš se slaninou a chorizem", "kcal": 590, "link": "https://cookidoo.cz/recipes/recipe/cs/r134781"},
            {"nazev": "Hovězí guláš s kulatými houskovými knedlíky", "kcal": 710, "link": "https://cookidoo.cz/recipes/recipe/cs/r134686"},
            {"nazev": "Kari kuře se žampióny a basmati rýží", "kcal": 610, "link": "https://cookidoo.cz/recipes/recipe/cs/r91869"},
            {"nazev": "Marocké kuřecí maso s kuskusem", "kcal": 580, "link": "https://cookidoo.cz/recipes/recipe/cs/r771394"},
            {"nazev": "Kuřecí kousky s mandlemi a rýží", "kcal": 560, "link": "https://cookidoo.cz/recipes/recipe/cs/r67383"},
            {"nazev": "Trhané kuřecí maso v tortille s avokádem a čedarem", "kcal": 630, "link": "https://cookidoo.cz/recipes/recipe/cs/r236960"},
            {"nazev": "Kuřecí kousky s paprikami a rýží", "kcal": 540, "link": "https://cookidoo.cz/recipes/recipe/cs/r496504"},
            {"nazev": "Kuřecí ragú se špenátovou rýží", "kcal": 570, "link": "https://cookidoo.cz/recipes/recipe/cs/r115310"},
            {"nazev": "Kuře po asijsku s rýží a zeleninou", "kcal": 600, "link": "https://cookidoo.cz/recipes/recipe/cs/r113021"},
            {"nazev": "Losos en crôute s citrónovým rizotem", "kcal": 763, "link": "https://cookidoo.cz/recipes/recipe/cs/r132025"},
            {"nazev": "Lososové rizoto s fenyklem", "kcal": 618, "link": "https://cookidoo.cz/recipes/recipe/cs/r132020"},
            {"nazev": "Rizoto s dýní a uzeným lososem", "kcal": 430, "link": "https://cookidoo.cz/recipes/recipe/cs/r152804"},
            {"nazev": "Losos se špenátem a divokou rýží", "kcal": 590, "link": "https://cookidoo.cz/recipes/recipe/cs/r67379"},
            {"nazev": "Zámecké rizoto", "kcal": 550, "link": "https://cookidoo.cz/recipes/recipe/cs/r139563"},
            {"nazev": "Pivní rizoto s houbami", "kcal": 520, "link": "https://cookidoo.cz/recipes/recipe/cs/r151751"}
        ],
        "Svačina 2": [
            {"nazev": "Česnekovo sýrová pomazánka", "kcal": 250, "link": "https://cookidoo.cz/recipes/recipe/cs/r52644"},
            {"nazev": "Liptovská pomazánka", "kcal": 230, "link": "https://cookidoo.cz/recipes/recipe/cs/r69983"},
            {"nazev": "Pomazánka s čedarem a česnekem", "kcal": 260, "link": "https://cookidoo.cz/recipes/recipe/cs/r152535"},
            {"nazev": "Pomazánka z makrely", "kcal": 240, "link": "https://cookidoo.cz/recipes/recipe/cs/r70166"},
            {"nazev": "Pomazánka z rybiček v tomatové omáčce", "kcal": 220, "link": "https://cookidoo.cz/recipes/recipe/cs/r52556"},
            {"nazev": "Avokádová pomazánka", "kcal": 210, "link": "https://cookidoo.cz/recipes/recipe/cs/r773884"},
            {"nazev": "Pomazánka z čabajky nebo loveckého salámu", "kcal": 260, "link": "https://cookidoo.cz/recipes/recipe/cs/r67018"},
            {"nazev": "Vaječná pomazánka s cibulí", "kcal": 220, "link": "https://cookidoo.cz/recipes/recipe/cs/r69969"},
            {"nazev": "Cizrnová pomazánka (Hummus)", "kcal": 230, "link": "https://cookidoo.cz/recipes/recipe/cs/r87099"}
        ],
        "Večeře": [
            {"nazev": "Polévka Tom Yum", "kcal": 250, "link": "https://cookidoo.cz/recipes/recipe/cs/r150774"},
            {"nazev": "Cizrnová polévka s listovým špenátem", "kcal": 320, "link": "https://cookidoo.cz/recipes/recipe/cs/r616374"},
            {"nazev": "Polévka z červených paprik a cuket", "kcal": 300, "link": "https://cookidoo.cz/recipes/recipe/cs/r120817"},
            {"nazev": "Chřestová polévka s rukolou a bazalkou", "kcal": 290, "link": "https://cookidoo.cz/recipes/recipe/cs/r337674"},
            {"nazev": "Celerová polévka se zakysanou smetanou", "kcal": 310, "link": "https://cookidoo.cz/recipes/recipe/cs/r98089"},
            {"nazev": "Polévka z máslové dýně s kokosovým mlékem", "kcal": 340, "link": "https://cookidoo.cz/recipes/recipe/cs/r659068"},
            {"nazev": "Čočková polévka", "kcal": 380, "link": "https://cookidoo.cz/recipes/recipe/cs/r52548"},
            {"nazev": "Hrstková polévka", "kcal": 350, "link": "https://cookidoo.cz/recipes/recipe/cs/r759531"},
            {"nazev": "Špenátové rizoto", "kcal": 460, "link": "https://cookidoo.cz/recipes/recipe/cs/r139574"},
            {"nazev": "Rizoto s paprikami a tuňákem", "kcal": 470, "link": "https://cookidoo.cz/recipes/recipe/cs/r139565"},
            {"nazev": "Kuřecí nudličky v rajčatové šťávě s bramborovými plátky", "kcal": 420, "link": "https://cookidoo.cz/recipes/recipe/cs/r69975"},
            {"nazev": "Kuřecí se zeleninou, rýží, medovou teriyaki omáčkou a brokolicí v páře", "kcal": 450, "link": "https://cookidoo.cz/recipes/recipe/cs/r302491"},
            {"nazev": "Losos v balíčku se sušenými rajčaty a kuskusem", "kcal": 430, "link": "https://cookidoo.cz/recipes/recipe/cs/r132024"},
            {"nazev": "Minestrone polévka", "kcal": 380, "link": cookidoo_search("Minestrone polévka")},
            {"nazev": "Frittata se zeleninou a sýrem", "kcal": 410, "link": cookidoo_search("Frittata se zeleninou a sýrem")}
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

# 3. Formulář pro přikládání vlastních receptů
st.sidebar.markdown("---")
with st.sidebar.expander("➕ Přidat vlastní recept z Cookidoo"):
    novy_kat = st.selectbox("Kategorie", ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"])
    novy_nazev = st.text_input("Název jídla")
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)
    novy_link_vstup = st.text_input("Přímý URL odkaz (nebo nechte prázdné pro automatické vyhledání)")

    if st.button("Uložit recept"):
        if novy_nazev:
            finalni_link = novy_link_vstup.strip() if novy_link_vstup.strip() else cookidoo_search(novy_nazev)
            st.session_state.recepty_db[novy_kat].append({
                "nazev": novy_nazev.strip(),
                "kcal": nove_kcal,
                "link": finalni_link
            })
            st.success(f"Recept **{novy_nazev}** byl úspěšně přidán!")
        else:
            st.warning("Vyplňte prosím název jídla.")

# 4. Hlavní zobrazení
if st.button("🎲 Vygenerovat nový týdenní plán"):
    st.rerun()

st.subheader("📅 Váš jídelníček na tento týden")

# Funkce zobrazující 3 náhodné možnosti z rozsáhlé databáze
def zobraz_den(chody):
    for chod in chody:
        st.write(f"### {chod}")
        dostupne_recepty = st.session_state.recepty_db[chod]

        pocet_moznosti = min(3, len(dostupne_recepty))
        moznosti = random.sample(dostupne_recepty, pocet_moznosti)

        cols = st.columns(3)
        for i, recept in enumerate(moznosti):
            with cols[i]:
                st.info(f"**{recept['nazev']}**\n\n🔥 ~{recept['kcal']} kcal\n\n[📖 Otevřít recept na Cookidoo]({recept['link']})")

chody_dne = ["Snídaně", "Oběd", "Večeře"] if pocet_jidel == 3 else ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]

dny_v_tydnu = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
zalozky = st.tabs(dny_v_tydnu)

for idx, tab in enumerate(zalozky):
    with tab:
        st.write(f"#### Plán na {dny_v_tydnu[idx]}")
        zobraz_den(chody_dne)
