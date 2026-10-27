import sys, time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options()
o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for a in ("--headless=new","--window-size=1400,4000","--lang=es-AR","--disable-gpu"): o.add_argument(a)
d = webdriver.Chrome(options=o)
place, ci, co, adults, out = sys.argv[1:6]
d.get(f"https://www.airbnb.com.ar/s/{place}/homes?checkin={ci}&checkout={co}&adults={adults}&currency=USD&price_filter_num_nights={(int(co[8:])-int(ci[8:]))}")
time.sleep(10); d.execute_script("window.scrollTo(0,3000)"); time.sleep(3)
open(out,"w",encoding="utf-8").write(d.find_element("tag name","body").text)
d.quit()
