import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from code_superman_plateforme import *
from fonctions_utiles_code_plateforme import *
    
def graphes_moustaches(df, df_temps_de_ski, liste_distance_des_ST, noms_intermediaires, nationalites, sexe, distance_de_1_tour, distance_toute_la_course, top_N_pour_comparer, nombre_de_shoots):

    ### MOYENNE DES TROIS TOURS POUR CHAQUE PORTION DU CIRCUIT ###
        
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]
    
    print("df_moy_3_tours: " + str(df_moy_3_tours))
    
    df_moy_3_tours.sort_values(by="Ranking").reset_index(drop=True, inplace=True)
    
    meilleurs_chronos = []
    for intermediaire in df_moy_3_tours.columns.tolist()[4:]:
        meilleurs_chronos.append(df_moy_3_tours[intermediaire].min())
    
    df_pour_boxplot = df_moy_3_tours.iloc[:, 4:].head(top_N_pour_comparer).copy()
    
    for index_colonne, colonne in enumerate(df_pour_boxplot.columns.tolist()):
        df_pour_boxplot[colonne] = (df_pour_boxplot[colonne] - meilleurs_chronos[index_colonne])/liste_distance_des_ST[index_colonne]
    
    labels = df_moy_3_tours.columns

    fig_perte_de_temps_superman = plt.figure()
    
    liste_pour_xticks = ["Départ - " + split_tour_par_tour(df, nombre_de_shoots)[0][0]]
    for index_split, split in enumerate(split_tour_par_tour(df, nombre_de_shoots)[0][:-1]):
        # print(index_split,split)
        liste_pour_xticks.append(str(split) + str(" - ") + str(split_tour_par_tour(df, nombre_de_shoots)[0][index_split+1]))
    
    df_pour_boxplot.boxplot(color='black', showmeans=False, showfliers=False)
    plt.xticks(list(range(1,len(labels[4:])+1)), liste_pour_xticks, rotation=45, fontsize=10)
    plt.title("Perte de temps par rapport au Superman en s/m")
    plt.grid(True, axis='y', color='grey',  linestyle='--', linewidth=0.04)
    plt.grid(False)
    plt.tight_layout()

    return fig_perte_de_temps_superman