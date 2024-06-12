import numpy as np
import pandas as pd
import zipfile
import streamlit as st 
import os
from pathlib import Path
import csv
import json


# from streamlit_option_menu import option_menu

from scripts_plateforme_finale.code_superman_plateforme import *
from scripts_plateforme_finale.code_moustache_plateforme import *
from scripts_plateforme_finale.code_analyse_individuelle_plateforme import *
from scripts_plateforme_finale.code_points_forts_faibles_plateforme import *
from scripts_plateforme_finale.code_analyse_portion_specifique_plateforme import *
from scripts_plateforme_finale.fonctions_utiles_code_plateforme import *
from scripts_plateforme_finale.fonctions_gestion_session_state_plateforme import *

from scripts_plateforme_finale.extraction_time_plateforme import time_data_to_excel


### CONFIGURATION DE LA PAGE ###


st.set_page_config(
    page_title="Plateforme analyse de course",
    layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #0000FF; font-family: Arial, sans-serif;'>Plateforme d'analyse de course</h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .main {
        background-color: white; # modifier ici la couleur
    }
    .sidebar {
        background-color: #d0e0f0;  /* Rouge */
    }
    </style>
    """,
    unsafe_allow_html=True
)


### CREATION DES ONGLETS ###


noms_des_onglets = ["1 - Sélection de la course", "2 - Analyse de la course", "3 - Analyse individuelle", "4 - Analyse de portion spécifique", "5 - Analyse collective", "6 - A remplir par Jonas"]
onglets = st.tabs(noms_des_onglets)


### ONGLET POUR JONAS ###


# csv_st_file_path_split = "jesptri\\Plateforme-analyse-de-course\\data_utile_csv\\data_listes_split.csv"
# csv_st_file_path_type = "jesptri\\Plateforme-analyse-de-course\\data_utile_csv\\data_listes_type_de_portion.csv"

csv_st_file_path_split = "data_utile_csv\\data_listes_split.csv"
csv_st_file_path_type = "data_utile_csv\\data_listes_type_de_portion.csv"


with onglets[5]:
    
    if 'button_clicked_jonas' not in st.session_state:
        st.session_state.button_clicked_jonas = False
    
    col_1_Jonas, col_2_Jonas, col_3_Jonas, col_4_Jonas= st.columns(4)
    
    with col_1_Jonas: # sport
        choix_sport_temporary_jonas = st.selectbox("Discipline", ["Biathlon"], key="choix_sport_Jonas", on_change=off_button_click_jonas)


    with col_2_Jonas: # saison
        choix_saison_temporary_jonas = st.selectbox("Saison", ["2023-2024"], key="choix_saison_Jonas", on_change=off_button_click_jonas)

    with col_3_Jonas: # lieu de la course
        choix_lieu_de_la_course_temporary_jonas = st.selectbox("Lieu de la course", ["Oestersund (SWE)", "Ruhpolding (GER)", "Lenzerheide (SUI)"], key="choix_lieu_de_la_course_Jonas", on_change=off_button_click_jonas)

    with col_4_Jonas: # type de la course
        choix_type_de_la_course_temporary_jonas = st.selectbox("Type de la course", ["Men 10km Sprint", "Women 7.5km Sprint"], key="choix_type_de_la_course_Jonas", on_change=off_button_click_jonas)


    st.button('Cliquez pour valider', key="bouton Jonas", on_click=on_button_click_jonas)
    
    # if st.session_state.button_clicked_jonas == False:
    #     st.subheader("Valider la course en cliquant sur le bouton !")        
    if st.session_state.button_clicked_jonas == True:
        
        # path_check = f"jesptri\\Plateforme-analyse-de-course\\data_ibu_excel\\{choix_lieu_de_la_course_temporary_jonas}_{choix_type_de_la_course_temporary_jonas}_{choix_saison_temporary_jonas}.xlsx"
        path_check = f"data_ibu_excel\\{choix_lieu_de_la_course_temporary_jonas}_{choix_type_de_la_course_temporary_jonas}_{choix_saison_temporary_jonas}.xlsx"
        path_check_if_exists = Path(path_check)
        if path_check_if_exists.is_file() and is_zipfile_valid(path_check_if_exists):
            st.success("Données du site IBU déjà téléchargées pour cette course !")
        # elif path_check_if_exists.is_file() and not is_zipfile_valid(path_check_if_exists):
        #     st.error("Fichier des données IBU corrompu !")
        
        choix_sport_Jonas = choix_sport_temporary_jonas
        choix_lieu_de_la_course_Jonas = choix_lieu_de_la_course_temporary_jonas
        choix_type_de_la_course_jonas = choix_type_de_la_course_temporary_jonas
        choix_saison_jonas = choix_saison_temporary_jonas
        
        ### REMPLISSAGE DES SPLIT TIME ###


        st.header("Remplissage des split time")
        
        nom_liste_split_Jonas = f'split_time_{choix_sport_Jonas}_{choix_lieu_de_la_course_Jonas}_{choix_type_de_la_course_jonas}_{choix_saison_jonas}'
        
        # Initialiser new_split dans session state si elle n'existe pas déjà
        if 'new_split' not in st.session_state:
            st.session_state.new_split = ""
        
        if nom_liste_split_Jonas not in st.session_state:
            st.session_state[nom_liste_split_Jonas] = []    
                
        st.text_input("Entrez le nouveau split time: ", key='new_split', on_change=add_split, args=(nom_liste_split_Jonas,))
            
        col_shoot_1, col_shoot_2, col_shoot_3, col_shoot_4, col_Finish, _, col_empty_the_list, col_delete_last_element = st.columns([1,1,1,1,1,1,1.5,1.5])
        with col_shoot_1:
            st.button("Ajouter shoot 1", on_click=add_shoot_1, args=(nom_liste_split_Jonas,))
        with col_shoot_2:
            st.button("Ajouter shoot 2", on_click=add_shoot_2, args=(nom_liste_split_Jonas,))
        with col_shoot_3:
            st.button("Ajouter shoot 3", on_click=add_shoot_3, args=(nom_liste_split_Jonas,))
        with col_shoot_4:
            st.button("Ajouter shoot 4", on_click=add_shoot_4, args=(nom_liste_split_Jonas,)) 
        with col_Finish:
            st.button("Ajouter Finish", on_click=add_Finish, args=(nom_liste_split_Jonas,)) 
            
        with col_empty_the_list:
            st.button("Supprimer le dernier élément ajouté", on_click=delete_last_element, args=(nom_liste_split_Jonas,))
        with col_delete_last_element:
            st.button("Recommencer le remplissage", on_click=empty_the_list, args=(nom_liste_split_Jonas,))


        st.write(f"**Liste en cours de remplissage:**  \n  {st.session_state[nom_liste_split_Jonas]}")
        
        if st.button("Valider la liste de split time", on_click=save_split_list, args=(csv_st_file_path_split,)) == True:
            show_temporary_message("Liste de split time validée !", 2)
        
        loaded_file_split = load_split_list(csv_st_file_path_split)

        if st.checkbox("Afficher les listes déjà remplies", key="split"):
            st.subheader("Listes de split déjà remplies: \n")
            # print("loaded_file_split: " + str(loaded_file_split))
                
            for liste_split in loaded_file_split:
                if loaded_file_split[liste_split]:
                    if loaded_file_split[liste_split] == ['']:
                        st.markdown(f"**{liste_split.replace('split_time_', '')}**:  \nListe vide !")
                    else:
                        # chaine_a_afficher = ""
                        # for element in loaded_file_split[liste_split]:
                        #     chaine_a_afficher = str(element) + " ; "
                        st.markdown(f"**{liste_split.replace('split_time_', '')}**:  \n{loaded_file_split[liste_split]}")

        
        dictionnaire_course_liste_st = loaded_file_split


        ### SHOOTS 


        if "Sprint" in choix_type_de_la_course_jonas:
            nombre_de_shoots_Jonas = 2
        elif "Individual" in choix_type_de_la_course_jonas or "Pursuit" in choix_type_de_la_course_jonas or "Mass start" in choix_type_de_la_course_jonas or "Short individual" in choix_type_de_la_course_jonas:
            nombre_de_shoots_Jonas = 4
    

        ### TOUS LES NOMS D'INTERMEDIAIRES ###
        
        st.header("Choix du type de chaque portion")
        
        loaded_file_type = load_type_list(csv_st_file_path_type)

        try:
            liste_des_ST_choix_portions_Jonas = dictionnaire_course_liste_st[nom_liste_split_Jonas]
            # print("split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas): " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)))  
            noms_intermediaires_Jonas = [] 
            for index_split, split in enumerate(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[0]):
                if index_split == 0:        
                    noms_intermediaires_Jonas.append("Départ - " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[0][index_split]) + "  ||  Shooting 1 - " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[1][index_split]) + "  ||  Shooting 2 - " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[2][index_split]))
                else:
                    noms_intermediaires_Jonas.append(str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[0][index_split-1]) + " - " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[0][index_split]) + "  ||  " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[1][index_split-1]) + " - " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[1][index_split]) + "  ||  " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[2][index_split-1]) + " - " + str(split_tour_par_tour_Jonas(liste_des_ST_choix_portions_Jonas, nombre_de_shoots_Jonas)[2][index_split]))

            ### CHOIX DES PORTIONS PAR TYPE ###
            
            nom_split_type_de_portion_Jonas = f'split_type_de_portion_{choix_sport_Jonas}_{choix_lieu_de_la_course_Jonas}_{choix_type_de_la_course_jonas}_{choix_saison_jonas}'

            if nom_split_type_de_portion_Jonas not in st.session_state:
                st.session_state[nom_split_type_de_portion_Jonas] = [[],[],[],[]] 


            col_noms_intermediaires_bosses, col_intermediaires_descentes, col_intermediaires_plats, col_interemediaires_vallonés = st.columns(4)
            
            with col_noms_intermediaires_bosses:
                noms_intermediaires_bosses_jonas = st.multiselect("Portions en bosse", noms_intermediaires_Jonas, key="choix bosse Jonas", on_change=update_type, args=(nom_split_type_de_portion_Jonas, "bosse",))
            with col_intermediaires_descentes:
                noms_intermediaires_descentes_jonas = st.multiselect("Portions en descente", noms_intermediaires_Jonas, key="choix descente Jonas", on_change=update_type, args=(nom_split_type_de_portion_Jonas, "descente",))
            with col_intermediaires_plats:
                noms_intermediaires_plats_jonas = st.multiselect("Portions plates", noms_intermediaires_Jonas, key="choix plat Jonas", on_change=update_type, args=(nom_split_type_de_portion_Jonas, "plat",))  
            with col_interemediaires_vallonés:
                noms_intermediaires_vallonés_jonas = st.multiselect("Portions vallonées", noms_intermediaires_Jonas, key="choix valloné Jonas", on_change=update_type, args=(nom_split_type_de_portion_Jonas, "valloné",))

            # st.session_state

            st.button("Valider les split par type de portion", on_click=save_type_list, args=(csv_st_file_path_type,))
            
            if st.checkbox("Afficher les listes déjà remplies", key="type de portion"):
                st.subheader("Listes type de portion déjà remplies: \n")
            
                for liste_type in loaded_file_type:
                    if loaded_file_type[liste_type]:
                        st.markdown(f"**{liste_type.replace('split_type_de_portion_','')}:**  \n Portions en bosse: {loaded_file_type[liste_type][0]}  \n Portions en descente: {loaded_file_type[liste_type][1]}  \n Portions plates: {loaded_file_type[liste_type][2]}  \n Portions vallonées: {loaded_file_type[liste_type][3]}")
                dictionnaire_course_liste_type = loaded_file_type
                # print("dictionnaire_course_liste_type: " + str(dictionnaire_course_liste_type))
            
        except: 
            st.error("Données de split time pas rentrées pour la course sélectionnée !")


with onglets[0]:
        
    st.header("Choix de la course")

    col1, col2, col3, col4= st.columns(4)

    with col1: # sport
        choix_sport_temporary = st.selectbox("Discipline", ["Biathlon"]) #["Biathlon", "Ski de fond"])

    with col2: # saison
        choix_saison_temporary = st.selectbox("Saison", ["2023-2024"], on_change=on_selectbox_change)

    with col3: # lieu de la course
        choix_lieu_de_la_course_temporary = st.selectbox("Lieu de la course", ["Oestersund (SWE)", "Ruhpolding (GER)", "Lenzerheide (SUI)"], on_change=on_selectbox_change)

    with col4: # type de la course
        choix_type_de_la_course_temporary = st.selectbox("Type de la course", ["Men 10km Sprint", "Women 7.5km Sprint"], on_change=on_selectbox_change)
     
    if "Men" in choix_type_de_la_course_temporary:
        choix_homme_ou_femme = "homme"
    elif "Women" in choix_type_de_la_course_temporary:
        choix_homme_ou_femme = "femme"
    
    
    ### NOMBRE DE SHOOTS EN FONCTION DU TYPE DE LA COURSE ###
    
    
    if "Sprint" in choix_type_de_la_course_temporary:
        nombre_de_shoots = 2
    elif "Individual" in choix_type_de_la_course_temporary or "Pursuit" in choix_type_de_la_course_temporary or "Mass start" in choix_type_de_la_course_temporary or "Short individual" in choix_type_de_la_course_temporary:
        nombre_de_shoots = 4
    
      
    # Création du bouton pour valider les choix
        
    # chemin_fichier_excel = f"jesptri\\Analyse_de_course\\data_ibu_excel\\{choix_lieu_de_la_course_temporary}_{choix_type_de_la_course_temporary}_{choix_saison_temporary}.xlsx"
    chemin_fichier_excel = f"data_ibu_excel\\{choix_lieu_de_la_course_temporary}_{choix_type_de_la_course_temporary}_{choix_saison_temporary}.xlsx"

    
    file_path = Path(chemin_fichier_excel)
    
    ### INITIALISATION DE L'ETAT DU BOUTON ET DES SELECTBOX ###

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    
    
    ### BOUTON VALIDER APPUYE OU PAS ###
      
    st.button('Cliquez pour valider', key="bouton entraineur", on_click=on_button_click_coach)
        
    _, col_texte, _ = st.columns([5,6,3])
        
    with col_texte:
        message_placeholder = st.empty()  
        
    dictionnaire_course_liste_st = load_split_list(csv_st_file_path_split)
                
    # if not st.session_state.button_clicked:
    #     with onglets[1]:
    #         st.subheader("**Sélectionnez une course et validez !**")
    #     with onglets[2]:
    #         st.subheader("**Sélectionnez une course et validez !**")
    #     with onglets[3]:
    #         st.subheader("**Sélectionnez une course et validez !**")
    #     with onglets[4]:
    #         st.subheader("**Sélectionnez une course et validez !**")
        
    
    choix_saison = choix_saison_temporary
    choix_lieu_de_la_course = choix_lieu_de_la_course_temporary
    choix_type_de_la_course = choix_type_de_la_course_temporary
    choix_sport = choix_sport_temporary
        
    # NOMS DES TYPES DE PORTION #
    
    try:
        nom_course = f'split_type_de_portion_{choix_sport}_{choix_lieu_de_la_course}_{choix_type_de_la_course}_{choix_saison}'
        noms_intermediaires_bosses = loaded_file_type[nom_course][0]  
        noms_intermediaires_descentes = loaded_file_type[nom_course][1]  
        noms_intermediaires_plats = loaded_file_type[nom_course][2]  
        noms_intermediaires_vallones = loaded_file_type[nom_course][3]  
    except:
        st.error("Données types de portion non rentrées pour la course sélectionnée !")
        
        
    ### TANT QUE LE FICHIER N'EST PAS VALIDE ###
        
    # while not file_path.is_file() or not is_zipfile_valid(file_path):

        ### SI LE FICHIER N'EXISTE PAS ###

    list_found_or_not = False
    if not file_path.is_file():

        for split_course in dictionnaire_course_liste_st:
            key = f'split_time_{choix_sport}_{choix_lieu_de_la_course}_{choix_type_de_la_course}_{choix_saison}'
            if key in split_course:    
                SPLIT_TIME = dictionnaire_course_liste_st[split_course]
                list_found_or_not = True
        
        if not list_found_or_not:
            message_placeholder.error("Erreur, liste de split time non trouvée.")
        else: 
        # try:
            message_placeholder.write("Données chronos non téléchargées ! Téléchargement en cours...")
            time_data_to_excel(choix_lieu_de_la_course, choix_type_de_la_course, choix_saison, SPLIT_TIME, "edge")  
        #     # break
        # except:
        #     message_placeholder.error("**Erreur, vérifiez les données ou réessayez !**")
        
    
    ### SI AU CONTRAIRE LE FICHIER EXISTE ###
    
    if file_path.is_file():
        
        ## SI LE FICHIER NE S'OUVRE PAS #
        
        if not is_zipfile_valid(file_path):
            os.remove(chemin_fichier_excel)
            # break    
    
    if file_path.is_file() and is_zipfile_valid(file_path):
    
        message_placeholder.success("**Données téléchargées ! Vous pouvez consulter les analyses !**")

        choix_saison = choix_saison_temporary
        choix_lieu_de_la_course = choix_lieu_de_la_course_temporary
        choix_type_de_la_course = choix_type_de_la_course_temporary
        choix_sport = choix_sport_temporary

        distance_toute_la_course = float(extract_distances(choix_type_de_la_course)[0])
        distance_de_1_tour = float(extract_distances(choix_type_de_la_course)[0])/(nombre_de_shoots+1)


        df = pd.read_excel(chemin_fichier_excel, engine='openpyxl')



        # ### TOUS LES NOMS D'INTERMEDIAIRES ###


        noms_intermediaires = [] 
        for index_split, split in enumerate(split_tour_par_tour(df, nombre_de_shoots)[0]):
            if index_split == 0:        
                noms_intermediaires.append("Départ - " + str(split_tour_par_tour(df, nombre_de_shoots)[0][index_split]) + "  ||  Shooting 1 - " + str(split_tour_par_tour(df, nombre_de_shoots)[1][index_split]) + "  ||  Shooting 2 - " + str(split_tour_par_tour(df, nombre_de_shoots)[2][index_split]))
            else:
                noms_intermediaires.append(str(split_tour_par_tour(df, nombre_de_shoots)[0][index_split-1]) + " - " + str(split_tour_par_tour(df, nombre_de_shoots)[0][index_split]) + "  ||  " + str(split_tour_par_tour(df, nombre_de_shoots)[1][index_split-1]) + " - " + str(split_tour_par_tour(df, nombre_de_shoots)[1][index_split]) + "  ||  " + str(split_tour_par_tour(df, nombre_de_shoots)[2][index_split-1]) + " - " + str(split_tour_par_tour(df, nombre_de_shoots)[2][index_split]))

        noms_des_PT = indices_ST_PT_tours(df)[0]
        noms_des_ST = indices_ST_PT_tours(df)[1]
        noms_des_tours = indices_ST_PT_tours(df)[2]
        
        split_time_a_afficher_un_par_un = []
        for splits_tour in split_tour_par_tour(df, nombre_de_shoots):
            split_time_a_afficher_un_par_un += splits_tour 

        # print("indices des PT: " + str(indices_ST_PT_tours(df)[0]))
        # print("indices des ST: " + str(indices_ST_PT_tours(df)[1]))
        # print("indices des tours: " + str(indices_ST_PT_tours(df)[2]))       

            
            # st.caption("Mettre une portion dans une seule catégorie")       
                

        dico_noms_dashboard_noms_code = {noms_intermediaires[i]: split_tour_par_tour(df, nombre_de_shoots)[0][i] for i in range(len(noms_intermediaires))}

        ### TOUS LES NOMS DES ATHLETES ###

        all_athletes = []
        for i in range(df.shape[0]):
                all_athletes.append(str(df.sort_values(by="Name").iloc[i,2]))




        ### PARTIE 1 ### #####     ANALYSE DE LA COURSE     #####




        with onglets[1]:

            st.header("Analyse de la course")

            col_top_n_1, col_nationalites_1, col_biathletes_1, col_chronos_1 = st.columns(4)

            with col_top_n_1:
                top_n_1 = st.slider("Top ...", min_value=0, max_value=80, value=10, key=" top N superman et ecart leader")
            with col_nationalites_1:
                nationalites_1 = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalites superman")
            with col_biathletes_1:
                biathletes_1 = st.multiselect("Biathlètes:", all_athletes, key="biathletes superman")
            with col_chronos_1:
                chronos_1 = st.multiselect("Données chronométriques:", ["Début/fin de tour", "Pre-time", "Split-time"])
                
            with st.container(height=500):
                col_ecart_au_leader, col_superman = st.columns(2)

            ## GRAPHE 1 ## ### COLONNE ECART AU LEADER ###

            with col_ecart_au_leader:
                st.markdown("### Ecart au meilleur skieur")
                if nombre_de_shoots == 2:
                    indices_a_enlever = [f_df_sans_temps_shoot(df, nombre_de_shoots)[3], f_df_sans_temps_shoot(df, nombre_de_shoots)[4]]
                elif nombre_de_shoots == 4:
                    indices_a_enlever = [f_df_sans_temps_shoot(df, nombre_de_shoots)[3], f_df_sans_temps_shoot(df, nombre_de_shoots)[4], f_df_sans_temps_shoot(df, nombre_de_shoots)[8], f_df_sans_temps_shoot(df, nombre_de_shoots)[9]]
                
                # print("indices: " + str(np.arange(df.shape[1]-4)[:-1]))
                
                fig_ecart_leader = graphes_superman_et_ecart_au_leader(f_df_sans_temps_shoot(df, nombre_de_shoots)[0], f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[1], df, 
                                                        indices_a_enlever, choix_homme_ou_femme, top_n_1, nationalites_1, 
                                                        np.arange(df.shape[1]-4)[:-1],
                                                        biathletes_1, nombre_de_shoots)[0]
                # with st.container(height=500):
                st.pyplot(fig_ecart_leader)
                
            ## GRAPHE 2 ## ### COLONNE SUPERMAN ###

            with col_superman:
                st.markdown("### Superman")
                fig_ecart_leader = graphes_superman_et_ecart_au_leader(f_df_sans_temps_shoot(df, nombre_de_shoots)[0], f_liste_distance_des_ST(df, distance_de_1_tour, distance_toute_la_course)[1], df, 
                                                        indices_a_enlever, 
                                                        choix_homme_ou_femme, 
                                                        top_n_1, 
                                                        nationalites_1, 
                                                        np.arange(df.shape[1]-4)[:-1], 
                                                        biathletes_1, nombre_de_shoots)[1]
                # with st.container(height=500):
                st.pyplot(fig_ecart_leader)

            ## GRAPHE 3 ## ### PORTIONS CREANT DE L'ECART ###
            
            st.subheader("Portions créant de l'écart")
            
            st.write("_Ce graphe représente la perte de temps moyenne du top ... par rapport au superman_.")

            _, col_moustache, _ = st.columns([2,8,2])

            with col_moustache:
                st.pyplot(graphes_moustaches(df, ["Intermédiaire " + str(i) for i in range(1, len(split_tour_par_tour(df, nombre_de_shoots)[0]) + 1)], # revoir ici
                        nationalites_1, choix_homme_ou_femme, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots), clear_figure=True, use_container_width=True)




        ### PARTIE 2 ### #####     ANALYSE INDIVIDUELLE     #####




        with onglets[2]:

            st.header("Analyse individuelle")

            # col_top_n_2, _, col_biathletes_2 = st.columns([5,0.25,5])            
            
            col_temps_de_ski_total_temps_de_ski_par_tour, _, col_pacing_tour_par_tour, _, col_tableau_temps_de_ski  = st.columns([4,0.2,4,0.2,3])

            with col_temps_de_ski_total_temps_de_ski_par_tour:
                top_n_2 = st.slider("Top ...", min_value=0, max_value=75, value=10, key="top n 2")
                st.info("Les biathlètes sont ordonnés par le classement de la course, les français sont placés sur la droite.")
            with col_pacing_tour_par_tour:
                biathletes_2 = st.multiselect("Biathlètes:", all_athletes, key="biathlètes 2")
                st.info("Ligne à 0=moyenne des 3 tours pour chaque biathlète. Les tours ne font pas exactement la même distance...")



            ## 3 GRAPHES DE L'ANALYSE INDIVIDUELLE ##        



            fig_temps_de_ski_total, fig_temps_de_ski_par_tour, _, _, fig_pacing_tour_par_tour = graphes_VTT(df, choix_homme_ou_femme, top_n_2, biathletes_2, nombre_de_shoots)



            with col_temps_de_ski_total_temps_de_ski_par_tour:
                with st.container(height=700):
                    st.pyplot(fig_temps_de_ski_total)
                    st.pyplot(fig_temps_de_ski_par_tour)
            with col_pacing_tour_par_tour:
                st.pyplot(fig_pacing_tour_par_tour)
                
            with col_tableau_temps_de_ski:
                st.markdown("Classement par temps de ski:")
                st.dataframe(tableau_temps_de_ski(df, nombre_de_shoots),hide_index=True)


            ### POINTS FORTS / POINTS FAIBLES ###
            
            st.subheader("Points forts & points faibles")

            st.info("Barre vers le haut: l'athlète a mieux performé par rapport à sa moyenne de performance sur la course. Barre vers le bas c'est l'inverse !")

            
            col_nationalites_points_forts_faibles, col_biathletes_points_forts_faibles = st.columns(2)
            
            with col_nationalites_points_forts_faibles:
                nationalites_2 = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalites points forts et faibles")
            with col_biathletes_points_forts_faibles:
                biathletes_points_forts_faibles = st.multiselect("Biathlètes:", all_athletes, key="biathletes points forts faibles")
            
            _, col_message, _ = st.columns([3,6,3])
            
            if len(nationalites_2) == 0:
                with col_message:
                    st.warning("**⚠️ Sélectionnez les nationalités/biathlètes à afficher ⚠️**")        
            else:
                fig_points_forts_faibles = f_points_forts_faibles_plateforme(df, f_df_sans_temps_shoot(df, nombre_de_shoots)[0], biathletes_points_forts_faibles, nationalites_2, noms_intermediaires, choix_homme_ou_femme, split_tour_par_tour(df, nombre_de_shoots), distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)
                st.pyplot(fig_points_forts_faibles)




        ### PARTIE 3 ### #####     ANALYSE DE PORTION SPECIFIQUE     #####




        with onglets[3]:
            
            st.header("Analyse de portion spécifique")
            
            col_partie_gauche, col_partie_droite = st.columns([8,8])
            
            with col_partie_gauche:
                st.subheader("Zoom sur le superman")
                with st.expander("Choix des données zoom sur le superman"):
                    col_biathletes_superman_agrandi_indiv, col_biathletes_superman_agrandi_nationalites = st.columns([4,3])
                    col_split_time_portion_specifique_indiv, col_comment_afficher = st.columns([4,3])
                
            with col_partie_droite:
                st.subheader("Une seule portion")  
                with st.expander("Choix des données une seule portion"):
                    col_top_N_une_seule_portion_indiv, col_biathletes_une_seule_portion_indiv, col_nationalites_une_seule_portion_indiv = st.columns([2,3,3])
                    # col_portion_une_seule_portion = st.columns(1)  
                    intermediaire_a_afficher = st.selectbox("Portion", noms_intermediaires)          
            
            
            with col_split_time_portion_specifique_indiv:
                split_time = st.multiselect("Split time à afficher:", split_time_a_afficher_un_par_un)
                st.write("_Sélectionnzr un split-time, la portion étudiée sera: split-time d'avant -> split-time choisi._")
                
            with col_comment_afficher:
                affichage = ["Athlète au meilleur temps de ski sur la course", "Meilleur athlète sélectionné/e", "Superman"]
                affichage_arg = st.selectbox("Affichage:", affichage)
                st.write("_Ecarts à l'athlète le plus rapide sur la course, au superman ou au meilleur athlète choisi._")        
            
            col_graphes_1, _, col_graphes_2 = st.columns([7,1,8])

                
            
            with col_biathletes_superman_agrandi_indiv:
                biathletes_3 = st.multiselect("Biathlètes:", all_athletes, key="biathlètes 3")
            with col_biathletes_superman_agrandi_nationalites:
                nationalites_3 = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalités 3")    
            with col_top_N_une_seule_portion_indiv:
                top_n_unique_portion = st.slider("Top ...", min_value=1, max_value=75, value=10, key="top N 3")    
            with col_biathletes_une_seule_portion_indiv:
                biathletes_une_seule_portion_individuel = st.multiselect("Biathlètes:", all_athletes, key="biathletes 4")
            with col_nationalites_une_seule_portion_indiv:
                nationalites_une_seule_portion_individuel = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalites 4")        
        
            with col_graphes_2:        
                st.pyplot(analyse_une_seule_portion_individuel(df, noms_intermediaires, intermediaire_a_afficher, biathletes_une_seule_portion_individuel, nationalites_une_seule_portion_individuel,top_n_unique_portion, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots))      
                
                
            with col_graphes_1:
                if len(split_time) == 0:
                    st.warning("**⚠️ Sélectionnez les split-time à afficher ⚠️**")
                elif len(biathletes_3) == 0 and len(nationalites_3) == 0:
                    st.warning("**⚠️ Sélectionnez un/e athlète ou une nationalité à afficher ⚠️**")                        
                else:
                    fig_superman_agrandi = analyse_portion_specifique_graphe_1(df, biathletes_3, nationalites_3, split_time, choix_homme_ou_femme, distance_de_1_tour, distance_toute_la_course, affichage_arg, nombre_de_shoots)
                    st.pyplot(fig_superman_agrandi)         
                
                
                
                
            st.header("Analyse par type de portion")
            
            # st.write("_Jonas a choisi quelles portions correspondent aux bosses, descentes, etc_")
                
            col_top_n_type_de_portion, col_nationalites_type_de_portion, col_biathletes_type_de_portion = st.columns(3)

            with col_top_n_type_de_portion:
                top_n_to_show = st.slider("Top ...", min_value=1, max_value=80, value=10, key="top N 5")
            with col_nationalites_type_de_portion:
                nationalites_a_afficher = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalites 5")
            with col_biathletes_type_de_portion:
                biathletes_a_afficher = st.multiselect("Biathlètes:", all_athletes, key="biathlètes 5")

            either_container_or_error_indiv = st.empty()
            
            try:
                with either_container_or_error_indiv.container(height=350):
                    col_graphe_bosse, col_graphe_descente, col_graphe_plat, col_graphe_valloné = st.columns(4)
                
                fig_type_de_portion_bosses, fig_type_de_portion_descentes, fig_type_de_portion_plats, fig_type_de_portion_vallonés = analyse_type_de_portion_individuel(df, noms_intermediaires, noms_intermediaires_bosses, noms_intermediaires_descentes, noms_intermediaires_vallones, noms_intermediaires_plats, biathletes_a_afficher, nationalites_a_afficher, top_n_to_show, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)

                with col_graphe_bosse:
                    st.pyplot(fig_type_de_portion_bosses)
                with col_graphe_descente:
                    st.pyplot(fig_type_de_portion_descentes)
                with col_graphe_plat:
                    st.pyplot(fig_type_de_portion_plats)
                with col_graphe_valloné:
                    st.pyplot(fig_type_de_portion_vallonés) 
            
            except:
                either_container_or_error_indiv.error("Données types de portion non rentrées pour la course sélectionnée !")   
                
                
                
            ### ANALYSE GLISSE INDIVIDUEL ###
                
                
            st.header("Analyse glisse")              
            with st.expander("L'analyse de la glisse est prévue pour les circuits comportant des descentes séparées en deux portions, si c'est le cas pour la course sélectionnée cliquez dessus !"):
                
                st.info("**_Choisir la portion 1, la portion 2 sera automatiquement la portion qui suit. Le graphe représente le ratio entre la vitesse moyenne sur la portion 2 et la vitesse moyenne sur la portion 1._**" + "  \n" + "_Plus la barre est haute, plus l'athlète a conservé/augmenté sa vitesse initiale, il a été plus efficace._")
                
                # st.write("Comment comprendre cette figure ?", key="comprendre la glisse individuel")
                # st.info("_Plus la barre est haute, plus l'athlète a conservé/augmenté sa vitesse initiale, il a été plus efficace._")

                col_top_n_ratio_indiv, col_top_n_split_amont_indiv, col_biathletes_ratio_indiv, col_nationalites_ratio_indiv = st.columns(4)
                
                with col_top_n_ratio_indiv:
                    top_n_ratio_indiv = st.slider("Top ...", min_value=1, max_value=75, value=10, key="top N 6")
                with col_top_n_split_amont_indiv:
                    split_amont_ratio_indiv = st.multiselect("Portion 1:", noms_intermediaires)
                with col_biathletes_ratio_indiv:
                    biathletes_a_afficher = st.multiselect("Biathlètes:", all_athletes, key="biathletes 6")
                with col_nationalites_ratio_indiv:
                    nationalites_a_afficher = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalites 6")
                    
                # print("split_amont sans modification: " + str(split_amont))

                # print("split_amont après modification: " + str(split_amont))
                
                _, col_ratio_indiv, _ = st.columns([2,6,2])
                
                with col_ratio_indiv:
                    if len(split_amont_ratio_indiv) == 0:
                        st.warning("**⚠️ Sélectionnez UN SEUL split-time à afficher ⚠️**")
                    elif len(split_amont_ratio_indiv) > 1:
                        st.warning("**⚠️ Sélectionnez UN SEUL split-time à afficher ⚠️**")
                    else:  
                        split_amont_ratio_indiv = dico_noms_dashboard_noms_code[split_amont_ratio_indiv[0]]         
                        st.pyplot(analyse_portion_specifique_ratio_individuel(df, top_n_ratio_indiv,  split_amont_ratio_indiv, nationalites_a_afficher, biathletes_a_afficher, choix_homme_ou_femme, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots))
                    
                    
                    
            st.header("Analyse de toutes les portions")
            
            col_top_N_toutes_les_portions, col_biathletes_toutes_les_portions, col_nationalites_toutes_les_portions = st.columns(3)
            
            with col_top_N_toutes_les_portions:
                top_n_toutes_les_portions = st.slider("Top ...", min_value=1, max_value=70, value=10, key="top N 7")    
            with col_biathletes_toutes_les_portions:
                biathletes_a_afficher = st.multiselect("Biathlètes:", all_athletes, key="biathletes 7")
            with col_nationalites_toutes_les_portions:
                nationalites_a_afficher = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalites 7")
            
            st.pyplot(analyse_toutes_les_portions_individuel(df, noms_intermediaires, biathletes_a_afficher, nationalites_a_afficher, top_n_toutes_les_portions, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots))
            
            
            

        ### PARTIE 4 ### #####     ANALYSE COLLECTIVE     #####




        with onglets[4]:

            st.header("Analyse collective")
                                       
            st.markdown("**_Choisir les meilleurs biathlètes par nationalité par rapport à leur classement final de la course._**")

            col_nb_FRA, col_nb_NOR, col_nb_GER, col_nb_SWE, col_nb_ITA = st.columns(5)
            with col_nb_FRA:
                nombre_FRA = st.selectbox("FRA", [1,2,3,4,5])
            with col_nb_NOR:
                nombre_NOR = st.selectbox("NOR", [1,2,3,4,5])
            with col_nb_GER:
                nombre_GER = st.selectbox("GER", [1,2,3,4,5])
            with col_nb_SWE:
                nombre_SWE = st.selectbox("SWE", [1,2,3,4,5])
            with col_nb_ITA:
                nombre_ITA = st.selectbox("ITA", [1,2,3,4,5])  
            
            col_portion_specifique_nationalite, _, col_une_seule_portion_nationalite = st.columns([6,1,6])
            
            with col_portion_specifique_nationalite:
                st.subheader("Analyse de portion spécifique")
                with st.expander("Choix des données à afficher"):
                    nationalites = st.multiselect("Nationalités:", ["FRA", "NOR", "GER", "SWE", "ITA"], key="nationalités superman agrandi par nationalité")
                    split_time = st.multiselect("Split time à afficher:", split_time_a_afficher_un_par_un, key="split time portion spécifique nationalité")
                    st.info("**_Sélectionnez un split-time, la portion ajoutée sera: split-time d'avant -> split-time choisi._**")
                
                if len(split_time) == 0:
                    st.warning("**⚠️ Sélectionnez les split-time à afficher ⚠️**")        
                else:
                    fig_superman_agrandi_nationalite = analyse_portion_specifique_graphe_1_par_nationalite(df, biathletes_a_afficher, nationalites, split_time, choix_homme_ou_femme, distance_de_1_tour, distance_toute_la_course, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, nombre_de_shoots)
                    st.pyplot(fig_superman_agrandi_nationalite)
            
            with col_une_seule_portion_nationalite:
                st.subheader("Une seule portion")
                intermediaire_a_afficher = st.selectbox("Portion", noms_intermediaires, key="intermédiaire à afficher une seule portion par nationalité")
                fig_une_seule_portion_nationalite = analyse_une_seule_portion_nationalites(df, noms_intermediaires, intermediaire_a_afficher, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)
                st.pyplot(fig_une_seule_portion_nationalite)
           

            st.subheader("Analyse par type de portion")
                           
            either_container_or_error_coll = st.empty()
      
            try:     
                with either_container_or_error_coll.container(height=300): 
                    col_graphe_bosse, col_graphe_descente, col_graphe_plat, col_graphe_valloné = st.columns(4) 
                
                fig_chronos_3_tours_nationalite, fig_type_de_portion_bosses, fig_type_de_portion_plats, fig_type_de_portion_descentes, fig_type_de_portion_vallonés = analyse_type_de_portion_nationalite(df, noms_intermediaires, noms_intermediaires_bosses, noms_intermediaires_descentes, noms_intermediaires_plats, noms_intermediaires_vallones, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, nombre_de_shoots, distance_de_1_tour, distance_toute_la_course)

                with col_graphe_bosse:
                    st.pyplot(fig_type_de_portion_bosses)
                with col_graphe_descente:
                    st.pyplot(fig_type_de_portion_descentes)
                with col_graphe_plat:
                    st.pyplot(fig_type_de_portion_plats)
                with col_graphe_valloné:
                    st.pyplot(fig_type_de_portion_vallonés)
            
            except:
                either_container_or_error_coll.error("Données types de portion non rentrées pour la course sélectionnée !")


            ### GLISSE PAR NATIONALITE ###


            st.subheader("Analyse glisse")
            
            with st.expander("L'analyse de la glisse est prévue pour les circuits comportant des descentes séparées en deux portions, si c'est le cas pour la course sélectionnée cliquez dessus !"):
            
                st.info("**_Choisir la portion 1, la portion 2 sera automatiquement la portion qui suit. Le graphe représente le ratio entre la vitesse moyenne sur la portion 2 et la vitesse moyenne sur la portion 1._**" + "  \n" + "_Plus la barre est haute, plus l'athlète a conservé/augmenté sa vitesse initiale._")
                # st.write("**_Comment comprendre cette figure ?_**", key="comprendre la glisse individuel")
                # st.write("_Plus la barre est haute, plus l'athlète a conservé/augmenté sa vitesse initiale._")
                    
                col_split_amont_ratio_nationalite, col_nb_FRA, col_nb_NOR, col_nb_GER, col_nb_SWE, col_nb_ITA = st.columns(6)
                
                with col_split_amont_ratio_nationalite:   
                    split_amont_ratio_nationalite = st.selectbox("Portion 1", noms_intermediaires)
                        

                _, col_ratio_nationalites, _ = st.columns([4,6,4])
                    
                    
                with col_ratio_nationalites:
                    # if len(split_amont_ratio_nationalite) == 0:
                    #     st.write("**⚠️ Veuillez sélectionnez UN SEUL split-time à afficher ⚠️**")
                    # elif len(split_amont_ratio_nationalite) > 1:
                    #     st.write("**⚠️ Veuillez sélectionnez UN SEUL split-time à afficher ⚠️**")
                    # else:     
                    split_amont_ratio_nationalite = dico_noms_dashboard_noms_code[split_amont_ratio_nationalite] 
                    fig_ratio_par_nationalite = analyse_portion_specifique_ratio_nationalite(df, split_amont_ratio_nationalite, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)
                    st.pyplot(fig_ratio_par_nationalite)


            ### TOUTES LES PORTIONS PAR NATIONALITE ###
            
            
            st.subheader("Toutes les portions")  
            
            fig_toutes_les_portions_par_nationalite = analyse_toutes_les_portions_nationalites(df, noms_intermediaires, nombre_FRA, nombre_NOR, nombre_GER, nombre_SWE, nombre_ITA, distance_de_1_tour, distance_toute_la_course, nombre_de_shoots)

            st.pyplot(fig_toutes_les_portions_par_nationalite)




        
