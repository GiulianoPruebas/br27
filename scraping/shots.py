import pathlib, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options(); o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
o.add_experimental_option("mobileEmulation", {"deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 2}, "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1"})
o.add_argument("--headless=new"); o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o); d.get((pathlib.Path("..").resolve()/"index.html").as_uri()); time.sleep(3)
def shot(name, y=None, sel=None):
    if sel: d.execute_script("document.querySelector(arguments[0]).scrollIntoView({block:'start'})", sel)
    elif y is not None: d.execute_script(f"window.scrollTo(0,{y})")
    time.sleep(1.4); d.save_screenshot(f"m_{name}.png")
shot("hero", 0)
jt = d.execute_script("return document.getElementById('journey').offsetTop"); jh = d.execute_script("return document.getElementById('journey').offsetHeight-innerHeight")
shot("tag", sel="#tagline"); shot("j1", jt+jh*0.5); shot("dias", sel="#days")
shot("stays", sel="#stRio"); shot("cars", sel="#stCar"); shot("offer", sel="#oferta")
print(d.execute_script("return [document.getElementById('fromPrice').textContent, document.getElementById('oPP').textContent, document.body.scrollWidth, innerWidth]"))
print([l["message"] for l in d.get_log("browser") if l["level"] == "SEVERE"]); d.quit()
