import requests
import urlparse
from argparse import ArgumentParser
from bs4 import BeautifulSoup

def extract_page_contacts(url):
	print "Parsing: %s" %(url)
	r = requests.get(url)
	page_html = BeautifulSoup(r.content, "lxml")

	items = page_html.find_all("div", {"class":"vcard"})
	for item in items:

		print "---------------"
		name = item.find("span", {"itemprop":"name"}).text.strip()
		print "Nome: %s" %(name)
		
		address = item.find("span", {"itemprop":"streetAddress"})
		if address:
			print "Indirizzo: %s" %(address.text.strip())
		else:
			address = ""
		
		postalCode = item.find("span", {"itemprop":"postalCode"})
		if postalCode:
			print "CAP: %s" %(postalCode.text.strip())
		else:
			postalCode = ""
		
		addressLocality = item.find("span", {"itemprop":"addressLocality"})
		if addressLocality:
			print "Citta: %s" %(addressLocality.text.strip())
		else:
			addressLocality = ""

                addressRegion = item.find("span", {"itemprop":"addressRegion"})
                if addressRegion:
                        print "Provincia: %s" %(addressRegion.text.strip())
                else:
                        addressRegion = ""
		
		telephone = item.find("div", {"itemprop":"telephone"})
		if telephone:
			print "Telefono: %s" %(telephone.text.strip())
		else:
			telephone = ""
		
	for next_button in page_html.find_all("a", {"class":"rightArrowBtn"}, href=True):
		next_button['href'] = urlparse.urljoin(url,next_button['href'])
		extract_page_contacts(next_button['href'])

parser = ArgumentParser()
parser.add_argument('-c', '--cosa', dest='cosa', help='Nome azienda, attivita o categoria da cercare')
parser.add_argument('-d', '--dove', dest='dove', help='Localita, indirizzo da cercare')
args = parser.parse_args()

url = "http://www.paginegialle.it/pgol/4-%s/3-%s?mr=50" %(args.cosa, args.dove)
extract_page_contacts(url)
