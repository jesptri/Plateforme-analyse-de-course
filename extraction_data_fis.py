import pandas as pd
import re
import pdfplumber
# import os

def convert_chrono_to_seconds(chrono):
    if '+' in chrono:
        chrono = chrono.replace('+', '')
    if ':' in chrono:
        if len(chrono.split(':')) == 2:
            minutes, secondes_dixiemes = chrono.split(':')
            minutes = int(minutes) if minutes != '' else 0
            secondes, dixiemes = map(float, secondes_dixiemes.split('.'))
            return minutes * 60 + secondes + dixiemes / 10
        elif len(chrono.split(':')) == 3:
            heures, minutes, secondes_dixiemes = chrono.split(':')
            heures = int(heures) if heures != '' else 0
            minutes = int(minutes) if minutes != '' else 0
            secondes, dixiemes = map(float, secondes_dixiemes.split('.'))
            return 3600 * heures + minutes * 60 + secondes + dixiemes / 10
    else:
        return float(chrono)   

# pattern à avoir

pattern_ligne_skieur = r"\d{1,3}\s+\d{1,3}\s+(?:[A-Za-z]*\s+)*(?:[A-Z]{3})"
pattern_nom_de_famille = r"^[A-Z]+$"
pattern_prenom = r"^[A-Z][a-z]+$"
pattern_nationalite = r"^[A-Z]{3}$"

data_fis_path_pdf = "c:\\Users\\jules\\Desktop\\Stage CNSNMM\\Analyse de course\\Ski de fond\\resultats FIS mail\\2024CC2274AL.pdf"


    
all_text = []

with pdfplumber.open(data_fis_path_pdf) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        all_text.append(text)
        # print(text)
        
# POUR TROUVER LES SPLIT #
        
text_0 = pdf.pages[0].extract_text()
split_re = re.compile(r"CODE TIME\n(.*)")
split = split_re.findall(text_0)
distance_pattern = re.compile(r'-?\d+\.\d+')
tous_les_split = distance_pattern.findall(split[0])
liste_split = [float(split) for split in tous_les_split]
liste_split.sort()
print("liste_split: " + str(liste_split))

# POUR TROUVER LIEU, TYPE ET SAISON DE LA COURSE

page_0_lines = text_0.split("\n")
mois_annee_de_la_course = page_0_lines[1][-8:]
mois, annee = mois_annee_de_la_course.split(" ")
if mois in ["JAN", "FEB", "MAR", "APR"]:
    Saison_de_la_course = str(int(annee) - 1) + "-" + annee
else:
    Saison_de_la_course = annee + "/" + str(int(annee) + 1)
    
# print(Saison_de_la_course)
Lieu_de_la_course = page_0_lines[2]
ligne_type_de_la_course = page_0_lines[3].split("Start")
Type_de_la_course = ligne_type_de_la_course[0]

pages = []

for text in all_text:
    # print(text.split("\n"))
    pages.append(text.split("\n"))

data_all_skieurs = []

for page in pages:

    filtered_lines = []
    for line in page:
        if "Sector Time/Speed" not in line:
            filtered_lines.append(line)
            
    # print("filtered_lines: " + str(filtered_lines))
    
    data_skieur = []

    for line in filtered_lines:   
        # print("line: " + str(line))           
        if re.match(pattern_ligne_skieur, line):
            # print("line: " + str(line))           
            if data_skieur:
            # if line == page[-1]:
                data_all_skieurs.append(data_skieur)
            data_skieur = []
            line_elements = line.split(" ")
            # print("line_elements: " + str(line_elements))
            data_skieur.append(int(line_elements[0])) # ranking
            data_skieur.append(int(line_elements[1])) # dossard
            data_skieur.append(line_elements[2]) # premiere partie du nom de famille
            # print("1 " + str(data_skieur))
            data_skieur[-1] += " " + line_elements[3] # premiere ou deuxieme partie du prénom
            if not re.match(pattern_nationalite, line_elements[4]): # première partie du prénom s'il y en a deux parties pour le nom
                data_skieur[-1] += " " + line_elements[4] 
                if not re.match(pattern_nationalite, line_elements[5]): # deuxième partie du prénom s'il y en a une
                    data_skieur[-1] += " " + line_elements[5] 
                    data_skieur.append(line_elements[6])    
                else:          
                    data_skieur.append(line_elements[5])
                    # print("2 " + str(data_skieur))
            elif re.match(pattern_nationalite, line_elements[4]):
                data_skieur.append(line_elements[4])
                # print("3 " + str(data_skieur))
        elif "Cumulative Time" in line:
            line_elements = line.split(" ")
            # print("line_elements: " + str(line_elements))
            for element in line_elements:
                if ":" in element and "+" not in element and "=" not in element:
                    # print("element: " + str(element))
                    data_skieur.append(convert_chrono_to_seconds(element))
        elif "Data Service" in line:
            data_all_skieurs.append(data_skieur)
                
# print("data_all_skieurs: " + str(data_all_skieurs))
        
data_fis_path_excel = f"c:\\Users\\jules\\Desktop\\Stage CNSNMM\\Analyse de course\\Ski de fond\\resultats FIS\\Ski de fond_{Lieu_de_la_course}_{Type_de_la_course}_{Saison_de_la_course}.xlsx"
writer =  pd.ExcelWriter(data_fis_path_excel, engine='xlsxwriter')

df_ski_de_fond = pd.DataFrame(data_all_skieurs)

beg_names = ["Ranking", "Bib", "Name", "Country"]
column_names = [str(split) + "km" for split in liste_split[:-1]]
column_names.append("Finish")

df_ski_de_fond.columns = beg_names + column_names

df_ski_de_fond.to_excel(writer, sheet_name="Tous les ST", index=False)
# writer.save()
writer.close()
# print(df_ski_de_fond)