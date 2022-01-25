# %%
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# %%
options = Options()
options.page_load_strategy = 'none'
options.add_argument("--headless")
driver = webdriver.Chrome()

url_template = 'https://www.vivareal.com.br/venda/rj/rio-de-janeiro/apartamento_residencial/?pagina='
parte2 = '#onde=BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro,BR-Rio_de_Janeiro-NULL-Rio_de_Janeiro-Zona_Sul-Ipanema'

# %%
imoveis = []

for page_number in range(1, 82):
    try:
        url = url_template + str(page_number) + parte2
        page = driver.get(url)

        sleep(10)
        print('-'*40)
        print(page_number)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        todos_elementos = soup.find_all(
            class_='property-card__container js-property-card')

        for elemento in todos_elementos:
            imovel = {}

            imovel['endereco'] = elemento.find(
                class_='property-card__address').getText()

            try:
                valor_imovel = float(elemento.find(
                    class_='property-card__price js-property-card-prices js-property-card__price-small').getText().split()[1].replace('.', ''))
            except:
                valor_imovel = 0.0

            imovel['valor'] = valor_imovel

            imovel['detalhes'] = elemento.find(class_ = 'property-card__details').getText()

            imovel['pagina'] = page_number

            try:
                imovel['extra'] = elemento.find(class_ = 'property-card__amenities').getText()
            except:
                imovel['extra'] = 0

            imoveis.append(imovel)
    except:
        pass

# %%
dataset = pd.DataFrame(imoveis)
dataset.to_csv('Dataset_imoveis.csv', sep=';', index=False)
driver.close()

# %%
