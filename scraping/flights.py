import sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options()
o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for a in ("--headless=new","--window-size=1400,3000","--lang=es-AR","--disable-gpu"): o.add_argument(a)
d = webdriver.Chrome(options=o)
url = sys.argv[1]; out = sys.argv[2]
d.get(url); time.sleep(12)
open(out,"w",encoding="utf-8").write(d.find_element("tag name","body").text)
d.save_screenshot(out.replace(".txt",".png"))
d.quit()
