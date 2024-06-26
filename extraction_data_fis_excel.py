import pandas as pd

import imaplib
import email

from fonctions_utiles_code_plateforme import convert_chrono_to_seconds

# imap_server = 'imap.gmail.com'
# username = 'plateformesplit.cnsn@gmail.com'
# password = 'analysedecourse'

# chemin_fichier_excel = '2024CC2310AL.xls'
# chemin_fichier_excel = "C:\\Users\\jules\\Plateforme-analyse-de-course\\2024CC2277AL.xls"

# df = pd.read_excel(chemin_fichier_excel)

# df_rank_bib_name_nat = df[["Rank", "Bib", "Name", "Noc"]].copy()
# df_rank_bib_name_nat = df_rank_bib_name_nat.dropna(axis=0)
# df_rank_bib_name_nat.reset_index(drop=True, inplace=True)

# df_time = df.copy()

# for index_line in range(df.shape[0]):
#     if not df.iloc[index_line]["Description"] == "Cumulative:":
#         df_time = df_time.drop(axis=0,index=index_line)
        
# for nom_colonne in df_time.columns.tolist():
#     if "Time" not in nom_colonne:
#         df_time = df_time.drop(nom_colonne, axis=1)
      
# df_time.reset_index(drop=True, inplace=True) 
# df_time_in_seconds = pd.DataFrame() 

# for index_ligne in range(df_time.shape[0]):
#     for index_colonne in range(len(df_time.columns.tolist())):
#         df_time_in_seconds.at[index_ligne, index_colonne] = convert_chrono_to_seconds(df_time.iloc[index_ligne, index_colonne])
        
# df_final = pd.concat([df_rank_bib_name_nat,df_time_in_seconds], axis=1)

# print(df_final)
