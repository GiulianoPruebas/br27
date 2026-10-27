import pathlib, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o = Options(); o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
o.add_argument("--headless=new"); o.add_argument("--window-size=420,900"); o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
d = webdriver.Chrome(options=o); url = (pathlib.Path("..").resolve()/"index.html").as_uri(); d.get(url); time.sleep(2)
pp = lambda: d.execute_script("return document.getElementById('oPP').textContent")
a = pp()
d.execute_script("document.querySelector('#gSeg button[data-n=\"12\"]').click()"); b = pp()
d.execute_script("document.querySelectorAll('#stRio .opt')[5].click()"); c = pp()
d.execute_script("document.querySelector('#stCar .opt[data-id=\"spin\"]').click()"); e = pp()
d.execute_script("document.querySelector('#cSeg button[data-c=\"ars\"]').click()"); f = pp()
print("8p:", a, "| 12p:", b, "| Rio premium:", c, "| 2 Spin:", e, "| ARS:", f)
h = d.execute_script("return location.hash"); print(h)
d.get(url + h); d.execute_script("location.reload()"); time.sleep(2); print("reload:", pp(), d.execute_script("return document.querySelectorAll('#gSeg button.on')[0].dataset.n"))
print([l["message"] for l in d.get_log("browser") if l["level"] == "SEVERE"]); d.quit()
