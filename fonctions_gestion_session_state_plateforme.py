import streamlit as st
import csv
import json
import time

# CHANGE L'ETAT DU BOUTON VALIDER SI LE CHOIX DU SELECTBOX CHANGE #

def on_selectbox_change():
    st.session_state.button_clicked = False
    
# CHANGE L'ETAT DU BOUTON SI ON CLIQUE DESSUS POUR LES COACHS #

def on_button_click_coach():
    st.session_state.button_clicked = True
    
def off_button_click_coach():
    st.session_state.button_clicked = False
    
# CHANGE L'ETAT DU BOUTON SI ON CLIQUE DESSUS POUR JONAS #

def on_button_click_jonas():
    st.session_state.button_clicked_jonas = True
    
def off_button_click_jonas():
    st.session_state.button_clicked_jonas = False
    
# POUR AJOUTER UN SPLIT DANS UNE LISTE DE SPLIT TIME #

def add_split(liste):
    split = st.session_state.new_split
    if split: # Vérifier que l'élément n'est pas vide
        st.session_state[liste].append(split)
        st.session_state.new_split = ""  # Réinitialiser le champ de texte
        
# AJOUTE ENTREE DE CHAQUE SHOOT DANS LA LISTE #
        
def add_shoot_1(nom_liste_split_Jonas):
    avant_shoot_1 = "→ Shooting 1"
    apres_shoot_1 = "Shooting 1"
    st.session_state[nom_liste_split_Jonas].append(avant_shoot_1)
    st.session_state[nom_liste_split_Jonas].append(apres_shoot_1)

def add_shoot_2(nom_liste_split_Jonas):
    avant_shoot_2 = "→ Shooting 2"
    apres_shoot_2 = "Shooting 2"
    st.session_state[nom_liste_split_Jonas].append(avant_shoot_2)
    st.session_state[nom_liste_split_Jonas].append(apres_shoot_2)

def add_shoot_3(nom_liste_split_Jonas):
    avant_shoot_3 = "→ Shooting 3"
    apres_shoot_3 = "Shooting 3"
    st.session_state[nom_liste_split_Jonas].append(avant_shoot_3)
    st.session_state[nom_liste_split_Jonas].append(apres_shoot_3)

def add_shoot_4(nom_liste_split_Jonas):
    avant_shoot_4 = "→ Shooting 4"
    apres_shoot_4 = "Shooting 4"
    st.session_state[nom_liste_split_Jonas].append(avant_shoot_4)
    st.session_state[nom_liste_split_Jonas].append(apres_shoot_4)
    
def add_Finish(nom_liste_split_Jonas):
    finish = "Finish"
    for_no_bug = "Liste terminée !"
    st.session_state[nom_liste_split_Jonas].append(finish)
    st.session_state[nom_liste_split_Jonas].append(for_no_bug)    

# SUPPRIME LE DERNIER ELEMENT DE LA LISTE #
    
def delete_last_element(nom_liste_split_Jonas):
    if st.session_state[nom_liste_split_Jonas]:
        del(st.session_state[nom_liste_split_Jonas][-1])
    
# VIDE LA LISTE #
    
def empty_the_list(nom_liste_split_Jonas):
    st.session_state[nom_liste_split_Jonas].clear()
    
# ENREGISTRE LA LISTE DE SPLIT TIME #
    
def save_split_list(csv_st_file_path):
    
    fichier_loaded = load_split_list(csv_st_file_path)
    # print("existing_items_split: " + str(fichier_loaded))
    
    # Ajouter ou mettre à jour les nouveaux éléments dans existing_items_split
    for key in st.session_state.keys():
        if "split_time_Biathlon_" in key:
            fichier_loaded[key] = st.session_state[key]
            # print("existing_items: " + str(existing_items_split))
    
    # Enregistrer tous les éléments dans le fichier CSV
    with open(csv_st_file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for nom_liste_split, liste_split in fichier_loaded.items():
            # Convertir la liste en chaîne JSON avant de l'écrire dans le fichier CSV
            valeur_json = json.dumps(liste_split)
            writer.writerow([nom_liste_split, valeur_json])
    
# CHARGE LA LISTE DE SPLIT #

def load_split_list(csv_st_file_path):
    my_list = {}
    try:
        with open(csv_st_file_path, "r", encoding="utf-8-sig") as f:  # Utilisation de l'encodage utf-8-sig
            reader = csv.reader(f)
            for row in reader:
                # row est une liste contenant une seule entrée
                # try:
                # row_data = row[0]
                row[0].split(",")
                # print("row[0].split(","): " + str(row[0].split(",")))

                nom_liste_split = row[0].split(",")[0]
                liste_split_json = row[0].split(",")[1]
                
                # nom_liste_split, liste_split_json = row.split(",", 1)
                
                liste_split_json = liste_split_json.replace('""', '"')
                liste_split = [element.strip().strip('"') for element in liste_split_json[1:-1].split(',')]
                my_list[nom_liste_split] = liste_split
                # except:
                #     print("exception levée")
                #     pass

        # Convertir les caractères Unicode en caractères normaux après avoir parcouru toute la liste
        
        for key, value in my_list.items():
            cleaned_list = []
            for element in value:
                if '["' in element:
                    element = element.replace('["', '')
                if '"]' in element:
                    element = element.replace('"]', '')
                element = element.encode('utf-8').decode('unicode_escape')
                cleaned_list.append(element)
            my_list[key] = cleaned_list
            # print("cleaned value: " + str(cleaned_list))
            
            # print("my_list: " + str(my_list))

        return my_list
    except FileNotFoundError:
        st.warning("Le fichier CSV n'existe pas encore. Ajoutez des éléments et enregistrez-les d'abord.")
    
# ENREGISTRE LA LISTE DE SPLIT TIME PAR TYPE DE PORTION #

def save_type_list(csv_st_file_path):

    existing_items_type = {}
    try:
        with open(csv_st_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                existing_items_type[row[0]] = json.loads(row[1])  # Convertir la chaîne JSON en liste
    except FileNotFoundError:
        pass
    
    # Ajouter ou mettre à jour les nouveaux éléments dans existing_items
    
    for key in st.session_state.keys():
        if "split_type_de_portion_Biathlon_" in key:
            existing_items_type[key] = st.session_state[key]
            # print("existing_items_type: " + str(existing_items_type))
        
    # Enregistrer tous les éléments dans le fichier CSV
    
    with open(csv_st_file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for nom_liste_type, liste_type in existing_items_type.items():
            # Convertir la liste en chaîne JSON avant de l'écrire dans le fichier CSV
            valeur_json = json.dumps(liste_type)
            writer.writerow([nom_liste_type, valeur_json])
    
# CHARGE LA LISTE DES SPLIT PAR TYPE #

def load_type_list(csv_st_file_path_type):
    my_list = {}
    try:
        with open(csv_st_file_path_type, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                nom_liste_type = row[0]
                listes_par_type_json = row[1]
                liste_par_type = json.loads(listes_par_type_json)
                
                liste_type_bosse = liste_par_type[0]
                liste_type_descente = liste_par_type[1]
                liste_type_plat = liste_par_type[2]
                liste_type_vallone = liste_par_type[3]

                my_list[nom_liste_type] = [liste_type_bosse, liste_type_descente, liste_type_plat, liste_type_vallone]
                             
        return my_list
    
    except FileNotFoundError:
        st.warning("Le fichier CSV n'existe pas encore. Ajoutez des éléments et enregistrez-les d'abord.")

# MULTISELECT #

def update_type(nom_split_type_de_portion_Jonas, type):
    
    if type == "bosse":
        st.session_state[nom_split_type_de_portion_Jonas][0] = st.session_state["choix bosse Jonas"]
    if type == "descente":
        st.session_state[nom_split_type_de_portion_Jonas][1] = st.session_state["choix descente Jonas"]
    if type == "plat":
        st.session_state[nom_split_type_de_portion_Jonas][2] = st.session_state["choix plat Jonas"]
    if type == "valloné":
        st.session_state[nom_split_type_de_portion_Jonas][3] = st.session_state["choix valloné Jonas"]

    # st.success("Les splits ont été mis à jour!")

# AFFICHAGE D'UN MESSAGE TEMPORAIRE #

def show_temporary_message(message, duration):
    placeholder = st.empty()
    placeholder.success(message)
    time.sleep(duration)
    placeholder.empty()