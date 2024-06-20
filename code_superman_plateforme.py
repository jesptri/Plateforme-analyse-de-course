import matplotlib.pyplot as plt
import streamlit as st

from code_moustache_plateforme import *
from code_analyse_individuelle_plateforme import *
from code_points_forts_faibles_plateforme import *
from code_analyse_portion_specifique_plateforme import *
from fonctions_utiles_code_plateforme import *




### TRACE DES GRAPHES SUPERMAN ET ECART A LA PREMIERE ###



@st.cache_data()
def graphes_superman_et_ecart_au_leader(df_temps_de_ski, liste_distance_au_depart_des_ST, df, indices_a_enlever, top_n, nationalites_a_afficher, indices, biathletes, nombre_de_shoots, avec_range, sport, df_temps_de_ski_et_temps_de_shoot):
    
    fontize_xticks = 6
    
    df_ecart_premiere_temps_reel_62 = df.copy()
    
    liste_des_meilleurs_chronos = []
    # print(df_temps_de_ski)
    # print(df_temps_de_ski.columns.tolist()[4:])
    
    # if avec_range:
    #     df_temps_de_ski = df

    for nom_colonne in df_temps_de_ski.columns.tolist()[4:]:
        for element in df_temps_de_ski[nom_colonne]:
            element = float(element)
        min_cl = df_temps_de_ski[nom_colonne].min()  
        liste_des_meilleurs_chronos.append(min_cl)
    df_ecart_premiere_temps_reel = df.copy()
    chronos_superman_biathletes = []
    
    df_temps_de_ski = df_temps_de_ski.sort_values(by='Ranking')
    df_temps_de_ski = df_temps_de_ski.reset_index(drop=True)
    print("df_temps_de_ski_et_temps_de_shoot: " + str(df_temps_de_ski_et_temps_de_shoot))
    
    # print(df_temps_de_ski)
    if not avec_range:
        for index_biathlete in range(df_temps_de_ski.shape[0]):
            if df_temps_de_ski.iloc[index_biathlete]["Ranking"] <= top_n or df_temps_de_ski.iloc[index_biathlete]["Country"] in nationalites_a_afficher or df_temps_de_ski.iloc[index_biathlete]["Name"] in biathletes:
                    
                chronos_par_biathlete = []
                chronos_par_biathlete.append(df_temps_de_ski.iloc[index_biathlete][1])
                chronos_par_biathlete.append(df_temps_de_ski.iloc[index_biathlete][2])
                chronos_par_biathlete.append(df_temps_de_ski.iloc[index_biathlete][3])
                ecart_grandissant = 0
                for index_intermediaire in range(len(df_temps_de_ski.columns.to_list()[4:])):
                    # print(index_intermediaire, len(liste_des_meilleurs_chronos), df_temps_de_ski.columns.to_list()[4:])
                    ecart_chrono_et_meilleur_chrono = liste_des_meilleurs_chronos[index_intermediaire] - df_temps_de_ski.iloc[index_biathlete][index_intermediaire+4]
                    ecart_grandissant = ecart_grandissant + ecart_chrono_et_meilleur_chrono 
                    chronos_par_biathlete.append(ecart_grandissant)
                # print(chronos_par_biathlete)
                chronos_superman_biathletes.append(chronos_par_biathlete)  
    else:
        for index_biathlete in range(df_temps_de_ski_et_temps_de_shoot.shape[0]):
            if df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete]["Ranking"] <= top_n or df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete]["Country"] in nationalites_a_afficher or df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete]["Name"] in biathletes:
                    
                chronos_par_biathlete = []
                chronos_par_biathlete.append(df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete][1])
                chronos_par_biathlete.append(df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete][2])
                chronos_par_biathlete.append(df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete][3])
                ecart_grandissant = 0
                for index_intermediaire in range(len(df_temps_de_ski_et_temps_de_shoot.columns.to_list()[4:])):
                    # print(index_intermediaire, len(liste_des_meilleurs_chronos), df_temps_de_ski_et_temps_de_shoot.columns.to_list()[4:])
                    ecart_chrono_et_meilleur_chrono = liste_des_meilleurs_chronos[index_intermediaire] - df_temps_de_ski_et_temps_de_shoot.iloc[index_biathlete][index_intermediaire+4]
                    ecart_grandissant = ecart_grandissant + ecart_chrono_et_meilleur_chrono 
                    chronos_par_biathlete.append(ecart_grandissant)
                # print(chronos_par_biathlete)
                chronos_superman_biathletes.append(chronos_par_biathlete)  
    # print("taille ordonnée sortie liste création: " + str(len(chronos_superman_biathletes[0][3:])))
    # print("chronos_superman_biathletes[0]: " + str(chronos_superman_biathletes[0]))

    
    ### CALCUL TEMPS SHOOT POUR LE DF PERSONNALISE

    temps_shoot_1 = df_ecart_premiere_temps_reel["Shooting 1"] - df_ecart_premiere_temps_reel["→ Shooting 1"]
    temps_shoot_2 = df_ecart_premiere_temps_reel["Shooting 2"] - df_ecart_premiere_temps_reel["→ Shooting 2"]
    
    if nombre_de_shoots == 4:
        temps_shoot_3 = df_ecart_premiere_temps_reel["Shooting 3"] - df_ecart_premiere_temps_reel["→ Shooting 3"]
        temps_shoot_4 = df_ecart_premiere_temps_reel["Shooting 4"] - df_ecart_premiere_temps_reel["→ Shooting 4"]

    ### SUPPRESSION DE CHRONOS POUR VISIBILITE SUR LE GRAPHE ### SUPERMAN 

    ## SUPPRIMER LES DEUX "AVANT SHOOT"
    if not avec_range:
        for chronos_biathlete in chronos_superman_biathletes:
            indice_colonne_shoot_1 = df.columns.get_loc("→ Shooting 1")
            del(chronos_biathlete[indice_colonne_shoot_1])
            indice_colonne_shoot_2 = df.columns.get_loc("→ Shooting 2")
            del(chronos_biathlete[indice_colonne_shoot_2-1]) 
            
            if nombre_de_shoots == 4:
                indice_colonne_shoot_3 = df.columns.get_loc("→ Shooting 3")
                del(chronos_biathlete[indice_colonne_shoot_3-2])
                indice_colonne_shoot_4 = df.columns.get_loc("→ Shooting 4")
                del(chronos_biathlete[indice_colonne_shoot_4-3])              
        
        ###  AU-DESSUS ###  EN REGARDANT LES CHRONOS J'AI VU QU'IL FALLAIT METTRE - 1 CAR UN PALIER ETAIT PRESENT AU DEBUT DU TOUR 3 POUR LES HOMMES ET LES FEMMES ###
    for chronos_biathlete in chronos_superman_biathletes:       
        chronos_biathlete.insert(3,0)
    # print("chronos_superman_biathletes[0]: " + str(chronos_superman_biathletes[0]))
        
    # print(chronos_superman_biathletes[17])
    
    nom_abscisse = df_temps_de_ski.columns.tolist()[4:]

    nom_abscisse_pour_plot = nom_abscisse.copy()
    if not avec_range:
        nom_abscisse_pour_plot.remove("→ Shooting 1") 
        nom_abscisse_pour_plot.remove("→ Shooting 2")
        if nombre_de_shoots == 4:
            nom_abscisse_pour_plot.remove("→ Shooting 3") 
            nom_abscisse_pour_plot.remove("→ Shooting 4")
    nom_abscisse_pour_plot.insert(0,"Départ")

    if not avec_range:
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 1")] = "Avant = après shoot 1"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 2")] = "Avant = après shoot 2"
        
        if nombre_de_shoots == 4:
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 3")] = "Avant = après shoot 3"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 4")] = "Avant = après shoot 4"
    else:
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 1")] = "Avant shoot 1"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 1")] = "Après shoot 1"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 2")] = "Avant shoot 2"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 2")] = "Après shoot 2"
        
        if nombre_de_shoots == 4:
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 3")] = "Avant shoot 3"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 3")] = "Après shoot 3"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 4")] = "Avant shoot 4"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 4")] = "Après shoot 4"

    liste_distance_au_depart_des_ST_pour_plot = liste_distance_au_depart_des_ST.copy()
    # print("taille abscisse début superman: " + str(len(liste_distance_au_depart_des_ST_pour_plot)))
    
    if not avec_range:
        if nombre_de_shoots == 4:
            liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[3]-4])
            liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[2]-4])
        
        liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[1]-4])
        liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[0]-4])
    liste_distance_au_depart_des_ST_pour_plot.insert(0,0)
    
    print("liste_distance_au_depart_des_ST_pour_plot: " + str(liste_distance_au_depart_des_ST_pour_plot))
    print("taille de liste_distance_au_depart_des_ST_pour_plot: " + str(len(liste_distance_au_depart_des_ST_pour_plot)))
    

    # print("taille abscisse superman: " + str(len(liste_distance_au_depart_des_ST_pour_plot)))
    # print("taille ordonnée superman: " + str(len(chronos_superman_biathletes[0])))
    # print("ordonnée superman: " + str(chronos_superman_biathletes[0]))
    

    ### PLOT ECART A LA PREMIERE EN TEMPS REEL ###

    if not avec_range:
        for intermediaire in df_ecart_premiere_temps_reel.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[3]:]:
            df_ecart_premiere_temps_reel[intermediaire] = df_ecart_premiere_temps_reel[intermediaire] - temps_shoot_1
        
        for intermediaire in df_ecart_premiere_temps_reel.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[4]:]:
            df_ecart_premiere_temps_reel[intermediaire] = df_ecart_premiere_temps_reel[intermediaire] - temps_shoot_2
        
        if nombre_de_shoots == 4:
            for intermediaire in df_ecart_premiere_temps_reel.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[8]:]:
                df_ecart_premiere_temps_reel[intermediaire] = df_ecart_premiere_temps_reel[intermediaire] - temps_shoot_3
        
            for intermediaire in df_ecart_premiere_temps_reel.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[9]:]:
                df_ecart_premiere_temps_reel[intermediaire] = df_ecart_premiere_temps_reel[intermediaire] - temps_shoot_4
        
    if not avec_range:
        for intermediaire in df_ecart_premiere_temps_reel_62.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[3]:]:
            df_ecart_premiere_temps_reel_62[intermediaire] = df_ecart_premiere_temps_reel_62[intermediaire] - temps_shoot_1
        
        for intermediaire in df_ecart_premiere_temps_reel_62.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[4]:]:
            df_ecart_premiere_temps_reel_62[intermediaire] = df_ecart_premiere_temps_reel_62[intermediaire] - temps_shoot_2
            
        if nombre_de_shoots == 4:
            for intermediaire in df_ecart_premiere_temps_reel_62.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[8]:]:
                df_ecart_premiere_temps_reel_62[intermediaire] = df_ecart_premiere_temps_reel_62[intermediaire] - temps_shoot_3
        
            for intermediaire in df_ecart_premiere_temps_reel_62.columns.to_list()[f_df_sans_temps_shoot(df, nombre_de_shoots)[9]:]:
                df_ecart_premiere_temps_reel_62[intermediaire] = df_ecart_premiere_temps_reel_62[intermediaire] - temps_shoot_4
        

    ### REPERAGE DU MEILLEUR CHRONO EN TEMPS DE SKI AU FINISH ###

    min_cl = df_ecart_premiere_temps_reel_62["Finish"].min()
    dossard_meilleure_tds_finish = df_ecart_premiere_temps_reel_62[df_ecart_premiere_temps_reel_62["Finish"] == min_cl].iloc[0,1]
    liste_chronos_premiere = []
    for index_colonne, nom_colonne in enumerate(df_ecart_premiere_temps_reel_62.columns.to_list()[4:]):
        liste_chronos_premiere.append(df_ecart_premiere_temps_reel_62[df_ecart_premiere_temps_reel_62["Bib"] == dossard_meilleure_tds_finish].iloc[0,index_colonne+4])
    chronos_ecart_premiere = []
    
    
        
    ###              SELECTION DE L'ECHANTILLON ICI                ###
    
    

    df_temps_de_ski = df_temps_de_ski.sort_values(by="Ranking")
    df_temps_de_ski = df_temps_de_ski[(df_temps_de_ski["Ranking"] <= top_n) | (df_temps_de_ski["Country"].isin(nationalites_a_afficher)) | (df_temps_de_ski["Name"].isin(biathletes))]
    df_temps_de_ski = df_temps_de_ski.reset_index(drop=True)
    
    df_ecart_premiere_temps_reel = df_ecart_premiere_temps_reel.sort_values(by="Ranking")
    df_ecart_premiere_temps_reel = df_ecart_premiere_temps_reel[(df_ecart_premiere_temps_reel["Ranking"] <= top_n) | (df_ecart_premiere_temps_reel["Country"].isin(nationalites_a_afficher)) | (df_ecart_premiere_temps_reel["Name"].isin(biathletes))] 
    df_ecart_premiere_temps_reel = df_ecart_premiere_temps_reel.reset_index(drop=True)
    
    for index_biathlete in range(df_ecart_premiere_temps_reel.shape[0]):
        chronos_par_biathlete = []
        chronos_par_biathlete.append(df_ecart_premiere_temps_reel.iloc[index_biathlete,1])
        chronos_par_biathlete.append(df_ecart_premiere_temps_reel.iloc[index_biathlete,2])
        chronos_par_biathlete.append(df_ecart_premiere_temps_reel.iloc[index_biathlete,3])
        for index_intermediaire in range(len(df_ecart_premiere_temps_reel.columns.to_list()[4:])):
            ecart_chrono_et_meilleur_chrono = liste_chronos_premiere[index_intermediaire] - df_ecart_premiere_temps_reel.iloc[index_biathlete][index_intermediaire+4] 
            chronos_par_biathlete.append(ecart_chrono_et_meilleur_chrono)
        chronos_ecart_premiere.append(chronos_par_biathlete)  
    # print(chronos_ecart_premiere)

    ### SUPPRESSION DE CHRONOS POUR VISIBILITE SUR LE GRAPHE ### ECART A LA PREMIERE


    for chronos_biathlete in chronos_ecart_premiere:
        if not avec_range:
            if nombre_de_shoots == 4:
                del(chronos_biathlete[indices_a_enlever[3]-1])            
                del(chronos_biathlete[indices_a_enlever[2]-1])
            del(chronos_biathlete[indices_a_enlever[1]-1]) ### indice est calculé sur le dataframe, sur les listes il y a la colonne Ranking en moins d'où le -1 !!!
            del(chronos_biathlete[indices_a_enlever[0]-1])
        chronos_biathlete.insert(3,0)
    
    nom_abscisse = df_ecart_premiere_temps_reel.columns.tolist()[4:]
    # print(nom_abscisse)

    nom_abscisse_pour_plot = nom_abscisse.copy()
    nom_abscisse_pour_plot.insert(0,"Départ")
    if not avec_range:
        nom_abscisse_pour_plot.remove("→ Shooting 1") 
        nom_abscisse_pour_plot.remove("→ Shooting 2")
        if nombre_de_shoots == 4:
            nom_abscisse_pour_plot.remove("→ Shooting 3") 
            nom_abscisse_pour_plot.remove("→ Shooting 4")

        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 1")] = "Fin du tour 1"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 2")] = "Fin du tour 2"
        if nombre_de_shoots == 4:
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 3")] = "Fin du tour 3"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 4")] = "Fin du tour 4" 
    else:   
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 1")] = "Entrée pas de tir 1"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 2")] = "Entrée pas de tir 2"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 1")] = "Sortie pas de tir 1"
        nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 2")] = "Sortie pas de tir 2"
        if nombre_de_shoots == 4:
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 3")] = "Entrée pas de tir 3"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("→ Shooting 4")] = "Entrée pas de tir 4"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 3")] = "Sortie pas de tir 3"
            nom_abscisse_pour_plot[nom_abscisse_pour_plot.index("Shooting 4")] = "Sortie pas de tir 4"

    # liste_distance_au_depart_des_ST_pour_plot = liste_distance_au_depart_des_ST.copy()
    
    # if nombre_de_shoots == 4:
    #     liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[3]-4])
    #     liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[2]-4])
        
    # liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[1]-4])
    # liste_distance_au_depart_des_ST_pour_plot.remove(liste_distance_au_depart_des_ST_pour_plot[indices_a_enlever[0]-4])
    # liste_distance_au_depart_des_ST_pour_plot.insert(0,0)
    
    indices = np.arange(len(liste_distance_au_depart_des_ST_pour_plot))

    ### PLOT SUPERMAN ###


    fig2 = plt.figure(figsize=(10,6))

    for biathlete_f in biathletes:
        # print("biathletes: " + str(biathletes))
        for chronos_ecart in chronos_superman_biathletes:
            # print("chronos_ecart: " + str(chronos_ecart))
            if biathlete_f == chronos_ecart[1]:
            
                if chronos_ecart[2] == "FRA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "GER":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "NOR":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "SWE":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "ITA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gray', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                    break
    for index_biathlete in range(len(chronos_superman_biathletes)):
        if chronos_superman_biathletes[index_biathlete][2] == "FRA" and ("FRA" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='royalblue', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "GER" and ("GER" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='black', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "NOR" and ("NOR" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='red', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "SWE" and ("SWE" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='gold', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "ITA" and ("ITA" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='limegreen', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        else:
            plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='lightgray', linewidth=0.4)

    plt.axhline(y=0, color='black', linewidth=0.1)#, alpha=0.25)
    plt.title("Ecart au superman (en secondes)", fontsize=12)
    plt.grid(True, color='black', linestyle = '--', linewidth=0.05)
    # print("liste_distance_au_depart_des_ST_pour_plot: " + str(liste_distance_au_depart_des_ST_pour_plot))
    # print("nom_abscisse_pour_plot: " + str(nom_abscisse_pour_plot))
    
    plt.xticks(liste_distance_au_depart_des_ST_pour_plot, nom_abscisse_pour_plot, rotation=90, fontsize=fontize_xticks)
            
    xtick_labels = plt.xticks()[1]
    for i, label in enumerate(xtick_labels):
        # print(label.get_text())
        if label.get_text() in ["Entrée pas de tir 1","Entrée pas de tir 2","Entrée pas de tir 3","Entrée pas de tir 4","Sortie pas de tir 1","Sortie pas de tir 2","Sortie pas de tir 3","Sortie pas de tir 4"]:
            plt.gca().get_xgridlines()[i].set_linewidth(0.5)
        else:
            plt.gca().get_xgridlines()[i].set_linewidth(0.05)
    
    
    limite_pour_plot_en_y = plt.ylim()[0]
    if not avec_range:
        plt.ylim(limite_pour_plot_en_y)
    # plt.ylabel("Ecart par rapport au Superman")
    plt.legend()  
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    
    
    
    # PLOT ECART MEILLEUR SKIEUR #
        
    fig1 = plt.figure(figsize=(10,6))   

    for biathlete_f in biathletes:
        for chronos_ecart in chronos_ecart_premiere:
            # print(chronos_ecart)
            # print(str(chronos_ecart[2]) + " " + str(chronos_ecart[1]) == biathlete_f)
            # print(str(chronos_ecart[2]) + " " + str(chronos_ecart[1]), biathlete_f)
            if str(chronos_ecart[1]) == biathlete_f:
                # print(chronos_ecart[2] == biathlete_f)
                if chronos_ecart[2] == "FRA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "GER":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "NOR":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "SWE":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "ITA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gray', linewidth=1.4)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                break
    for index_biathlete in range(df_ecart_premiere_temps_reel.shape[0]):
            if df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "FRA" and "FRA" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "FRA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "GER" and "GER" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "GER":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "NOR" and "NOR" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "NOR":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "SWE" and "SWE" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "SWE":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "ITA" and "ITA" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "ITA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            else:
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='lightgray', linewidth=0.4)#, label=chronos_ecart_premiere[index_biathlete][2])
                # plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][2], fontsize=8, va='center')


    plt.axhline(y=0, color='black', linewidth=0.1)
    plt.title("Ecart au meilleur skieur sur la course (en secondes)", fontsize=12)
    # labels = [str(label.get_text()) + "s" for label in plt.gca().get_yticklabels()]
    # plt.gca().set_yticklabels(labels)
    
    plt.grid(True, color='black', linestyle='--', linewidth=0.05)
    # print([liste_distance_au_depart_des_ST_pour_plot[i] for i in indices], [nom_abscisse_pour_plot[i] for i in indices])
    plt.xticks([liste_distance_au_depart_des_ST_pour_plot[i] for i in indices], [nom_abscisse_pour_plot[i] for i in indices], rotation=90, fontsize=fontize_xticks)
    
    xtick_labels = plt.xticks()[1]
    for i, label in enumerate(xtick_labels):
        # print(label.get_text())
        if label.get_text() in ["Entrée pas de tir 1","Entrée pas de tir 2","Entrée pas de tir 3","Entrée pas de tir 4","Sortie pas de tir 1","Sortie pas de tir 2","Sortie pas de tir 3","Sortie pas de tir 4"]:
            plt.gca().get_xgridlines()[i].set_linewidth(0.5)
        else:
            plt.gca().get_xgridlines()[i].set_linewidth(0.05)
            
            
    if not avec_range:
        plt.ylim(limite_pour_plot_en_y)
    
    # plt.ylabel("Ecart par rapport au leader en temps réel (s)")
    plt.legend()   
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.tight_layout() 
                  
    return fig1, fig2




### SKI DE FOND ###




@st.cache_data()
def graphes_superman_et_ecart_au_leader_ski_de_fond(df, liste_distance_au_depart_des_ST, top_n, nationalites_a_afficher, biathletes):
    
    fontize_xticks = 6
    
    df_ecart_premiere_temps_reel_62 = df.copy()
    
    liste_des_meilleurs_chronos = []
    # print(df_temps_de_ski)
    # print(df_temps_de_ski.columns.tolist()[4:])
    
    # if avec_range:
    #     df_temps_de_ski = df
    
    df_temps_de_ski = df_temps_de_ski_ski_de_fond(df)
    print("df_temps_de_ski_ca_ca: " + str(df_temps_de_ski))

    for nom_colonne in df_temps_de_ski.columns.tolist()[4:]:
        for element in df_temps_de_ski[nom_colonne]:
            element = float(element)
        min_cl = df_temps_de_ski[nom_colonne].min()  
        liste_des_meilleurs_chronos.append(min_cl)
    df_ecart_premiere_temps_reel = df.copy()
    chronos_superman_biathletes = []
    
    df_temps_de_ski = df_temps_de_ski.sort_values(by='Ranking')
    df_temps_de_ski = df_temps_de_ski.reset_index(drop=True)
    

    for index_biathlete in range(df_temps_de_ski.shape[0]):
        if df_temps_de_ski.iloc[index_biathlete]["Ranking"] <= top_n or df_temps_de_ski.iloc[index_biathlete]["Country"] in nationalites_a_afficher or df_temps_de_ski.iloc[index_biathlete]["Name"] in biathletes:
                
            chronos_par_biathlete = []
            chronos_par_biathlete.append(df_temps_de_ski.iloc[index_biathlete][1])
            chronos_par_biathlete.append(df_temps_de_ski.iloc[index_biathlete][2])
            chronos_par_biathlete.append(df_temps_de_ski.iloc[index_biathlete][3])
            ecart_grandissant = 0
            for index_intermediaire in range(len(df_temps_de_ski.columns.to_list()[4:])):
                # print(index_intermediaire, len(liste_des_meilleurs_chronos), df_temps_de_ski.columns.to_list()[4:])
                ecart_chrono_et_meilleur_chrono = liste_des_meilleurs_chronos[index_intermediaire] - df_temps_de_ski.iloc[index_biathlete][index_intermediaire+4]
                ecart_grandissant = ecart_grandissant + ecart_chrono_et_meilleur_chrono 
                chronos_par_biathlete.append(ecart_grandissant)
            # print(chronos_par_biathlete)
            chronos_superman_biathletes.append(chronos_par_biathlete)  
           
        
        ###  AU-DESSUS ###  EN REGARDANT LES CHRONOS J'AI VU QU'IL FALLAIT METTRE - 1 CAR UN PALIER ETAIT PRESENT AU DEBUT DU TOUR 3 POUR LES HOMMES ET LES FEMMES ###
    for chronos_biathlete in chronos_superman_biathletes:       
        chronos_biathlete.insert(3,0)
    # print("chronos_superman_biathletes[0]: " + str(chronos_superman_biathletes[0]))
        
    # print(chronos_superman_biathletes[17])
    
    nom_abscisse = df_temps_de_ski.columns.tolist()[4:]

    nom_abscisse_pour_plot = nom_abscisse.copy()

    nom_abscisse_pour_plot.insert(0,"Départ")

    liste_distance_au_depart_des_ST_pour_plot = liste_distance_au_depart_des_ST.copy()
    liste_distance_au_depart_des_ST_pour_plot.insert(0,0)
    
    print("liste_distance_au_depart_des_ST_pour_plot: " + str(liste_distance_au_depart_des_ST_pour_plot))
    print("taille de liste_distance_au_depart_des_ST_pour_plot: " + str(len(liste_distance_au_depart_des_ST_pour_plot)))
    

    # print("taille abscisse superman: " + str(len(liste_distance_au_depart_des_ST_pour_plot)))
    # print("taille ordonnée superman: " + str(len(chronos_superman_biathletes[0])))
    # print("ordonnée superman: " + str(chronos_superman_biathletes[0]))
    

    ### PLOT ECART A LA PREMIERE EN TEMPS REEL ###

    ### REPERAGE DU MEILLEUR CHRONO EN TEMPS DE SKI AU FINISH ###

    min_cl = df_ecart_premiere_temps_reel_62["Finish"].min()
    dossard_meilleure_tds_finish = df_ecart_premiere_temps_reel_62[df_ecart_premiere_temps_reel_62["Finish"] == min_cl].iloc[0,1]
    liste_chronos_premiere = []
    for index_colonne, nom_colonne in enumerate(df_ecart_premiere_temps_reel_62.columns.to_list()[4:]):
        liste_chronos_premiere.append(df_ecart_premiere_temps_reel_62[df_ecart_premiere_temps_reel_62["Bib"] == dossard_meilleure_tds_finish].iloc[0,index_colonne+4])
    chronos_ecart_premiere = []
    
    
        
    ###              SELECTION DE L'ECHANTILLON ICI                ###
    
    

    df_temps_de_ski = df_temps_de_ski.sort_values(by="Ranking")
    df_temps_de_ski = df_temps_de_ski[(df_temps_de_ski["Ranking"] <= top_n) | (df_temps_de_ski["Country"].isin(nationalites_a_afficher)) | (df_temps_de_ski["Name"].isin(biathletes))]
    df_temps_de_ski = df_temps_de_ski.reset_index(drop=True)
    
    df_ecart_premiere_temps_reel = df_ecart_premiere_temps_reel.sort_values(by="Ranking")
    df_ecart_premiere_temps_reel = df_ecart_premiere_temps_reel[(df_ecart_premiere_temps_reel["Ranking"] <= top_n) | (df_ecart_premiere_temps_reel["Country"].isin(nationalites_a_afficher)) | (df_ecart_premiere_temps_reel["Name"].isin(biathletes))] 
    df_ecart_premiere_temps_reel = df_ecart_premiere_temps_reel.reset_index(drop=True)
    
    for index_biathlete in range(df_ecart_premiere_temps_reel.shape[0]):
        chronos_par_biathlete = []
        chronos_par_biathlete.append(df_ecart_premiere_temps_reel.iloc[index_biathlete,1])
        chronos_par_biathlete.append(df_ecart_premiere_temps_reel.iloc[index_biathlete,2])
        chronos_par_biathlete.append(df_ecart_premiere_temps_reel.iloc[index_biathlete,3])
        for index_intermediaire in range(len(df_ecart_premiere_temps_reel.columns.to_list()[4:])):
            ecart_chrono_et_meilleur_chrono = liste_chronos_premiere[index_intermediaire] - df_ecart_premiere_temps_reel.iloc[index_biathlete][index_intermediaire+4] 
            chronos_par_biathlete.append(ecart_chrono_et_meilleur_chrono)
        chronos_ecart_premiere.append(chronos_par_biathlete)  
    # print(chronos_ecart_premiere)

    ### SUPPRESSION DE CHRONOS POUR VISIBILITE SUR LE GRAPHE ### ECART A LA PREMIERE


    for chronos_biathlete in chronos_ecart_premiere:
        chronos_biathlete.insert(3,0)
    
    nom_abscisse = df_ecart_premiere_temps_reel.columns.tolist()[4:]
    # print(nom_abscisse)

    nom_abscisse_pour_plot = nom_abscisse.copy()
    nom_abscisse_pour_plot.insert(0,"Départ")
    
    indices = np.arange(len(liste_distance_au_depart_des_ST_pour_plot))

    ### PLOT SUPERMAN ###


    fig2 = plt.figure(figsize=(10,6))

    for biathlete_f in biathletes:
        # print("biathletes: " + str(biathletes))
        for chronos_ecart in chronos_superman_biathletes:
            # print("chronos_ecart: " + str(chronos_ecart))
            if biathlete_f == chronos_ecart[1]:
            
                if chronos_ecart[2] == "FRA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "GER":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "NOR":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "SWE":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "ITA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gray', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                    break
    for index_biathlete in range(len(chronos_superman_biathletes)):
        if chronos_superman_biathletes[index_biathlete][2] == "FRA" and ("FRA" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='royalblue', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "GER" and ("GER" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='black', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "NOR" and ("NOR" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='red', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "SWE" and ("SWE" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='gold', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        elif chronos_superman_biathletes[index_biathlete][2] == "ITA" and ("ITA" in nationalites_a_afficher or chronos_superman_biathletes[index_biathlete][1] in biathletes):
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='limegreen', linewidth=1.2)
                plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_superman_biathletes[index_biathlete][-1], chronos_superman_biathletes[index_biathlete][1], fontsize=8, va='center')
        else:
            # print("ABSCISSE: " + str(liste_distance_au_depart_des_ST_pour_plot))
            # print("ORDONNEE: " + str(chronos_superman_biathletes[index_biathlete][3:]))
            plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_superman_biathletes[index_biathlete][3:], color='lightgray', linewidth=0.4)

    plt.axhline(y=0, color='black', linewidth=0.1)#, alpha=0.25)
    plt.title("Ecart au superman (en secondes)", fontsize=12)
    plt.grid(True, color='black', linestyle = '--', linewidth=0.05)
    # print("liste_distance_au_depart_des_ST_pour_plot: " + str(liste_distance_au_depart_des_ST_pour_plot))
    # print("nom_abscisse_pour_plot: " + str(nom_abscisse_pour_plot))
    
    print("nom abscisse: " + str(liste_distance_au_depart_des_ST_pour_plot))
    print("nom ordonnée: " + str(nom_abscisse_pour_plot))
    
    plt.xticks(liste_distance_au_depart_des_ST_pour_plot, nom_abscisse_pour_plot, rotation=90, fontsize=fontize_xticks)
            
    xtick_labels = plt.xticks()[1]
    for i, label in enumerate(xtick_labels):
        # print(label.get_text())
        if label.get_text() in ["Entrée pas de tir 1","Entrée pas de tir 2","Entrée pas de tir 3","Entrée pas de tir 4","Sortie pas de tir 1","Sortie pas de tir 2","Sortie pas de tir 3","Sortie pas de tir 4"]:
            plt.gca().get_xgridlines()[i].set_linewidth(0.5)
        else:
            plt.gca().get_xgridlines()[i].set_linewidth(0.05)
    
    
    limite_pour_plot_en_y = plt.ylim()[0]

    plt.ylim(limite_pour_plot_en_y)
    # plt.ylabel("Ecart par rapport au Superman")
    plt.legend()  
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    
    
    
    # PLOT ECART MEILLEUR SKIEUR #
        
    fig1 = plt.figure(figsize=(10,6))   

    for biathlete_f in biathletes:
        for chronos_ecart in chronos_ecart_premiere:
            # print(chronos_ecart)
            # print(str(chronos_ecart[2]) + " " + str(chronos_ecart[1]) == biathlete_f)
            # print(str(chronos_ecart[2]) + " " + str(chronos_ecart[1]), biathlete_f)
            if str(chronos_ecart[1]) == biathlete_f:
                # print(chronos_ecart[2] == biathlete_f)
                if chronos_ecart[2] == "FRA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "GER":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "NOR":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "SWE":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                elif chronos_ecart[2] == "ITA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart[3:], color='gray', linewidth=1.4)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart[-1], chronos_ecart[1], fontsize=8, va='center')
                break
    for index_biathlete in range(df_ecart_premiere_temps_reel.shape[0]):
            if df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "FRA" and "FRA" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "FRA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='royalblue', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "GER" and "GER" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "GER":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='black', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "NOR" and "NOR" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "NOR":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='red', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "SWE" and "SWE" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "SWE":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='gold', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            elif df_ecart_premiere_temps_reel.iloc[index_biathlete,3] == "ITA" and "ITA" in nationalites_a_afficher:
                if df_temps_de_ski.iloc[index_biathlete,3] == "ITA":
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
                else:
                    plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='limegreen', linewidth=1.2)
                    plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][1], fontsize=8, va='center')
            else:
                plt.plot(liste_distance_au_depart_des_ST_pour_plot, chronos_ecart_premiere[index_biathlete][3:], color='lightgray', linewidth=0.4)#, label=chronos_ecart_premiere[index_biathlete][2])
                # plt.text(liste_distance_au_depart_des_ST_pour_plot[-1] + 0.1, chronos_ecart_premiere[index_biathlete][-1], chronos_ecart_premiere[index_biathlete][2], fontsize=8, va='center')


    plt.axhline(y=0, color='black', linewidth=0.1)
    plt.title("Ecart au meilleur skieur sur la course (en secondes)", fontsize=12)
    # labels = [str(label.get_text()) + "s" for label in plt.gca().get_yticklabels()]
    # plt.gca().set_yticklabels(labels)
    
    plt.grid(True, color='black', linestyle='--', linewidth=0.05)
    # print([liste_distance_au_depart_des_ST_pour_plot[i] for i in indices], [nom_abscisse_pour_plot[i] for i in indices])
    plt.xticks([liste_distance_au_depart_des_ST_pour_plot[i] for i in indices], [nom_abscisse_pour_plot[i] for i in indices], rotation=90, fontsize=fontize_xticks)
    
    xtick_labels = plt.xticks()[1]
    for i, label in enumerate(xtick_labels):
        # print(label.get_text())
        if label.get_text() in ["Entrée pas de tir 1","Entrée pas de tir 2","Entrée pas de tir 3","Entrée pas de tir 4","Sortie pas de tir 1","Sortie pas de tir 2","Sortie pas de tir 3","Sortie pas de tir 4"]:
            plt.gca().get_xgridlines()[i].set_linewidth(0.5)
        else:
            plt.gca().get_xgridlines()[i].set_linewidth(0.05)
            
            
    plt.ylim(limite_pour_plot_en_y)
    
    # plt.ylabel("Ecart par rapport au leader en temps réel (s)")
    plt.legend()   
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.tight_layout() 
                  
    return fig1, fig2
