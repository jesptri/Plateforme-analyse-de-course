### IMPORTS POUR SELENIUM ###

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

### IMPORTS CLASSIQUES

# from openpyxl import Workbook
from time import sleep
from time import time
import pandas as pd

### IMPORTS POUR EDGE ###

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver import Edge

from fonctions_utiles_code_plateforme import convert_chrono_to_seconds
from fonctions_utiles_code_plateforme import capture_screenshot
from fonctions_utiles_code_plateforme import save_html_content


def time_data_to_excel_ski_de_fond(Competition_de_la_course, Lieu_de_la_course, Type_de_la_course, Saison_de_la_course):
    
    Sexe, Type_de_la_course = Type_de_la_course.split(" ",1)
    
    # print("Sexe: " + str(Sexe))
    
    if Sexe in ["men", "Men", "man", "Man"]:
        sexe = "M"
    else:
        sexe = "W"

    # Driver

    # PATH = "C:\\Users\\jules\\Plateforme-analyse-de-course\\msedgedriver.exe" # pour local
    
    PATH = "msedgedriver.exe" # pour github
    
    service = Service(PATH)

    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument('--headless')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--window-size=1920x1080')

    # Initialisation du WebDriver

    service = Service(PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
            
    url = "https://www.fis-ski.com/"
    driver.get(url)
    driver.maximize_window()

    # Cookies

    sleep(1)

    cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']")))
    # cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Allow all')]")))
    cookies.click()

    sleep(1)

    # En mode headless il doit falloir cliquer sur les 3 barres en haut à droite

    # Calendar & Results

    Calendar_and_Results = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Calendar & Results')]")))
    Calendar_and_Results.click()

    # Selection: Results only

    Selection = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Selection')]")))
    Selection.click()

    Results_only = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Results only')]")))
    Results_only.click() 

    # Category: World Cup

    Category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Category')]")))
    Category.click()
    sleep(0.2)
    World_cup = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{Competition_de_la_course}')]")))
    World_cup.click() 
    sleep(0.2)

    # Discipline: Cross-Country

    Discipline = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Discipline')]")))
    Discipline.click() 
    sleep(0.2)

    Cross_Country = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Cross-Country')]")))
    Cross_Country.click() 
    sleep(0.2)

    # Saison: 2024

    Season = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Season')]")))
    Season.click() 
    sleep(0.2)

    annee_2024 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{Saison_de_la_course}')]")))
    annee_2024.click() 
    sleep(0.2)

    # Button Search
    
    capture_screenshot(driver,"C:\\Users\\jules\\Plateforme-analyse-de-course\\avant_reduction_taille.png")

    driver.set_window_size(1280, 800) # diminue la taille de la fenetre pour que ça soit configuré comme sans le mode headless !
    
    capture_screenshot(driver,"C:\\Users\\jules\\Plateforme-analyse-de-course\\apres_reduction_taille.png")
    save_html_content(driver, "C:\\Users\\jules\\Plateforme-analyse-de-course\\erreur.html")
    
    # element_1 = driver.find_element(By.XPATH,"//div[@class='collapse-in-modal']//div[@class='collapse-in-modal__content']//form[@class='form']//div[@class='form__inner']//div[@class='row']//button[contains(text(), 'Search')]")#//div[@class='col-md-4 hidden-lg hidden-sm-down form__itempt-1']")
    # if element_1.is_displayed():
    #     print("element_1 est visible sur la page.")
    
    Button_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn_yellow btn_fluid btn_size_small btn_label_bold']")))
    # Button_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn_yellow btn_fluid btn_size_small btn_label_bold']")))
    
    Button_search.click() 
    
    print("Ca a cliqué sur Search !")

    # Lieu de la course

    Race_place = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='g-lg-18 g-md-18 justify-left']//div[@class='split-row split-row']//div[@class='split-row__item']//div[contains(text(), '{Lieu_de_la_course}')]")))
    Race_place.click() 

    # Lignes avec les courses

    lignes_courses = driver.find_elements(By.XPATH, '//div[@class="container g-row px-sm-1 px-xs-0"]')

    for ligne_course in lignes_courses:
        # print("ligne_course.text: " + str((ligne_course.text).split("\n")))
        # print("type de ligne_course.text: " + str(type((ligne_course.text).split("\n"))))        
        try:
            if Type_de_la_course in (ligne_course.text).split("\n") and sexe in (ligne_course.text).split("\n"):
                # print("ligne_course.text: " + str((ligne_course.text).split("\n")))
                # Cliquer sur l'élément ou effectuer une autre action
                ligne_course.click()
                # print("Élément cliqué avec succès.")
                break  # Sortir de la boucle une fois l'élément trouvé et cliqué
        except StaleElementReferenceException:
            # Relocaliser les éléments si l'élément est devenu obsolète
            lignes_courses = driver.find_elements(By.XPATH, '//div[@class="container g-row px-sm-1 px-xs-0"]')

            # print("prout: " + str(ligne_course.text))
            
    # Results Details

    Result_Details = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Result Details')]")))
    Result_Details.click() 
    sleep(1)

    athletes_containers = driver.find_elements(By.XPATH, '//div[@class="g-row container px-0"]')

    data_all_athletes = []

    split_time_list = []

    to_avoid_DNF = 0

    for index_data_scraped, data_athlete_scraped in enumerate(athletes_containers):
        
        data_text = data_athlete_scraped.text
        data_text_list = data_text.split("\n")
        
        # print("taille liste: " + str(len(data_text_list)))

        if index_data_scraped == 0:
            # print(data_text_list)
            to_avoid_DNF = len(data_text_list)
            
        if len(data_text_list) != to_avoid_DNF:
            break

        # print(data_text)

        ranking = int(data_text_list[0])
        bib = int(data_text_list[1])
        name = data_text_list[2]
        country = data_text_list[3]
        data_athlete = []
        data_athlete.append(ranking)
        data_athlete.append(bib)
        data_athlete.append(name)
        data_athlete.append(country)

        for index_element, element in enumerate(data_text_list): 
            if element == "Sector Time":
                if index_data_scraped == 0:
                    split_time_list.append(str(round(float(data_text_list[index_element+1]),1)) + "km")
                element_bis = data_text_list[index_element+2]
                data_athlete.append(convert_chrono_to_seconds(element_bis))
                index_chrono = 0
                while element_bis != "Sector Time":
                    index_chrono += 7
                    if index_element+2+index_chrono < len(data_text_list):
                        element_bis = data_text_list[index_element+2+index_chrono]
                        if index_data_scraped == 0:
                            try:
                                split_time_list.append(str(round(float(data_text_list[index_element+1+index_chrono]),1)) + "km")
                            except:
                                pass
                    else: 
                        break
                    if element_bis == "Sector Time":
                        break
                    # print("element_bis: " + str(element_bis))
                    data_athlete.append(convert_chrono_to_seconds(element_bis))

        # print(data_athlete) 
        data_all_athletes.append(data_athlete)
        
    # print("split_time_list: " + str(split_time_list))
        
    df = pd.DataFrame(data_all_athletes)

    colonnes_df = ["Ranking", "Bib", "Name", "Country"] + split_time_list

    df.columns = colonnes_df
    
    # chemin_fichier_excel = f"c:\\Users\\jules\\Plateforme-analyse-de-course\\Ski de fond_{Competition_de_la_course}_{Lieu_de_la_course}_{Sexe + " " + Type_de_la_course}_{Saison_de_la_course}.xlsx" # pour local

    chemin_fichier_excel = f"Ski de fond_{Competition_de_la_course}_{Lieu_de_la_course}_{Sexe} {Type_de_la_course}_{Saison_de_la_course}.xlsx" # pour Github
        
    writer = pd.ExcelWriter(chemin_fichier_excel, engine='xlsxwriter')
    
    df.to_excel(writer, index=False)
        
    writer.close() 
    driver.close()


# time_data_to_excel_ski_de_fond("World Cup", "Canmore", "Women 15km Mass Start Free", 2024)

