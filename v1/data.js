// Datos del viaje + calc() compartidos por las 3 paginas. Fuentes y fechas en 3-vuelos-logistica.html.
// "REAL" = leido el 26/10/2026 (Google Flights / Airbnb via Selenium, ANP, open.er-api). "EST" = estimacion editable.
const D = {
  fx: { brl: 4.995, ars: 1575 },                       // REAL: open.er-api 26/10/2026 / dolarapi blue
  groups: [4, 8, 12],
  // vuelos solo-ida por persona, USD (REAL, Google Flights, consulta 26/10/2026)
  out: [
    { id: "gol2300",  label: "Gol 23:00 AEP→GIG (llega 01:50 del 2/4)", usd: 338, ok: true },
    { id: "jet1555",  label: "JetSMART 15:55 AEP→GIG (llega 18:50) · NO cumple >20 h", usd: 236, ok: false },
    { id: "lat1455",  label: "LATAM 14:55 AEP→GIG · NO cumple >20 h", usd: 306, ok: false },
    { id: "aer1730",  label: "Aerolíneas 17:30 AEP→GIG · NO cumple >20 h", usd: 421, ok: false },
  ],
  ret: [
    { id: "jet2005", label: "JetSMART 20:05 GIG→AEP (llega 23:33)", usd: 171, ok: true },
    { id: "gol1735", label: "Gol 17:35 GIG→AEP (llega 21:00)", usd: 181, ok: true },
    { id: "jet1600", label: "JetSMART 16:00 GIG→AEP (llega 19:20)", usd: 171, ok: true },
    { id: "aer2115", label: "Aerolíneas/Gol 21:15 GIG→AEP (llega 00:40 del 12/4)", usd: 181, ok: true },
    { id: "aer1555", label: "Aerolíneas 15:55 GIG→AEP (llega 19:20)", usd: 197, ok: true },
  ],
  // alojamiento USD/noche TOTAL del grupo (REAL: Airbnb, todo incluido, mediana "med" y percentil 25 "econ")
  lodging: {
    rio:     { 4: { econ: 82,  med: 102 }, 8: { econ: 211, med: 230 }, 12: { econ: 428, med: 519 } },
    arraial: { 4: { econ: 91,  med: 132 }, 8: { econ: 112, med: 130 }, 12: { econ: 186, med: 286 } },
    buzios:  { 4: { econ: 68,  med: 102 }, 8: { econ: 148, med: 192 }, 12: { econ: 275, med: 326 } },
  },
  nights: { rio: 6, arraial: 2, buzios: 2 },           // 1-5/4 (4), 5-7 Arraial, 7-9 Búzios, 9-11 Rio (2)
  // tramos en auto (km REAL de guias; peajes BRL por auto: Arraial REAL R$13,65 + puente Rio-Niterói EST)
  legs: [
    { name: "Rio (Copacabana) → Arraial do Cabo", km: 165, toll: 21 },
    { name: "Arraial: Pontal, Forno, Prainhas (local)", km: 25, toll: 0 },
    { name: "Arraial → Búzios (por Cabo Frío)", km: 55, toll: 0 },
    { name: "Búzios: Geribá, João Fernandes, Ferradura (local)", km: 40, toll: 0 },
    { name: "Búzios → Rio (Ponte Rio-Niterói)", km: 170, toll: 30 },
  ],
  // actividades: BRL por persona (Cristo REAL; resto EST)
  acts: [
    { id: "cristo", label: "Cristo Redentor (van Paineiras)", brl: 87, on: true },
    { id: "pao",    label: "Pão de Açúcar (bondinho)", brl: 190, on: true },
    { id: "arr",    label: "Barco Arraial: Prainhas/Gruta Azul/Farol", brl: 150, on: true },
    { id: "buz",    label: "Barco/goleta Búzios", brl: 120, on: true },
    { id: "ilha",   label: "Dois Irmãos / Parque Lage / Jardim Botânico", brl: 40, on: true },
  ],
  food:  { econ: 25, med: 40, alto: 60 },               // USD por persona por dia (EST sobre almuerzo R$40-60, cena 2 pers. R$204)
};

const ceil4 = n => Math.ceil(n / 4);

// p: {outId, retId, bag, lodg:'econ'|'med', food:'econ'|'med'|'alto', night, carDay, carDays, kml, fuel, ubDay, seguro, sim, cont, acts:{id:bool}, legs:[km,toll]}
function calc(n, p) {
  const f = D.fx, cars = ceil4(n), L = [];
  const add = (cat, label, usd) => L.push({ cat, label, usd });
  const o = D.out.find(x => x.id === p.outId), r = D.ret.find(x => x.id === p.retId);
  add("Vuelos", `Ida ${o.label.split(" (")[0]} ×${n}`, o.usd * n);
  add("Vuelos", `Vuelta ${r.label.split(" (")[0]} ×${n}`, r.usd * n);
  if (p.bag) add("Vuelos", `Equipaje despachado ×${n} (EST)`, p.bag * n);
  for (const k of ["rio", "arraial", "buzios"])
    add("Alojamiento", `${k} ${D.nights[k]} noches`, D.lodging[k][n][p.lodg] * D.nights[k]);
  const dias = 10;
  add("Comida", `${dias} días × ${n} pers`, D.food[p.food] * dias * n);
  add("Joda", `3 noches (entradas+tragos) × ${n}`, p.night * 3 * n);
  const km = p.legs.reduce((s, l) => s + l[0], 0), toll = p.legs.reduce((s, l) => s + l[1], 0);
  add("Auto", `${cars} auto(s) × ${p.carDays} días`, cars * p.carDays * p.carDay);
  add("Nafta", `${km} km ÷ ${p.kml} km/l × R$${p.fuel} × ${cars} auto(s)`, cars * km / p.kml * p.fuel / f.brl);
  add("Peajes", `R$${toll} × ${cars} auto(s)`, cars * toll / f.brl);
  add("Uber Rio", `6 días × ${cars} auto-equiv. + 4 traslados aeropuerto`, cars * (6 * p.ubDay + 4 * 20));
  add("Actividades", "entradas y tours", D.acts.filter(a => p.acts[a.id]).reduce((s, a) => s + a.brl, 0) / f.brl * n);
  if (p.seguro) add("Extras", `Asistencia médica ×${n}`, p.seguro * n);
  add("Extras", `eSIM ×${n}`, p.sim * n);
  const sub = L.reduce((s, x) => s + x.usd, 0);
  add("Imprevistos", `${p.cont}%`, sub * p.cont / 100);
  return { L, km, toll, cars, total: sub * (1 + p.cont / 100) };
}

const DEF = { outId: "gol2300", retId: "jet2005", bag: 70, lodg: "med", food: "med", night: 35, carDay: 45, carDays: 4,
  kml: 11, fuel: 6.4, ubDay: 18, seguro: 45, sim: 12, cont: 10, acts: Object.fromEntries(D.acts.map(a => [a.id, a.on])),
  legs: D.legs.map(l => [l.km, l.toll]) };

const usd = x => "USD " + Math.round(x).toLocaleString("es-AR");
const ars = x => "$ " + Math.round(x * D.fx.ars).toLocaleString("es-AR");

// self-check: corre con `node data.js`
if (typeof module === "undefined" && typeof window === "undefined" || typeof process !== "undefined" && process.argv[1]?.endsWith("data.js")) {
  const t = D.groups.map(n => calc(n, DEF).total);
  console.assert(t[0] < t[1] && t[1] < t[2], "el total debe crecer con el grupo");
  console.assert(calc(4, DEF).cars === 1 && calc(12, DEF).cars === 3, "autos = ceil(n/4)");
  console.log(D.groups.map((n, i) => `${n}p: ${usd(t[i])} (${usd(t[i] / n)} c/u)`).join(" | "));
}
