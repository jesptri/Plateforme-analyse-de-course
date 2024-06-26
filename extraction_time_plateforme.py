### IMPORTS POUR SELENIUM ###

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

### IMPORTS CLASSIQUES

# from openpyxl import Workbook
from time import sleep
from time import time
import pandas as pd

### IMPORTS POUR EDGE ###

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver import Edge

### IMPORTS POUR MOZILLA ###

# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager

### IMPORTS AUTRES FONCTIONS ###

# from extraction_nom_nationalite_plateforme import tableau_nom_nationalite
from fonctions_utiles_code_plateforme import convert_chrono_to_seconds



### FONCTION ###



def time_data_to_excel(Competition_de_la_course, Lieu_de_la_course, Type_de_la_course, Saison_de_la_course, SPLIT_TIME, moteur_de_recherche=str):
    
    
    ##### CREATION DU TABLEAU BIB_NOM_NATIONALITE #####
    
    
    annee_1_course = int(Saison_de_la_course.split("-")[0])
        
        
    # Chemin vers le webdriver d'Edge + initialisation du service du pilote Edge + initialisation du pilote Edge en utilisant le service


    # if moteur_de_recherche == "edge":
    PATH = "msedgedriver.exe"
    service = Service(PATH)
    
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')

    # Initialisation du WebDriver
    service = Service(PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
            
    url = "https://biathlonresults.com/#/datacenter"
    driver.get(url)
    
    ### PREMIER BOUTON + COOKIES

    lien1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'CONTINUE WITHOUT REGISTRATION')]")))
    lien1.click()
    cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[au-target-id='327']")))
    cookies.click()
    
    ### REVENIR SUR LA SAISON DE LA COURSE ###
    
    saison_site = driver.find_element(By.XPATH, '//div[@au-target-id="168"]//div[@au-target-id="215"]//span[@au-target-id="262"]')
        
    annee_1_site = int(saison_site.text.split("/")[0])
    
    number_of_clicks = annee_1_site - annee_1_course
        
    fleche_gauche = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@au-target-id="168"]//div[@au-target-id="215"]//span[@au-target-id="262"]//span[@au-target-id="235"]')))
    fleche_droite = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@au-target-id="168"]//div[@au-target-id="215"]//span[@au-target-id="262"]//span[@au-target-id="237"]')))

    for _ in range(number_of_clicks):
        if number_of_clicks > 0:
            fleche_gauche.click()
        elif number_of_clicks < 0:
            fleche_droite.click()     
            
    ### IBU CUP
    
    if Competition_de_la_course == "IBU CUP":
        ibu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#dbSchedule2']")))
        ibu.click() 
    
    ### SELECTION DE LA COURSE ###
    
    try:
        course1 = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{Lieu_de_la_course}')]")))
        course1.click()
    except:
        # print("Pas de course pour le lieu sélectionné !")
        pass
            
    format1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{Type_de_la_course}')]")))
    format1.click()
    relive = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'RE-LIVE')]")))
    relive.click()
    reload_live_data = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RE-LOAD LIVE DATA')]")))
    reload_live_data.click()
                
    ### OUVERTURE DE LA PREMIERE PAGE

    STstart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{SPLIT_TIME[0]}']")))
    STstart.click()   
    
    biathlete_data = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")
    
    bib_data_0 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colBib']")
    noms_data_0 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='au-target colShortName']")
    nationalites_data_0 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colNat']/img[@class='au-target']")
            
    try:
        bib_data_0 = [bib for bib in bib_data_0 if bib.text != "Bib"]
    except:
        pass
                    
    data_0 = []
    
    for index_biathlete in range(len(bib_data_0)):
        data_biathlete = [
            bib_data_0[index_biathlete].text,
            noms_data_0[index_biathlete].text,
            nationalites_data_0[index_biathlete].get_attribute("src").split('/')[-1][:3].upper(),
        ]
        data_0.append(data_biathlete)  
    
    #### PREMIER SCROLL
    
    scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
    driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section)  
    
    biathlete_data = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")

    bib_data_1 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colBib']")
    noms_data_1 = driver.find_elements(By.XPATH, ".//div[@class='au-target colShortName']")
    nationalites_data_1 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colNat']/img[@class='au-target']")
    
    try:
        bib_data_1 = [bib for bib in bib_data_1 if bib.text != "Bib"]
    except:
        pass
            
    data_1 = []
            
    for index_biathlete in range(len(bib_data_1)):
        data_biathlete = []
        data_biathlete.append(bib_data_1[index_biathlete].text)
        data_biathlete.append(noms_data_1[index_biathlete].text)
        data_biathlete.append(nationalites_data_1[index_biathlete].get_attribute("src").split('/')[-1][:3].upper())
        data_1.append(data_biathlete)    

    #### DEUXIEME SCROLL
    
    scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
    driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section) 
    
    biathlete_data = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")

    bib_data_2 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colBib']")
    noms_data_2 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='au-target colShortName']")
    nationalites_data_2 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colNat']/img[@class='au-target']")

    try:
        bib_data_2 = [bib for bib in bib_data_2 if bib.text != "Bib"]
    except:
        pass
    
    data_2 = []
    
    for index_biathlete in range(len(bib_data_2)):
        data_biathlete = []
        data_biathlete.append(bib_data_2[index_biathlete].text)
        data_biathlete.append(noms_data_2[index_biathlete].text)
        data_biathlete.append(nationalites_data_2[index_biathlete].get_attribute("src").split('/')[-1][:3].upper())
        data_2.append(data_biathlete)  
    
    #### TROISIEME SCROLL
    
    scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
    driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section) 
    
    biathlete_data = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")
    
    bib_data_3 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colBib']")
    noms_data_3 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='au-target colShortName']")
    nationalites_data_3 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colNat']/img[@class='au-target']")

    try:
        bib_data_3 = [bib for bib in bib_data_3 if bib.text != "Bib"]
    except:
        pass
    
    data_3 = []
    
    for index_biathlete in range(len(bib_data_3)):
        data_biathlete = []
        data_biathlete.append(bib_data_3[index_biathlete].text)
        data_biathlete.append(noms_data_3[index_biathlete].text)
        data_biathlete.append(nationalites_data_3[index_biathlete].get_attribute("src").split('/')[-1][:3].upper())
        data_3.append(data_biathlete)   
        
    #### QUATRIEME SCROLL
    
    scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
    driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section)  
    
    biathlete_data = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")

    bib_data_4 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colBib']")
    noms_data_4 = driver.find_elements(By.XPATH, ".//div[@class='au-target colShortName']")
    nationalites_data_4 = biathlete_data[0].find_elements(By.XPATH, ".//div[@class='colNat']/img[@class='au-target']")
    
    try:
        bib_data_4 = [bib for bib in bib_data_4 if bib.text != "Bib"]
    except:
        pass
            
    data_4 = []
            
    for index_biathlete in range(len(bib_data_4)):
        data_biathlete = []
        data_biathlete.append(bib_data_4[index_biathlete].text)
        data_biathlete.append(noms_data_4[index_biathlete].text)
        data_biathlete.append(nationalites_data_4[index_biathlete].get_attribute("src").split('/')[-1][:3].upper())
        data_4.append(data_biathlete)  
        
    liste_bib_name_nat = data_0 + data_1 + data_2 + data_3 + data_4
    
    
    ### FERMER LA PAGE DU SPLIT TIME ###
    
    STstart.click()  
         
    # driver.close()
    
    for data_biathlete in liste_bib_name_nat:
        lettre_1_prenom = data_biathlete[1].split(". ")[0]
        nom = data_biathlete[1].split(". ")[1]
        if " " in nom:
            nom = nom.replace(" ","")
        data_biathlete[1] = nom + " " + lettre_1_prenom + "."
    
    ### TABLEAU AVEC [DOSSARD, NOM P., NATIONALITE], ex: [21, OEBERG A., SWE] ###
    
    bib_name_nat = liste_bib_name_nat
    
    
    
    ##### PARTIE EXTRACTION DES DONNEES SPLIT-TIME #####
    

    
    ### CREATION DU FICHIER EXCEL ###

    # chemin_fichier_excel = f"jesptri\\Plateforme-analyse-de-course\\Biathlon_{Competition_de_la_course}_{Lieu_de_la_course}_{Type_de_la_course}_{Saison_de_la_course}.xlsx" # pour Github

    chemin_fichier_excel = f"Biathlon_{Competition_de_la_course}_{Lieu_de_la_course}_{Type_de_la_course}_{Saison_de_la_course}.xlsx" # pour Github
    
    # chemin_fichier_excel = f"c:\\Users\\jules\\Plateforme-analyse-de-course\\Biathlon_{Competition_de_la_course}_{Lieu_de_la_course}_{Type_de_la_course}_{Saison_de_la_course}.xlsx" # pour ordi
    
    writer = pd.ExcelWriter(chemin_fichier_excel, engine='xlsxwriter')
    
    ### SELECTION DES SPLIT TIME ###
    
    df_final = pd.DataFrame(columns=['Ranking', 'Bib', 'Name', 'Country'])

    for i in range(0,len(SPLIT_TIME)-1): ## -1 pour test 

        donnees_csv_tot = []
        
        ### OUVERTURE DE LA PREMIERE PAGE
        
        STstart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{SPLIT_TIME[i]}']")))
        STstart.click() 

        ### SANS AVOIR SCROLL ###

        donnees_csv_0 = []

        cellules_data_0 = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")
        for cellule in cellules_data_0:
            ligne = cellule.text.split('\n')
            donnees_csv_0.append(ligne)

        donnees_csv_tot += donnees_csv_0[0]

        #### PREMIER SCROLL
        
        scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
        driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section)
        
        donnees_csv_1 = []

        cellules_data_1 = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")
        for cellule in cellules_data_1:
            ligne = cellule.text.split('\n')
            donnees_csv_1.append(ligne)
        del(donnees_csv_1[0][0])
        
        donnees_csv_tot += donnees_csv_1[0]

        # print("taille 1: " + str(len(donnees_csv_1[0])))
        # print("donnees_csv_1: " + str(donnees_csv_1))


        #### DEUXIEME SCROLL
        
        scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
        driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section)
        
        donnees_csv_2 = []

        cellules_data_2 = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")
        
        for cellule in cellules_data_2:
            ligne = cellule.text.split('\n')
            donnees_csv_2.append(ligne)
        del(donnees_csv_2[0][0])
        
        donnees_csv_tot += donnees_csv_2[0]
        
        # print("taille 2: " + str(len(donnees_csv_2[0])))
        
        #### TROISIEME SCROLL
        
        scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
        driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section)
            
        donnees_csv_3 = []

        cellules_data_3 = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")           
        
        for cellule in cellules_data_3:
            ligne = cellule.text.split('\n')
            donnees_csv_3.append(ligne)
        del(donnees_csv_3[0][0])
        donnees_csv_tot += donnees_csv_3[0]
        
        #### QUATRIEME SCROLL
        
        scrollable_section = driver.find_element(By.XPATH,"//div[@class='rtBody scrollable-resultTable au-target']")
        driver.execute_script("arguments[0].scrollBy(0, 500);", scrollable_section)
            
        donnees_csv_4 = []

        cellules_data_4 = driver.find_elements(By.XPATH, "//div[@au-target-id='762']")           
        
        for cellule in cellules_data_4:
            ligne = cellule.text.split('\n')
            donnees_csv_4.append(ligne)
        del(donnees_csv_4[0][0])        
        donnees_csv_tot += donnees_csv_4[0]
                
        # print("donnees_csv_tot: " + str(donnees_csv_tot))
        # print(" taille donnees_csv_tot: " + str(len(donnees_csv_tot)))
        
        STstart.click()  

        # # MISE EN FORME
        
        donnees_csv_int = []
        donnees_csv_int = [element.split(',') for element in donnees_csv_tot]
        donnees_csv_final = []
        k = -1
        for j in range(len(donnees_csv_int)):        
            k += 1
            for element in donnees_csv_int[j]:
                if k == 0:
                    donnees_csv_final.append(element.split(' '))
                if k >= 1:
                    donnees_csv_final.append(element.split(' '))
                    element[0].replace("'","")   
        
        ### GERER LES NOMS DE FAMILLES COMPOSES PAS SEPARES PAR UN TIRET ###
        
        for element in donnees_csv_final:
            if len(element) > 4:
                if(element[3].isupper() == True and element[4].isupper() == True):
                    element[3] = element[3] + element[4]
                    del(element[4])
        
        donnees_finales = [mot for mot in donnees_csv_final if len(mot) >= 5]

        
        try:
            if type(donnees_finales[0][0]) == str:
                del(donnees_finales[0])
        except:
            continue

        for data in donnees_finales:
            if 'DNF'in data:
                # print("DNF catched !" + str(data))
                # print('taille donnees_finales avant: ' + str(len(donnees_finales)))
                donnees_finales.remove(data) 
                # print('taille donnees_finales après: ' + str(len(donnees_finales)))
            else:
                data[0] = int(data[0])
                data[1] = int(data[1])
                if len(data) == 5:
                    # print("taille 5: " + str(data))
                    data[4] = data[4].replace("'","").replace("+","")
                elif len(data) == 6:
                    # print("6 avant: " + str(data))
                    if "+" in data[4]:
                        data[4] = data[4].replace("'","").replace("+","")
                    if "+" or ":" in data[5]:
                        data[5] = data[5].replace("'","").replace("+","")
                        data.remove(data[4])
                    # print("6 après: " + str(data))
                    
        for data in donnees_finales:
            if len(data) != 5:
                # print("taille irrégulière: " + str(data))
                if type(data[4]) == int or ":" in data[5]:
                    if ":" in data[5] and "+" in data[5]:
                        data[5] = data[5].replace("+", "")
                    data.remove(data[4])

        new_good_data = pd.DataFrame(donnees_finales)
        
        # print("AVANT: " + str(new_good_data))
        
        ### SI LES DONNEES SONT MAL FORMATEES ###
        
        # print("taille du df: " + str(len(new_good_data.columns)))
        # if len(new_good_data.columns) == 6:
        #     print("new_good_data: " + str(new_good_data))
        
        if len(new_good_data.columns) == 7:
            new_good_data.drop(new_good_data.columns[6], axis=1, inplace=True)        
        elif len(new_good_data.columns) == 6:
            # print("AVANT: " + str(new_good_data))
            new_good_data.drop(new_good_data.columns[5], axis=1, inplace=True)# c'était la 4 avant       
            # print("APRES: " + str(new_good_data))
        # new_good_data = new_good_data.drop(new_good_data.columns[-1], axis=1)
        
        # print("APRES: " + str(new_good_data))
        
        ### SUPPRESSION DE LA DERNIERE LIGNE ###
        
        new_good_data.drop(new_good_data.index[-1] and new_good_data.index[-2], inplace=True)
               
        new_good_data.columns = ['Ranking', 'Bib', 'Name', 'Country', SPLIT_TIME[i]]
        
        # print("APRES: " + str(new_good_data))        
        
        ### concaténation des noms et prénoms dans la même colonne 
        
        new_good_data['Name'] = new_good_data["Country"] + " " + new_good_data["Name"]
                
        ### CHANGER LE FORMAT A. OEBERG EN OEBERG A. ### c'est pour pouvoir comparer avec le tableau [dossard, nom p., nationalité]
        
        # bib_name_nat_BON = []
        # for index_biathlete in range(len(bib_name_nat)):
        #     nom = bib_name_nat[index_biathlete][1].split(' ')
        #     bib_name_nat_BON.append([bib_name_nat[index_biathlete][0], nom[1] + " " + nom[0], bib_name_nat[index_biathlete][2]])

        # print("bib_name_nat: " + str(bib_name_nat))


        for index_biathlete in range(new_good_data.shape[0]):
            for nom_nationalite in bib_name_nat:
                if new_good_data.iloc[index_biathlete]["Name"] == nom_nationalite[1]:
                    new_good_data.at[index_biathlete,"Country"] = nom_nationalite[2]

        new_good_data = new_good_data.dropna()
                
        ### CONVERSION EN INT DES VALEURS DES DOSSARDS ###
        
        for index, num_dossard in new_good_data.iterrows():
            new_good_data.at[index, 'Bib'] = int(new_good_data.at[index, 'Bib'])
            
        ### TRIE PAR RANKING + SUPPRESSION DES DOUBLONS ###
        
        new_good_data['Ranking'] = pd.to_numeric(new_good_data['Ranking'], errors='coerce')
        new_good_data.sort_values(by='Ranking', inplace=True)  
        new_good_data.drop_duplicates(inplace=True)     
        
        ### CONVERSION DES TIME EN SECONDES ###
              
        new_good_data[SPLIT_TIME[i]] = new_good_data[SPLIT_TIME[i]].apply(convert_chrono_to_seconds)
        new_good_data.drop_duplicates(inplace=True) 
        
        # print("taille de new_good_data " + str(i) + ": " + str(new_good_data.shape[0]))
        
        # print("après conversion en secondes: " + str(new_good_data))
        

        temps_leader = new_good_data.at[new_good_data.index[0], SPLIT_TIME[i]]
        # print("new_good_data: " + str(new_good_data))

        for index, row in new_good_data.iterrows():
            # print("row[-1]: " + str(row[-1]))
            if index == new_good_data.index[0] or row[-1] == temps_leader:  # Vérifiez que ce n'est pas la première ligne
                # print("Premier cas !")
                new_good_data.at[index, SPLIT_TIME[i]] = temps_leader
            else:
                # print("Deuxième cas !")
                new_good_data.at[index, SPLIT_TIME[i]] += temps_leader 
                      
        
        new_good_data.sort_values(by='Bib', inplace=True)
        new_good_data.reset_index(inplace=True, drop=True) # ajouté le drop=True
                
        if i==0:
            df_final["Bib"] = new_good_data["Bib"]
            df_final["Name"] = new_good_data["Name"]
            df_final["Country"] = new_good_data["Country"]
            df_final.sort_values(by='Bib', inplace=True)
            df_final.reset_index(drop=True, inplace=True)
            
        if SPLIT_TIME[i] == SPLIT_TIME[-2]: ### -2 pour test !!!
            # df_final["Ranking"] = new_good_data["Ranking"]
            for index_biathlete in range(df_final.shape[0]):
                for index_biathlete_bis in range(new_good_data.shape[0]):
                    if df_final.iloc[index_biathlete]["Bib"] == new_good_data.iloc[index_biathlete_bis]["Bib"]:
                        df_final.at[index_biathlete,"Ranking"] = new_good_data.iloc[index_biathlete_bis]["Ranking"]
                        break
                        
        for index_biathlete in range(df_final.shape[0]):
            for index_biathlete_bis in range(new_good_data.shape[0]):
                if df_final.iloc[index_biathlete]["Bib"] == new_good_data.iloc[index_biathlete_bis]["Bib"]:
                    df_final.at[index_biathlete,SPLIT_TIME[i]] = new_good_data.iloc[index_biathlete_bis][SPLIT_TIME[i]]
                    break  
                        
        ### ici il y a les erreurs dans les chronos ###
        
        # print("df_final: " + str(df_final))
            
    ### FERMER LA PAGE OUVERTE POUR PAS QUE CA PLANTE + ENREGISTREMENT

    nom_feuille_fusionnee = "Tous les ST"
    
    df_final.dropna(inplace=True)
    
    df_final = df_final.drop_duplicates(subset=["Bib", "Name"])

    df_final.to_excel(writer, sheet_name=nom_feuille_fusionnee, index=False)
        
        
    writer.close() 
    driver.close()


# ST_M_spr_OBERHOF = ["0.6km", "1.7km (PT)", "1.9km", "2.5km", "3.0km (PT)", "→ Shooting 1", "Shooting 1", "3.9km", "5.0km (PT)", "5.2km", "5.8km", "6.3km (PT)", "→ Shooting 2", "Shooting 2","7.3km", "8.4km (PT)", "8.6km", "9.2km", "9.7km (PT)", "Finish", "Test"]

# time_data_to_excel("Oberhof (GER)", "Men 10km test", "2023-2024", ST_M_spr_OBERHOF)
