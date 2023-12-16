import os
import datetime as d
import pandas as pd

path = r"last_report.csv"
modify_time = os.path.getmtime(path)
modify_date = d.datetime.fromtimestamp(modify_time).strftime('%d-%m-%Y - %H:%M:%S')

print("\nReport precedente, data:", modify_date,"\n")
df_last_report = pd.read_csv("last_report.csv") #lettura ultimo report
print(df_last_report.to_string(index=False))

df_users_logs = pd.read_csv("logs.csv") #lettura csv
df_users_events = df_users_logs.groupby(["User full name","Event name"]).count().reset_index() #raggruppo tutte le righe in funzione dell'utente e degli eventi da quest'ultimo attivati, e conto questi ultimi

dfue_sent_message = df_users_events[df_users_events["Event name"]=="Message sent"] #scelgo solo gli eventi riguardanti l'invio di un messaggio da parte dei diversi utenti
dfue_posted_content = df_users_events[df_users_events["Event name"]=="Some content has been posted."] #scelgo solo gli eventi riguardanti la pubblicazione di un contenuto nei forum da parte dei diversi utenti
dfue_created_discussion = df_users_events[df_users_events["Event name"]=="Discussion created"] #scelgo solo gli eventi riguardanti la creazione di una discussione nei forum da parte dei diversi utenti

df_users_interactions = pd.concat([dfue_sent_message, dfue_posted_content, dfue_created_discussion]) #unisco i 3 mini dataframe
df_users_interactions = df_users_interactions.rename(columns = {"Time" : "Interaction occurrences"}) #essendo la data di ogni azione di un utente univoca, rinomino questa per contare le righe

df_user_sum_of_interactions = df_users_interactions.groupby(by="User full name").sum().reset_index() #raggruppo il nuovo dataframe in funzione di ogni utente, e sommo le sue occorrenze dei 3 eventi
report = df_user_sum_of_interactions[["User full name", "Interaction occurrences"]].sort_values(by="User full name", ascending=True) #nome e somma occorrenze dei 3 eventi per ciascun utente

print("\nNuovo report\n")
print(report.to_string(index=False)) #stampa a video
report.to_csv('last_report.csv', index=False) #creazione file report.csv
print("\n")
os.system(("pause"))