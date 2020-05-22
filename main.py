import requests
from bs4 import BeautifulSoup
import re

print("What would you like to shop for today?")
print("Input your items one at a time and type 'quit' when you are done!\n")

file = "groceries.csv"
f = open(file, "w+")

labels = "ITEM, NAME, AMOUNT, PRICE, UNIT PRICE\n"
f.write(labels)

while True:
    search = input("Add an item: ") 

    if search != "quit":
        params = {"q": search}
        r = requests.get("https://www.heb.com/search", params = params)

        #if website is not responsive
        if r.status_code != 200:
            print("Website is down. Please try again later.")    
            break     
        
        #collects all items from search results 
        soup = BeautifulSoup(r.text, "html.parser")
        item_list = soup.findAll("li", {"class": \
            "responsivegriditem product-grid-large-fifth product-grid-small-6"})\
                [:4] #gets first 5 items in search (for relevancy; # can be changed)
        
        #if no results found
        if (len(item_list) == 0):
            print("Item cannot be found.\n")

        else: 
            for item in item_list: 
                name = item.a.span.text.strip()
                name = re.sub(",", ";", name)
                index = name.rfind(';')
                item_name = name[0:index] #splits unit size from name
                
                unit_size = name[index+1:len(name)]

                prices_by_item = item.findAll("span", \
                    {"class": "cat-price-number"})
                price = prices_by_item[0].text.strip()

                #exception block for items that do not have a unit price
                try:
                    unit_prices = item.findAll("span", {"class": "uomSalePrice"})
                    per_unit = unit_prices[0].text.strip()
                except:
                    per_unit = "N/A"
                            
                f.write(search + "," + item_name + "," + unit_size + "," \
                    + price + "," + per_unit + "\n")
                search = "" #leaves blank cell under ITEMS column after first iteration (for looks)
        
            print("Successfully added.\n")

    #exits program if user quits
    else:
        print("\nThanks for shopping! Check out your groceries.csv file.")
        break
