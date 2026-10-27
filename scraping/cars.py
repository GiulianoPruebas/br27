import sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options(); o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for a in ("--headless=new","--window-size=1400,3500","--lang=es-AR","--disable-gpu"): o.add_argument(a)
d = webdriver.Chrome(options=o); d.get(sys.argv[1]); time.sleep(int(sys.argv[3]) if len(sys.argv)>3 else 14)
open(sys.argv[2],"w",encoding="utf-8").write(d.find_element("tag name","body").text); d.save_screenshot(sys.argv[2].replace(".txt",".png")); d.quit()
