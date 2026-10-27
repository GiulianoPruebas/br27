import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options(); o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for a in ("--headless=new","--window-size=1200,1800","--allow-file-access-from-files"): o.add_argument(a)
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o); root = pathlib.Path("..").resolve()
for p in ("1-plan","2-presupuesto","3-vuelos-logistica"):
    d.get((root/f"{p}.html").as_uri())
    print(p, [l["message"] for l in d.get_log("browser") if l["level"] == "SEVERE"], len(d.find_element("tag name","body").text))
    d.save_screenshot(f"shot_{p}.png")
d.quit()
