import os
import requests
import sys
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def search(product):
    ruta = os.getcwd()
    global browser
    driver_path = "{}\chromedriver.exe".format(ruta)
    browser = webdriver.Chrome(driver_path)


    browser.get('https://www.ebay.com/')

    browser.find_element(By.ID, "gh-ac").send_keys(product)
    browser.find_element(By.ID, "gh-btn").click()

def get_page_data(product):
    print("Please hold!")
    f = open("{} pricing.txt".format(product), 'w+', encoding="utf-8")

    for i in range (1,10):
        url = browser.current_url + str (i)
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        listings = soup.findAll("div", {"class":"s-item__wrapper clearfix"})[1:]

        for listing in listings:
            title = listing.find('div', {'class' : 's-item__title'})
            price = listing.find("span", class_="s-item__price")
            st.write(title.text + ":  " + price.text + "\n\n")
    f.close
    print("We have queried all your search results!")


def main():
    inp = True
    while inp:
        query = st.text_input('Search Query', "")
        st.write('What would you like to search for?\n',query)
        search(query)
        userInput = input ("Is this what you wanted to search for?\n").capitalize()
        if userInput == "No":
            query = input("What would you like to search for?\n").capitalize()
            search(query)
            inp = True
        elif userInput == "Yes":
            get_page_data(query)
            inp = False
        else:
            userInput = input("I'm sorry, we could not understand your request, please try again!").capitalize()

        userInput = input("Would you like to search another term?").capitalize()
        if userInput == "Yes":
            inp = True
        else:
            inp = False
    print("Thank you for using the Ebay Webscraper!  Goodbye!")
    sys.exit()




if __name__ == "__main__":
    main()