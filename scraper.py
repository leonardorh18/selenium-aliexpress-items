from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd

today = date.today()

option = Options()
option.headless = False 
driver = webdriver.Chrome(options = option)
produtos = []

itens= ["fone de ouvido bluetooth", 'ssd', 'carregador']


for item in itens:
    item = item.replace(" ", "+")
    for page in range(1,11): #paginas 1 a 10
        print(f"PAGE {page}")
        url = f"https://pt.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText={item}&ltype=wholesale&SortType=default&page={page}"

        driver.get(url)
        elements = driver.find_elements(By.CLASS_NAME, "_3GR-w")


        for el in elements:
            el_html = el.get_attribute('outerHTML')
            el_html =  BeautifulSoup(el_html, 'html.parser')
            
            titulo = el.find_element(By.CLASS_NAME, '_18_85').text
            print("titulo", titulo)
            preco = el_html.find('div', {'class': 'mGXnE _37W_B'}).text
            print("preco", preco)
            try:
                vendidos = el.find_element(By.CLASS_NAME, '_1kNf9').text
            except:
                vendidos = 0
            print("vendidos", vendidos)
            try:
                rating = el.find_element(By.CLASS_NAME, 'eXPaM').text
            except:
                rating = 0
            print("rating", rating)
            try:
                frete = el.find_element(By.CLASS_NAME, '_2jcMA').text
            except:
                frete = 0
                
            print("frete", frete)
            loja = el.find_element(By.CLASS_NAME, 'ox0KZ').text
            print("loja", loja)
            produtos.append([titulo, preco, vendidos, rating, frete, loja, item])
        
    csv = pd.DataFrame(produtos, columns = ['titulo', 
                                            'preco',
                                            'vendidos',
                                            'rating',
                                            'frete',
                                            'loja', 
                                            'busca'])
csv.to_csv("aliexpress.csv")