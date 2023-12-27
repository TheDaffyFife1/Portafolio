#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import threading
import plotly.express as px
import xlsxwriter
import tempfile
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import csv
from itertools import zip_longest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, urlunparse
import pandas as pd
import re
import pymysql  # o el módulo que corresponda a tu base de datos
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import datetime
import mysql.connector
import facebook_scraper as fs
import tqdm as notebook_tqdm
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import sqlite3
from sqlalchemy import create_engine


# In[24]:


os.environ['GH_TOKEN'] = "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"
#Almacenamiento de variables del scrapper
original_data = pd.DataFrame() #Almacenamiento del link original
driver = None #Webdriver 
yesterday = datetime.date.today() - datetime.timedelta(days=1) #fecha que utiliza 
formatted_date = yesterday.strftime("%Y-%m-%d") #formato de fecha
url_original = '' 
compartida = []
link = []
linkactual = []
resultado = pd.DataFrame()
#variable nueva de comparacion de usuarios
comparaciones =[]


# In[25]:


lista = pd.read_csv('2023-11-28_links.csv')
print(lista)
# Supongamos que ya tienes un DataFrame llamado "lista"

# Verifica si la columna "URL_post" existe en el DataFrame
if "enlace" in lista.columns:
    # Extrae el contenido de la columna "URL_post" y guárdalo en una lista
    contenido_url_post = lista["enlace"].tolist()
    
    # contenido_url_post ahora contiene el contenido de la columna "URL_post" en forma de lista
else:
    print("La columna 'URL_post' no existe en el DataFrame.")
print(contenido_url_post)


# In[26]:


#Almacenamiento de los POST para compartidas y likes 
urls =contenido_url_post.copy()


# In[27]:


def open_browser():
    global driver 
    firefox_options = Options()
    firefox_options.add_argument('window-size=1280,800')
    firefox_options.add_argument('user-agent=mozilla/5.0 (windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/74.0.3729.169 Safari/537.36')

    # Use the GeckoDriverManager to automatically download and manage GeckoDriver
    driver_service = Service(GeckoDriverManager().install())

    # Create the Firefox WebDriver without specifying executable_path
    driver = webdriver.Firefox(service=driver_service, options=firefox_options)


    driver.get("https://www.facebook.com/")
    username = driver.find_element(By.XPATH, '//input[@type="text"]')
    username.send_keys("riltuvirdo@gufum.com") #alondra.rosas75@kewip.com
    password = driver.find_element(By.XPATH, '//input[@type="password"]')
    password.send_keys("Operador03") #alo12375
    login = driver.find_element(By.XPATH, '//button[@name="login"]')
    login.click()
    WebDriverWait(driver, 10).until(EC.url_contains("facebook.com"))
    return driver


# In[28]:


def scrapper_completo(driver,urls):
    for url_original in urls:
        parsed_url = urlparse(url_original)
        new_netloc = parsed_url.netloc.replace("www.", "mbasic.")
        modified_url = urlunparse(parsed_url._replace(netloc=new_netloc))

        time.sleep(30)
        driver.get(modified_url)
        time.sleep(30)

        try:
            like = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/div/a/div')
            like.click()
            time.sleep(10)
            nueva_url = driver.current_url
            print(nueva_url)
        except NoSuchElementException:
                # Si no se encuentra el elemento 'like', imprime un mensaje de error y pasa al siguiente enlace.
            try:
                likes = driver.find_element(By.XPATH, '//*[contains(@id, "like_")]/a[position() = 1]')
                likes.click()
                time.sleep(10)
                like = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/div/a/div')
                like.click()
                time.sleep(10)
                nueva_url = driver.current_url
                print(nueva_url)
            except NoSuchElementException:
                # Si no se encuentra el elemento 'like' con ninguno de los dos xpaths, imprime un mensaje de error y pasa al siguiente enlace.
                print("Elemento 'like' no encontrado en", modified_url)
                continue
            except ElementClickInterceptedException:
                print("No se puede hacer clic en el elemento 'like'. Saltando al siguiente enlace.")
                # Puedes agregar aquí cualquier lógica adicional que necesites cuando no se puede hacer clic en el elemento.
                continue
        except ElementClickInterceptedException:
            print("No se puede hacer clic en el elemento 'like'. Saltando al siguiente enlace.")
            # Puedes agregar aquí cualquier lógica adicional que necesites cuando no se puede hacer clic en el elemento.
            continue

        time.sleep(40)
        parsed_modified_url = urlparse(nueva_url)
        new_netloc2 = parsed_modified_url.netloc.replace("mbasic.", "m.")
        modified_url2 = urlunparse(parsed_modified_url._replace(netloc=new_netloc2))
        print(modified_url2)
        driver.get(modified_url2)
        linkactual.append(modified_url2)
        time.sleep(30)
        def get():
            while True:
                try:
                    # Recopilar los elementos antes de intentar hacer clic en "ver más"
                    likes = driver.find_elements(By.XPATH, '//*[@id="reaction_profile_browser"]/div/div/div//a')

                    for i in likes:
                        enlace = i.get_attribute('href')
                        texto = i.text
                        max_url_length = 255
                        link.append({'url_like': url_original[:max_url_length], 'usuario': texto, 'link': enlace, 'fecha': formatted_date})

                    # Intenta encontrar y hacer clic en el elemento "ver más"
                    element = driver.find_element(By.XPATH, '//*[@id="reaction_profile_pager"]/a/div/div/div/strong')
                    element.click()

                    # Espera un tiempo antes de continuar
                    time.sleep(2)

                except NoSuchElementException:
                    # Si no se encuentra el elemento "ver más", sal del bucle
                    print("No se puede encontrar el elemento 'Ver más'. Salir del bucle.")
                    break
                except Exception as e:
                    # Manejar otras excepciones si es necesario
                    print(f"Error: {e}")
                    break

        # Llama a la función get()
        get()


        df = pd.DataFrame(link)
        df = df.reset_index(drop=True)

        def transformar_link(link):
            if link is not None:
                link = link.replace('m.facebook.com', 'www.facebook.com')

                # Extract the part up to and including the 'id' parameter
                match = re.search(r'(.*?\bid=[^&]+)', link)
                if match:
                    return match.group(1)

                # If 'id' parameter is not found, look for the first '&' and trim the link
                match = re.search(r'(^[^?]+)', link)
                if match:
                    return match.group(1)

                # If neither 'id' nor '&' is found, return the original link
                return link
            else:
                return None

            
        def todas_columnas_tienen_valores(fila):
            return all(fila)
        if 'link' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'])
            df['cliente'] = df['url_like'].str.extract(r'https://www.facebook.com/(\w+)/')
            df['link'] = df['link'].apply(transformar_link)
            
            df = df[df.apply(todas_columnas_tienen_valores, axis=1)]
            df = df[~df.apply(lambda row: 'Seguir' in row.values, axis=1)]
            df = df.drop_duplicates()
            df.to_csv('Likesd.csv', mode='a', header=False, index=False)
            db_url = 'mysql://root:@localhost/facebook_data'
            engine = create_engine(db_url)
            
            df.to_sql(name='likes_data', con=engine, if_exists='append', index=False)
            print("DataFrame subido exitosamente a la base de datos.")

            time.sleep(15)

        else:
            print("'link' column not found in DataFrame.")
            print("Link list:", link)
        df.head(15)
        
        
        cadena_a_reemplazar = "/ufi/reaction/profile/browser/?ft_ent_identifier="
        nueva_cadena = '/browse/shares?id='
        primer_enlace = linkactual.pop(0)

        link_modificado = primer_enlace.replace(cadena_a_reemplazar, nueva_cadena)
        driver.get(link_modificado)
        shared_data = []
        time.sleep(10)
        if driver.current_url != link_modificado:
            print(f"El enlace modificado no es válido: {link_modificado}")

            link_modificados = link_modificado.replace("m.", "mbasic.")
            driver.get(link_modificados)
            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                                (By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div[1]/a[1]')))
                    likes = driver.find_elements(By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div[1]/a[1]')

                    for i in likes:
                        enlace = i.get_attribute('href')
                        texto = i.text
                        max_url_length = 255
                        shared_data.append(
                                                            {'url_like': url_original[:max_url_length], 'usuario': texto, 'link': enlace, 'fecha': formatted_date})
                    try:
                        element = driver.find_element(
                        By.XPATH, '//*[@id="m_more_item"]/a/span')
                        element.click()
                        time.sleep(10)
                    except Exception as e:
                                        # Si no se encuentra el elemento "ver más", sal del bucle interno
                        break
                except Exception as e:# Si no se encuentra ningún elemento para esperar, sal del bucle externo
                    break
            df_compartidas = pd.DataFrame(shared_data)
            def transformar_link1(link):
                if link is not None:
                    link = link.replace('mbasic.facebook.com', 'www.facebook.com')

                                # Extract the part up to and including the 'id' parameter
                    match = re.search(r'(.*?\bid=[^&]+)', link)
                    if match:
                        return match.group(1)

                                # If 'id' parameter is not found, look for the first '&' and trim the link
                    match = re.search(r'(^[^?]+)', link)
                    if match:
                        return match.group(1)

                                # If neither 'id' nor '&' is found, return the original link
                    return link
                else:
                    return None
                            
            if 'link' in df_compartidas.columns:
                df_compartidas['link'] = df_compartidas['link'].apply(transformar_link1)
                df_compartidas['cliente'] = df_compartidas['url_like'].str.extract(r'https://www.facebook.com/(\w+)/')
                db_url = 'mysql://root:@localhost/facebook_data'
                df_compartidas.to_csv("verificar_lite.csv")
                engine = create_engine(db_url)
                df_compartidas['fecha'] = pd.to_datetime(df_compartidas['fecha'])
            df_compartidas.to_sql(name='compartidas_data', con=engine, if_exists='append', index=False)
            print("DataFrame subido exitosamente a la base de datos.")
                        
        else:
            print(f"Enlace valido: {link_modificado}")
            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div[1]/div/div/div//a')))
                    likes = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div/div/div/div//a')
                    for i in likes:
                        enlace = i.get_attribute('href')
                        texto = i.text
                        max_url_length = 255
                        shared_data.append(
                                        {'url_like': url_original[:max_url_length], 'usuario': texto, 'link': enlace, 'fecha': formatted_date})

                    try:
                        element = driver.find_element(
                        By.XPATH, '//*[@id="m_more_item"]/a/div/div/div/strong')
                        element.click()
                        time.sleep(5)
                    except Exception as e:
                    # Si no se encuentra el elemento "ver más", sal del bucle interno
                        break
                except Exception as e:# Si no se encuentra ningún elemento para esperar, sal del bucle externo
                    break
        
            df_compartidas = pd.DataFrame(shared_data)
            def todas_columnas_tienen_valores1(fila):
                return all(fila)
            
            def transformar_link1(link):
                if link is not None:
                    link = link.replace('m.facebook.com', 'www.facebook.com')

                    # Extract the part up to and including the 'id' parameter
                    match = re.search(r'(.*?\bid=[^&]+)', link)
                    if match:
                        return match.group(1)

                    # If 'id' parameter is not found, look for the first '&' and trim the link
                    match = re.search(r'(^[^?]+)', link)
                    if match:
                        return match.group(1)

                    # If neither 'id' nor '&' is found, return the original link
                    return link
                else:
                    return None
                
            if 'link' in df_compartidas.columns:
                df_compartidas['link'] = df_compartidas['link'].apply(transformar_link1)

                if 'usuario' in df.columns:
                    indices_ver_mas = df_compartidas.index[df_compartidas['usuario'] == 'Ver más…'].tolist()
                    if indices_ver_mas:
                        index_of_ver_mas = indices_ver_mas[-1]
                        df_compartidas = df_compartidas.iloc[index_of_ver_mas + 1:]
                        df_compartidas = df_compartidas[df_compartidas.apply(todas_columnas_tienen_valores1, axis=1)]
                        df_compartidas = df_compartidas[~df_compartidas.apply(lambda row: 'Seguir' in row.values, axis=1)]
                        df_compartidas = df_compartidas.reset_index(drop=True)
                        print(f"Índice de la última ocurrencia de 'Ver más…': {index_of_ver_mas}")

            print("Link list:", link)
            df_compartidas['cliente'] = df_compartidas['url_like'].str.extract(r'https://www.facebook.com/(\w+)/')
            df_compartidas.to_csv("verificar.csv")
            db_url = 'mysql://root:@localhost/facebook_data'
            engine = create_engine(db_url)
            df_compartidas['fecha'] = pd.to_datetime(df_compartidas['fecha'])
            df_compartidas.to_sql(name='compartidas_data', con=engine, if_exists='append', index=False)
            print("DataFrame subido exitosamente a la base de datos.")




        


# In[29]:


driver = open_browser()
for url in urls:
    scrapper_completo(driver, [url])

