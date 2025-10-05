import requests
from bs4 import BeautifulSoup

# Structure:
#

class Scrapper:

    def __init__(self) -> None:
        self.base_url = "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&disposition=DISP_3_KK&disposition=DISP_3_1&priceTo=31000&regionOsmIds=R439840&osm_value=Praha%2C+obvod+Praha+4%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&location=exact&currency=CZK&searchPriceWithCharges=true#lat=49.86&lng=14.8&zoom=6"
        self.header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}
        self.apartments = []

    def scrap_page(self):
        base_link = requests.get(self.base_url, headers=self.header)
        soup = BeautifulSoup(base_link.content, 'lxml')
        offers = soup.find_all('article', class_='PropertyCard_propertyCard__moO_5 propertyCard PropertyCard_propertyCard--landscape__XvPmC')
        for offer in offers:
            location = offer.find('span', class_='PropertyCard_propertyCardAddress__hNqyR text-subheadline text-truncate').text.strip()
            apt_type = offer.find('li', class_='FeaturesList_featuresListItem__RYf_f').text.strip()
            print(apt_type)
            rent = offer.find('span', class_='PropertyPrice_propertyPriceAmount__WdEE1')
            poplatky = offer.find("span", class_="PropertyPrice_propertyPriceAdditional__5jYQ6")
            rent = rent.text[:-3] if rent else "0"
            poplatky = poplatky.text[3:-3] if poplatky else "0"
            #total_rent = int(rent) + int(poplatky)
            print(int(rent))
            print(int(poplatky))
            


test = Scrapper()
test.scrap_page()