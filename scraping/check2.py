import pathlib, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options(); o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for a in ("--headless=new","--window-size=1200,1500"): o.add_argument(a)
o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o); d.get((pathlib.Path("..").resolve()/"index.html").as_uri()); time.sleep(1)
d.save_screenshot("s_plan.png")
for t in ("lugares","vuelos","auto","presu","check"):
    d.execute_script(f"go('{t}')"); time.sleep(.6)
    if t=="presu": d.execute_script("document.querySelector('#gSeg button[data-n=\"12\"]').click();document.querySelectorAll('#presets .chip')[2].click()")
    if t=="lugares": d.execute_script("document.querySelector('.pl').click();document.querySelector('.star').click()")
    d.save_screenshot(f"s_{t}.png")
print([l["message"] for l in d.get_log("browser") if l["level"]=="SEVERE"]); d.quit()
