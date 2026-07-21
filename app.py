{\rtf1\ansi\ansicpg1252\cocoartf2905
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs26 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import streamlit as st\
import random\
\
st.set_page_config(page_title="Thermomix J\'eddeln\'ed\uc0\u269 ek", page_icon="\u55356 \u57202 ", layout="wide")\
\
st.title("\uc0\u55356 \u57202  Thermomix & Cookidoo Pl\'e1nova\u269  J\'eddeln\'ed\u269 ku")\
\
# 1. Datab\'e1ze recept\uc0\u367  (Ulo\'9een\'e1 ve st.session_state, aby do n\'ed \'9alo p\u345 id\'e1vat za chodu)\
if "recepty_db" not in st.session_state:\
    st.session_state.recepty_db = \{\
        "Sn\'eddan\uc0\u283 ": [\
            \{"nazev": "Ovesn\'e1 ka\'9ae s jablky a sko\uc0\u345 ic\'ed", "kcal": 380, "link": "https://cookidoo.cz"\},\
            \{"nazev": "M\'edchan\'e1 vaj\'ed\uc0\u269 ka z Varomy", "kcal": 410, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Smoothie bowl s lesn\'edm ovocem", "kcal": 350, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Dom\'e1c\'ed granola s \uc0\u345 eck\'fdm jogurtem", "kcal": 390, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Nad\'fdchan\'e9 l\'edvance z Thermomixu", "kcal": 430, "link": "https://cookidoo.cz"\},\
        ],\
        "Sva\uc0\u269 ina 1": [\
            \{"nazev": "Jable\uc0\u269 n\'e9 pyr\'e9 s o\u345 echy", "kcal": 200, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Proteinov\'fd koktejl s ban\'e1nem", "kcal": 220, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Mrkvov\'fd sal\'e1t s jablkem", "kcal": 180, "link": "https://cookidoo.cz"\},\
        ],\
        "Ob\uc0\u283 d": [\
            \{"nazev": "D\'fd\uc0\u328 ov\'e1 kr\'e9mov\'e1 pol\'e9vka + Ku\u345 ec\'ed prsa v pari", "kcal": 650, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Losos s brokolic\'ed a bramborem z Varomy", "kcal": 680, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Hov\uc0\u283 z\'ed gul\'e1\'9a z Thermomixu", "kcal": 720, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Rizoto s houbami a parmaz\'e1nem", "kcal": 610, "link": "https://cookidoo.cz"\},\
        ],\
        "Sva\uc0\u269 ina 2": [\
            \{"nazev": "Kef\'edrov\'e9 smoothie s bor\uc0\u367 vkami", "kcal": 190, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Kr\'e1jen\'e1 zelenina s hummusem", "kcal": 230, "link": "https://cookidoo.cz"\},\
        ],\
        "Ve\uc0\u269 e\u345 e": [\
            \{"nazev": "Zeleninov\'fd kr\'e9m s krutony", "kcal": 450, "link": "https://cookidoo.cz"\},\
            \{"nazev": "T\uc0\u283 stoviny s raj\u269 atovou om\'e1\u269 kou a bazalkou", "kcal": 520, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Sal\'e1t s grilovan\'fdm s\'fdrem Halloumi", "kcal": 490, "link": "https://cookidoo.cz"\},\
            \{"nazev": "Pe\uc0\u269 en\'e1 zelenina s tvarohem", "kcal": 430, "link": "https://cookidoo.cz"\},\
        ]\
    \}\
\
# 2. Postrann\'ed panel - Vstupy od u\'9eivatele\
st.sidebar.header("\uc0\u9881 \u65039  Va\'9ae parametry")\
\
pohlavi = st.sidebar.selectbox("Pohlav\'ed", ["\'8eena", "Mu\'9e"])\
vek = st.sidebar.number_input("V\uc0\u283 k", min_value=15, max_value=100, value=30)\
vaha = st.sidebar.number_input("V\'e1ha (kg)", min_value=40.0, max_value=200.0, value=65.0)\
vyska = st.sidebar.number_input("V\'fd\'9aka (cm)", min_value=130, max_value=220, value=170)\
\
aktivity_dict = \{\
    "Sedav\'e9 zam\uc0\u283 stn\'e1n\'ed (minim\'e1ln\'ed pohyb)": 1.2,\
    "Lehk\'e1 aktivita (1-3x t\'fddn\uc0\u283  cvi\u269 en\'ed)": 1.375,\
    "St\uc0\u345 edn\'ed aktivita (3-5x t\'fddn\u283  cvi\u269 en\'ed)": 1.55,\
    "Vysok\'e1 aktivita (6-7x t\'fddn\uc0\u283  n\'e1ro\u269 n\'fd sport)": 1.725\
\}\
\
aktivita = st.sidebar.selectbox("\'darove\uc0\u328  aktivity", list(aktivity_dict.keys()))\
pocet_jidel = st.sidebar.radio("Po\uc0\u269 et j\'eddel denn\u283 ", [3, 5], index=0)\
\
# V\'fdpo\uc0\u269 et BMR a TDEE\
if pohlavi == "Mu\'9e":\
    bmr = 10 * vaha + 6.25 * vyska - 5 * vek + 5\
else:\
    bmr = 10 * vaha + 6.25 * vyska - 5 * vek - 161\
\
tdee = round(bmr * aktivity_dict[aktivita])\
\
st.sidebar.markdown("---")\
st.sidebar.metric("V\'e1\'9a denn\'ed c\'edlov\'fd p\uc0\u345 \'edjem", f"\{tdee\} kcal")\
\
# 3. Formul\'e1\uc0\u345  pro p\u345 id\'e1n\'ed nov\'e9ho receptu do datab\'e1ze p\u345 \'edmo v aplikaci\
st.sidebar.markdown("---")\
with st.sidebar.expander("\uc0\u10133  P\u345 idat vlastn\'ed recept z Cookidoo"):\
    novy_kat = st.selectbox("Kategorie", ["Sn\'eddan\uc0\u283 ", "Sva\u269 ina 1", "Ob\u283 d", "Sva\u269 ina 2", "Ve\u269 e\u345 e"])\
    novy_nazev = st.text_input("N\'e1zev j\'eddla")\
    nove_kcal = st.number_input("Kalorie (kcal)", min_value=50, max_value=2000, value=400)\
    novy_link = st.text_input("Odkaz na Cookidoo", value="https://cookidoo.cz")\
    \
    if st.button("Ulo\'9eit recept"):\
        if novy_nazev:\
            st.session_state.recepty_db[novy_kat].append(\{\
                "nazev": novy_nazev,\
                "kcal": nove_kcal,\
                "link": novy_link\
            \})\
            st.success(f"Recept **\{novy_nazev\}** byl p\uc0\u345 id\'e1n!")\
        else:\
            st.warning("Vypl\uc0\u328 te pros\'edm n\'e1zev j\'eddla.")\
\
# 4. Hlavn\'ed \uc0\u269 \'e1st - Tla\u269 \'edtko pro nov\'fd v\'fdb\u283 r a T\'fddenn\'ed z\'e1lo\'9eky\
if st.button("\uc0\u55356 \u57266  Vygenerovat nov\'fd t\'fddenn\'ed pl\'e1n"):\
    st.rerun()\
\
st.subheader("\uc0\u55357 \u56517  V\'e1\'9a j\'eddeln\'ed\u269 ek na tento t\'fdden")\
\
# Pomocn\'e1 funkce pro zobrazen\'ed jednoho dne\
def zobraz_den(chody):\
    for chod in chody:\
        st.write(f"### \{chod\}")\
        dostupne_recepty = st.session_state.recepty_db[chod]\
        moznosti = random.sample(dostupne_recepty, min(3, len(dostupne_recepty)))\
        cols = st.columns(len(moznosti))\
        for i, recept in enumerate(moznosti):\
            with cols[i]:\
                st.info(f"**\{recept['nazev']\}**\\n\\n\uc0\u55357 \u56613  ~\{recept['kcal']\} kcal\\n\\n[\u55357 \u56534  Otev\u345 \'edt v Cookidoo](\{recept['link']\})")\
\
# Definice chod\uc0\u367 \
chody_dne = ["Sn\'eddan\uc0\u283 ", "Ob\u283 d", "Ve\u269 e\u345 e"] if pocet_jidel == 3 else ["Sn\'eddan\u283 ", "Sva\u269 ina 1", "Ob\u283 d", "Sva\u269 ina 2", "Ve\u269 e\u345 e"]\
\
# Tvorba t\'fddenn\'edch z\'e1lo\'9eek (Tabs)\
dny_v_tydnu = ["Pond\uc0\u283 l\'ed", "\'dater\'fd", "St\u345 eda", "\u268 tvrtek", "P\'e1tek", "Sobota", "Ned\u283 le"]\
zalozky = st.tabs(dny_v_tydnu)\
\
for idx, tab in enumerate(zalozky):\
    with tab:\
        st.write(f"#### Pl\'e1n na \{dny_v_tydnu[idx]\}")\
        zobraz_den(chody_dne)}