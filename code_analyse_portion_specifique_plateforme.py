import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# from code_superman_plateforme import *

from fonctions_utiles_code_plateforme import split_tour_par_tour
from fonctions_utiles_code_plateforme import df_to_df_moy_3_tours
from fonctions_utiles_code_plateforme import f_df_sans_temps_shoot
from fonctions_utiles_code_plateforme import f_liste_distance_des_ST

from fonctions_utiles_code_plateforme import split_tour_par_tour_ski_de_fond
from fonctions_utiles_code_plateforme import df_to_df_moy_3_tours_ski_de_fond
from fonctions_utiles_code_plateforme import f_liste_distance_des_ST_ski_de_fond
from fonctions_utiles_code_plateforme import df_temps_de_ski_ski_de_fond
from fonctions_utiles_code_plateforme import custom_format

@st.cache_data()
def analyse_portion_specifique_graphe_1_sans_meme_echelle(df, biathletes_a_afficher, nationalites, liste_des_split_time, distance_de_1_tour, distance_toute_la_course, affichage, nombre_de_shoots, numero_du_tour):
    
    ### REPERER L'ATHLETE AU MEILLEUR TEMPS DE SKI PAR SON DOSSARD
    
    df_sans_temps_shoot = f_df_sans_temps_shoot(df, nombre_de_shoots)[7]

    dossard_meilleur_skieur = df_sans_temps_shoot.loc[df_sans_temps_shoot["Finish"].idxmin(), "Bib"]
    
    # Boucle pour remettre les split time dans l'ordre s'ils sont mélangés dans la liste argument
    
    tous_les_ST = []
    for splits_tour in split_tour_par_tour(df, nombre_de_shoots):
        tous_les_ST += splits_tour  
      
    split_time = []
    for splits_tour in split_tour_par_tour(df, nombre_de_shoots):
        split_time += splits_tour
      
    split_time = [split for split in split_time if split in liste_des_split_time]
    
    noms_de_tous_les_splits = []
    for numero_tour in range(nombre_de_shoots+1):
        noms_de_tous_les_splits += split_tour_par_tour(df, nombre_de_shoots)[numero_tour]
           
    nombre_de_ST = len(liste_des_split_time)
    
    indices_de_tous_les_ST = []
    
    for indice_split, split in enumerate(tous_les_ST):
        for split_bis in liste_des_split_time:
            if split == split_bis:
                indices_de_tous_les_ST.append(indice_split)

    df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0].sort_values(by="Ranking") # 0 et pas -1

    liste_pour_plot_en_abscisse = [0]

    for index_split in range(nombre_de_ST):
        if indices_de_tous_les_ST[0] == 0:
            liste_pour_plot_en_abscisse.append(round(f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]],1)) 
        else:
            liste_pour_plot_en_abscisse.append(round(liste_pour_plot_en_abscisse[-1] + f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]] - f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]-1],1)) 
        
    for nom_colonne in df_temps_de_ski.columns.tolist()[4:]:
        if nom_colonne not in noms_de_tous_les_splits:
                df_temps_de_ski.drop(nom_colonne, axis=1, inplace=True)     
                
    df_analyse_portion_specifique = df_temps_de_ski.iloc[:, :4].copy()

    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique[split_time[index_portion]] = df_temps_de_ski[liste_des_split_time[index_portion]]
        
    df_analyse_portion_specifique["Temps total"] = 0
    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique["Temps total"] +=  df_temps_de_ski[liste_des_split_time[index_portion]]

    fig_analyse_portion_specifique = plt.figure()
    
    df_analyse_portion_specifique.sort_values(by="Temps total", inplace=True)
    df_analyse_portion_specifique.reset_index(inplace=True, drop=True)
    
    df_best_selected_athlete = df_analyse_portion_specifique[df_analyse_portion_specifique["Name"].isin(biathletes_a_afficher) | df_analyse_portion_specifique["Country"].isin(nationalites)]
           
    
    ### SI MEILLEUR SKIEUR ###
 
    if affichage == "Athlète au meilleur temps de ski sur la course":
        
        best_skiier_row = df_analyse_portion_specifique[df_analyse_portion_specifique["Bib"] == dossard_meilleur_skieur]
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, 0, best_skiier_row.iloc[0, 2])# + " - meilleur temps de ski sur la course")
        
        for index_biathlete in range(0,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                if df_best_selected_athlete.iloc[index_biathlete, 2] == best_skiier_row.iloc[0, 2]:
                    pass
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        y_min = plt.ylim()[0]        
        y_max = plt.ylim()[1]
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            # print("split_time: " + str(split_time))
            # print(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time)
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)

        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
    
    ### SI MEILLEUR ATHLETE SELECTIONNE ### 
    
    elif affichage == "Meilleur athlète sélectionné/e":
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, 0, df_best_selected_athlete.iloc[0, 2])
        
        for index_biathlete in range(1,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                
                if df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1], liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        y_min = plt.ylim()[0]        
        y_max = plt.ylim()[1]
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
         
        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
         
    ### SI SUPERMAN DE LA COURSE ###  
        
    elif affichage == "Superman":
        
        meilleurs_temps_de_ski = []
    
        for intermediaire in df_analyse_portion_specifique.columns.tolist()[4:]:
            meilleurs_temps_de_ski.append(df_analyse_portion_specifique[intermediaire].min())
        
        for index_biathlete in range(1,df_analyse_portion_specifique.shape[0]):
            if df_analyse_portion_specifique.iloc[index_biathlete, 2] in biathletes_a_afficher or df_analyse_portion_specifique.iloc[index_biathlete, 3] in nationalites:
                
                if df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        y_min = plt.ylim()[0]        
        y_max = plt.ylim()[1]
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
            
        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
            
    ### SI SUPERMAN DE LA PORTION SELECTIONNEE ###
            
        
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    
    return fig_analyse_portion_specifique, y_min, y_max

@st.cache_data()
def analyse_portion_specifique_graphe_1(df, biathletes_a_afficher, nationalites, liste_des_split_time, distance_de_1_tour, distance_toute_la_course, affichage, nombre_de_shoots, limite_y_min, limite_y_max, numero_du_tour):
    
    ### REPERER L'ATHLETE AU MEILLEUR TEMPS DE SKI PAR SON DOSSARD
    
    df_sans_temps_shoot = f_df_sans_temps_shoot(df, nombre_de_shoots)[7]

    dossard_meilleur_skieur = df_sans_temps_shoot.loc[df_sans_temps_shoot["Finish"].idxmin(), "Bib"]
    
    # Boucle pour remettre les split time dans l'ordre s'ils sont mélangés dans la liste argument
    
    tous_les_ST = []
    for splits_tour in split_tour_par_tour(df, nombre_de_shoots):
        tous_les_ST += splits_tour  
       

    split_time = []  
    for splits_tour in split_tour_par_tour(df, nombre_de_shoots):
        split_time += splits_tour
        

    split_time = [split for split in split_time if split in liste_des_split_time]
    
    noms_de_tous_les_splits = []
    for numero_tour in range(nombre_de_shoots+1):
        noms_de_tous_les_splits += split_tour_par_tour(df, nombre_de_shoots)[numero_tour]
               
    nombre_de_ST = len(liste_des_split_time)
    
    indices_de_tous_les_ST = []
    
    for indice_split, split in enumerate(tous_les_ST):
        for split_bis in liste_des_split_time:
            if split == split_bis:
                indices_de_tous_les_ST.append(indice_split)
    df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0].sort_values(by="Ranking")


    liste_pour_plot_en_abscisse = [0]
    for index_split in range(nombre_de_ST):
        if indices_de_tous_les_ST[0] == 0:
            liste_pour_plot_en_abscisse.append(round(f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]],1)) 
        else:
            liste_pour_plot_en_abscisse.append(round(liste_pour_plot_en_abscisse[-1] + f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]] - f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]-1],1)) 

    # print("liste_pour_plot_en_abscisse: " + str(liste_pour_plot_en_abscisse))

    for nom_colonne in df_temps_de_ski.columns.tolist()[4:]:
        if nom_colonne not in noms_de_tous_les_splits:
            df_temps_de_ski.drop(nom_colonne, axis=1, inplace=True)            

    # print(df_temps_de_ski)

    df_analyse_portion_specifique = df_temps_de_ski.iloc[:, :4].copy()

    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique[split_time[index_portion]] = df_temps_de_ski[liste_des_split_time[index_portion]]
        
    df_analyse_portion_specifique["Temps total"] = 0
    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique["Temps total"] +=  df_temps_de_ski[liste_des_split_time[index_portion]]

    fig_analyse_portion_specifique = plt.figure()
    
    df_analyse_portion_specifique.sort_values(by="Temps total", inplace=True)
    df_analyse_portion_specifique.reset_index(inplace=True, drop=True)
    
    df_best_selected_athlete = df_analyse_portion_specifique[df_analyse_portion_specifique["Name"].isin(biathletes_a_afficher) | df_analyse_portion_specifique["Country"].isin(nationalites)]
           
    
    ### SI MEILLEUR SKIEUR ###
    
 
    if affichage == "Athlète au meilleur temps de ski sur la course":
        
        best_skiier_row = df_analyse_portion_specifique[df_analyse_portion_specifique["Bib"] == dossard_meilleur_skieur]
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, 0, best_skiier_row.iloc[0, 2])# + " - meilleur temps de ski sur la course")
        
        for index_biathlete in range(0,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                if df_best_selected_athlete.iloc[index_biathlete, 2] == best_skiier_row.iloc[0, 2]:
                    pass
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            # print("split_time: " + str(split_time))
            # print(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time)
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)

        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
    
    ### SI MEILLEUR ATHLETE SELECTIONNE ### 
    
    
    elif affichage == "Meilleur athlète sélectionné/e":
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, 0, df_best_selected_athlete.iloc[0, 2])
        
        for index_biathlete in range(1,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                
                if df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
        
        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
        
    ### SI SUPERMAN DE LA COURSE ###
    
        
        
    elif affichage == "Superman":
        
        meilleurs_temps_de_ski = []
    
        for intermediaire in df_analyse_portion_specifique.columns.tolist()[4:]:
            meilleurs_temps_de_ski.append(df_analyse_portion_specifique[intermediaire].min())
        
        for index_biathlete in range(1,df_analyse_portion_specifique.shape[0]):
            if df_analyse_portion_specifique.iloc[index_biathlete, 2] in biathletes_a_afficher or df_analyse_portion_specifique.iloc[index_biathlete, 3] in nationalites:
                
                if df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
        
        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
        
    ### SI SUPERMAN DE LA PORTION SELECTIONNEE ###
            
        
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.ylim(limite_y_min, limite_y_max)
    
    return fig_analyse_portion_specifique

@st.cache_data()
def analyse_portion_specifique_ratio_individuel(df, top_n, split_amont, nationalites_a_afficher, biathletes_a_afficher, homme_ou_femme, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots, sport, nombre_de_tours): 
    
    df_filtered = df.loc[(df['Ranking'] <= top_n) | (df['Country'].isin(nationalites_a_afficher)) | (df['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    
    if sport == "Biathlon":
        df_temps_de_ski = f_df_sans_temps_shoot(df_filtered, nombre_de_shoots)[0]
        indice_split_amont = df.columns.get_loc(split_amont) - 4
        distance_portion_amont = f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[0][indice_split_amont]        
        indice_split_aval = df.columns.get_loc(split_amont) - 3
        distance_portion_aval = f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[0][indice_split_aval]
    else:
        df_temps_de_ski = df_temps_de_ski_ski_de_fond(df_filtered)
        indice_split_amont = df.columns.get_loc(split_amont) - 4
        distance_portion_amont = f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indice_split_amont]        
        indice_split_aval = df.columns.get_loc(split_amont) - 3
        distance_portion_aval = f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indice_split_aval]        
        
          
    ### TOP n ###
    
    fig_ratio_top_N = plt.figure()

    df_ratio = df_temps_de_ski.iloc[:, :4].copy()
    if sport == "Biathlon":
        if nombre_de_shoots == 2:
            df_ratio["Portion 1"] = (df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[0][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[1][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[2][indice_split_amont]])/3
            df_ratio["Portion 2"] = (df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[0][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[1][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[2][indice_split_aval]])/3
        if nombre_de_shoots == 4:
            df_ratio["Portion 1"] = (df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[0][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[1][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[2][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[3][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[4][indice_split_amont]])/5
            df_ratio["Portion 2"] = (df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[0][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[1][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[2][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[3][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df_filtered, nombre_de_shoots)[4][indice_split_aval]])/5
    else:
        df_ratio["Portion 1"] = 0
        df_ratio["Portion 2"] = 0
        for numero_tour in range(nombre_de_tours):
            df_ratio["Portion 1"] += df_temps_de_ski[split_tour_par_tour_ski_de_fond(df_filtered, nombre_de_tours)[numero_tour][indice_split_amont]]
            df_ratio["Portion 2"] += df_temps_de_ski[split_tour_par_tour_ski_de_fond(df_filtered, nombre_de_tours)[numero_tour][indice_split_aval]]
            

    df_ratio["Temps total"] = df_ratio["Portion 1"] + df_ratio["Portion 2"]

    df_descente = df_ratio
    
    for index_biathlete in range(df_descente.shape[0]):
        vitesse_portion_1 = distance_portion_amont/df_descente.iloc[index_biathlete,4]
        vitesse_portion_2 = distance_portion_aval/df_descente.iloc[index_biathlete,5]
        
        
        if df_descente.iloc[index_biathlete,3] == "FRA":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, color="royalblue")
        elif df_descente.iloc[index_biathlete,3] == "NOR":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, color="red")
        elif df_descente.iloc[index_biathlete,3] == "SWE":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, color="gold")
        elif df_descente.iloc[index_biathlete,3] == "GER":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, color="black")
        elif df_descente.iloc[index_biathlete,3] == "ITA":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, color="limegreen")
        elif df_descente.iloc[index_biathlete,3] == "FIN":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, edgecolor='blue', color='white', hatch=['//'])
        elif df_descente.iloc[index_biathlete,3] == "USA":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, edgecolor='red', color='blue', hatch=["*"])
        elif df_descente.iloc[index_biathlete,3] == "SUI":
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, edgecolor='red', color='white')
        else:
            plt.bar(index_biathlete,vitesse_portion_2/vitesse_portion_1, color="gray")

    plt.title("Vitesse moyenne portion 2 % vitesse moyenne portion 1")

    min_y = min((df_descente.iloc[i,4]*distance_portion_aval) / (df_descente.iloc[i,5]*distance_portion_amont) for i in range(df_descente.shape[0])) - 0.05
    max_y = max((df_descente.iloc[i,4]*distance_portion_aval) / (df_descente.iloc[i,5]*distance_portion_amont) for i in range(df_descente.shape[0])) + 0.05

    plt.ylim(min_y, max_y)
    plt.xticks(np.arange(df_filtered.shape[0]), [df_filtered.iloc[index_biathlete]["Name"] for index_biathlete in range(df_filtered.shape[0])], rotation=90)
    plt.grid(True, axis='y', linewidth=0.2, color="grey")       
    plt.tight_layout()
    
    return fig_ratio_top_N

@st.cache_data()
def analyse_toutes_les_portions_individuel(df, noms_intermediaires, biathletes_a_afficher, nationalites_a_afficher, top_n_to_show, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
    
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]   
    
    df_moy_3_tours_filtered = df_moy_3_tours.loc[(df_moy_3_tours['Ranking'] <= top_n_to_show) | (df_moy_3_tours['Country'].isin(nationalites_a_afficher)) | (df_moy_3_tours['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    df_filtered = df.loc[(df['Ranking'] <= top_n_to_show) | (df['Country'].isin(nationalites_a_afficher)) | (df['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    
    fig_subplot = plt.figure()

    # plt.suptitle("Chronos moyens top 10 et français")

    for index_intermediate, intermediate in enumerate(noms_intermediaires):
                
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 3, index_intermediate+1)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 8:
            plt.subplot(2, 5, index_intermediate+1)            
        if len(noms_intermediaires) == 9:
            plt.subplot(2, 5, index_intermediate+1)            
        if len(noms_intermediaires) == 10:
            plt.subplot(2, 6, index_intermediate+1)  
            
        min_values = []
        max_values = []
        
        for index_biathlete, biathlete in enumerate(df_moy_3_tours_filtered['Name'].unique()):
            biathlete_data = df_moy_3_tours_filtered[df_moy_3_tours_filtered['Name'] == biathlete]
            if biathlete_data.iloc[0]["Country"] == "FRA":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='royalblue')
            elif biathlete_data.iloc[0]["Country"] == "NOR":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='red')
            elif biathlete_data.iloc[0]["Country"] == "GER":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='black')
            elif biathlete_data.iloc[0]["Country"] == "SWE":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='gold')
            elif biathlete_data.iloc[0]["Country"] == "ITA":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='limegreen')
            else:
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='lightgray')

            min_values.append(biathlete_data[intermediate].min())
            max_values.append(biathlete_data[intermediate].max())
        
        min_value = min(min_values)
        max_value = max(max_values)
        
        plt.ylim(min_value*0.9, max_value*1.1)
    
        plt.title(intermediate, fontsize=4)
        plt.yticks(fontsize=6)
        plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]), [str(df_moy_3_tours_filtered["Ranking"][i]) + " - " + df_moy_3_tours_filtered["Name"][i] for i in range(df_moy_3_tours_filtered.shape[0])], rotation=90, fontsize=4)
        plt.grid(True, axis='y', linewidth=0.2, color="grey")    
        plt.tight_layout()
        
        # plot de la partie dans le stand de tir
        
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 3, len(noms_intermediaires)+1)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, len(noms_intermediaires)+1)            
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 4, len(noms_intermediaires)+1)            
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, len(noms_intermediaires)+1)            
        if len(noms_intermediaires) == 8:
            plt.subplot(2, 5, len(noms_intermediaires)+1)            
        if len(noms_intermediaires) == 9:
            plt.subplot(2, 5, len(noms_intermediaires)+1)            
        if len(noms_intermediaires) == 10:
            plt.subplot(2, 6, len(noms_intermediaires)+1) 
            
        min_values_tir = []
        max_values_tir = []
        
        for index_biathlete, biathlete in enumerate(df_filtered['Name'].tolist()):
            valeur_ordonnee = 0
            if nombre_de_shoots == 2:
                valeur_ordonnee = (df_filtered.iloc[index_biathlete]["Shooting 2"] - df_filtered.iloc[index_biathlete]["→ Shooting 2"] + df_filtered.iloc[index_biathlete]["Shooting 1"] - df_filtered.iloc[index_biathlete]["→ Shooting 1"])/2
            else:
                valeur_ordonnee = (df_filtered.iloc[index_biathlete]["Shooting 4"] - df_filtered.iloc[index_biathlete]["→ Shooting 4"] + df_filtered.iloc[index_biathlete]["Shooting 3"] - df_filtered.iloc[index_biathlete]["→ Shooting 3"] + df_filtered.iloc[index_biathlete]["Shooting 2"] - df_filtered.iloc[index_biathlete]["→ Shooting 2"] + df_filtered.iloc[index_biathlete]["Shooting 1"] - df_filtered.iloc[index_biathlete]["→ Shooting 1"])/4
                        
            if df_filtered.iloc[index_biathlete]["Country"] == "FRA":
                plt.bar(index_biathlete, valeur_ordonnee, color='royalblue')
            elif df_filtered.iloc[index_biathlete]["Country"] == "NOR":
                plt.bar(index_biathlete, valeur_ordonnee, color='red')
            elif df_filtered.iloc[index_biathlete]["Country"] == "GER":
                plt.bar(index_biathlete, valeur_ordonnee, color='black')
            elif df_filtered.iloc[index_biathlete]["Country"] == "SWE":
                plt.bar(index_biathlete, valeur_ordonnee, color='gold')
            elif df_filtered.iloc[index_biathlete]["Country"] == "ITA":
                plt.bar(index_biathlete, valeur_ordonnee, color='limegreen')
            else:
                plt.bar(index_biathlete, valeur_ordonnee, color='lightgray')

            min_values_tir.append(valeur_ordonnee)
            max_values_tir.append(valeur_ordonnee)
    
            min_value_tir = min(min_values_tir)
            max_value_tir = max(max_values_tir)
        
            plt.ylim(min_value_tir -2, max_value_tir + 2)
    plt.grid(True, axis='y', linewidth=0.2, color="grey")    
    plt.title("Tous les tirs", fontsize=4)
    plt.yticks(fontsize=6)
    plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]),[str(df_moy_3_tours_filtered["Ranking"][i]) + " - " + df_moy_3_tours_filtered["Name"][i] for i in range(df_moy_3_tours_filtered.shape[0])], rotation=90, fontsize=4)

    plt.tight_layout()
    
    return fig_subplot

@st.cache_data()
def analyse_une_seule_portion_individuel(df, noms_intermediaires, intermediaire_a_afficher, biathletes_a_afficher, nationalites_a_afficher, top_n_to_show, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
    
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]   
    
    df_moy_3_tours_filtered = df_moy_3_tours.loc[(df_moy_3_tours['Ranking'] <= top_n_to_show) | (df_moy_3_tours['Country'].isin(nationalites_a_afficher)) | (df_moy_3_tours['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    df_filtered = df.loc[(df['Ranking'] <= top_n_to_show) | (df['Country'].isin(nationalites_a_afficher)) | (df['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    
    fig_intermediaire_seul = plt.figure()

    if intermediaire_a_afficher in ["Tir 1 et tir 2", "Tir 1, tir 2, tir 3 et tir 4"]:
        
            min_values = []
            max_values = []
            print("df_filtered: " + str(df_filtered))
            for index_biathlete, biathlete in enumerate(df_filtered['Name'].tolist()):
                valeur_ordonnee = 0
                if nombre_de_shoots == 2:
                    valeur_ordonnee = (df_filtered.iloc[index_biathlete]["Shooting 2"] - df_filtered.iloc[index_biathlete]["→ Shooting 2"] + df_filtered.iloc[index_biathlete]["Shooting 1"] - df_filtered.iloc[index_biathlete]["→ Shooting 1"])/2
                else:
                    valeur_ordonnee = (df_filtered.iloc[index_biathlete]["Shooting 4"] - df_filtered.iloc[index_biathlete]["→ Shooting 4"] + df_filtered.iloc[index_biathlete]["Shooting 3"] - df_filtered.iloc[index_biathlete]["→ Shooting 3"] + df_filtered.iloc[index_biathlete]["Shooting 2"] - df_filtered.iloc[index_biathlete]["→ Shooting 2"] + df_filtered.iloc[index_biathlete]["Shooting 1"] - df_filtered.iloc[index_biathlete]["→ Shooting 1"])/4
                print("valeur_ordonnee: " + str(valeur_ordonnee))
                if df_filtered.iloc[index_biathlete]["Country"] == "FRA":
                    plt.bar(index_biathlete, valeur_ordonnee, color='royalblue')
                elif df_filtered.iloc[index_biathlete]["Country"] == "NOR":
                    plt.bar(index_biathlete, valeur_ordonnee, color='red')
                elif df_filtered.iloc[index_biathlete]["Country"] == "GER":
                    plt.bar(index_biathlete, valeur_ordonnee, color='black')
                elif df_filtered.iloc[index_biathlete]["Country"] == "SWE":
                    plt.bar(index_biathlete, valeur_ordonnee, color='gold')
                elif df_filtered.iloc[index_biathlete]["Country"] == "ITA":
                    plt.bar(index_biathlete, valeur_ordonnee, color='limegreen')
                elif df_filtered.iloc[index_biathlete]["Country"] == "FIN":
                    plt.bar(index_biathlete, valeur_ordonnee, edgecolor='blue', color='white', hatch=['//'])
                elif df_filtered.iloc[index_biathlete]["Country"] == "USA":
                    plt.bar(index_biathlete, valeur_ordonnee, edgecolor='red', color='blue', hatch=["*"])
                elif df_filtered.iloc[index_biathlete]["Country"] == "SUI":
                    plt.bar(index_biathlete, valeur_ordonnee, edgecolor='red', color='white')
                else:
                    plt.bar(index_biathlete, valeur_ordonnee, color='lightgray')

                min_values.append(valeur_ordonnee)
                max_values.append(valeur_ordonnee)
        
                min_value = min(min_values)
                max_value = max(max_values)
            
                plt.ylim(min_value -2, max_value + 2)

    for intermediate in noms_intermediaires:
        
        if intermediate == intermediaire_a_afficher:
 
            min_values = []
            max_values = []
            
            for index_biathlete, biathlete in enumerate(df_moy_3_tours_filtered['Name'].unique()):
                biathlete_data = df_moy_3_tours_filtered[df_moy_3_tours_filtered['Name'] == biathlete]
                # print(biathlete_data)
                # print(type(biathlete_data))
                if biathlete_data.iloc[0]["Country"] == "FRA":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='royalblue')
                elif biathlete_data.iloc[0]["Country"] == "NOR":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='red')
                elif biathlete_data.iloc[0]["Country"] == "GER":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='black')
                elif biathlete_data.iloc[0]["Country"] == "SWE":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='gold')
                elif biathlete_data.iloc[0]["Country"] == "ITA":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='limegreen')
                elif biathlete_data.iloc[0]["Country"] == "FIN":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='blue', color='white', hatch=['//'])
                elif biathlete_data.iloc[0]["Country"] == "USA":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='red', color='blue', hatch=["*"])
                elif biathlete_data.iloc[0]["Country"] == "SUI":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='red', color='white')
                else:
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='lightgray')

                min_values.append(biathlete_data[intermediate].min())
                max_values.append(biathlete_data[intermediate].max())
        
                min_value = min(min_values)
                max_value = max(max_values)
            
                plt.ylim(min_value -2, max_value + 2)
        
        plt.grid(True, axis='y', linewidth=0.2, color="grey")    
        plt.title(intermediaire_a_afficher, fontsize=10)
        plt.ylabel('Chronos (s)')#, fontsize=10)
        plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]),[str(df_moy_3_tours_filtered["Ranking"][i]) + " - " + df_moy_3_tours_filtered["Name"][i] for i in range(df_moy_3_tours_filtered.shape[0])], rotation=90, fontsize=8)
        # plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]), df_moy_3_tours_filtered['Name'].unique(), rotation=90, fontsize=8)


    plt.tight_layout()
    
    return fig_intermediaire_seul

@st.cache_data()
def analyse_type_de_portion_individuel(df, noms_intermediaires, noms_intermediaires_bosses_arg, noms_intermediaires_descentes_arg, noms_intermediaires_vallonés_arg, noms_intermediaires_plats_arg, biathletes_a_afficher, nationalites_a_afficher, top_n_to_show, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
    
    if top_n_to_show < 25:
        police = 10
    elif top_n_to_show >= 25 and top_n_to_show < 45:
        police = 8
    elif top_n_to_show >= 45 and top_n_to_show <= 55:
        police = 6
    else:
        police = 4
    
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]
    
    df_moy_3_tours.sort_values(by="Ranking", inplace=True)
    df_moy_3_tours.reset_index(drop=True, inplace=True)
    
    data_biathletes = []
    
    min_max_bosses = []
    min_max_descentes = []
    min_max_plats = []
    min_max_vallonés = []
    
    for index_biathlete in range(df_moy_3_tours.shape[0]):
        
        if df_moy_3_tours.iloc[index_biathlete]["Ranking"] <= top_n_to_show or df_moy_3_tours.iloc[index_biathlete]["Country"] in nationalites_a_afficher or df_moy_3_tours.iloc[index_biathlete]["Name"] in biathletes_a_afficher:
        
            data_biathlete = []
            
            data_biathlete.append(df_moy_3_tours.iloc[index_biathlete]["Ranking"])
            data_biathlete.append(df_moy_3_tours.iloc[index_biathlete]["Bib"])
            data_biathlete.append(df_moy_3_tours.iloc[index_biathlete]["Name"])
            data_biathlete.append(df_moy_3_tours.iloc[index_biathlete]["Country"])
            
            chrono_bosses_biathlete = 0
            chrono_descentes_biathlete = 0
            chrono_plats_biathlete = 0
            chrono_vallonés_biathlete = 0
            
            for intermediaire in noms_intermediaires:
                if intermediaire in noms_intermediaires_bosses_arg:
                    chrono_bosses_biathlete += df_moy_3_tours.iloc[index_biathlete][intermediaire]
                elif intermediaire in noms_intermediaires_descentes_arg:
                    chrono_descentes_biathlete += df_moy_3_tours.iloc[index_biathlete][intermediaire]
                elif intermediaire in noms_intermediaires_plats_arg:
                    chrono_plats_biathlete += df_moy_3_tours.iloc[index_biathlete][intermediaire]
                elif intermediaire in noms_intermediaires_vallonés_arg:
                    chrono_vallonés_biathlete += df_moy_3_tours.iloc[index_biathlete][intermediaire]
            
            data_biathlete.append(chrono_bosses_biathlete)
            min_max_bosses.append(chrono_bosses_biathlete)
            
            data_biathlete.append(chrono_descentes_biathlete)
            min_max_descentes.append(chrono_descentes_biathlete)
            
            data_biathlete.append(chrono_plats_biathlete)
            min_max_plats.append(chrono_plats_biathlete)
            
            data_biathlete.append(chrono_vallonés_biathlete)
            min_max_vallonés.append(chrono_vallonés_biathlete)
            
            data_biathletes.append(data_biathlete)
                
    ### BOSSES ###
                
    fig_indiv_bosses = plt.figure(figsize=(8, 6))
    
    for index_biathlete, data_biathlete in enumerate(data_biathletes):   
        if data_biathlete[3] == "FRA":
            plt.bar(index_biathlete, data_biathlete[4], color="royalblue")
        elif data_biathlete[3] == "NOR":
            plt.bar(index_biathlete, data_biathlete[4], color="red")            
        elif data_biathlete[3] == "GER":
            plt.bar(index_biathlete, data_biathlete[4], color="black")            
        elif data_biathlete[3] == "SWE":
            plt.bar(index_biathlete, data_biathlete[4], color="gold")            
        elif data_biathlete[3] == "ITA":
            plt.bar(index_biathlete, data_biathlete[4], color="limegreen")  
        else:
            plt.bar(index_biathlete, data_biathlete[4], color="lightgray")            
                        
    plt.xticks(np.arange(len(data_biathletes)), [str(data_biathlete[0]) + " - " + data_biathlete[2] for data_biathlete in data_biathletes], rotation=90, fontsize=police)
    plt.grid(True, axis='y', linewidth=0.2, color="grey")    
    plt.ylim(min(min_max_bosses) - 1, max(min_max_bosses) + 1)
    plt.title("Bosses")
    
    ### DESCENTES ###
    
    fig_indiv_descentes = plt.figure(figsize=(8, 6))
    
    for index_biathlete, data_biathlete in enumerate(data_biathletes):
        if data_biathlete[3] == "FRA":
            plt.bar(index_biathlete, data_biathlete[5], color="royalblue")
        elif data_biathlete[3] == "NOR":
            plt.bar(index_biathlete, data_biathlete[5], color="red")            
        elif data_biathlete[3] == "GER":
            plt.bar(index_biathlete, data_biathlete[5], color="black")            
        elif data_biathlete[3] == "SWE":
            plt.bar(index_biathlete, data_biathlete[5], color="gold")            
        elif data_biathlete[3] == "ITA":
            plt.bar(index_biathlete, data_biathlete[5], color="limegreen")  
        else:
            plt.bar(index_biathlete, data_biathlete[5], color="lightgray")           
                        
    plt.xticks(np.arange(len(data_biathletes)), [str(data_biathlete[0]) + " - " + data_biathlete[2] for data_biathlete in data_biathletes], rotation=90, fontsize=police)
    plt.grid(True, axis='y', linewidth=0.2, color="grey")    
    plt.ylim(min(min_max_descentes) - 1, max(min_max_descentes) + 1)
    plt.title("Descentes")

    ### PLATS ###

    fig_indiv_plats = plt.figure(figsize=(8, 6))
    for index_biathlete, data_biathlete in enumerate(data_biathletes):
        if data_biathlete[3] == "FRA":
            plt.bar(index_biathlete, data_biathlete[6], color="royalblue")
        elif data_biathlete[3] == "NOR":
            plt.bar(index_biathlete, data_biathlete[6], color="red")            
        elif data_biathlete[3] == "GER":
            plt.bar(index_biathlete, data_biathlete[6], color="black")            
        elif data_biathlete[3] == "SWE":
            plt.bar(index_biathlete, data_biathlete[6], color="gold")            
        elif data_biathlete[3] == "ITA":
            plt.bar(index_biathlete, data_biathlete[6], color="limegreen")            
        else:
            plt.bar(index_biathlete, data_biathlete[6], color="lightgray") 

    plt.xticks(np.arange(len(data_biathletes)), [str(data_biathlete[0]) + " - " + data_biathlete[2] for data_biathlete in data_biathletes], rotation=90, fontsize=police)
    plt.grid(True, axis='y', linewidth=0.2, color="grey")    
    plt.ylim(min(min_max_plats) - 1, max(min_max_plats) + 1)
    plt.title("Plats")
    
    ### VALLONES ###
    
    fig_indiv_vallonés = plt.figure(figsize=(8, 6))
    for index_biathlete, data_biathlete in enumerate(data_biathletes):
        if data_biathlete[3] == "FRA":
            plt.bar(index_biathlete, data_biathlete[7], color="royalblue")
        elif data_biathlete[3] == "NOR":
            plt.bar(index_biathlete, data_biathlete[7], color="red")            
        elif data_biathlete[3] == "GER":
            plt.bar(index_biathlete, data_biathlete[7], color="black")            
        elif data_biathlete[3] == "SWE":
            plt.bar(index_biathlete, data_biathlete[7], color="gold")            
        elif data_biathlete[3] == "ITA":
            plt.bar(index_biathlete, data_biathlete[7], color="limegreen")     
        else:
            plt.bar(index_biathlete, data_biathlete[7], color="lightgray")        
                        
    plt.xticks(np.arange(len(data_biathletes)), [str(data_biathlete[0]) + " - " + data_biathlete[2] for data_biathlete in data_biathletes], rotation=90, fontsize=police)
    plt.grid(True, axis='y', linewidth=0.2, color="grey")    
    plt.ylim(min(min_max_vallonés) - 1, max(min_max_vallonés) + 1)
    plt.title("Vallonés")
    
    return fig_indiv_bosses, fig_indiv_descentes, fig_indiv_plats, fig_indiv_vallonés
    
    
    
### PAR NATIONALITE ###
    
    
    
@st.cache_data() 
def analyse_portion_specifique_ratio_nationalite(df, split_amont, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots): 
    
    df.sort_values(by='Finish', inplace=True)
    df.reset_index(drop="True", inplace=True)
    
    df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0]
        
    indice_split_amont = df.columns.get_loc(split_amont) - 4
    distance_portion_amont = f_liste_distance_des_ST(df,distance_de_1_tour, distance_toute_la_course)[0][indice_split_amont]
    
    indice_split_aval = df.columns.get_loc(split_amont) - 3
    distance_portion_aval = f_liste_distance_des_ST(df,distance_de_1_tour, distance_toute_la_course)[0][indice_split_aval]

    df_ratio = df_temps_de_ski.iloc[:, :4].copy()
    if nombre_de_shoots == 2:
        df_ratio["Portion 1"] = (df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[0][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[1][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[2][indice_split_amont]])/3
        df_ratio["Portion 2"] = (df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[0][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[1][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[2][indice_split_aval]])/3
    if nombre_de_shoots == 4:
        df_ratio["Portion 1"] = (df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[0][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[1][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[2][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[3][indice_split_amont]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[4][indice_split_amont]])/5
        df_ratio["Portion 2"] = (df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[0][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[1][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[2][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[3][indice_split_aval]] + df_temps_de_ski[split_tour_par_tour(df, nombre_de_shoots)[4][indice_split_aval]])/5
    
    df_ratio["Temps total"] = df_ratio["Portion 1"] + df_ratio["Portion 2"]

    ### NATIONALITE ###

    nationalites_interessantes = ["FRA", "NOR", "GER", "SWE", "ITA"]
    couleurs = ["royalblue", "red", "black", "gold", "limegreen"]
    
    ratios_pour_plot = []

    for nationalite in nationalites_interessantes:
        df_nat_boucle = df_ratio[df_ratio["Country"] == nationalite]
        
        if nationalite =="FRA":
            df_nat_boucle = df_nat_boucle.head(nombre_FRA)
        elif nationalite == "NOR":
            df_nat_boucle = df_nat_boucle.head(nombre_NOR)
        elif nationalite == "GER":
            df_nat_boucle = df_nat_boucle.head(nombre_GER)
        elif nationalite == "SWE":
            df_nat_boucle = df_nat_boucle.head(nombre_SWE)
        elif nationalite == "ITA":
            df_nat_boucle = df_nat_boucle.head(nombre_ITA)
            
        ratio_nat = []
        
        for index_biathlete in range(df_nat_boucle.shape[0]):
            vitesse_moyenne_portion_1 = distance_portion_amont/df_nat_boucle.iloc[index_biathlete]["Portion 1"]
            vitesse_moyenne_portion_2 = distance_portion_aval/df_nat_boucle.iloc[index_biathlete]["Portion 2"]
            ratio_nat.append(vitesse_moyenne_portion_2/vitesse_moyenne_portion_1)
        
        ratios_pour_plot.append(np.mean(ratio_nat))
     
    fig_ratio_nationalites = plt.figure()
    
    plt.bar(np.arange(len(nationalites_interessantes)), ratios_pour_plot, color = couleurs)

    plt.xticks([0,1,2,3,4], nationalites_interessantes)
    plt.title("Vitesse moyenne portion 2 % vitesse moyenne portion 1")
    plt.ylim(min(ratios_pour_plot) - 0.05, max(ratios_pour_plot) + 0.05)
    plt.tight_layout()
    
    return fig_ratio_nationalites
  
@st.cache_data 
def analyse_toutes_les_portions_nationalites(df, noms_intermediaires, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
    
    df.sort_values(by="Finish").reset_index(drop=True, inplace=True)
    
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]   
        
    fig_subplot = plt.figure()

    # plt.suptitle("Chronos moyens top 10 et français")
    
    nationalites = ["FRA", "NOR", "GER", "SWE", "ITA"]
    couleurs = ["royalblue", "red", "black", "gold", "limegreen"]

    for index_intermediate, intermediate in enumerate(noms_intermediaires):
        
        chronos_pour_plot_intermediaire = []
                
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 2, index_intermediate+1)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 8:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 9:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 10:
            plt.subplot(2, 5, index_intermediate+1)  
                    
        for nationalite in nationalites:
            
            df_nat_boucle = df_moy_3_tours[df_moy_3_tours["Country"] == nationalite]
            
            if nationalite =="FRA":
                df_nat_boucle = df_nat_boucle.head(nombre_FRA)
            elif nationalite == "NOR":
                df_nat_boucle = df_nat_boucle.head(nombre_NOR)
            elif nationalite == "GER":
                df_nat_boucle = df_nat_boucle.head(nombre_GER)
            elif nationalite == "SWE":
                df_nat_boucle = df_nat_boucle.head(nombre_SWE)
            elif nationalite == "ITA":
                df_nat_boucle = df_nat_boucle.head(nombre_ITA)
                
            chronos_pour_plot_intermediaire.append(df_nat_boucle[intermediate].mean())
       
        plt.bar(np.arange(len(nationalites)), chronos_pour_plot_intermediaire, color=couleurs)
        
        min_value = min(chronos_pour_plot_intermediaire)
        max_value = max(chronos_pour_plot_intermediaire)
        
        plt.ylim(min_value -2, max_value + 2)
    
        plt.title(intermediate, fontsize=4)
        plt.ylabel('Chronos (s)', fontsize=6)
        plt.yticks(fontsize=4)
        plt.xticks(np.arange(len(nationalites)), nationalites, rotation=90, fontsize=4)
        plt.grid(True, axis='y', linewidth=0.2, color="grey") 
        # plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]), df_moy_3_tours_filtered['Name'].unique(), rotation=90, fontsize=8)
        # plt.legend()

        plt.tight_layout()
    
    return fig_subplot  
  
@st.cache_data()
def analyse_une_seule_portion_nationalites(df, noms_intermediaires, intermediaire_a_afficher, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
   
    df.sort_values(by="Finish").reset_index(drop=True, inplace=True)
   
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]   
    
    fig = plt.figure()

    # plt.suptitle("Chronos moyens top 10 et français")
    
    nationalites = ["FRA", "NOR", "GER", "SWE", "ITA"]
    couleurs = ["royalblue", "red", "black", "gold", "limegreen"]

    for intermediate in noms_intermediaires:
        
        if intermediate == intermediaire_a_afficher:
        
            chronos_pour_plot_intermediaire = []
                    
            for nationalite in nationalites:
                
                df_nat_boucle = df_moy_3_tours[df_moy_3_tours["Country"] == nationalite]
                
                if nationalite =="FRA":
                    df_nat_boucle = df_nat_boucle.head(nombre_FRA)
                elif nationalite == "NOR":
                    df_nat_boucle = df_nat_boucle.head(nombre_NOR)
                elif nationalite == "GER":
                    df_nat_boucle = df_nat_boucle.head(nombre_GER)
                elif nationalite == "SWE":
                    df_nat_boucle = df_nat_boucle.head(nombre_SWE)
                elif nationalite == "ITA":
                    df_nat_boucle = df_nat_boucle.head(nombre_ITA)
                    
                chronos_pour_plot_intermediaire.append(df_nat_boucle[intermediate].mean())
        
            plt.bar(np.arange(len(nationalites)), chronos_pour_plot_intermediaire, color=couleurs)
            
            min_value = min(chronos_pour_plot_intermediaire)
            max_value = max(chronos_pour_plot_intermediaire)
            
            plt.ylim(min_value -2, max_value + 2)
        
            plt.title(intermediate, fontsize=8)
            plt.yticks(fontsize=8)
            plt.xticks(np.arange(len(nationalites)), nationalites, rotation=90, fontsize=8)
            plt.grid(True, axis='y', linewidth=0.2, color="grey")
            plt.tight_layout()
    
    return fig

@st.cache_data()
def analyse_type_de_portion_nationalite(df, noms_intermediaires, noms_intermediaires_bosses_arg, noms_intermediaires_descentes_arg, noms_intermediaires_plats_arg, noms_intermediaires_vallonés_arg, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, nombre_de_shoots, distance_de_1_tour, distance_toute_la_course):
    
    df.sort_values(by="Finish").reset_index(drop=True, inplace=True)
    
    noms_intermediaires_bosses = [intermediaire for intermediaire in noms_intermediaires_bosses_arg]
    noms_intermediaires_descentes = [intermediaire for intermediaire in noms_intermediaires_descentes_arg]
    noms_intermediaires_plats = [intermediaire for intermediaire in noms_intermediaires_plats_arg]    
    noms_intermediaires_vallonés = [intermediaire for intermediaire in noms_intermediaires_vallonés_arg]    
    
    df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0]

    nationalites_interessantes = ["FRA", "NOR", "GER", "SWE", "ITA"]

    chronos_type_portion_62 = []

    for index_biathlete in range(df_temps_de_ski.shape[0]):  
        # print("df_temps_de_ski.iloc[index_biathlete,3]: " + str(df_temps_de_ski.iloc[index_biathlete,3]))
        if df_temps_de_ski.iloc[index_biathlete,3] in nationalites_interessantes:
            temps_athlete = []
            temps_bosses = 0
            temps_descentes = 0
            temps_plats = 0
            temps_vallonés = 0
            temps_athlete.append(df_temps_de_ski.iloc[index_biathlete,0])
            temps_athlete.append(df_temps_de_ski.iloc[index_biathlete,2])
            temps_athlete.append(df_temps_de_ski.iloc[index_biathlete,3])
            for index_colonne, nom_colonne in enumerate(df_temps_de_ski.columns.tolist()):
                if nom_colonne in noms_intermediaires_bosses:
                    temps_bosses += df_temps_de_ski.iloc[index_biathlete,index_colonne]
                elif nom_colonne in noms_intermediaires_descentes:
                    temps_descentes += df_temps_de_ski.iloc[index_biathlete,index_colonne]
                elif nom_colonne in noms_intermediaires_plats:
                    temps_plats += df_temps_de_ski.iloc[index_biathlete,index_colonne]
                elif nom_colonne in noms_intermediaires_vallonés:
                    temps_vallonés += df_temps_de_ski.iloc[index_biathlete,index_colonne]
                                       
            temps_athlete.append(temps_bosses/3)
            temps_athlete.append(temps_descentes/3)
            temps_athlete.append(temps_plats/3)
            temps_athlete.append(temps_vallonés/3)
        
            chronos_type_portion_62.append(temps_athlete)

    liste_FRA = []
    liste_NOR = []
    liste_GER = []
    liste_SWE = []
    liste_ITA = []
    for index_biathlete, biathlete in enumerate(chronos_type_portion_62):
        if biathlete[2] == "FRA":
            liste_FRA.append(biathlete)
        if biathlete[2] == "NOR":
            liste_NOR.append(biathlete)
        if biathlete[2] == "GER":
            liste_GER.append(biathlete)
        if biathlete[2] == "SWE":
            liste_SWE.append(biathlete)
        if biathlete[2] == "ITA":
            liste_ITA.append(biathlete)
        

    ### EVOLUTION DES CHRONOS MOYENS DE CHAQUE PORTION ENTRE CHAQUE NATIONALITE ###

    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]
    
    # trois_ou_quatre_meilleures = 4

    couleurs = ['royalblue', 'red', 'black', 'gold', 'limegreen']

    chronos_par_nationalite = [[] for _ in range(len(nationalites_interessantes))]

    chronos_nat_bosses = [0 for nation in nationalites_interessantes]
    chronos_nat_descentes = [0 for nation in nationalites_interessantes]
    chronos_nat_plats = [0 for nation in nationalites_interessantes]
    chronos_nat_vallonés = [0 for nation in nationalites_interessantes]


    df_par_nationalite = df_moy_3_tours.copy()
    

    for index_intermediaire, nom_intermediaire in enumerate(noms_intermediaires):
        # print(index_intermediaire)
        # print([index_intermediaire, nom_intermediaire])
        for index_nationalite, nationalite in enumerate(nationalites_interessantes):
            if nationalite == "FRA":
                trois_ou_quatre_meilleures = nombre_FRA
            elif nationalite == "NOR":
                trois_ou_quatre_meilleures = nombre_NOR
            elif nationalite == "GER":
                trois_ou_quatre_meilleures = nombre_GER
            elif nationalite == "SWE":
                trois_ou_quatre_meilleures = nombre_SWE
            else:
                trois_ou_quatre_meilleures = nombre_ITA
                
            # print([index_nationalite, nationalite])
            df_nat_boucle = df_par_nationalite[df_par_nationalite["Country"] == nationalite]    
            
            ### GARDER LES N PREMIERES DE CHAQUE NATIONALITE ###
            
            df_nat_3 = df_nat_boucle.head(trois_ou_quatre_meilleures)
            df_nat_3 = df_nat_3.reset_index(drop=True)
            chronos_par_nationalite[index_nationalite].append(df_nat_3[nom_intermediaire].mean())
            
            if nom_intermediaire in noms_intermediaires_bosses:
                chronos_nat_bosses[index_nationalite] += df_nat_3[nom_intermediaire].mean() 
                
            elif nom_intermediaire in noms_intermediaires_descentes:
                chronos_nat_descentes[index_nationalite] += df_nat_3[nom_intermediaire].mean()

            elif nom_intermediaire in noms_intermediaires_plats:
                chronos_nat_plats[index_nationalite] += df_nat_3[nom_intermediaire].mean()

            elif nom_intermediaire in noms_intermediaires_vallonés:
                chronos_nat_vallonés[index_nationalite] += df_nat_3[nom_intermediaire].mean()
                
            # print("chronos_nat_bosses: " + str(chronos_nat_bosses))

    barWidth1 = 0.25

    fig_chronos_3_tours_nationalite = plt.figure()
    
    for i in range(len(noms_intermediaires)): ### l'intermédiaire 1 n'est pas intéressant, il ne débute pas au même endroit pour le tour 1 et les deux autres tours
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 2, i+1)
        if len(noms_intermediaires) == 5:
            plt.subplot(3, 2, i+1)            
        if len(noms_intermediaires) == 6:
            plt.subplot(3, 2, i+1)            
        if len(noms_intermediaires) == 7:
            plt.subplot(4, 2, i+1)            
        if len(noms_intermediaires) == 8:
            plt.subplot(4, 2, i+1)            
        if len(noms_intermediaires) == 9:
            plt.subplot(4, 2, i+1)            
        if len(noms_intermediaires) == 10:
            plt.subplot(5, 2, i+1)            
            
        r = np.arange(len(nationalites_interessantes)) + 1
       
        plt.bar(r, [chronos_par_nationalite[j][i] for j in range(0,len(nationalites_interessantes))], color=couleurs, width=barWidth1, edgecolor='grey')#, label=nationalites_interessantes)

        # Ajout des étiquettes des axes et du titre
        # plt.xlabel('Tours', fontweight='bold', fontsize=10)
        plt.ylabel('Chronos (secondes)', fontweight='bold', fontsize=10)
        
        # plt.title(noms_intermediaires[i-1], fontsize=12)
        # plt.xticks([r for r in range(1,4)], ['Tour 1', 'Tour 2', 'Tour 3'])
        
        plt.title(noms_intermediaires[i], fontsize=12)    
        plt.xticks([r for r in range(1,len(nationalites_interessantes)+1)], nationalites_interessantes, rotation=90, fontsize=8)
        
        plt.ylim(np.min([chronos_par_nationalite[j][i] for j in range(0,len(nationalites_interessantes))]) - 1, np.max([chronos_par_nationalite[j][i] for j in range(0,len(nationalites_interessantes))]) + 1)
        
        plt.legend()

        plt.tight_layout()
        

    ### PLOT DES CHRONOS MOYENS PAR TYPE DE PORTION ###


    barWidth2 = 0.5

    r = np.arange(len(nationalites_interessantes)) + 1

    fig_type_de_portion_bosses = plt.figure()

    plt.bar(r,chronos_nat_bosses, color=couleurs, width=barWidth2)
    plt.xticks([r for r in range(1,len(nationalites_interessantes)+1)], nationalites_interessantes, rotation=90, fontsize=8)
    # plt.ylabel("Chronos sommés (s)")
    plt.grid(True, axis='y', linewidth=0.2, color="grey") 
    plt.ylim(np.min([chronos_nat_bosses[j] for j in range(0,len(nationalites_interessantes))]) - 1, np.max([chronos_nat_bosses[j] for j in range(0,len(nationalites_interessantes))]) + 1)
    # plt.ylim(100, 160)
    plt.title("Bosses")

    fig_type_de_portion_descentes = plt.figure()

    plt.bar(r,chronos_nat_descentes, color=couleurs, width=barWidth2)
    plt.xticks([r for r in range(1,len(nationalites_interessantes)+1)], nationalites_interessantes, rotation=90, fontsize=8)
    # plt.ylabel("Chronos sommés (s)")
    plt.grid(True, axis='y', linewidth=0.2, color="grey") 
    plt.ylim(np.min([chronos_nat_descentes[j] for j in range(0,len(nationalites_interessantes))]) - 1, np.max([chronos_nat_descentes[j] for j in range(0,len(nationalites_interessantes))]) + 1)
    plt.title("Descentes")
   
    fig_type_de_portion_plats = plt.figure()
    
    plt.bar(r,chronos_nat_plats, color=couleurs, width=barWidth2)
    plt.xticks([r for r in range(1,len(nationalites_interessantes)+1)], nationalites_interessantes, rotation=90, fontsize=8)
    # plt.ylabel("Chronos sommés (s)")
    plt.grid(True, axis='y', linewidth=0.2, color="grey")    
    plt.ylim(np.min([chronos_nat_plats[j] for j in range(0,len(nationalites_interessantes))]) - 1, np.max([chronos_nat_plats[j] for j in range(0,len(nationalites_interessantes))]) + 1)
    plt.title("Plats")

    fig_type_de_portion_vallonés = plt.figure()
    
    plt.bar(r,chronos_nat_vallonés, color=couleurs, width=barWidth2)
    plt.xticks([r for r in range(1,len(nationalites_interessantes)+1)], nationalites_interessantes, rotation=90, fontsize=8)
    # plt.ylabel("Chronos sommés (s)")
    plt.grid(True, axis='y', linewidth=0.2, color="grey") 
    plt.ylim(np.min([chronos_nat_vallonés[j] for j in range(0,len(nationalites_interessantes))]) - 1, np.max([chronos_nat_vallonés[j] for j in range(0,len(nationalites_interessantes))]) + 1)
    plt.title("Vallonés")


    # plt.legend()
    plt.tight_layout()

    return fig_chronos_3_tours_nationalite, fig_type_de_portion_bosses, fig_type_de_portion_plats, fig_type_de_portion_descentes, fig_type_de_portion_vallonés

@st.cache_data()
def analyse_portion_specifique_graphe_1_par_nationalite(df, nationalites, liste_des_split_time, distance_de_1_tour, distance_toute_la_course, nb_FRA, nb_NOR, nb_GER, nb_SWE, nb_ITA, nombre_de_shoots):
    
    # Boucle pour remettre les split time dans l'ordre s'ils sont mélangés dans la liste argument
    
    tous_les_ST = split_tour_par_tour(df, nombre_de_shoots)[0] + split_tour_par_tour(df, nombre_de_shoots)[1] + split_tour_par_tour(df, nombre_de_shoots)[2]
    
    split_time = split_tour_par_tour(df, nombre_de_shoots)[0] + split_tour_par_tour(df, nombre_de_shoots)[1] + split_tour_par_tour(df, nombre_de_shoots)[2]
    
    # print("split_time avant: " + str(split_time))
    # print("liste_des_split_time: " + str(liste_des_split_time))
    
    split_time = [split for split in split_time if split in liste_des_split_time]
            
    # print("split_time après: " + str(split_time))   
    
    noms_tour_1 = split_tour_par_tour(df, nombre_de_shoots)[0]
    noms_tour_2 = split_tour_par_tour(df, nombre_de_shoots)[1]
    noms_tour_3 = split_tour_par_tour(df, nombre_de_shoots)[2]   
    
    nombre_de_ST = len(liste_des_split_time)
    
    indices_de_tous_les_ST = []
    
    for indice_split, split in enumerate(tous_les_ST):
        for indice_split_bis, split_bis in enumerate(liste_des_split_time):
            if split == split_bis:
                indices_de_tous_les_ST.append(indice_split)
                
    df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0].sort_values(by="Finish").reset_index(drop=True)

    liste_pour_plot_en_abscisse = [0]
    for index_split in range(nombre_de_ST):
        if indices_de_tous_les_ST[0] == 0:
            liste_pour_plot_en_abscisse.append(round(f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]],1)) 
        else:
            liste_pour_plot_en_abscisse.append(round(liste_pour_plot_en_abscisse[-1] + f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]] - f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]-1],1)) 
    
    # print("nombre_de_ST: " + str(nombre_de_ST))
    # print("liste_pour_plot_en_abscisse: " + str(liste_pour_plot_en_abscisse))
    # print("f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2]: " + str(f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2]))
    
    for index_colonne, nom_colonne in enumerate(df_temps_de_ski.columns.tolist()[4:]):
        if nom_colonne not in noms_tour_1 + noms_tour_2 + noms_tour_3:
            df_temps_de_ski.drop(nom_colonne, axis=1, inplace=True)

    df_analyse_portion_specifique = df_temps_de_ski.iloc[:, :4].copy()

    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique[split_time[index_portion]] = df_temps_de_ski[liste_des_split_time[index_portion]]
        
    df_analyse_portion_specifique["Temps total"] = 0
    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique["Temps total"] +=  df_temps_de_ski[liste_des_split_time[index_portion]]

    fig_analyse_portion_specifique = plt.figure()

    # print(df_analyse_portion_specifique)
    
    # df_analyse_portion_specifique.sort_values(by="Temps total", inplace=True)
    # df_analyse_portion_specifique.reset_index(inplace=True, drop=True)
    
    ### Trouver les meilleurs temps de ski pour ensuite comparer au superman ###
    
    meilleurs_temps_de_ski = []
    
    for intermediaire in df_analyse_portion_specifique.columns.tolist()[4:]:
        meilleurs_temps_de_ski.append(df_analyse_portion_specifique[intermediaire].min())
    
    # print("df_analyse_portion_specifique: " + str(df_analyse_portion_specifique))
    # print("df_best_selected_athlete: " + str(df_best_selected_athlete))
    # print("affichage: " + str(affichage))
    
    
    ### SI MEILLEUR ATHLETE SELECTIONNE ###
    
    
    for nationalite in nationalites:
        if nationalite == "FRA":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_FRA)  
            # print("df_nat: " + str(df_nat))
            couleur = "royalblue"
        elif nationalite == "NOR":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_NOR) 
            couleur = "red" 
        elif nationalite == "GER":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_GER)   
            couleur = "black" 
        elif nationalite == "SWE":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_SWE)  
            couleur = "gold"
        elif nationalite == "ITA":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_ITA)
            couleur = "limegreen"
 
        liste_ordonnee_biathlete = [0]                            
        for index in range(nombre_de_ST):
            temps_a_ajouter = liste_ordonnee_biathlete[-1]
            liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_nat.iloc[:,4 + index].mean()) # 4 + 1 + index pour commencer à 6 pour index 0
            # print("temps_a_ajouter: " + str(temps_a_ajouter) + " et meilleurs_temps_de_ski[index]: " + str(meilleurs_temps_de_ski[index]) + " et df_nat.iloc[:,4 + index].mean(): " + str(df_nat.iloc[:,4 + index].mean()))

        plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color=couleur)       
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, liste_ordonnee_biathlete[-1], nationalite)
                    
    plt.title("Evolution des écarts")
    plt.grid()
    if indices_de_tous_les_ST[0] == 0:
        plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
    else:
        plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)           
        
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    
    return fig_analyse_portion_specifique


### SKI DE FOND ###


@st.cache_data()
def analyse_portion_specifique_graphe_1_sans_meme_echelle_ski_de_fond(df, biathletes_a_afficher, nationalites, liste_des_split_time, affichage, nombre_de_tours, numero_du_tour):
    
    ### REPERER L'ATHLETE AU MEILLEUR TEMPS DE SKI PAR SON DOSSARD
    
    df_sans_temps_shoot = df
    
    dossard_meilleur_skieur = df_sans_temps_shoot.loc[df_sans_temps_shoot["Finish"].idxmin(), "Bib"]
    
    # Boucle pour remettre les split time dans l'ordre s'ils sont mélangés dans la liste argument
    
    tous_les_ST = []
    for splits_tour in split_tour_par_tour_ski_de_fond(df, nombre_de_tours):
        tous_les_ST += splits_tour           

    split_time = []
    for splits_tour in split_tour_par_tour_ski_de_fond(df, nombre_de_tours):
        split_time += splits_tour         

    split_time = [split for split in split_time if split in liste_des_split_time]
    
    noms_de_tous_les_splits = []
    for numero_tour in range(nombre_de_tours):
        noms_de_tous_les_splits += split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[numero_tour]
            
    
    nombre_de_ST = len(liste_des_split_time)
    
    indices_de_tous_les_ST = []
    
    for indice_split, split in enumerate(tous_les_ST):
        for split_bis in liste_des_split_time:
            if split == split_bis:
                indices_de_tous_les_ST.append(indice_split)
    
    df_temps_de_ski = df_temps_de_ski_ski_de_fond(df).sort_values(by="Ranking")
        
    liste_pour_plot_en_abscisse = [0]
    for index_split in range(nombre_de_ST):
        if indices_de_tous_les_ST[0] == 0:
            liste_pour_plot_en_abscisse.append(round(f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indices_de_tous_les_ST[index_split]],1)) 
        else:
            liste_pour_plot_en_abscisse.append(round(liste_pour_plot_en_abscisse[-1] + f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indices_de_tous_les_ST[index_split]] - f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indices_de_tous_les_ST[index_split]-1],1)) 
    
    for nom_colonne in df_temps_de_ski.columns.tolist()[4:]:
        if nom_colonne not in noms_de_tous_les_splits:
                df_temps_de_ski.drop(nom_colonne, axis=1, inplace=True)           

    df_analyse_portion_specifique = df_temps_de_ski.iloc[:, :4].copy()

    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique[split_time[index_portion]] = df_temps_de_ski[liste_des_split_time[index_portion]]
        
    df_analyse_portion_specifique["Temps total"] = 0
    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique["Temps total"] +=  df_temps_de_ski[liste_des_split_time[index_portion]]

    fig_analyse_portion_specifique = plt.figure()
    
    df_analyse_portion_specifique.sort_values(by="Temps total", inplace=True)
    df_analyse_portion_specifique.reset_index(inplace=True, drop=True)
    
    df_best_selected_athlete = df_analyse_portion_specifique[df_analyse_portion_specifique["Name"].isin(biathletes_a_afficher) | df_analyse_portion_specifique["Country"].isin(nationalites)]
           
    
    ### SI MEILLEUR SKIEUR ###
    
 
    if affichage == "Athlète au meilleur temps de ski sur la course":
        
        best_skiier_row = df_analyse_portion_specifique[df_analyse_portion_specifique["Bib"] == dossard_meilleur_skieur]
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, 0, best_skiier_row.iloc[0, 2])# + " - meilleur temps de ski sur la course")
        
        for index_biathlete in range(0,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                if df_best_selected_athlete.iloc[index_biathlete, 2] == best_skiier_row.iloc[0, 2]:
                    pass
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        y_min = plt.ylim()[0]        
        y_max = plt.ylim()[1]
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            # print("split_time: " + str(split_time))
            # print(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time)
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)

    
    ### SI MEILLEUR ATHLETE SELECTIONNE ### 
    
    
    elif affichage == "Meilleur athlète sélectionné/e":
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, 0, df_best_selected_athlete.iloc[0, 2])
        
        for index_biathlete in range(1,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                
                if df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1], liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        y_min = plt.ylim()[0]        
        y_max = plt.ylim()[1]
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
        
        
        
    ### SI SUPERMAN DE LA COURSE ###
    
        
        
    elif affichage == "Superman":
        
        meilleurs_temps_de_ski = []
    
        for intermediaire in df_analyse_portion_specifique.columns.tolist()[4:]:
            meilleurs_temps_de_ski.append(df_analyse_portion_specifique[intermediaire].min())
        
        for index_biathlete in range(1,df_analyse_portion_specifique.shape[0]):
            if df_analyse_portion_specifique.iloc[index_biathlete, 2] in biathletes_a_afficher or df_analyse_portion_specifique.iloc[index_biathlete, 3] in nationalites:
                
                if df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        y_min = plt.ylim()[0]        
        y_max = plt.ylim()[1]
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
        
        
    ### SI SUPERMAN DE LA PORTION SELECTIONNEE ###
            
        
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    
    return fig_analyse_portion_specifique, y_min, y_max

@st.cache_data()
def analyse_portion_specifique_graphe_1_ski_de_fond(df, biathletes_a_afficher, nationalites, liste_des_split_time, distance_de_1_tour, distance_toute_la_course, affichage, limite_y_min, limite_y_max, nombre_de_tours, numero_du_tour):
    
    ### REPERER L'ATHLETE AU MEILLEUR TEMPS DE SKI PAR SON DOSSARD
    
    df_sans_temps_shoot = df
            
    dossard_meilleur_skieur = df_sans_temps_shoot.loc[df_sans_temps_shoot["Finish"].idxmin(), "Bib"]
    
    # Boucle pour remettre les split time dans l'ordre s'ils sont mélangés dans la liste argument
    
    tous_les_ST = []
    for splits_tour in split_tour_par_tour_ski_de_fond(df, nombre_de_tours):
        tous_les_ST += splits_tour           

    split_time = []
    for splits_tour in split_tour_par_tour_ski_de_fond(df, nombre_de_tours):
        split_time += splits_tour         

    split_time = [split for split in split_time if split in liste_des_split_time]
    
    noms_de_tous_les_splits = []
    for numero_tour in range(nombre_de_tours):
        noms_de_tous_les_splits += split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[numero_tour]
    
    nombre_de_ST = len(liste_des_split_time)
    
    indices_de_tous_les_ST = []
    
    for indice_split, split in enumerate(tous_les_ST):
        for split_bis in liste_des_split_time:
            if split == split_bis:
                indices_de_tous_les_ST.append(indice_split)
    df_temps_de_ski = df_temps_de_ski_ski_de_fond(df).sort_values(by="Ranking")

    liste_pour_plot_en_abscisse = [0]
    for index_split in range(nombre_de_ST):
        if indices_de_tous_les_ST[0] == 0:
            liste_pour_plot_en_abscisse.append(round(f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]],1)) 
        else:
            liste_pour_plot_en_abscisse.append(round(liste_pour_plot_en_abscisse[-1] + f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]] - f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2][indices_de_tous_les_ST[index_split]-1],1)) 

    # print("liste_pour_plot_en_abscisse: " + str(liste_pour_plot_en_abscisse))

    for nom_colonne in df_temps_de_ski.columns.tolist()[4:]:
        if nom_colonne not in noms_de_tous_les_splits:
            df_temps_de_ski.drop(nom_colonne, axis=1, inplace=True)            

    # print(df_temps_de_ski)

    df_analyse_portion_specifique = df_temps_de_ski.iloc[:, :4].copy()

    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique[split_time[index_portion]] = df_temps_de_ski[liste_des_split_time[index_portion]]
        
    df_analyse_portion_specifique["Temps total"] = 0
    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique["Temps total"] +=  df_temps_de_ski[liste_des_split_time[index_portion]]

    fig_analyse_portion_specifique = plt.figure()
    
    df_analyse_portion_specifique.sort_values(by="Temps total", inplace=True)
    df_analyse_portion_specifique.reset_index(inplace=True, drop=True)
    
    df_best_selected_athlete = df_analyse_portion_specifique[df_analyse_portion_specifique["Name"].isin(biathletes_a_afficher) | df_analyse_portion_specifique["Country"].isin(nationalites)]
           
    
    ### SI MEILLEUR SKIEUR ###
    
 
    if affichage == "Athlète au meilleur temps de ski sur la course":
        
        best_skiier_row = df_analyse_portion_specifique[df_analyse_portion_specifique["Bib"] == dossard_meilleur_skieur]
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, 0, best_skiier_row.iloc[0, 2])# + " - meilleur temps de ski sur la course")
        
        for index_biathlete in range(0,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                if df_best_selected_athlete.iloc[index_biathlete, 2] == best_skiier_row.iloc[0, 2]:
                    pass
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + best_skiier_row.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            # print("split_time: " + str(split_time))
            # print(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time)
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)

        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
    
    ### SI MEILLEUR ATHLETE SELECTIONNE ### 
    
    
    elif affichage == "Meilleur athlète sélectionné/e":
        
        plt.plot(liste_pour_plot_en_abscisse, [0 for split in liste_pour_plot_en_abscisse], marker="*")
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, 0, df_best_selected_athlete.iloc[0, 2])
        
        for index_biathlete in range(1,df_best_selected_athlete.shape[0]):
            if df_best_selected_athlete.iloc[index_biathlete, 2] in biathletes_a_afficher or df_best_selected_athlete.iloc[index_biathlete, 3] in nationalites:
                
                if df_best_selected_athlete.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                elif df_best_selected_athlete.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + df_best_selected_athlete.iloc[0, 4 + index] - df_best_selected_athlete.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_best_selected_athlete.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
        
        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)
        
    ### SI SUPERMAN DE LA COURSE ###
    
        
        
    elif affichage == "Superman":
        
        meilleurs_temps_de_ski = []
    
        for intermediaire in df_analyse_portion_specifique.columns.tolist()[4:]:
            meilleurs_temps_de_ski.append(df_analyse_portion_specifique[intermediaire].min())
        
        for index_biathlete in range(1,df_analyse_portion_specifique.shape[0]):
            if df_analyse_portion_specifique.iloc[index_biathlete, 2] in biathletes_a_afficher or df_analyse_portion_specifique.iloc[index_biathlete, 3] in nationalites:
                
                if df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'FRA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="royalblue")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'GER':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="black")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'NOR':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="red")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'SWE':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gold")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                elif df_analyse_portion_specifique.iloc[index_biathlete, 3] == 'ITA':
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="limegreen")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                
                else:
                    liste_ordonnee_biathlete = [0]
                    for index in range(nombre_de_ST):
                        temps_a_ajouter = liste_ordonnee_biathlete[-1]
                        liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_analyse_portion_specifique.iloc[index_biathlete, 4 + index]) # 4 + 1 + index pour commencer à 6 pour index 0
                    # print(str(liste_pour_plot_en_abscisse) + " et " + str(liste_ordonnee_biathlete))
                    plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color="gray")       
                    plt.text(liste_pour_plot_en_abscisse[-1] + 0.01, liste_ordonnee_biathlete[-1], df_analyse_portion_specifique.iloc[index_biathlete, 2])
                        
        plt.title("Tour " + str(numero_du_tour))
        plt.grid()
        if indices_de_tous_les_ST[0] == 0:
            plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
        else:
            plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)
        
        formatter = plt.FuncFormatter(custom_format)
        plt.gca().yaxis.set_major_formatter(formatter)

    ### SI SUPERMAN DE LA PORTION SELECTIONNEE ###
            
        
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.ylim(limite_y_min, limite_y_max)
    
    return fig_analyse_portion_specifique

@st.cache_data()
def analyse_une_seule_portion_individuel_ski_de_fond(df, noms_intermediaires, intermediaire_a_afficher, biathletes_a_afficher, nationalites_a_afficher, top_n_to_show, nombre_de_tours):
    
    df_moy_3_tours = df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_tours)[0]   
    
    df_moy_3_tours_filtered = df_moy_3_tours.loc[(df_moy_3_tours['Ranking'] <= top_n_to_show) | (df_moy_3_tours['Country'].isin(nationalites_a_afficher)) | (df_moy_3_tours['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    
    fig_intermediaire_seul = plt.figure()

    for intermediate in noms_intermediaires:
        
        if intermediate == intermediaire_a_afficher:
 
            min_values = []
            max_values = []
            
            for index_biathlete, biathlete in enumerate(df_moy_3_tours_filtered['Name'].unique()):
                biathlete_data = df_moy_3_tours_filtered[df_moy_3_tours_filtered['Name'] == biathlete]
                if biathlete_data.iloc[0]["Country"] == "FRA":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='royalblue')
                elif biathlete_data.iloc[0]["Country"] == "NOR":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='red')
                elif biathlete_data.iloc[0]["Country"] == "GER":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='black')
                elif biathlete_data.iloc[0]["Country"] == "SWE":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='gold')
                elif biathlete_data.iloc[0]["Country"] == "ITA":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='limegreen')
                elif biathlete_data.iloc[0]["Country"] == "SUI":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='red', color='white')
                elif biathlete_data.iloc[0]["Country"] == "USA":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='red', color='blue', hatch=["*"])
                elif biathlete_data.iloc[0]["Country"] == "FIN":
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='blue', color='white', hatch=['//'])
                else:
                    plt.bar(index_biathlete, biathlete_data[intermediate].values, color='lightgray')

                min_values.append(biathlete_data[intermediate].min())
                max_values.append(biathlete_data[intermediate].max())
        
                min_value = min(min_values)
                max_value = max(max_values)
            
                plt.ylim(min_value -2, max_value + 2)
        
        plt.grid(True, axis='y', linewidth=0.2, color="grey")    
        plt.title(intermediaire_a_afficher, fontsize=10)
        plt.ylabel('Chronos (s)')#, fontsize=10)
        plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]),[str(df_moy_3_tours_filtered["Ranking"][i]) + " - " + df_moy_3_tours_filtered["Name"][i] for i in range(df_moy_3_tours_filtered.shape[0])], rotation=90, fontsize=8)
        # plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]), df_moy_3_tours_filtered['Name'].unique(), rotation=90, fontsize=8)


    plt.tight_layout()
    
    return fig_intermediaire_seul

@st.cache_data()
def analyse_toutes_les_portions_individuel_ski_de_fond(df, noms_intermediaires, biathletes_a_afficher, nationalites_a_afficher, top_n_to_show, nombre_de_tours):    
    
    df_moy_3_tours = df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_tours)[0]   
    
    df_moy_3_tours_filtered = df_moy_3_tours.loc[(df_moy_3_tours['Ranking'] <= top_n_to_show) | (df_moy_3_tours['Country'].isin(nationalites_a_afficher)) | (df_moy_3_tours['Name'].isin(biathletes_a_afficher))].sort_values(by='Ranking').reset_index(drop=True)
    
    fig_subplot = plt.figure()

    # plt.suptitle("Chronos moyens top 10 et français")

    for index_intermediate, intermediate in enumerate(noms_intermediaires):
                
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 2, index_intermediate+1)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 8:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 9:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 10:
            plt.subplot(2, 5, index_intermediate+1)  
        if len(noms_intermediaires) == 11:
            plt.subplot(3, 5, index_intermediate+1)  
        if len(noms_intermediaires) == 12:
            plt.subplot(3, 5, index_intermediate+1)  
        if len(noms_intermediaires) == 13:
            plt.subplot(3, 5, index_intermediate+1)  
            
        min_values = []
        max_values = []
        
        for index_biathlete, biathlete in enumerate(df_moy_3_tours_filtered['Name'].unique()):
            biathlete_data = df_moy_3_tours_filtered[df_moy_3_tours_filtered['Name'] == biathlete]
            # print(biathlete_data)
            # print(type(biathlete_data))
            if biathlete_data.iloc[0]["Country"] == "FRA":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='royalblue')
            elif biathlete_data.iloc[0]["Country"] == "NOR":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='red')
            elif biathlete_data.iloc[0]["Country"] == "GER":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='black')
            elif biathlete_data.iloc[0]["Country"] == "SWE":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='gold')
            elif biathlete_data.iloc[0]["Country"] == "ITA":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='limegreen')
            elif biathlete_data.iloc[0]["Country"] == "USA":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='red', color='blue', hatch=["*"])
            elif biathlete_data.iloc[0]["Country"] == "FIN":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='blue', color='white', hatch=['//'])
            elif biathlete_data.iloc[0]["Country"] == "SUI":
                plt.bar(index_biathlete, biathlete_data[intermediate].values, edgecolor='red', color='white')
            else:
                plt.bar(index_biathlete, biathlete_data[intermediate].values, color='lightgray')

            min_values.append(biathlete_data[intermediate].min())
            max_values.append(biathlete_data[intermediate].max())
        
        min_value = min(min_values)
        max_value = max(max_values)
        
        plt.ylim(min_value*0.9, max_value*1.1)
    
        plt.title(intermediate, fontsize=4)
        plt.yticks(fontsize=6)
        plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]), [str(df_moy_3_tours_filtered["Ranking"][i]) + " - " + df_moy_3_tours_filtered["Name"][i] for i in range(df_moy_3_tours_filtered.shape[0])], rotation=90, fontsize=4)
        plt.grid(True, axis='y', linewidth=0.2, color="grey")    


        plt.tight_layout()
    
    return fig_subplot

@st.cache_data 
def analyse_toutes_les_portions_nationalites_ski_de_fond(df, noms_intermediaires, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, nombre_USA, nombre_FIN, nombre_SUI, nombre_de_tours):
    
    df.sort_values(by=df.columns.tolist()[-1]).reset_index(drop=True, inplace=True)
    
    df_moy_3_tours = df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_tours)[0]
        
    fig_subplot = plt.figure()

    # plt.suptitle("Chronos moyens top 10 et français")
    
    nationalites = ["FRA", "NOR", "GER", "SWE", "ITA", "FIN", "USA", "SUI"]
    couleurs = ["royalblue", "red", "black", "gold", "limegreen", "white", "blue", "white"]
    edgecolor = ["royalblue","red","black","gold","limegreen","blue","red","red"]
    hatch = ["", "", "", "", "", '//', "*", ""]

    for index_intermediate, intermediate in enumerate(noms_intermediaires):
        
        chronos_pour_plot_intermediaire = []
                
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 2, index_intermediate+1)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 3, index_intermediate+1)            
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 8:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 9:
            plt.subplot(2, 4, index_intermediate+1)            
        if len(noms_intermediaires) == 10:
            plt.subplot(2, 5, index_intermediate+1)  
                    
        for nationalite in nationalites:
            
            df_nat_boucle = df_moy_3_tours[df_moy_3_tours["Country"] == nationalite]
            
            if nationalite =="FRA":
                df_nat_boucle = df_nat_boucle.head(nombre_FRA)
            elif nationalite == "NOR":
                df_nat_boucle = df_nat_boucle.head(nombre_NOR)
            elif nationalite == "GER":
                df_nat_boucle = df_nat_boucle.head(nombre_GER)
            elif nationalite == "SWE":
                df_nat_boucle = df_nat_boucle.head(nombre_SWE)
            elif nationalite == "ITA":
                df_nat_boucle = df_nat_boucle.head(nombre_ITA)
            elif nationalite == "FIN":
                df_nat_boucle = df_nat_boucle.head(nombre_FIN)
            elif nationalite == "USA":
                df_nat_boucle = df_nat_boucle.head(nombre_USA)
            elif nationalite == "SUI":
                df_nat_boucle = df_nat_boucle.head(nombre_SUI)
            chronos_pour_plot_intermediaire.append(df_nat_boucle[intermediate].mean())
            
        plt.bar(np.arange(len(nationalites)), chronos_pour_plot_intermediaire, color=couleurs, edgecolor=edgecolor, hatch=hatch)
        
        min_value = min(chronos_pour_plot_intermediaire)
        max_value = max(chronos_pour_plot_intermediaire)
        
        plt.ylim(min_value -2, max_value + 2)
    
        plt.title(intermediate, fontsize=4)
        plt.ylabel('Chronos (s)', fontsize=6)
        plt.yticks(fontsize=4)
        plt.xticks(np.arange(len(nationalites)), nationalites, rotation=90, fontsize=4)
        plt.grid(True, axis='y', linewidth=0.2, color="grey")
        # plt.xticks(np.arange(df_moy_3_tours_filtered.shape[0]), df_moy_3_tours_filtered['Name'].unique(), rotation=90, fontsize=8)
        # plt.legend()

        plt.tight_layout()
    
    return fig_subplot

@st.cache_data()
def analyse_une_seule_portion_nationalites_ski_de_fond(df, noms_intermediaires, intermediaire_a_afficher, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, nombre_USA, nombre_FIN, nombre_SUI, nombre_de_shoots):
   
    df.sort_values(by=df.columns.tolist()[-1]).reset_index(drop=True, inplace=True)
   
    df_moy_3_tours = df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_shoots)[0]   
    
    fig = plt.figure()

    # plt.suptitle("Chronos moyens top 10 et français")
    
    nationalites = ["FRA", "NOR", "GER", "SWE", "ITA", "FIN", "USA", "SUI"]
    couleurs = ["royalblue", "red", "black", "gold", "limegreen", "white", "blue", "white"]
    edgecolor = ["royalblue","red","black","gold","limegreen","blue","red","red"]
    hatch = ["", "", "", "", "", '//', "*", ""]
    
    for intermediate in noms_intermediaires:
        
        if intermediate == intermediaire_a_afficher:
        
            chronos_pour_plot_intermediaire = []
                    
            for nationalite in nationalites:
                
                df_nat_boucle = df_moy_3_tours[df_moy_3_tours["Country"] == nationalite]
                
                if nationalite =="FRA":
                    df_nat_boucle = df_nat_boucle.head(nombre_FRA)
                elif nationalite == "NOR":
                    df_nat_boucle = df_nat_boucle.head(nombre_NOR)
                elif nationalite == "GER":
                    df_nat_boucle = df_nat_boucle.head(nombre_GER)
                elif nationalite == "SWE":
                    df_nat_boucle = df_nat_boucle.head(nombre_SWE)
                elif nationalite == "ITA":
                    df_nat_boucle = df_nat_boucle.head(nombre_ITA)
                elif nationalite == "USA":
                    df_nat_boucle = df_nat_boucle.head(nombre_USA)
                elif nationalite == "FIN":
                    df_nat_boucle = df_nat_boucle.head(nombre_FIN)
                elif nationalite == "SUI":
                    df_nat_boucle = df_nat_boucle.head(nombre_SUI)
                    
                chronos_pour_plot_intermediaire.append(df_nat_boucle[intermediate].mean())
        
            plt.bar(np.arange(len(nationalites)), chronos_pour_plot_intermediaire, color=couleurs, edgecolor=edgecolor, hatch=hatch)
            
            min_value = min(chronos_pour_plot_intermediaire)
            max_value = max(chronos_pour_plot_intermediaire)
            
            plt.ylim(min_value -2, max_value + 2)
        
            plt.title(intermediate, fontsize=8)
            plt.yticks(fontsize=8)
            plt.xticks(np.arange(len(nationalites)), nationalites, rotation=90, fontsize=8)
            plt.grid(True, axis='y', linewidth=0.2, color="grey")
            plt.tight_layout()
    
    return fig

@st.cache_data()
def analyse_portion_specifique_graphe_1_par_nationalite_ski_de_fond(df, nationalites, liste_des_split_time, nb_FRA, nb_NOR, nb_GER, nb_SWE, nb_ITA, nb_USA, nb_FIN, nb_SUI, nombre_de_tours):
    
    # Boucle pour remettre les split time dans l'ordre s'ils sont mélangés dans la liste argument
    tous_les_ST = []
    for numero_tour in range(nombre_de_tours):
        tous_les_ST += split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[numero_tour]
    split_time = tous_les_ST.copy()
    
    split_time = [split for split in split_time if split in liste_des_split_time]
            
    # print("split_time après: " + str(split_time))
    
    noms_split_de_tous_les_tours = split_tour_par_tour_ski_de_fond(df, nombre_de_tours)  
    
    nombre_de_ST = len(liste_des_split_time)
    
    indices_de_tous_les_ST = []
    
    for indice_split, split in enumerate(tous_les_ST):
        for indice_split_bis, split_bis in enumerate(liste_des_split_time):
            if split == split_bis:
                indices_de_tous_les_ST.append(indice_split)
                
    df_temps_de_ski = df.copy()

    liste_pour_plot_en_abscisse = [0]
    for index_split in range(nombre_de_ST):
        if indices_de_tous_les_ST[0] == 0:
            liste_pour_plot_en_abscisse.append(round(f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indices_de_tous_les_ST[index_split]],1)) 
        else:
            liste_pour_plot_en_abscisse.append(round(liste_pour_plot_en_abscisse[-1] + f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indices_de_tous_les_ST[index_split]] - f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indices_de_tous_les_ST[index_split]-1],1)) 
 
    # print("nombre_de_ST: " + str(nombre_de_ST))
    # print("liste_pour_plot_en_abscisse: " + str(liste_pour_plot_en_abscisse))
    # print("f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2]: " + str(f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[2]))
    
    for index_colonne, nom_colonne in enumerate(df_temps_de_ski.columns.tolist()[4:]):
        if nom_colonne not in tous_les_ST:
            df_temps_de_ski.drop(nom_colonne, axis=1, inplace=True)

    df_analyse_portion_specifique = df_temps_de_ski.iloc[:, :4].copy()

    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique[split_time[index_portion]] = df_temps_de_ski[liste_des_split_time[index_portion]]
        
    df_analyse_portion_specifique["Temps total"] = 0
    for index_portion in range(nombre_de_ST):
        df_analyse_portion_specifique["Temps total"] +=  df_temps_de_ski[liste_des_split_time[index_portion]]

    fig_analyse_portion_specifique = plt.figure()

    # print(df_analyse_portion_specifique)
    
    # df_analyse_portion_specifique.sort_values(by="Temps total", inplace=True)
    # df_analyse_portion_specifique.reset_index(inplace=True, drop=True)
    
    ### Trouver les meilleurs temps de ski pour ensuite comparer au superman ###
    
    meilleurs_temps_de_ski = []
    
    for intermediaire in df_analyse_portion_specifique.columns.tolist()[4:]:
        meilleurs_temps_de_ski.append(df_analyse_portion_specifique[intermediaire].min())
       
    
    ### SI MEILLEUR ATHLETE SELECTIONNE ###
    
    
    for nationalite in nationalites:
        if nationalite == "FRA":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_FRA)  
            # print("df_nat: " + str(df_nat))
            couleur = "royalblue"
        elif nationalite == "NOR":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_NOR) 
            couleur = "red" 
        elif nationalite == "GER":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_GER)   
            couleur = "black" 
        elif nationalite == "SWE":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_SWE)  
            couleur = "gold"
        elif nationalite == "ITA":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_ITA)
            couleur = "limegreen"
        elif nationalite == "USA":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_USA)
            couleur = "grey"
        elif nationalite == "FIN":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_FIN)
            couleur = "grey"
        elif nationalite == "SUI":
            df_nat = df_analyse_portion_specifique[df_analyse_portion_specifique["Country"] == nationalite].head(nb_SUI)
            couleur = "grey"
 
        liste_ordonnee_biathlete = [0]                            
        for index in range(nombre_de_ST):
            temps_a_ajouter = liste_ordonnee_biathlete[-1]
            liste_ordonnee_biathlete.append(temps_a_ajouter + meilleurs_temps_de_ski[index] - df_nat.iloc[:,4 + index].mean()) # 4 + 1 + index pour commencer à 6 pour index 0
            # print("temps_a_ajouter: " + str(temps_a_ajouter) + " et meilleurs_temps_de_ski[index]: " + str(meilleurs_temps_de_ski[index]) + " et df_nat.iloc[:,4 + index].mean(): " + str(df_nat.iloc[:,4 + index].mean()))

        plt.plot(liste_pour_plot_en_abscisse, liste_ordonnee_biathlete, marker="o", color=couleur)       
        plt.text(liste_pour_plot_en_abscisse[-1] + 0.1, liste_ordonnee_biathlete[-1], nationalite)
                    
    plt.title("Evolution des écarts")
    plt.grid()
    if indices_de_tous_les_ST[0] == 0:
        plt.xticks(liste_pour_plot_en_abscisse, ["Départ"] + split_time, rotation=90)
    else:
        plt.xticks(liste_pour_plot_en_abscisse, [df.columns.tolist()[df.columns.get_loc(split_time[0]) - 1]] + split_time, rotation=90)           
        
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    
    return fig_analyse_portion_specifique

@st.cache_data() 
def analyse_portion_specifique_ratio_nationalite_ski_de_fond(df, split_amont, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, nombre_USA, nombre_FIN, nombre_SUI, nombre_de_tours): 
    
    df.sort_values(by=df.columns.tolist()[-1], inplace=True)
    df.reset_index(drop="True", inplace=True)
    
    df_temps_de_ski = df.copy()
        
    indice_split_amont = df.columns.get_loc(split_amont) - 4
    distance_portion_amont = f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indice_split_amont]
    
    indice_split_aval = df.columns.get_loc(split_amont) - 3
    distance_portion_aval = f_liste_distance_des_ST_ski_de_fond(df, nombre_de_tours)[0][indice_split_aval]

    df_ratio = df_temps_de_ski.iloc[:, :4].copy()
    df_ratio["Portion 1"] = 0
    df_ratio["Portion 2"] = 0
    for numero_tour in range(nombre_de_tours):
        df_ratio["Portion 1"] += df_temps_de_ski[split_tour_par_tour_ski_de_fond(df_temps_de_ski, nombre_de_tours)[numero_tour][indice_split_amont]]
        df_ratio["Portion 2"] += df_temps_de_ski[split_tour_par_tour_ski_de_fond(df_temps_de_ski, nombre_de_tours)[numero_tour][indice_split_aval]]
      
    df_ratio["Temps total"] = df_ratio["Portion 1"] + df_ratio["Portion 2"]

    ### NATIONALITE ###

    nationalites_interessantes = ["FRA", "NOR", "GER", "SWE", "ITA", "FIN", "USA", "SUI"]
    couleurs = ["royalblue", "red", "black", "gold", "limegreen", "white", "blue", "white"]
    edgecolor = ["royalblue","red","black","gold","limegreen","blue","red","red"]
    hatch = ["", "", "", "", "", '//', "*", ""]
    
    ratios_pour_plot = []

    for nationalite in nationalites_interessantes:
        df_nat_boucle = df_ratio[df_ratio["Country"] == nationalite]
        
        if nationalite =="FRA":
            df_nat_boucle = df_nat_boucle.head(nombre_FRA)
        elif nationalite == "NOR":
            df_nat_boucle = df_nat_boucle.head(nombre_NOR)
        elif nationalite == "GER":
            df_nat_boucle = df_nat_boucle.head(nombre_GER)
        elif nationalite == "SWE":
            df_nat_boucle = df_nat_boucle.head(nombre_SWE)
        elif nationalite == "ITA":
            df_nat_boucle = df_nat_boucle.head(nombre_ITA)
        elif nationalite == "USA":
            df_nat_boucle = df_nat_boucle.head(nombre_USA)
        elif nationalite == "FIN":
            df_nat_boucle = df_nat_boucle.head(nombre_FIN)
        elif nationalite == "SUI":
            df_nat_boucle = df_nat_boucle.head(nombre_SUI)
            
        ratio_nat = []
        
        for index_biathlete in range(df_nat_boucle.shape[0]):
            vitesse_moyenne_portion_1 = distance_portion_amont/df_nat_boucle.iloc[index_biathlete]["Portion 1"]
            vitesse_moyenne_portion_2 = distance_portion_aval/df_nat_boucle.iloc[index_biathlete]["Portion 2"]
            ratio_nat.append(vitesse_moyenne_portion_2/vitesse_moyenne_portion_1)
        
        ratios_pour_plot.append(np.mean(ratio_nat))
     
    fig_ratio_nationalites = plt.figure()
    
    plt.bar(np.arange(len(nationalites_interessantes)), ratios_pour_plot, color=couleurs, edgecolor=edgecolor, hatch=hatch)

    plt.xticks(np.arange(len(nationalites_interessantes)), nationalites_interessantes)
    plt.title("Vitesse moyenne portion 2 % vitesse moyenne portion 1")
    plt.ylim(min(ratios_pour_plot) - 0.05, max(ratios_pour_plot) + 0.05)
    plt.tight_layout()
    
    return fig_ratio_nationalites