from bs4 import BeautifulSoup
import requests
import time
import csv

set_card_count = 0
is_next_card = True
is_valid = False

def take_mtg_set():
    global is_valid
    while is_valid == False:
        mtg_set = input("What MTG set would you like to pull? e.g. \"M21\": ")
        mtg_set = mtg_set.lower()
        if len(mtg_set) != 3:
            print("Sorry, the MTG set must be a 3 letter set code e.g. \"M21\".")
            continue
        if not mtg_set.isalnum():
            print("Sorry, the MTG set must only contain letters and numbers.") 
            continue
        is_valid = True
        generate_url(mtg_set)

def generate_url(mtg_set):
    while is_next_card == True:
        global set_card_count
        set_card_count = set_card_count + 1
        current_card = set_card_count
        url = "https://scryfall.com/card/" + mtg_set + "/" + str(current_card)
        read_html(url, current_card)

def read_html(url, card):
    print("Scraping website.. Card #: " + str(card))
    result = requests.get(url).text
    soup = BeautifulSoup(result, features="html.parser")
    scrape_card_info(soup)

def scrape_card_info(soup):
    title_string = soup.find("title").string
    if title_string != "Not Found · Scryfall Magic: The Gathering Search":
        global set_card_count
        card_name = title_string[0:(title_string.index("·")) - 1]
        card_set = title_string[(title_string.index("·") + 2):title_string.index(")") + 1]
        card_value = soup.find("meta", attrs={"name": "twitter:data2"})
        write_to_csv(card_name, card_set, card_value["content"])
    else:
        print("It looks like there are no more cards in the set..")
        global is_next_card
        is_next_card = False
    time.sleep(1)

def total_card_value():
    with open("cardlist.csv") as csv_file:
        total = 0
        for row in csv.reader(csv_file):
            total += float(row[2][1:])
        value = float(format(total, ".2f"))
        value_dollar = "${:.2f}".format(value)
    return(value_dollar)

def average_card_value():
    with open("cardlist.csv") as csv_file:
        total = 0
        rowcount = 0
        for row in csv.reader(csv_file):
            total += float(row[2][1:])
            rowcount+= 1
        value = float(format(total, ".2f"))
        average_value = value / rowcount
        value_dollar = "${:.2f}".format(average_value)
    return(value_dollar)

def lowest_card_value():
    with open("cardlist.csv") as csv_file:
        min_card_value = 10000000.00
        for row in csv.reader(csv_file):
            if float(row[2][1:]) < min_card_value:
                min_card_value = float(row[2][1:])
                max_card_value_name = row[0]
            value_dollar = "${:.2f}".format(min_card_value)
    return(max_card_value_name + " · " + value_dollar)

def highest_card_value():
    with open("cardlist.csv") as csv_file:
        max_card_value = 0.00
        max_card_value_name = ""
        for row in csv.reader(csv_file):
            if float(row[2][1:]) > max_card_value:
                max_card_value = float(row[2][1:])
                max_card_value_name = row[0]
            value_dollar = "${:.2f}".format(max_card_value)
    return(max_card_value_name + " · " + value_dollar)

def write_to_csv(card_name, card_set, card_value):
    with open ("cardlist.csv", "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([card_name, card_set, card_value])
    csv_file.close()

def main():
    #take_mtg_set()
    print("The total value of all cards is: " + total_card_value())
    print("The average value of a card is: " + average_card_value())
    print("The lowest value card is: " + lowest_card_value())
    print("The highest value card is: " + highest_card_value())

if __name__ == "__main__":
    main()










    