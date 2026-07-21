import React, { useState, useMemo } from "react";

/* --------------------------------------------------------- 
Databáze receptů — reálné recepty a odkazy z cookidoo.cz 
(kalorie u receptů bez zveřejněné nutriční hodnoty jsou 
orientační odhady, přesná data ukáže Cookidoo po přihlášení) 
kategorie: snidane | obed | vecere | svacina 
--------------------------------------------------------- */ 
const RECIPES = [ 
// SNÍDANĚ 
{ id: "s1", cat: "snidane", name: "Ovesná kaše se skořicí", kcal: 320, icon: "🥣", url: "https://cookidoo.cz/recipes/recipe/cs/r73547" }, 
{ id: "s2", cat: "snidane", name: "Ovesná kaše s ovocem", kcal: 300, icon: "🍓", url: "https://cookidoo.cz/recipes/recipe/cs/r73425" }, 
{ id: "s3", cat: "snidane", name: "Jablečná ovesná kaše", kcal: 300, icon: "🍎", url: "https://cookidoo.cz/recipes/recipe/cs/r133742" }, 
{ id: "s4", cat: "snidane", name: "Vločková kaše", kcal: 280, icon: "🥄", url: "https://cookidoo.cz/recipes/recipe/cs/r87338" }, 
{ id: "s5", cat: "snidane", name: "Ovocný dezert s bílým jogurtem a domácí granolou", kcal: 629, icon: "🍇", url: "https://cookidoo.cz/recipes/recipe/cs/r177499" }, 
{ id: "s6", cat: "snidane", name: "Banánový jogurt", kcal: 395, icon: "🍌", url: "https://cookidoo.cz/recipes/recipe/cs/r73426" }, 
{ id: "s7", cat: "snidane", name: "Toust s avokádem a vejcem Benedikt", kcal: 420, icon: "🥑", url: "https://cookidoo.cz/recipes/recipe/cs/r548454" }, 
{ id: "s8", cat: "snidane", name: "Španělská bramborová omeleta", kcal: 481, icon: "🍳", url: "https://cookidoo.cz/recipes/recipe/cs/r70468" },

// OBĚD 
{ id: "o1", cat: "obed", name: "Kuřecí prsa v jogurtové omáčce s bramborami", kcal: 375, icon: "🍗", url: "https://cookidoo.cz/recipes/recipe/cs/r67384" }, 
{ id: "o2", cat: "obed", name: "Kuře po asijsku s rýží a zeleninou", kcal: 560, icon: "🍚", url: "https://cookidoo.cz/recipes/recipe/cs/r113021" }, 
{ id: "o3", cat: "obed", name: "Hovězí guláš s kulatými houskovými knedlíky", kcal: 554, icon: "🍲", url: "https://cookidoo.cz/recipes/recipe/cs/r134686" }, 
{ id: "o4", cat: "obed", name: "Klasický maďarský guláš", kcal: 420, icon: "🥘", url: "https://cookidoo.cz/recipes/recipe/cs/r134656" }, 
{ id: "o5", cat: "obed", name: "Losos s bramborami, brokolicí a koprovou omáčkou", kcal: 520, icon: "🐟", url: "https://cookidoo.cz/recipes/recipe/cs/r815752" }, 
{ id: "o6", cat: "obed", name: "Losos se zeleninou a kuskusem", kcal: 393, icon: "🥗", url: "https://cookidoo.cz/recipes/recipe/cs/r154943" }, 
{ id: "o7", cat: "obed", name: "Krůtí špíz s rýží a zeleninovou omáčkou", kcal: 480, icon: "🍢", url: "https://cookidoo.cz/recipes/recipe/cs/r69952" }, 
{ id: "o8", cat: "obed", name: "Kuřecí se zeleninou, rýží a teriyaki omáčkou v páře", kcal: 540, icon: "🥦", url: "https://cookidoo.cz/recipes/recipe/cs/r302491" },

// VEČEŘE 
{ id: "v1", cat: "vecere", name: "Losos s bramborovou kaší", kcal: 221, icon: "🐟", url: "https://cookidoo.cz/recipes/recipe/cs/r87071" }, 
{ id: "v2", cat: "vecere", name: "Krémová zeleninová polévka", kcal: 90, icon: "🍵", url: "https://cookidoo.cz/recipes/recipe/cs/r55011" }, 
{ id: "v3", cat: "vecere", name: "Bílá zelná polévka se šťouchanými brambory", kcal: 192, icon: "🥣", url: "https://cookidoo.cz/recipes/recipe/cs/r72362" }, 
{ id: "v4", cat: "vecere", name: "Zeleninová polévka s těstovinami", kcal: 160, icon: "🍝", url: "https://cookidoo.cz/recipes/recipe/cs/r418225" }, 
{ id: "v5", cat: "vecere", name: "Čočková polévka s rajčaty", kcal: 254, icon: "🍅", url: "https://cookidoo.cz/recipes/recipe/cs/r86542" }, 
{ id: "v6", cat: "vecere", name: "Krémová polévka z červené čočky", kcal: 272, icon: "🥕", url: "https://cookidoo.cz/recipes/recipe/cs/r785604" }, 
{ id: "v7", cat: "vecere", name: "Bramborová kaše s medvědím česnekem a hořčičným máslem", kcal: 498, icon: "🧈", url: "https://cookidoo.cz/recipes/recipe/cs/r725086" }, 
{ id: "v8", cat: "vecere", name: "Bramborovo-dýňová kaše", kcal: 312, icon: "🎃", url: "https://cookidoo.cz/recipes/recipe/cs/r265473" },

// SVAČINY 
{ id: "sv1", cat: "svacina", name: "Jahodovo-jogurtové smoothie s chia semínky", kcal: 87, icon: "🍓", url: "https://cookidoo.cz/recipes/recipe/cs/r177507" }, 
{ id: "sv2", cat: "svacina", name: "Kokosový jogurt (veganský)", kcal: 190, icon: "🥥", url: "https://cookidoo.cz/recipes/recipe/cs/r539672" }, 
{ id: "sv3", cat: "svacina", name: "Studená okurková polévka s bílým jogurtem a avokádem", kcal: 191, icon: "🥒", url: "https://cookidoo.cz/recipes/recipe/cs/r177503" }, 
{ id: "sv4", cat: "svacina", name: "Veganská pěna s banány a avokádem", kcal: 267, icon: "🍌", url: "https://cookidoo.cz/recipes/recipe/cs/r761186" }, 
{ id: "sv5", cat: "svacina", name: "Domácí jogurt zalitý horkým ovocem", kcal: 191, icon: "🫐", url: "https://cookidoo.cz/recipes/recipe/cs/r122393" }, 
{ id: "sv6", cat: "svacina", name: "Bramborová kaše (malá porce)", kcal: 200, icon: "🥔", url: "https://cookidoo.cz/recipes/recipe/cs/r770148" }, 
];

const ACTIVITY = { 
zadna: { label: "Žádná aktivita", desc: "sedavé zaměstnání, minimum pohybu", factor: 1.2, icon: "🛋️" }, 
mirna: { label: "Mírná aktivita", desc: "lehký pohyb / sport 1–3× týdně", factor: 1.375, icon: "🚶" }, 
velka: { label: "Velká aktivita", desc: "sport 4–6× týdně / fyzická práce", factor: 1.55, icon: "🏃" }, 
};

const PLAN_3 = [ 
{ key: "snidane", cat: "snidane", label: "Snídaně", icon: "🌅", share: 0.3 }, 
{ key: "obed", cat: "obed", label: "Oběd", icon: "☀️", share: 0.4 }, 
{ key: "vecere", cat: "vecere", label: "Večeře", icon: "🌙", share: 0.3 }, 
];

const PLAN_5 = [ 
{ key: "snidane", cat: "snidane", label: "Snídaně", icon: "🌅", share: 0.25 }, 
{ key: "sv1", cat: "svacina", label: "Dopolední svačina", icon: "🍎", share: 0.1 }, 
{ key: "obed", cat: "obed", label: "Oběd", icon: "☀️", share: 0.35 }, 
{ key: "sv2", cat: "svacina", label: "Odpolední svačina", icon: "🥨", share: 0.1 }, 
{ key: "vecere", cat: "vecere", label: "Večeře", icon: "🌙", share: 0.2 }, 
];

function toNum(v, fallback) { 
const n = parseFloat(v); 
return Number.isFinite(n) ? n : fallback; 
}

function bmr({ gender, age, weight, height }) { 
const base = 10 * toNum(weight, 0) + 6.25 * toNum(height, 0) - 5 * toNum(age, 0); 
return gender = "muz" ? base + 5 : base - 161; 
}

function pickThree(cat, target, usedIds) { 
const pool = RECIPES.filter((r) => r.cat = cat); 
const sorted = [...pool].sort( 
(a, b) => Math.abs(a.kcal - target) - Math.abs(b.kcal - target) 
); 
const fresh = sorted.filter((r) => !usedIds.has(r.id)); 
const ordered = [...fresh, ...sorted.filter((r) => usedIds.has(r.id))]; 
const chosen = ordered.slice(0, 3); 
chosen.forEach((r) => usedIds.add(r.id)); 
return chosen; 
}

function portionNote(recipeKcal, target) { 
const ratio = target / recipeKcal; 
const rounded = Math.round(ratio * 4) / 4; 
const clamped = Math.min(2, Math.max(0.5, rounded)); 
return clamped = 1 ? "odpovídá 1 porci" : doporučená porce ${clamped}×; 
}

/* Číselné pole, které nezobrazuje nulu na začátku a dovolí 
pole dočasně smazat, aniž by tam blikla 0 / 
function NumberField({ label, value, onChange, min, max, suffix }) { 
return ( 
<div className="field"> 
<label className="label">{label}</label> 
<div className="numWrap"> 
<input 
type="text" 
inputMode="numeric" 
pattern="[0-9]" 
value={value} 
min={min} 
max={max} 
onChange={(e) => { 
const raw = e.target.value.replace(/[^\d]/g, ""); 
const stripped = raw.replace(/^0+(?=\d)/, ""); 
onChange(stripped); 
}} 
onBlur={(e) => { 
if (e.target.value = "") onChange(String(min)); 
}} 
className="input" 
/> 
{suffix && <span className="suffix">{suffix}</span>} 
</div> 
</div> 
); 
}

export default function App() { 
const [form, setForm] = useState({ 
gender: "zena", 
age: "30", 
weight: "65", 
height: "168", 
activity: "mirna", 
mealsPerDay: 3, 
}); 
const [selections, setSelections] = useState({}); 
const [showPlan, setShowPlan] = useState(false);

const results = useMemo(() => { 
const base = bmr(form); 
const t
