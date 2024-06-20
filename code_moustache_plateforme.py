import numpy as np
import matplotlib.pyplot as plt

from code_superman_plateforme import *
from fonctions_utiles_code_plateforme import *

@st.cache_data()
def graphes_moustaches(df, noms_intermediaires, nationalites, sexe, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots):

    ### MOYENNE DES TROIS TOURS POUR CHAQUE PORTION DU CIRCUIT ###
        
    df_moy_3_tours = df_to_df_moy_3_tours(df, noms_intermediaires, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)[0]
    
    df_moy_3_tours.sort_values(by="Ranking").reset_index(drop=True, inplace=True)
    
    labels = df_moy_3_tours.columns
    
    fig_portions_creant_ecart = plt.figure()
    
    listes_coef_de_variation = []
    
    for intermediaire in df_moy_3_tours.columns[4:].to_list():
        ecart_type = df_moy_3_tours[intermediaire].std()
        moyenne = df_moy_3_tours[intermediaire].mean()
        listes_coef_de_variation.append(ecart_type/moyenne)

    
    liste_pour_xticks = ["Départ - " + split_tour_par_tour(df, nombre_de_shoots)[0][0]]
    for index_split, split in enumerate(split_tour_par_tour(df, nombre_de_shoots)[0][:-1]):
        # print(index_split,split)
        liste_pour_xticks.append(str(split) + str(" - ") + str(split_tour_par_tour(df, nombre_de_shoots)[0][index_split+1]))
    
    plt.bar(np.arange(len(noms_intermediaires)), listes_coef_de_variation, width=0.4, color="black")
    plt.xticks(list(range(len(labels[4:]))), liste_pour_xticks, rotation=90, fontsize=10)
    plt.title("Portions créant le plus d'écart")
    plt.grid(True, axis='y', color='grey',  linestyle='--', linewidth=0.04)
    # plt.grid(False)
    plt.tight_layout()

    return fig_portions_creant_ecart

@st.cache_data()
def graphes_moustaches_ski_de_fond(df, noms_intermediaires, nombre_de_tours):

    ### MOYENNE DES TROIS TOURS POUR CHAQUE PORTION DU CIRCUIT ###
        
    df_moy_3_tours = df_to_df_moy_3_tours_ski_de_fond(df, noms_intermediaires, nombre_de_tours)[0]
    
    df_moy_3_tours.sort_values(by="Ranking").reset_index(drop=True, inplace=True)
    
    labels = df_moy_3_tours.columns
    
    fig_portions_creant_ecart = plt.figure()
    
    listes_coef_de_variation = []
    
    for intermediaire in df_moy_3_tours.columns[4:].to_list():
        ecart_type = df_moy_3_tours[intermediaire].std()
        moyenne = df_moy_3_tours[intermediaire].mean()
        listes_coef_de_variation.append(ecart_type/moyenne)

    
    liste_pour_xticks = ["Départ - " + split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[0][0]]
    for index_split, split in enumerate(split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[0][:-1]):
        # print(index_split,split)
        liste_pour_xticks.append(str(split) + str(" - ") + str(split_tour_par_tour_ski_de_fond(df, nombre_de_tours)[0][index_split+1]))
    
    plt.bar(np.arange(len(noms_intermediaires)), listes_coef_de_variation, width=0.4, color="black")
    plt.xticks(list(range(len(labels[4:]))), liste_pour_xticks, rotation=90, fontsize=10)
    plt.title("Portions créant le plus d'écart")
    plt.grid(True, axis='y', color='grey',  linestyle='--', linewidth=0.04)
    # plt.grid(False)
    plt.tight_layout()

    return fig_portions_creant_ecart
