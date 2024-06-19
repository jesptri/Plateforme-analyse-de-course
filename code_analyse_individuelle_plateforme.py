import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from fonctions_utiles_code_plateforme import f_df_sans_temps_shoot
from fonctions_utiles_code_plateforme import split_tour_par_tour

# df = pd.read_excel("c:\\Users\\jules\\Desktop\\Stage CNSNMM\\Analyse de course\\Lenzerheide\\ST sprint femmes.xlsx", sheet_name='ST Lenzerheide')

@st.cache_data()
def tableau_ranking_course(df):

    colonnes_a_copier = ["Ranking", "Name", "Finish"]
    df_tableau = df.loc[:,colonnes_a_copier].sort_values(by="Ranking")
    df_tableau = df_tableau.round(0)

    df_tableau = df_tableau.sort_values(by="Ranking").reset_index(drop=True)

    df_tableau.columns = ["Ranking", "Nom", "Temps de course"]

    for index_biathlete in range(1,df_tableau.shape[0]):
        df_tableau.at[index_biathlete, "Temps de course"] = "+ " + str(df_tableau.at[index_biathlete, "Temps de course"] - df_tableau.at[0, "Temps de course"]) + "s"
    
    df_tableau.at[0, "Temps de course"] = str(int(df_tableau.at[0, "Temps de course"]/60)) + "'" + str(int(df_tableau.at[0, "Temps de course"]%60)) + "s"

    return df_tableau

@st.cache_data()
def tableau_temps_de_ski(df, nombre_de_shoots):
    df_sans_temps_shoot = f_df_sans_temps_shoot(df, nombre_de_shoots)[7]
    df_sans_temps_shoot = df_sans_temps_shoot.sort_values(by="Finish")
    
    colonnes_a_copier = ["Ranking", "Name", "Finish"]
    
    df_tableau = df_sans_temps_shoot.loc[:, colonnes_a_copier]
    
    df_tableau = df_tableau.round(0)
    
    df_tableau = df_tableau.reset_index(drop=True)
    
    df_tableau.columns = ["Ranking", "Nom", "Ski time"]
    
    for index_biathlete in range(1,df_tableau.shape[0]):
        df_tableau.at[index_biathlete, "Ski time"] = "+ " + str(df_tableau.at[index_biathlete, "Ski time"] - df_tableau.at[0, "Ski time"]) + "s"
    
    df_tableau.at[0, "Ski time"] = str(int(df_tableau.at[0, "Ski time"]/60)) + "'" + str(int(df_tableau.at[0, "Ski time"]%60)) + "s"
    
    return df_tableau


st.cache_data()
def graphes_VTT(df, sexe, top_n, biathletes_a_afficher, nombre_de_shoots, split_pour_graphe_pacing_tour_1):
    
    if top_n < 25:
        police = 10
    elif top_n >= 25 and top_n < 45:
        police = 8
    elif top_n >= 45 and top_n <= 55:
        police = 6
    else:
        police = 4
    
    df_3_tours = df.iloc[:, :4].copy()
    
    if nombre_de_shoots == 2:
        df_3_tours["Temps tour 1"] = df["→ Shooting 1"]
        df_3_tours["Temps tour 2"] = df["→ Shooting 2"] - df["Shooting 1"]
        df_3_tours["Temps tour 3"] = df["Finish"] - df["Shooting 2"]
        df_3_tours["Temps total"] = df_3_tours["Temps tour 1"] + df_3_tours["Temps tour 2"] + df_3_tours["Temps tour 3"]
        
    elif nombre_de_shoots == 4:
        df_3_tours["Temps tour 1"] = df["→ Shooting 1"]
        df_3_tours["Temps tour 2"] = df["→ Shooting 2"] - df["Shooting 1"]
        df_3_tours["Temps tour 3"] = df["→ Shooting 3"] - df["Shooting 2"]
        df_3_tours["Temps tour 4"] = df["→ Shooting 4"] - df["Shooting 3"]
        df_3_tours["Temps tour 5"] = df["Finish"] - df["Shooting 4"]
        df_3_tours["Temps total"] = df_3_tours["Temps tour 1"] + df_3_tours["Temps tour 2"] + df_3_tours["Temps tour 3"] + df_3_tours["Temps tour 4"] + df_3_tours["Temps tour 5"]
   
    df_3_tours = df_3_tours.sort_values(by="Ranking")
    
    df_3_tours_not_filtered = df_3_tours.copy()
    
    df_3_tours = df_3_tours[(df_3_tours["Ranking"] <= top_n) | (df_3_tours["Country"] == "FRA") | df_3_tours["Name"].isin(biathletes_a_afficher)] 
    df_3_tours = df_3_tours.reset_index(drop=True)
    
    fig1 = plt.figure()
    
    
    ### TROUVER LE MEILLEUR TEMPS DE SKI TOTAL ###
    
    
    chrono_meilleur_temps_de_ski = df_3_tours_not_filtered["Temps total"].min()


    ### TEMPS DE SKI TOTAL ###

    if nombre_de_shoots == 2:
        for index_biathlete in range(df_3_tours.shape[0]):
            if df_3_tours.iloc[index_biathlete, 3] == "FRA":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] - chrono_meilleur_temps_de_ski, color="blue")
            elif df_3_tours.iloc[index_biathlete, 3] == "GER":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] - chrono_meilleur_temps_de_ski, color="black")
            elif df_3_tours.iloc[index_biathlete, 3] == "NOR":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] - chrono_meilleur_temps_de_ski, color="red")
            elif df_3_tours.iloc[index_biathlete, 3] == "SWE":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] - chrono_meilleur_temps_de_ski, color="orange")
            elif df_3_tours.iloc[index_biathlete, 3] == "ITA":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] - chrono_meilleur_temps_de_ski, color="green")
            else:
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] - chrono_meilleur_temps_de_ski, color="grey")
    elif nombre_de_shoots == 4:
        for index_biathlete in range(df_3_tours.shape[0]):
            # print(df_3_tours.iloc[index_biathlete][4] == "FRA")
            if df_3_tours.iloc[index_biathlete, 3] == "FRA":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] + df_3_tours.iloc[index_biathlete, 7] + df_3_tours.iloc[index_biathlete, 8] - chrono_meilleur_temps_de_ski, color="blue")
            elif df_3_tours.iloc[index_biathlete, 3] == "GER":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] + df_3_tours.iloc[index_biathlete, 7] + df_3_tours.iloc[index_biathlete, 8] - chrono_meilleur_temps_de_ski, color="black")
            elif df_3_tours.iloc[index_biathlete, 3] == "NOR":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] + df_3_tours.iloc[index_biathlete, 7] + df_3_tours.iloc[index_biathlete, 8] - chrono_meilleur_temps_de_ski, color="red")
            elif df_3_tours.iloc[index_biathlete, 3] == "SWE":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] + df_3_tours.iloc[index_biathlete, 7] + df_3_tours.iloc[index_biathlete, 8] - chrono_meilleur_temps_de_ski, color="orange")
            elif df_3_tours.iloc[index_biathlete, 3] == "ITA":
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] + df_3_tours.iloc[index_biathlete, 7] + df_3_tours.iloc[index_biathlete, 8] - chrono_meilleur_temps_de_ski, color="green")
            else:
                plt.scatter(index_biathlete+1, df_3_tours.iloc[index_biathlete, 5] + df_3_tours.iloc[index_biathlete, 6] + df_3_tours.iloc[index_biathlete, 4] + df_3_tours.iloc[index_biathlete, 7] + df_3_tours.iloc[index_biathlete, 8] - chrono_meilleur_temps_de_ski, color="grey")

    # plt.scatter(np.arange(df_3_tours.shape[0])+1, df_3_tours.iloc[:, 5] + df_3_tours.iloc[:, 6] + df_3_tours.iloc[:, 7])
    labels = ["+" + str(label.get_text()) + "s" for label in plt.gca().get_yticklabels()]
    plt.gca().set_yticklabels(labels)
    plt.xticks(np.arange(df_3_tours.shape[0])+1, [str(df_3_tours.iloc[i, 0]) + " - " + df_3_tours.iloc[i, 2] for i in range(df_3_tours.shape[0])], rotation=90, fontsize=police)
    plt.grid(linestyle='--', linewidth=0.5)
    plt.title("Temps de ski total (retard au meilleur temps)")
    plt.tight_layout()


    ### TEMPS DE SKI PAR TOUR ###


    fig2 = plt.figure()
    for index_biathlete in range(df_3_tours.shape[0]):
        if df_3_tours.iloc[index_biathlete, 3] == "FRA":
            plt.boxplot(df_3_tours.transpose().iloc[4:-1, index_biathlete], positions=[index_biathlete+1], boxprops=dict(color="blue"), whiskerprops=dict(color="blue"), medianprops=dict(color="blue"), whis=[0, 100])
        elif df_3_tours.iloc[index_biathlete, 3] == "GER":
            plt.boxplot(df_3_tours.transpose().iloc[4:-1, index_biathlete], positions=[index_biathlete+1], boxprops=dict(color="black"), whiskerprops=dict(color="black"), medianprops=dict(color="black"), whis=[0, 100])       
        elif df_3_tours.iloc[index_biathlete, 3] == "NOR":        
            plt.boxplot(df_3_tours.transpose().iloc[4:-1, index_biathlete], positions=[index_biathlete+1], boxprops=dict(color="red"), whiskerprops=dict(color="red"), medianprops=dict(color="red"), whis=[0, 100])
        elif df_3_tours.iloc[index_biathlete, 3] == "SWE":
            plt.boxplot(df_3_tours.transpose().iloc[4:-1, index_biathlete], positions=[index_biathlete+1], boxprops=dict(color="orange"), whiskerprops=dict(color="orange"), medianprops=dict(color="orange"), whis=[0, 100])       
        elif df_3_tours.iloc[index_biathlete, 3] == "ITA":
            plt.boxplot(df_3_tours.transpose().iloc[4:-1, index_biathlete], positions=[index_biathlete+1], boxprops=dict(color="green"), whiskerprops=dict(color="green"), medianprops=dict(color="green"), whis=[0, 100])
        else:
            plt.boxplot(df_3_tours.transpose().iloc[4:-1, index_biathlete], positions=[index_biathlete+1], boxprops=dict(color="grey"), whiskerprops=dict(color="grey"), medianprops=dict(color="grey"), whis=[0, 100])
                       
    labels = [str(label.get_text()) + "s" for label in plt.gca().get_yticklabels()]
    plt.gca().set_yticklabels(labels)
    plt.xticks(np.arange(df_3_tours.shape[0])+1, [str(df_3_tours.iloc[i]["Ranking"]) + " - " + df_3_tours.iloc[i]["Name"] for i in range(df_3_tours.shape[0])], rotation=90, fontsize=police)
    plt.grid(linestyle='--', linewidth=0.5)
    plt.title("Temps de ski par tour")
    plt.tight_layout()
    
    # ### % D'AMELIORATION SUR LE DERNIER TOUR ###

    fig3 = plt.figure()
        
    # ### % D'AMELIORATION SUR LE DERNIER TOUR ###

    fig4 = plt.figure()   
    
    ### PACING TOUR PAR TOUR ###
    
    ecarts_X_tours = [[] for _ in range(df_3_tours.shape[0])]
    
    if nombre_de_shoots == 2:

        tous_les_split = split_tour_par_tour(df, nombre_de_shoots)[0] + split_tour_par_tour(df, nombre_de_shoots)[1] + split_tour_par_tour(df, nombre_de_shoots)[2]

        index_des_split_choisis = []

        for split in split_pour_graphe_pacing_tour_1:
            for index_split_bis, split_bis in enumerate(tous_les_split):
                if split == split_bis:
                    index_des_split_choisis.append(index_split_bis)

        # tour 2

        split_pour_graphe_pacing_tour_2 = []

        for index in index_des_split_choisis:
            split_pour_graphe_pacing_tour_2.append(split_tour_par_tour(df, nombre_de_shoots)[1][index])

        # tour 3

        split_pour_graphe_pacing_tour_3 = []

        for index in index_des_split_choisis:
            split_pour_graphe_pacing_tour_3.append(split_tour_par_tour(df, nombre_de_shoots)[2][index])

        df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0]

        for index_biathlete in range(df_3_tours.shape[0]):
            for split in split_pour_graphe_pacing_tour_1:

                # tour 1

                temps_portion_tour_1 = 0
                for split in split_pour_graphe_pacing_tour_1:
                    temps_portion_tour_1 += df_temps_de_ski.iloc[index_biathlete][split]

                # tour 2

                temps_portion_tour_2 = 0
                for split in split_pour_graphe_pacing_tour_2:
                    temps_portion_tour_2 += df_temps_de_ski.iloc[index_biathlete][split]

                # tour 3

                temps_portion_tour_3 = 0
                for split in split_pour_graphe_pacing_tour_3:
                    temps_portion_tour_3 += df_temps_de_ski.iloc[index_biathlete][split]

            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,0])
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,1])
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,2])
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,3])
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_1 - temps_portion_tour_1) # 2ème terme = pour avoir le premier tour comme référence 
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_2 - temps_portion_tour_1)
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_3 - temps_portion_tour_1)
                                
        fig5 = plt.figure()
        
        # print("ecarts_X_tours: " + str(ecarts_X_tours))
        for biathlete in biathletes_a_afficher:
            for index_biathlete in range(len(ecarts_X_tours)):
                if ecarts_X_tours[index_biathlete][2] == biathlete:
                    if ecarts_X_tours[index_biathlete][3] == "FRA":
                        plt.plot([1,2,3], ecarts_X_tours[index_biathlete][4:], "royalblue", marker="o")
                        plt.text(3 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "NOR":
                        plt.plot([1,2,3], ecarts_X_tours[index_biathlete][4:], "red", marker="o")
                        plt.text(3 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "GER":
                        plt.plot([1,2,3], ecarts_X_tours[index_biathlete][4:], "black", marker="o")
                        plt.text(3 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "SWE":
                        plt.plot([1,2,3], ecarts_X_tours[index_biathlete][4:], "gold", marker="o")
                        plt.text(3 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "ITA":
                        plt.plot([1,2,3], ecarts_X_tours[index_biathlete][4:], "limegreen", marker="o")
                        plt.text(3 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    else:
                        plt.plot([1,2,3], ecarts_X_tours[index_biathlete][4:], "gray", marker="o")      
                        plt.text(3 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])          

    elif nombre_de_shoots == 4:

        tous_les_split = split_tour_par_tour(df, nombre_de_shoots)[0] + split_tour_par_tour(df, nombre_de_shoots)[1] + split_tour_par_tour(df, nombre_de_shoots)[2] + split_tour_par_tour(df, nombre_de_shoots)[3] + split_tour_par_tour(df, nombre_de_shoots)[4]

        index_des_split_choisis = []

        for split in split_pour_graphe_pacing_tour_1:
            for index_split_bis, split_bis in enumerate(tous_les_split):
                if split == split_bis:
                    index_des_split_choisis.append(index_split_bis)

        # tour 2

        split_pour_graphe_pacing_tour_2 = []

        for index in index_des_split_choisis:
            split_pour_graphe_pacing_tour_2.append(split_tour_par_tour(df, nombre_de_shoots)[1][index])

        # tour 3

        split_pour_graphe_pacing_tour_3 = []

        for index in index_des_split_choisis:
            split_pour_graphe_pacing_tour_3.append(split_tour_par_tour(df, nombre_de_shoots)[2][index])
 
        # tour 4

        split_pour_graphe_pacing_tour_4 = []
        for index in index_des_split_choisis:
            split_pour_graphe_pacing_tour_4.append(split_tour_par_tour(df, nombre_de_shoots)[3][index])

        # tour 5

        split_pour_graphe_pacing_tour_5 = []

        for index in index_des_split_choisis:
            split_pour_graphe_pacing_tour_5.append(split_tour_par_tour(df, nombre_de_shoots)[4][index])

        df_temps_de_ski = f_df_sans_temps_shoot(df, nombre_de_shoots)[0]

        for index_biathlete in range(df_3_tours.shape[0]):
            for split in split_pour_graphe_pacing_tour_1:

                # tour 1

                temps_portion_tour_1 = 0
                for split in split_pour_graphe_pacing_tour_1:
                    temps_portion_tour_1 += df_temps_de_ski.iloc[index_biathlete][split]

                # tour 2

                temps_portion_tour_2 = 0
                for split in split_pour_graphe_pacing_tour_2:
                    temps_portion_tour_2 += df_temps_de_ski.iloc[index_biathlete][split]

                # tour 3

                temps_portion_tour_3 = 0
                for split in split_pour_graphe_pacing_tour_3:
                    temps_portion_tour_3 += df_temps_de_ski.iloc[index_biathlete][split]

                # tour 4

                temps_portion_tour_4 = 0
                for split in split_pour_graphe_pacing_tour_4:
                    temps_portion_tour_4 += df_temps_de_ski.iloc[index_biathlete][split]

                # tour 5

                temps_portion_tour_5 = 0
                for split in split_pour_graphe_pacing_tour_5:
                    temps_portion_tour_5 += df_temps_de_ski.iloc[index_biathlete][split]
    
        # for index_biathlete in range(df_3_tours.shape[0]):
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,0])
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,1])
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,2])
            ecarts_X_tours[index_biathlete].append(df_3_tours.iloc[index_biathlete,3])
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_1 - temps_portion_tour_1)
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_2 - temps_portion_tour_1)
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_3 - temps_portion_tour_1)
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_4 - temps_portion_tour_1)
            ecarts_X_tours[index_biathlete].append(temps_portion_tour_5 - temps_portion_tour_1)
            
        fig5 = plt.figure()
        
        for biathlete in biathletes_a_afficher:
            for index_biathlete in range(len(ecarts_X_tours)):
                # print("print prout : ", ecarts_tours_1_2_3[index_biathlete][2], biathlete)
                # print("condition if: ", ecarts_tours_1_2_3[index_biathlete][2], biathlete)
                if ecarts_X_tours[index_biathlete][2] == biathlete:
                    if ecarts_X_tours[index_biathlete][3] == "FRA":
                        plt.plot([1,2,3,4,5], ecarts_X_tours[index_biathlete][4:], "royalblue", marker="o")
                        plt.text(5 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "NOR":
                        plt.plot([1,2,3,4,5], ecarts_X_tours[index_biathlete][4:], "red", marker="o")
                        plt.text(5 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "GER":
                        plt.plot([1,2,3,4,5], ecarts_X_tours[index_biathlete][4:], "black", marker="o")
                        plt.text(5 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "SWE":
                        plt.plot([1,2,3,4,5], ecarts_X_tours[index_biathlete][4:], "gold", marker="o")
                        plt.text(5 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    elif ecarts_X_tours[index_biathlete][3] == "ITA":
                        plt.plot([1,2,3,4,5], ecarts_X_tours[index_biathlete][4:], "limegreen", marker="o")
                        plt.text(5 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])
                    else:
                        plt.plot([1,2,3,4,5], ecarts_X_tours[index_biathlete][4:], "gray", marker="o")      
                        plt.text(5 + 0.1, ecarts_X_tours[index_biathlete][-1], ecarts_X_tours[index_biathlete][2])  


    plt.title("Pacing tour par tour")
    plt.xticks(np.arange(nombre_de_shoots+1)+1, ["Tour " + str(i) for i in range(1, nombre_de_shoots+2)])
    plt.gca().spines['right'].set_visible(False)
    if nombre_de_shoots == 2:
       plt.xlim(0,4)    
    if nombre_de_shoots == 4:    
       plt.xlim(0,6)
    y_max = max(abs(plt.ylim()[0]-1), abs(plt.ylim()[1]+1))
    plt.ylim(-y_max,y_max)
    plt.grid()
    plt.tight_layout()
    # plt.show()
    
    return fig1, fig2, fig3, fig4, fig5
