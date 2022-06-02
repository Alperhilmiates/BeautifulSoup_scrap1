from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
google_doc_link = "https://docs.google.com/forms/d/e/1FAIpQLSc4VDvNMRrk12nt0kO3c8qk6nWHmn9J_snLk4jn0QQ2ntkc6g/viewform?usp=sf_link"
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
chrome_driver = Service(executable_path= "/Users/hilmialperates/development_alper/chromedriver")
#scrolling = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div/div[1]")
responde = requests.get(zillow_link, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"})
respo_txt = responde.text
webscrape = BeautifulSoup(respo_txt, "html.parser")
find_den = webscrape.select(selector="article a", class_=".list-card-link.list-card-link-top-margin", href=True)
find_adress = webscrape.select(selector="article address", class_="list-card-addr")
find_adress2 = webscrape.select(".list-card-info address")
find_price = webscrape.find_all(name="div", class_="list-card-price")
links_list = []
adress_list = []
price_list = []
for n in find_den:
    den = n.get("href")
    if den[0] == "h":
        links_list.append(den)
    else:
        marge = "https://www.zillow.com/" + den
        links_list.append(marge)
for adress in find_adress:
    adr1 = adress.text
    adress_list.append(adr1)
all_addresses = [address.get_text().split(" | ")[-1] for address in find_adress2]
for price in find_price:
    price_total = int(price.text[1]) * 1000 + int(price.text[3]) * 100 + int(price.text[4]) * 10 + int(
        price.text[5])
    price_list.append(price_total)
print(links_list)
print(adress_list)
print(price_list)
#verical_ordinate = 300
#driver.execute_script("arguments[0].scrollTop = arguments[1]", scrolling, verical_ordinate)
#verical_ordinate += 300

class Excel():
    def __init__(self):
        self.driver = webdriver.Chrome(service=chrome_driver)
    def data(self,veri):
        self.driver.get("https://docs.google.com/forms/d/e/1FAIpQLSc4VDvNMRrk12nt0kO3c8qk6nWHmn9J_snLk4jn0QQ2ntkc6g/viewform?usp=sf_link")
        time.sleep(3)
        adress_pro = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
        adress_pro.send_keys(adress_list[veri])
        price_pro = self.driver.find_element(By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
        price_pro.send_keys(price_list[veri])
        link_pro = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
        link_pro.send_keys(links_list[veri])
        gonder = self.driver.find_element(By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span")
        gonder.click()
    def quit(self):
        self.driver.quit()
#deneme = Excel()
#range_list = len(price_list)
#for n in range (0,range_list):
    #deneme.data(n)
#deneme.quit()




