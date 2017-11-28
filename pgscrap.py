import requests
from urllib.parse import urlparse, urljoin
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from models.vcard import VCard

vcards = []

def extract_page_contacts(url):
    print ("Parsing: %s" %(url))
    r = requests.get(url)
    page_html = BeautifulSoup(r.content, "lxml")

    items = page_html.find_all("section", {"class":"vcard"})
	
    for item in items:
        vcard = VCard()
        
        vcard.name = item.find("h1", {"itemprop":"name"}).text.strip()
            
        _address = item.find("span", {"class":"street-address"})
        if _address:
            vcard.address = _address.text.strip()
            
        _postalCode = item.find("span", {"class":"postal-code"})
        if _postalCode:
            vcard.postalCode = _postalCode.text.strip()
        
        _locality = item.find("span", {"class":"locality"})
        if _locality:
            vcard.locality = _locality.text.strip()
        
        _region = item.find("span", {"class":"region"})
        if _region:
            vcard.region = _region.text.strip()
        
        _phoneNumbers = item.find("div", {"class":"phoneNumbers"})
        if _phoneNumbers:
            vcard.phoneNumbers = _phoneNumbers.text.strip()
        
        print (vcard)
		
		vcards.push(vcard.toJson())
        
    for next_button in page_html.find_all("a", {"class":"rightArrowBtn"}, href=True):
        next_button['href'] = urljoin(url,next_button['href'])
        extract_page_contacts(next_button['href'])

parser = ArgumentParser()
parser.add_argument('-c', '--cosa', dest='cosa', help='Nome azienda, attivita o categoria da cercare')
parser.add_argument('-d', '--dove', dest='dove', help='Localita, indirizzo da cercare')
args = parser.parse_args()

url = "https://www.paginegialle.it/ricerca/%s/%s?" %(args.cosa, args.dove)
extract_page_contacts(url)

print('[')
for v in vcards:
	print (v)
print(']')