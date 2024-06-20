import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from fonctions_utiles_code_plateforme import df_to_df_moy_3_tours
from fonctions_utiles_code_plateforme import df_to_df_moy_3_tours_ski_de_fond

# from code_superman_plateforme import *

@st.cache_data()
def f_points_forts_faibles_plateforme(df, biathletes_a_afficher, nationalites_a_afficher, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):
    
    ##  A PARTIR DU DF DE BASE JE CREE LE DF AVEC LA MOYENNE DES 3 TOURS POUR CHAQUE PORTION ##

    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]

    fig_10_int = plt.figure(figsize=(20, 10))
    fig_10_int.subplots_adjust(hspace=0.5, wspace=0.5)
    y_list= []
    df_moy_3_tours_ranked_by_finish = df_moy_3_tours.sort_values(by="Ranking").copy()
    liste_pour_boxplot = []
    
    moyenne_top_15 = [df_moy_3_tours_ranked_by_finish.head(15).iloc[:, index_intermediaire+4].mean() for index_intermediaire in range(len(noms_intermediaires))]
    # print(moyenne_top_15)

    # print("noms_intermediaires : " + str(noms_intermediaires))
    
    for index_intermediaire, intermediaire in enumerate(noms_intermediaires):
               
        ### VARIABLES POUR Y_LIM, X_TICKS, ETC ###
        abs_x = []
        label_x = [] 
        
        if len(noms_intermediaires) == 4:
            fig_10_int.add_subplot(2, 3, index_intermediaire+1)
        if len(noms_intermediaires) == 5:
            fig_10_int.add_subplot(2, 3, index_intermediaire+1)            
        if len(noms_intermediaires) == 6:
            fig_10_int.add_subplot(2, 4, index_intermediaire+1)            
        if len(noms_intermediaires) == 7:
            fig_10_int.add_subplot(2, 4, index_intermediaire+1)            
        if len(noms_intermediaires) == 8:
            fig_10_int.add_subplot(3, 3, index_intermediaire+1)            
        if len(noms_intermediaires) == 9:
            fig_10_int.add_subplot(3, 4, index_intermediaire+1)            
        if len(noms_intermediaires) == 10:
            fig_10_int.add_subplot(3, 4, index_intermediaire+1)  
        
        # fig_10_int.add_subplot(2, 5, index_intermediaire + 1)   
        i_abs = -1     
        
        if len(biathletes_a_afficher) != 0 or len(nationalites_a_afficher) != 0:
            
            # print("condition if points forts/faibles : " + str(len(biathletes_a_afficher) != 0) + " or " + str(len(nationalites_a_afficher) != 0))
            
            for index_biathlete in range(df_moy_3_tours.shape[0]):
                biathlete = str(df_moy_3_tours.iloc[index_biathlete, 2])
                if biathlete in biathletes_a_afficher or df_moy_3_tours.iloc[index_biathlete, 3] in nationalites_a_afficher:
                    
                    moyenne_des_pourcents_biathlete = np.mean([(moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/[df_moy_3_tours_ranked_by_finish.head(15).iloc[:, i+4].mean() for i in range(len(noms_intermediaires))][index_intermediaire] for index_intermediaire in range(len(noms_intermediaires))])
                    
                    i_abs += 1
                    
                    if i_abs in abs_x:
                        # print("True")
                        liste_pour_boxplot.append(((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete)                    
                    else:
                        # print("false")
                        liste_pour_boxplot.append([])
                        liste_pour_boxplot[i_abs].append(((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete)
                    # print(liste_pour_boxplot)
                    
                    abs_x.append(i_abs)

                    label_x.append(str(df_moy_3_tours.iloc[index_biathlete, 2]))
                    y_list.append((((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete)*1.1)
                    
                    if df_moy_3_tours.iloc[index_biathlete, 3] == "FRA":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="royalblue")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "GER":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="black")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "NOR":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="red")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "SWE":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="gold")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "ITA":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="limegreen") 
                    else:
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="gray")
            
            plt.xticks(abs_x, label_x, rotation=90)
            plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            plt.title(intermediaire, fontsize=9)
            plt.tight_layout()
            plt.grid()
    
    for index_intermediaire in range(len(noms_intermediaires)):
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 3, index_intermediaire+1)
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, index_intermediaire+1)  
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 4, index_intermediaire+1)    
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, index_intermediaire+1)       
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 8:
            plt.subplot(3, 3, index_intermediaire+1)   
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 9:
            plt.subplot(3, 4, index_intermediaire+1)  
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 10:
            plt.subplot(3, 4, index_intermediaire+1)  
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
               
    liste_pour_boxplot = [liste for liste in liste_pour_boxplot if liste]
    
    fig_10_int.add_subplot(2, 5, 10)  
    
    plt.boxplot(liste_pour_boxplot, whis=[0,100])
    plt.xticks([abs_x[i] + 1 for i in range(len(abs_x))], label_x, rotation=90)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.ylim(-max(abs(min(y_list)),abs(max(y_list))), max(abs(min(y_list)),abs(max(y_list))))

    plt.title("Consistance des athlètes")
    
    return fig_10_int

@st.cache_data()
def f_points_forts_faibles_plateforme_ski_de_fond(df, biathletes_a_afficher, nationalites_a_afficher, noms_intermediaires, nombre_de_tours):
    
    ##  A PARTIR DU DF DE BASE JE CREE LE DF AVEC LA MOYENNE DES 3 TOURS POUR CHAQUE PORTION ##

    df_moy_3_tours = df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_tours)[0]

    fig_10_int = plt.figure(figsize=(20, 10))
    fig_10_int.subplots_adjust(hspace=0.5, wspace=0.5)
    y_list= []
    df_moy_3_tours_ranked_by_finish = df_moy_3_tours.sort_values(by="Ranking").copy()
    liste_pour_boxplot = []
    
    moyenne_top_15 = [df_moy_3_tours_ranked_by_finish.head(15).iloc[:, index_intermediaire+4].mean() for index_intermediaire in range(len(noms_intermediaires))]
    # print(moyenne_top_15)

    # print("noms_intermediaires : " + str(noms_intermediaires))
    
    for index_intermediaire, intermediaire in enumerate(noms_intermediaires):
               
        ### VARIABLES POUR Y_LIM, X_TICKS, ETC ###
        abs_x = []
        label_x = [] 
        
        if len(noms_intermediaires) == 4:
            fig_10_int.add_subplot(2, 3, index_intermediaire+1)
        if len(noms_intermediaires) == 5:
            fig_10_int.add_subplot(2, 3, index_intermediaire+1)            
        if len(noms_intermediaires) == 6:
            fig_10_int.add_subplot(2, 4, index_intermediaire+1)            
        if len(noms_intermediaires) == 7:
            fig_10_int.add_subplot(2, 4, index_intermediaire+1)            
        if len(noms_intermediaires) == 8:
            fig_10_int.add_subplot(3, 3, index_intermediaire+1)            
        if len(noms_intermediaires) == 9:
            fig_10_int.add_subplot(3, 4, index_intermediaire+1)            
        if len(noms_intermediaires) == 10:
            fig_10_int.add_subplot(3, 4, index_intermediaire+1)  
        
        # fig_10_int.add_subplot(2, 5, index_intermediaire + 1)   
        i_abs = -1     
        
        if len(biathletes_a_afficher) != 0 or len(nationalites_a_afficher) != 0:
            
            # print("condition if points forts/faibles : " + str(len(biathletes_a_afficher) != 0) + " or " + str(len(nationalites_a_afficher) != 0))
            
            for index_biathlete in range(df_moy_3_tours.shape[0]):
                biathlete = str(df_moy_3_tours.iloc[index_biathlete, 2])
                if biathlete in biathletes_a_afficher or df_moy_3_tours.iloc[index_biathlete, 3] in nationalites_a_afficher:
                    
                    moyenne_des_pourcents_biathlete = np.mean([(moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/[df_moy_3_tours_ranked_by_finish.head(15).iloc[:, i+4].mean() for i in range(len(noms_intermediaires))][index_intermediaire] for index_intermediaire in range(len(noms_intermediaires))])
                    
                    i_abs += 1
                    
                    if i_abs in abs_x:
                        # print("True")
                        liste_pour_boxplot.append(((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete)                    
                    else:
                        # print("false")
                        liste_pour_boxplot.append([])
                        liste_pour_boxplot[i_abs].append(((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete)
                    # print(liste_pour_boxplot)
                    
                    abs_x.append(i_abs)

                    label_x.append(str(df_moy_3_tours.iloc[index_biathlete, 2]))
                    y_list.append((((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete)*1.1)
                    
                    if df_moy_3_tours.iloc[index_biathlete, 3] == "FRA":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="royalblue")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "GER":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="black")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "NOR":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="red")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "SWE":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="gold")
                    elif df_moy_3_tours.iloc[index_biathlete, 3] == "ITA":
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="limegreen") 
                    else:
                        plt.bar(i_abs, ((moyenne_top_15[index_intermediaire] - df_moy_3_tours.iloc[index_biathlete, index_intermediaire+4])/moyenne_top_15[index_intermediaire]) - moyenne_des_pourcents_biathlete, color="gray")
            
            plt.xticks(abs_x, label_x, rotation=90)
            plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            plt.title(intermediaire, fontsize=9)
            plt.tight_layout()
            plt.grid()
    
    for index_intermediaire in range(len(noms_intermediaires)):
        if len(noms_intermediaires) == 4:
            plt.subplot(2, 3, index_intermediaire+1)
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 5:
            plt.subplot(2, 3, index_intermediaire+1)  
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 6:
            plt.subplot(2, 4, index_intermediaire+1)    
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 7:
            plt.subplot(2, 4, index_intermediaire+1)       
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 8:
            plt.subplot(3, 3, index_intermediaire+1)   
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 9:
            plt.subplot(3, 4, index_intermediaire+1)  
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
        if len(noms_intermediaires) == 10:
            plt.subplot(3, 4, index_intermediaire+1)  
            plt.ylim(-max(abs(min(y_list)),abs(max(y_list))) - 0.01, max(abs(min(y_list)),abs(max(y_list))) + 0.01)
               
    liste_pour_boxplot = [liste for liste in liste_pour_boxplot if liste]
    
    fig_10_int.add_subplot(2, 5, 10)  
    
    plt.boxplot(liste_pour_boxplot, whis=[0,100])
    plt.xticks([abs_x[i] + 1 for i in range(len(abs_x))], label_x, rotation=90)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.ylim(-max(abs(min(y_list)),abs(max(y_list))), max(abs(min(y_list)),abs(max(y_list))))

    plt.title("Consistance des athlètes")
    
    return fig_10_int
