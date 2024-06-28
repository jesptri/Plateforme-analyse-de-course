import re as re
import streamlit as st
import zipfile

# format des yticks, remplacer les - par un +

def custom_format(value, pos):
    if value < 0:
        return f"+{-value:.1f}"
    elif value == 0:
        return 0
    else:
        return f"-{value:.1f}"

### FONCTION QUI VERIFIE SI LE FICHIER SOULEVE UNE EXCEPTION DE TYPE BADZIPFILE ###

def is_zipfile_valid(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            return True
    except zipfile.BadZipFile:
        return False
    except zipfile.LargeZipFile:
        return False
    except Exception:
        return False

def split_tour_par_tour(df, nombre_de_shoots): ### RETOURNE 1 LISTE COMPOSEE DE 3 LISTES CONTENANT LES NOMS DES SPLITS POUR LE TOUR ### 3 LISTES CAR 3 TOURS
    
    noms_des_splits = [[] for _ in range(nombre_de_shoots + 1)]
    
    tous_les_splits = df.columns.to_list()[4:]
    
    avant_shoot1_trouve = False
    entre_shoot1_et_shoot2_trouve = False
    entre_shoot2_et_shoot3_trouve = False
    entre_shoot3_et_shoot4_trouve = False
    
    for nom_colonne in tous_les_splits:
        if nom_colonne == "→ Shooting 1":
            avant_shoot1_trouve = True
            entre_shoot1_et_shoot2_trouve = False
            entre_shoot2_et_shoot3_trouve = False
            entre_shoot3_et_shoot4_trouve = False
            continue
        elif nom_colonne == "→ Shooting 2":
            entre_shoot1_et_shoot2_trouve = True
            entre_shoot2_et_shoot3_trouve = False
            entre_shoot3_et_shoot4_trouve = False
            continue
        
        if nombre_de_shoots == 4:
            if nom_colonne == "→ Shooting 3":
                entre_shoot2_et_shoot3_trouve = True
                entre_shoot3_et_shoot4_trouve = False
                continue
            elif nom_colonne == "→ Shooting 4":
                entre_shoot3_et_shoot4_trouve = True
                continue
        
        if nombre_de_shoots == 2:
            if not avant_shoot1_trouve:
                noms_des_splits[0].append(nom_colonne)
            elif avant_shoot1_trouve and not entre_shoot1_et_shoot2_trouve:
                noms_des_splits[1].append(nom_colonne) 
            else:
                noms_des_splits[2].append(nom_colonne)
        
        elif nombre_de_shoots == 4:
            if not avant_shoot1_trouve:
                noms_des_splits[0].append(nom_colonne)
            elif avant_shoot1_trouve and not entre_shoot1_et_shoot2_trouve:
                noms_des_splits[1].append(nom_colonne) 
            elif entre_shoot1_et_shoot2_trouve and not entre_shoot2_et_shoot3_trouve:
                noms_des_splits[2].append(nom_colonne)
            elif entre_shoot2_et_shoot3_trouve and not entre_shoot3_et_shoot4_trouve:
                noms_des_splits[3].append(nom_colonne)    
            else:
                noms_des_splits[4].append(nom_colonne)  
        
    if nombre_de_shoots == 4:        
        del(noms_des_splits[3][0])
        del(noms_des_splits[4][0])  
        
        noms_des_splits[2].append("→ Shooting 3")
        noms_des_splits[3].append("→ Shooting 4") 
                                       
    del(noms_des_splits[1][0])
    del(noms_des_splits[2][0])
    
    noms_des_splits[0].append("→ Shooting 1")
    noms_des_splits[1].append("→ Shooting 2")

    # print("noms_des_splits: " + str(noms_des_splits))

    return noms_des_splits

def split_tour_par_tour_Jonas(liste_de_split, nombre_de_shoots): ### RETOURNE 1 LISTE COMPOSEE DE 3 LISTES CONTENANT LES NOMS DES SPLITS POUR LE TOUR ### 3 LISTES CAR 3 TOURS
    
    noms_des_splits = [[] for _ in range(nombre_de_shoots + 1)]
    
    tous_les_splits = liste_de_split[:-1]
    
    avant_shoot1_trouve = False
    entre_shoot1_et_shoot2_trouve = False
    entre_shoot2_et_shoot3_trouve = False
    entre_shoot3_et_shoot4_trouve = False
    
    for nom_split in tous_les_splits:
        if nom_split == "→ Shooting 1":
            avant_shoot1_trouve = True
            entre_shoot1_et_shoot2_trouve = False
            entre_shoot2_et_shoot3_trouve = False
            entre_shoot3_et_shoot4_trouve = False
            continue
        elif nom_split == "→ Shooting 2":
            entre_shoot1_et_shoot2_trouve = True
            entre_shoot2_et_shoot3_trouve = False
            entre_shoot3_et_shoot4_trouve = False
            continue
        
        if nombre_de_shoots == 4:
            if nom_split == "→ Shooting 3":
                entre_shoot2_et_shoot3_trouve = True
                entre_shoot3_et_shoot4_trouve = False
                continue
            elif nom_split == "→ Shooting 4":
                entre_shoot3_et_shoot4_trouve = True
                continue
        
        if nombre_de_shoots == 2:
            if not avant_shoot1_trouve:
                noms_des_splits[0].append(nom_split)
            elif avant_shoot1_trouve and not entre_shoot1_et_shoot2_trouve:
                noms_des_splits[1].append(nom_split) 
            else:
                noms_des_splits[2].append(nom_split)
        
        elif nombre_de_shoots == 4:
            if not avant_shoot1_trouve:
                noms_des_splits[0].append(nom_split)
            elif avant_shoot1_trouve and not entre_shoot1_et_shoot2_trouve:
                noms_des_splits[1].append(nom_split) 
            elif entre_shoot1_et_shoot2_trouve and not entre_shoot2_et_shoot3_trouve:
                noms_des_splits[2].append(nom_split)
            elif entre_shoot2_et_shoot3_trouve and not entre_shoot3_et_shoot4_trouve:
                noms_des_splits[3].append(nom_split)    
            else:
                noms_des_splits[4].append(nom_split)  
        
    if nombre_de_shoots == 4:        
        del(noms_des_splits[3][0])
        del(noms_des_splits[4][0])  
        
        noms_des_splits[2].append("→ Shooting 3")
        noms_des_splits[3].append("→ Shooting 4") 
    
    # print("noms_des_splits[1]: " + str(noms_des_splits[1]))
                       
    del(noms_des_splits[1][0])
    del(noms_des_splits[2][0])
    
    noms_des_splits[0].append("→ Shooting 1")
    noms_des_splits[1].append("→ Shooting 2")

    # print("noms_des_splits: " + str(noms_des_splits))

    return noms_des_splits

def f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course):
    
    colonnes_df = df.iloc[:, 4:].columns.tolist()
    # print(colonnes_df)
    
    liste_distance_au_depart_des_ST = []
    liste_distance_au_depart_des_ST_sans_shoots = []

    for nom_colonne in colonnes_df:
        if nom_colonne == "→ Shooting 1":
            liste_distance_au_depart_des_ST.append(distance_de_1_tour)
            liste_distance_au_depart_des_ST_sans_shoots.append(distance_de_1_tour)
        elif nom_colonne == "Shooting 1":
            liste_distance_au_depart_des_ST.append(distance_de_1_tour+0.2)        
        elif nom_colonne == "→ Shooting 2":
            liste_distance_au_depart_des_ST.append(2*distance_de_1_tour)
            liste_distance_au_depart_des_ST_sans_shoots.append(2*distance_de_1_tour)
        elif nom_colonne == "Shooting 2":
            liste_distance_au_depart_des_ST.append(2*distance_de_1_tour+0.2)  
        elif nom_colonne == "→ Shooting 3":
            liste_distance_au_depart_des_ST.append(3*distance_de_1_tour)
            liste_distance_au_depart_des_ST_sans_shoots.append(3*distance_de_1_tour)
        elif nom_colonne == "Shooting 3":
            liste_distance_au_depart_des_ST.append(3*distance_de_1_tour+0.2) 
        elif nom_colonne == "→ Shooting 4":
            liste_distance_au_depart_des_ST.append(4*distance_de_1_tour)
            liste_distance_au_depart_des_ST_sans_shoots.append(4*distance_de_1_tour)
        elif nom_colonne == "Shooting 4":
            liste_distance_au_depart_des_ST.append(4*distance_de_1_tour+0.2) 
        elif nom_colonne == "Finish":
            liste_distance_au_depart_des_ST.append(distance_toute_la_course)
            liste_distance_au_depart_des_ST_sans_shoots.append(distance_toute_la_course)               
        else:
            liste_distance_au_depart_des_ST.append(float(nom_colonne.split("km")[0]))
            liste_distance_au_depart_des_ST_sans_shoots.append(float(nom_colonne.split("km")[0]))
        # print(nom_colonne.split("km ")[0])
        
    liste_distance_des_ST = []
    
    liste_distance_des_ST.append(liste_distance_au_depart_des_ST[0]*1000)
    for index_distance in range(1,len(liste_distance_au_depart_des_ST)):
        liste_distance_des_ST.append(1000*(liste_distance_au_depart_des_ST[index_distance] - liste_distance_au_depart_des_ST[index_distance-1]))

    return liste_distance_des_ST, liste_distance_au_depart_des_ST, liste_distance_au_depart_des_ST_sans_shoots

def f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours):
    liste_distance_au_depart_des_ST = []
    distance_de_1_tour = extract_distances(split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[0][-1])        

    distance_de_la_course = nombre_de_tours*distance_de_1_tour[0]
    for split in df.columns.to_list()[4:]:
        liste_distance_au_depart_des_ST += (extract_distances(split))

    liste_distance_au_depart_des_ST_good = []
    for split in liste_distance_au_depart_des_ST:
        try:
            liste_distance_au_depart_des_ST_good.append(float(split[0]))
        except:
            liste_distance_au_depart_des_ST_good.append(float(split))
    # print("liste_distance_au_depart_des_ST_good: " + str(liste_distance_au_depart_des_ST_good))
    return liste_distance_au_depart_des_ST_good, distance_de_1_tour[0], distance_de_la_course

### SOUSTRACTION DES TEMPS DE SHOOT ###

def f_df_sans_temps_shoot(df, nombre_de_shoots):

    index_avant_shoot_1 = df.columns.get_loc("→ Shooting 1")
    index_avant_shoot_2 = df.columns.get_loc("→ Shooting 2")
    
    temps_shoot_1 = df["Shooting 1"] - df["→ Shooting 1"]
    temps_shoot_2 = df["Shooting 2"] - df["→ Shooting 2"] 
    
    df_sans_temps_shoot = df.copy()
    df_temps_de_ski_et_temps_de_shoot = df.copy()
    for intermediaire in df_sans_temps_shoot.columns.to_list()[index_avant_shoot_1 + 1:]:
        df_sans_temps_shoot[intermediaire] = df_sans_temps_shoot[intermediaire] - temps_shoot_1
    
    for intermediaire in df_sans_temps_shoot.columns.to_list()[index_avant_shoot_2 + 1:]:
        df_sans_temps_shoot[intermediaire] = df_sans_temps_shoot[intermediaire] - temps_shoot_2
        
    index_avant_shoot_3 = 0
    index_avant_shoot_4 = 0
        
    if nombre_de_shoots == 4:
        
        index_avant_shoot_3 = df.columns.get_loc("→ Shooting 3")
        index_avant_shoot_4 = df.columns.get_loc("→ Shooting 4")
        
        temps_shoot_3 = df["Shooting 3"] - df["→ Shooting 3"]
        temps_shoot_4 = df["Shooting 4"] - df["→ Shooting 4"] 
        
        for intermediaire in df_sans_temps_shoot.columns.to_list()[index_avant_shoot_3 + 1:]:
            df_sans_temps_shoot[intermediaire] = df_sans_temps_shoot[intermediaire] - temps_shoot_3
    
        for intermediaire in df_sans_temps_shoot.columns.to_list()[index_avant_shoot_4 + 1:]:
            df_sans_temps_shoot[intermediaire] = df_sans_temps_shoot[intermediaire] - temps_shoot_4
        
    df_temps_de_ski = df_sans_temps_shoot.copy()
    df_chute_perf_62 = df_temps_de_ski.copy()
    
    for index_biathlete in range(df_sans_temps_shoot.shape[0]):
        for index_intermediaire in range(len(df_temps_de_ski.columns.to_list()[5:])):
            df_temps_de_ski.iat[index_biathlete, index_intermediaire + 5] = df_temps_de_ski.iat[index_biathlete, index_intermediaire + 5] - df_sans_temps_shoot.iat[index_biathlete, index_intermediaire + 4] # 4 pour -1 + 5
    
    for index_biathlete in range(df_temps_de_ski_et_temps_de_shoot.shape[0]):
        for index_intermediaire in range(len(df_temps_de_ski_et_temps_de_shoot.columns.to_list()[5:])):
            df_temps_de_ski_et_temps_de_shoot.iat[index_biathlete, index_intermediaire + 5] = df_temps_de_ski_et_temps_de_shoot.iat[index_biathlete, index_intermediaire + 5] - df.iat[index_biathlete, index_intermediaire + 4] # 4 pour -1 + 5
            
    df_chute_perf_nat_10 = df_temps_de_ski.copy()

    return df_temps_de_ski, df_chute_perf_62, df_chute_perf_nat_10, index_avant_shoot_1, index_avant_shoot_2, temps_shoot_1, temps_shoot_2, df_sans_temps_shoot, index_avant_shoot_3, index_avant_shoot_4, df_temps_de_ski_et_temps_de_shoot

def extract_distances(text):
    # Utilisation de l'expression régulière pour trouver les sous-chaînes entre un espace et "km"
    pattern = r'(\d+(\.\d+)?)\s*km'
    matches = re.findall(pattern, text)
    
    # Extraire uniquement la première capture (le nombre) de chaque correspondance
    distances = [float(match[0]) for match in matches]
    return distances

def indices_ST_PT_tours(df):
    colonnes_df = df.iloc[:, 4:].columns.tolist()
    noms_PT = []
    noms_ST = []
    noms_tours = ["Shooting 1", "Shooting 2", "Finish"]
    
    for colonne in colonnes_df:
        if colonne[-4:] == "(PT)":
            noms_PT.append(colonne)
        elif colonne[-2:] == "km":
            noms_ST.append(colonne)      
                            
    return noms_PT, noms_ST, noms_tours

def df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
    
    liste_distance_des_ST = f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[0]
    
    df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0]
        
    df_box_plot = df_temps_de_ski
    
    df_moy_3_tours = df.iloc[:, :4].copy()
    df_moy_3_tours_normed = df.iloc[:, :4].copy()

    for index_intermediaire, intermediaire in enumerate(noms_intermediaires):
        
        if nombre_de_shoots == 2:
            if index_intermediaire == 0:
                df_moy_3_tours[noms_intermediaires[0]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][0]])/2
                df_moy_3_tours_normed[noms_intermediaires[0]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][0]])/(2*liste_distance_des_ST[0])
            elif index_intermediaire == len(split_tour_par_tour(df, nombre_de_shoots)[0]) - 1:
                df_moy_3_tours[noms_intermediaires[-1]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][-1]])/2
                df_moy_3_tours_normed[noms_intermediaires[-1]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][-1]])/(2*liste_distance_des_ST[-1]) 
            else:
                df_moy_3_tours[noms_intermediaires[index_intermediaire]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][index_intermediaire]])/3
                df_moy_3_tours_normed[noms_intermediaires[index_intermediaire]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][index_intermediaire]])/(3*liste_distance_des_ST[index_intermediaire])         
        
        elif nombre_de_shoots == 4:
            if index_intermediaire == 0:
                df_moy_3_tours[noms_intermediaires[0]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[3][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[4][0]])/4
                df_moy_3_tours_normed[noms_intermediaires[0]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[3][0]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[4][0]])/(4*liste_distance_des_ST[0])
            elif index_intermediaire == len(split_tour_par_tour(df, nombre_de_shoots)[0]) - 1:
                df_moy_3_tours[noms_intermediaires[-1]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[3][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[4][-1]])/4
                df_moy_3_tours_normed[noms_intermediaires[-1]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][-1]]) + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[3][-1]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[4][-1]]/(4*liste_distance_des_ST[-1]) 
            else:
                df_moy_3_tours[noms_intermediaires[index_intermediaire]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[3][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[4][index_intermediaire]])/5
                df_moy_3_tours_normed[noms_intermediaires[index_intermediaire]] = (df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[0][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[1][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[2][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[3][index_intermediaire]] + df_box_plot[split_tour_par_tour(df, nombre_de_shoots)[4][index_intermediaire]])/(5*liste_distance_des_ST[index_intermediaire])         

    return df_moy_3_tours, df_moy_3_tours_normed

def delete_fake_value(df):

    indexes_to_drop = []
    
    for index_biathlete in range(df.shape[0]):
        for index_interemediaire in range(5, len(df.columns.tolist()[5:])): # partir de 5 et comparer à l'interemediaire d'avant
            if df.iloc[index_biathlete, index_interemediaire] - df.iloc[index_biathlete, index_interemediaire-1] < 0:
                indexes_to_drop.append(index_biathlete)
    
    df = df.drop(indexes_to_drop).reset_index(drop=True)
    
    return df

### SKI DE FOND ###

def df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_tours):
    
    liste_distance_des_ST = f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0]
    
    df_temps_de_ski = df_temps_de_ski_ski_de_fond(df)
        
    df_box_plot = df_temps_de_ski
        
    df_moy_3_tours = df.iloc[:, :4].copy()
    df_moy_3_tours_normed = df.iloc[:, :4].copy()

    for index_intermediaire in range(len(noms_intermediaires)):
        df_moy_3_tours[noms_intermediaires[index_intermediaire]] = 0
        df_moy_3_tours_normed[noms_intermediaires[index_intermediaire]] = 0
        for numero_du_tour in range(nombre_de_tours):
            df_moy_3_tours[noms_intermediaires[index_intermediaire]] += df_box_plot[split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[numero_du_tour][index_intermediaire]]/nombre_de_tours
            df_moy_3_tours_normed[noms_intermediaires[index_intermediaire]] += df_box_plot[split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[numero_du_tour][index_intermediaire]]/(nombre_de_tours*liste_distance_des_ST[index_intermediaire])        

    return df_moy_3_tours, df_moy_3_tours_normed    
    
def split_tour_par_tour_ski_de_fond(df, nombre_de_tours):
    liste_a_retourner = []
    liste_des_split = df.columns.tolist()[4:]
    nombre_de_split_par_tour = int(len(liste_des_split)/nombre_de_tours)
    for numero_tour in range(nombre_de_tours):
        liste_a_retourner.append(liste_des_split[numero_tour*nombre_de_split_par_tour:(1+numero_tour)*nombre_de_split_par_tour])
    # print("liste_a_retourner: " + str(liste_a_retourner))
    return liste_a_retourner
    
def df_temps_de_ski_ski_de_fond(df):
    
    df_temps_de_ski = df.copy()

    for index_biathlete in range(df.shape[0]):
        for index_intermediaire in range(len(df.columns.to_list()[5:])):
            df_temps_de_ski.iat[index_biathlete, index_intermediaire + 5] = df.iat[index_biathlete, index_intermediaire + 5] - df.iat[index_biathlete, index_intermediaire + 4] # 4 pour -1 + 5
    
    return df_temps_de_ski
    
### CONVERSION DES CHRONOS EN SECONDES

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
            return heures * 3600 + minutes * 60 + secondes + dixiemes / 10
    else:
        return float(chrono)    

### PERSONNALISATION DES TEXTES

# message d'erreur

def show_custom_error(message, place_to_write):
    custom_error = f"""
    <div style="
        max-width: 500px;
        margin: auto;
        border-radius: 5px;
        background-color: #ffcccc;
        padding: 10px;
        color: #990000;
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
    ">
        {message}
    </div>
    """
    place_to_write.markdown(custom_error, unsafe_allow_html=True)   

# message de succès

def show_custom_success(message, place_to_write):
    custom_error = f"""
    <div style="
        max-width: 500px;
        margin: auto;
        border-radius: 5px;
        background-color: #ccffcc;
        padding: 10px;
        color: #006600;
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
    ">
        {message}
    </div>
    """
    place_to_write.markdown(custom_error, unsafe_allow_html=True)   
       

# font-weight: bold;

# question posée à l'utilisateur

def show_custom_question(message, place_to_write):
    custom_question = f"""
    <div style="
        max-width: 500px;
        margin: auto;
        border-radius: 5px;
        background-color: #ffffcc;
        padding: 10px;
        color: black;
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
    ">
        {message}
    </div>
    """
    place_to_write.markdown(custom_question, unsafe_allow_html=True)
    
def capture_screenshot(driver, file_name="error_screenshot.png"):
    driver.save_screenshot(file_name)
    print(f"Capture d'écran sauvegardée sous {file_name}")
    
def save_html_content(driver, file_name="page_source.html"):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"Contenu HTML de la page sauvegardé sous {file_name}")