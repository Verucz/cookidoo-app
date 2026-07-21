import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Thermomix Jídelníček", page_icon="🍲", layout="wide")

st.title("🍲 Thermomix & Cookidoo Plánovač Jídelníčku")

# Pomocná funkce pro vyhledávání na Cookidoo
def cookidoo_search(dotaz):
    encoded = urllib.parse.quote(dotaz)
    return f"https://cookidoo.cz/search/cs?context=recipes&query={encoded}"

# Funkce pro vygenerování rozsáhlé databáze (100+ receptů pro každou kategorii)
@st.cache_data
def nacti_velkou_databazi():
    db = {
        "Snídaně": [
            {"nazev": "Nadýchané americké palačinky (Pancakes)", "kcal": 430, "link": "https://cookidoo.cz/recipes/recipe/cs/r88410"},
            {"nazev": "Palačinky (Crêpes)", "kcal": 380, "link": "https://cookidoo.cz/recipes/recipe/cs/r54963"},
            {"nazev": "Palačinky s tvarohem", "kcal": 400, "link": "https://cookidoo.cz/recipes/recipe/cs/r52523"},
            {"nazev": "Čokoládové palačinky", "kcal": 420, "link": "https://cookidoo.cz/recipes/recipe/cs/r73428"},
            {"nazev": "Palačinky z ovesných otrub a tvarohu", "kcal": 360, "link": "https://cookidoo.cz/recipes/recipe/cs/r178395"},
            {"nazev": "Crêpes Suzette", "kcal": 410, "link": "https://cookidoo.cz/recipes/recipe/cs/r178389"},
            {"nazev": "Krupicová kaše pro děti", "kcal": 340, "link": "https://cookidoo.cz/recipes/recipe/cs/r73541"},
            {"nazev": "Bílý a kokosový jogurt", "kcal": 200, "link": "https://cookidoo.cz/recipes/recipe/cs/r6875"},
            {"nazev": "Jogurtovo-citrónové muffiny", "kcal": 207, "link": "https://cookidoo.cz/recipes/recipe/cs/r93006"},
            {"nazev": "Pomerančovo-brusinkové muffiny", "kcal": 250, "link": "https://cookidoo.cz/recipes/recipe/cs/r93011"}
        ],
        "Svačina 1": [
            {"nazev": "Kozí jogurt", "kcal": 150, "link": "https://cookidoo.cz/recipes/recipe/cs/r539669"},
            {"nazev": "Kokosový jogurt (veganský)", "kcal": 190, "link": "https://cookidoo.cz/recipes/recipe/cs/r539672"},
            {"nazev": "Jahodovo-jogurtové smoothie s chia", "kcal": 210, "link": "https://cookidoo.cz/recipes/recipe/cs/r177507"},
            {"nazev": "Banánové smoothie s arašídy", "kcal": 368, "link": "https://cookidoo.cz/recipes/recipe/cs/r122391"},
            {"nazev": "Banánovo-čokoládové muffiny", "kcal": 280, "link": "https://cookidoo.cz/recipes/recipe/cs/r812011"},
            {"nazev": "Muffiny s čokoládovými kousky", "kcal": 270, "link": "https://cookidoo.cz/recipes/recipe/cs/r54988"}
        ],
        "Oběd": [
            {"nazev": "Drůbeží guláš s knedlíkem", "kcal": 620, "link": "https://cookidoo.cz/recipes/recipe/cs/r58189"},
            {"nazev": "Bramborový guláš", "kcal": 351, "link": "https://cookidoo.cz/recipes/recipe/cs/r365840"},
            {"nazev": "Guláš z vepřové panenky", "kcal": 640, "link": "https://cookidoo.cz/recipes/recipe/cs/r710014"},
            {"nazev": "Guláš se středozemní zeleninou", "kcal": 480, "link": "https://cookidoo.cz/recipes/recipe/cs/r134669"},
            {"nazev": "Zabijačkový guláš s knedlíkem", "kcal": 700, "link": "https://cookidoo.cz/recipes/recipe/cs/r73546"},
            {"nazev": "Čočkový guláš se slaninou a chorizem", "kcal": 590, "link": "https://cookidoo.cz/recipes/recipe/cs/r134781"},
            {"nazev": "Hovězí guláš s houskovým knedlíkem", "kcal": 710, "link": "https://cookidoo.cz/recipes/recipe/cs/r134686"},
            {"nazev": "Kari kuře se žampióny a basmati rýží", "kcal": 610, "link": "https://cookidoo.cz/recipes/recipe/cs/r91869"},
            {"nazev": "Marocké kuřecí maso s kuskusem", "kcal": 580, "link": "https://cookidoo.cz/recipes/recipe/cs/r771394"},
            {"nazev": "Kuřecí kousky s mandlemi a rýží", "kcal": 560, "link": "https://cookidoo.cz/recipes/recipe/cs/r67383"},
            {"nazev": "Trhané kuřecí maso v tortille", "kcal": 630, "link": "https://cookidoo.cz/recipes/recipe/cs/r236960"},
            {"nazev": "Kuřecí kousky s paprikami a rýží", "kcal": 540, "link": "https://cookidoo.cz/recipes/recipe/cs/r496504"},
            {"nazev": "Kuřecí ragú se špenátovou rýží", "kcal": 570, "link": "https://cookidoo.cz/recipes/recipe/cs/r115310"},
            {"nazev": "Kuře po asijsku s rýží", "kcal": 600, "link": "https://cookidoo.cz/recipes/recipe/cs/r113021"},
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
            {"nazev": "Pomazánka z rybiček v tomatě", "kcal": 220, "link": "https://cookidoo.cz/recipes/recipe/cs/r52556"},
            {"nazev": "Avokádová pomazánka", "kcal": 210, "link": "https://cookidoo.cz/recipes/recipe/cs/r773884"},
            {"nazev": "Pomazánka z čabajky", "kcal": 260, "link": "https://cookidoo.cz/recipes/recipe/cs/r67018"},
            {"nazev": "Vaječná pomazánka s cibulí", "kcal": 220, "link": "https://cookidoo.cz/recipes/recipe/cs/r69969"},
            {"nazev": "Cizrnová pomazánka (Hummus)", "kcal": 230, "link": "https://cookidoo.cz/recipes/recipe/cs/r87099"}
        ],
        "Večeře": [
            {"nazev": "Polévka Tom Yum", "kcal": 250, "link": "https://cookidoo.cz/recipes/recipe/cs/r150774"},
            {"nazev": "Cizrnová polévka se špenátem", "kcal": 320, "link": "https://cookidoo.cz/recipes/recipe/cs/r616374"},
            {"nazev": "Polévka z červených paprik a cuket", "kcal": 300, "link": "https://cookidoo.cz/recipes/recipe/cs/r120817"},
            {"nazev": "Chřestová polévka s rukolou", "kcal": 290, "link": "https://cookidoo.cz/recipes/recipe/cs/r337674"},
            {"nazev": "Celerová polévka se smetanou", "kcal": 310, "link": "https://cookidoo.cz/recipes/recipe/cs/r98089"},
            {"nazev": "Polévka z dýně s kokosovým mlékem", "kcal": 340, "link": "https://cookidoo.cz/recipes/recipe/cs/r659068"},
            {"nazev": "Čočková polévka", "kcal": 380, "link": "https://cookidoo.cz/recipes/recipe/cs/r52548"},
            {"nazev": "Hrstková polévka", "kcal": 350, "link": "https://cookidoo.cz/recipes/recipe/cs/r759531"},
            {"nazev": "Špenátové rizoto", "kcal": 460, "link": "https://cookidoo.cz/recipes/recipe/cs/r139574"},
            {"nazev": "Rizoto s paprikami a tuňákem", "kcal": 470, "link": "https://cookidoo.cz/recipes/recipe/cs/r139565"},
            {"nazev": "Kuřecí nudličky v rajčatové šťávě", "kcal": 420, "link": "https://cookidoo.cz/recipes/recipe/cs/r69975"},
            {"nazev": "Kuřecí se zeleninou v teriyaki omáčce", "kcal": 450, "link": "https://cookidoo.cz/recipes/recipe/cs/r302491"},
            {"nazev": "Losos v balíčku s kuskusem", "kcal": 430, "link": "https://cookidoo.cz/recipes/recipe/cs/r132024"}
        ]
    }

    # Šablony pro vygenerování přes 100 receptů do každé kategorie
    sablony = {
        "Snídaně": [
            ("Ovesná kaše s {}", range(300, 420)),
            ("Krupicová kaše s {}", range(320, 450)),
            ("Pohanková kaše s {}", range(290, 390)),
            ("Rýžová kaše s {}", range(310, 410)),
            ("Lívance s {}", range(360, 480)),
            ("Palačinky s {}", range(350, 460)),
            ("Waffle s {}", range(380, 500)),
            ("Smoothie bowl s {}", range(280, 390)),
            ("Toast s {}", range(300, 450)),
            ("Míchaná vajíčka s {}", range(320, 440)),
            ("Omeleta s {}", range(330, 460)),
            ("Jogurt s {}", range(200, 350))
        ],
        "Svačina 1": [
            ("Smoothie s {}", range(150, 280)),
            ("Tvarohový krém s {}", range(180, 290)),
            ("Ovocný salát s {}", range(120, 220)),
            ("Chia pudink s {}", range(190, 310)),
            ("Muffin s {}", range(220, 330)),
            ("Pečené jablko s {}", range(160, 250)),
            ("Jogurtová pěna s {}", range(170, 260)),
            ("Kefírový nápoj s {}", range(140, 230))
        ],
        "Oběd": [
            ("Kuřecí plátky s {}", range(480, 680)),
            ("Hovězí guláš s {}", range(580, 780)),
            ("Vepřová panenka s {}", range(520, 710)),
            ("Losos na páře s {}", range(490, 660)),
            ("Rizoto s {}", range(450, 640)),
            ("Těstoviny s {}", range(500, 720)),
            ("Gnocchi s {}", range(520, 710)),
            ("Čočkový dhal s {}", range(420, 580)),
            ("Kari s {}", range(480, 660)),
            ("Špíz s {}", range(460, 650)),
            ("Slaný koláč s {}", range(530, 730))
        ],
        "Svačina 2": [
            ("Pomazánka z {}", range(180, 290)),
            ("Hummus s {}", range(200, 310)),
            ("Tvarohová pomazánka s {}", range(160, 260)),
            ("Salát s {}", range(170, 280)),
            ("Guacamole s {}", range(210, 320)),
            ("Pesto s {}", range(220, 340))
        ],
        "Večeře": [
            ("Krémová polévka z {}", range(250, 390)),
            ("Zeleninové rizoto s {}", range(380, 520)),
            ("Pečená zelenina s {}", range(320, 460)),
            ("Těstovinový salát s {}", range(400, 550)),
            ("Frittata s {}", range(350, 480)),
            ("Cuketové placky s {}", range(360, 490)),
            ("Kus-kus salát s {}", range(370, 510)),
            ("Zapékaná zelenina s {}", range(340, 470))
        ]
    }

    ingredience = [
        "jahodami", "borůvkami", "jablky", "banánem", "hruškami", "ořechy", "čokoládou", "medem", "skořicí",
        "malinami", "broskvemi", "tvarohem", "chia semínky", "kokosem", "sušeným ovocem", "brusinkami",
        "špenátem", "rajčaty", "paprikou", "cukotou", "dýní", "brokolicí", "květákem", "houbami", "česnekem",
        "bylinkami", "sýrem", "mozzarellou", "balkánským sýrem", "parmazánem", "tuňákem", "lososem",
        "kuřecím masem", "vepřovým masem", "hovězím masem", "slaninou", "šunkou", "avokádem", "kukuřicí",
        "hráškem", "mrkví", "celerem", "červenou řepou", "cizrnou", "čočkou", "fazolemi", "tofu", "pórkem"
    ]

    # Automatické dogenerování do počtu 110+ receptů na kategorii
    for kat, sablony_list in sablony.items():
        count = len(db[kat])
        for sablona, kcal_range in sablony_list:
            for ingr in ingredience:
                if count >= 115:
                    break
                nazev = sablona.format(ingr)
                # Ochrana proti duplicitám
                if not any(r["nazev"] == nazev for r in db[kat]):
                    db[kat].append({
                        "nazev": nazev,
                        "kcal": random.choice(list(kcal_range)),
                        "link": cookidoo_search(nazev)
                    })
                    count += 1
            if count >= 115:
                break

    return db

# 1. Inicializace databáze v session_state
if "recepty_db" not in st.session_state:
    st.session_state.recepty_db = nacti_velkou_databazi()

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

# Zobrazení statistik databáze v sidebaru
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Databáze receptů")
for kat, recepty in st.session_state.recepty_db.items():
    st.sidebar.text(f"{kat}: {len(recepty)} receptů")

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
            st.rerun()
        else:
            st.warning("Vyplňte prosím název jídla.")

# 4. Generování celého týdne zcela BEZ OPAKIVÁNÍ
dny_v_tydnu = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
chody_dne = ["Snídaně", "Oběd", "Večeře"] if pocet_jidel == 3 else ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]

if st.button("🎲 Vygenerovat nový týdenní plán") or "tydenni_plan" not in st.session_state:
    st.session_state.tydenni_plan = {}
    
    # Pro každý chod si vybereme 21 zcela unikátních receptů na celý týden (7 dní * 3 možnosti)
    vybrane_recepty_pro_chod = {}
    for chod in ["Snídaně", "Svačina 1", "Oběd", "Svačina 2", "Večeře"]:
        db = st.session_state.recepty_db[chod]
        potrebny_pocet = 7 * 3
        vybrane_recepty_pro_chod[chod] = random.sample(db, potrebny_pocet)

    # Rozřazení do dnů
    for i_den, den in enumerate(dny_v_tydnu):
        st.session_state.tydenni_plan[den] = {}
        for chod in chody_dne:
            start_idx = i_den * 3
            st.session_state.tydenni_plan[den][chod] = vybrane_recepty_pro_chod[chod][start_idx:start_idx + 3]

# 5. Hlavní zobrazení jídelníčku
st.subheader("📅 Váš jídelníček na tento týden")

zalozky = st.tabs(dny_v_tydnu)

for idx, tab in enumerate(zalozky):
    den_nazev = dny_v_tydnu[idx]
    with tab:
        st.write(f"#### Plán na {den_nazev}")
        for chod in chody_dne:
            st.write(f"### {chod}")
            moznosti = st.session_state.tydenni_plan[den_nazev][chod]
            
            cols = st.columns(3)
            for i, recept in enumerate(moznosti):
                with cols[i]:
                    st.info(f"**{recept['nazev']}**\n\n🔥 ~{recept['kcal']} kcal\n\n[📖 Otevřít recept na Cookidoo]({recept['link']})")
