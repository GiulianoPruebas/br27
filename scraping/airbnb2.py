import sys, time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
place, ci, co, adults, minbd, out = sys.argv[1:7]
o = Options(); o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for a in ("--headless=new","--window-size=1400,3000","--lang=es-AR","--disable-gpu"): o.add_argument(a)
d = webdriver.Chrome(options=o)
d.get(f"https://www.airbnb.com.ar/s/{place}/homes?checkin={ci}&checkout={co}&adults={adults}&min_bedrooms={minbd}&currency=USD")
time.sleep(9)
for y in (1200,2400,3600,4800,6000): d.execute_script(f"window.scrollTo(0,{y})"); time.sleep(1.2)
js = """return [...document.querySelectorAll('[data-testid="card-container"]')].map(c=>({href:(c.querySelector('a[href*="/rooms/"]')||{}).href,text:c.innerText,imgs:[...c.querySelectorAll('img')].map(i=>i.src).filter(s=>s.includes('muscache'))}))"""
json.dump(d.execute_script(js), open(out,"w",encoding="utf-8"), ensure_ascii=False)
d.quit()
