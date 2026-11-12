############################################################################################
# Script che legge tutti i file sorgenti con i dati relativi a PIng Talk e                 #
# crea i grafici corrispondenti.                                                           #
#                                                                                          #
# Autore: Pietro Boccadoro                                                                 #
# email: pieroboccadoro13[at]gmail[dot]com                                                 #
# Creazione: 2024-06-10                                                                    #
#                                                                                          #
# Licenza: MIT License                                                                     #
# Copyright (c) 2026 Pietro Boccadoro                                                      #
#                                                                                          #
# Questo file serve per generare i grafici a partire dai files CSV che produce Spotify.    #
# I grafici vengono salvati nella cartella Grafici.                                        #
#                                                                                          #
# Per usare questo file, servono le seguenti librerie Python: pandas, matplotlib.          #
# Per installarle, eseguire il comando: pip install pandas matplotlib.                     #
############################################################################################

# Import della classe Path per la gestione dei percorsi
from pathlib import Path

# Import della libreria pandas per leggere i file CSV
import pandas as pd

# Import della libreria matplotlib per la generazione dei grafici
import matplotlib.pyplot as plt

# Import della libreria per la gestione delle espressioni regolari
import re

# Import del gestore che limita il numero di label sugli assi
from matplotlib.ticker import MaxNLocator


def nome_file_valido(nome):
    """
    Genera un nome file compatibile con il filesystem.

    Parametri:
        nome (str): stringa da convertire in nome file.

    Restituisce:
        str: nome file ripulito dai caratteri non validi.
    """

    # Rimuove tutti i caratteri non ammessi nei nomi file
    return re.sub(r'[<>:"/\\|?*]', '', nome)


def genera_titolo(df, nome_csv):
    """
    Genera automaticamente il titolo del grafico.

    Parametri:
        df (DataFrame): dataframe contenente i dati.
        nome_csv (str): nome del file CSV.

    Restituisce:
        str: titolo del grafico.
    """

    # Recupera l'elenco delle colonne del dataframe
    colonne = list(df.columns)

    # Se il dataframe contiene almeno due colonne
    if len(colonne) >= 2:

        # Costruisce un titolo descrittivo
        return f"Andamento di {', '.join(colonne[1:])} rispetto a {colonne[0]}"

    # Titolo di fallback nel caso di struttura inattesa
    return f"Visualizzazione dati di {nome_csv}"


def determina_tipo_grafico(df):
    """
    Determina automaticamente il grafico più adatto
    in base alla struttura del dataset.

    Parametri:
        df (DataFrame): dataframe da analizzare.

    Restituisce:
        str: tipologia di grafico.
    """

    # Recupera i nomi delle colonne in minuscolo
    colonne = [str(colonna).lower() for colonna in df.columns]

    # Verifica presenza di coordinate geografiche
    if (
        ("lat" in colonne and "lon" in colonne)
        or
        ("latitude" in colonne and "longitude" in colonne)
    ):
        return "mappa"

    # Recupera le colonne numeriche
    colonne_numeriche = df.select_dtypes(include="number").columns

    # Dataset composto da una sola colonna
    if len(df.columns) == 1:
        return "torta"

    # Controlla se la prima colonna contiene date
    try:

        pd.to_datetime(df.iloc[:, 0])

        return "linea"

    except Exception:

        pass

    # Dataset con due sole colonne numeriche
    if (
        len(df.columns) == 2
        and len(colonne_numeriche) == 2
    ):
        return "scatter"

    # Prima colonna testuale
    if df.iloc[:, 0].dtype == "object":
        return "barre"

    # Più colonne numeriche
    return "linea"


def salva_grafico(csv_file, cartella_grafici):
    """
    Legge un file CSV, determina automaticamente il tipo di grafico
    più adatto e salva il risultato nella cartella Grafici.

    Parametri:
        csv_file (Path):
            Percorso del file CSV da elaborare.

        cartella_grafici (Path):
            Cartella in cui salvare i grafici generati.

    Restituisce:
        None

    Eccezioni:
        Tutte le eccezioni vengono intercettate e mostrate
        a video senza interrompere l'esecuzione del programma.
    """

    try:

        # Legge il file CSV utilizzando Pandas
        df = pd.read_csv(csv_file)

        # Verifica che il DataFrame non sia vuoto
        if df.empty:

            # Mostra un messaggio di avviso
            print(f"File vuoto: {csv_file.name}")

            # Termina l'elaborazione del file corrente
            return

        # Determina automaticamente il grafico più adatto
        tipo_grafico = determina_tipo_grafico(df)

        # Genera il titolo del grafico
        titolo = genera_titolo(df, csv_file.stem)

        # Crea figura e assi
        fig, ax = plt.subplots(figsize=(12, 6))

        ######################################################################
        # GRAFICO A LINEE
        ######################################################################

        if tipo_grafico == "linea":

            # Recupera la prima colonna da usare come asse X
            x = df.iloc[:, 0]

            # Disegna tutte le colonne successive come serie
            for colonna in df.columns[1:]:

                ax.plot(
                    x,
                    df[colonna],
                    label=colonna
                )

            # Mostra la legenda
            ax.legend()

            # Imposta etichette assi
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel("Valore")

        ######################################################################
        # GRAFICO A BARRE
        ######################################################################

        elif tipo_grafico == "barre":

            # Disegna grafico a barre
            ax.bar(
                df.iloc[:, 0],
                df.iloc[:, 1]
            )

            # Imposta etichette assi
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel(df.columns[1])

        ######################################################################
        # SCATTER PLOT
        ######################################################################

        elif tipo_grafico == "scatter":

            # Disegna il grafico di dispersione
            ax.scatter(
                df.iloc[:, 0],
                df.iloc[:, 1]
            )

            # Imposta etichette assi
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel(df.columns[1])

        ######################################################################
        # GRAFICO GEOGRAFICO SEMPLIFICATO
        ######################################################################

        elif tipo_grafico == "mappa":

            # Verifica utilizzo di lat/lon
            if "lat" in df.columns and "lon" in df.columns:

                ax.scatter(
                    df["lon"],
                    df["lat"],
                    s=50
                )

            # Verifica utilizzo di latitude/longitude
            elif (
                "latitude" in df.columns
                and
                "longitude" in df.columns
            ):

                ax.scatter(
                    df["longitude"],
                    df["latitude"],
                    s=50
                )

            # Imposta assi geografici
            ax.set_xlabel("Longitudine")
            ax.set_ylabel("Latitudine")

        ######################################################################
        # GRAFICO A TORTA
        ######################################################################

        elif tipo_grafico == "torta":

            # Calcola frequenze delle categorie
            frequenze = df.iloc[:, 0].value_counts()

            # Disegna il grafico a torta
            ax.pie(
                frequenze.values,
                labels=frequenze.index,
                autopct="%1.1f%%"
            )

        ######################################################################
        # GRAFICO DI DEFAULT
        ######################################################################

        else:

            # Recupera la prima colonna come asse X
            x = df.iloc[:, 0]

            # Disegna tutte le serie presenti
            for colonna in df.columns[1:]:

                ax.plot(
                    x,
                    df[colonna],
                    label=colonna
                )

            # Mostra legenda
            ax.legend()

        # Imposta il titolo del grafico
        ax.set_title(titolo)

        # Attiva la griglia
        ax.grid(True)

        # Limita le label visualizzate sull'asse X
        ax.xaxis.set_major_locator(MaxNLocator(nbins=5))

        # Limita le label visualizzate sull'asse Y
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

        # Ottimizza il layout della figura
        plt.tight_layout()

        # Costruisce il nome del file PNG
        nome_immagine = nome_file_valido(titolo) + ".png"

        # Costruisce il percorso completo del file
        percorso_output = cartella_grafici / nome_immagine

        # Salva il grafico sul disco
        plt.savefig(
            percorso_output,
            dpi=300
        )

        # Chiude la figura liberando memoria
        plt.close()

        # Mostra il risultato dell'elaborazione
        print(
            f"Creato: {nome_immagine} "
            f"(Tipo: {tipo_grafico})"
        )

    except Exception as e:

        # Mostra l'errore verificatosi durante l'elaborazione
        print(
            f"Errore con {csv_file.name}: {e}"
        )


def main():
    """
    Funzione principale del programma.

    Individua i file CSV nella cartella Sorgenti e genera
    i grafici nella cartella Grafici.

    Restituisce:
        None
    """

    # Individua la cartella che contiene questo script
    cartella_script = Path(__file__).resolve().parent

    # Costruisce il percorso della cartella Sorgenti
    cartella_sorgenti = cartella_script / "Sorgenti"

    # Costruisce il percorso della cartella Grafici
    cartella_grafici = cartella_script / "Grafici"

    # Crea la cartella Grafici se non esiste
    cartella_grafici.mkdir(exist_ok=True)

    # Verifica che la cartella Sorgenti esista
    if not cartella_sorgenti.exists():

        # Segnala l'errore
        print("Cartella 'Sorgenti' non trovata.")

        # Termina il programma
        return

    # Recupera tutti i file CSV presenti nella cartella Sorgenti
    csv_files = list(cartella_sorgenti.glob("*.csv"))

    # Verifica che siano stati trovati file CSV
    if not csv_files:

        # Segnala l'assenza di file da elaborare
        print("Nessun file CSV trovato.")

        # Termina il programma
        return

    # Elabora ciascun file CSV trovato
    for csv_file in csv_files:

        # Genera il grafico associato al file CSV
        salva_grafico(csv_file, cartella_grafici)


# Verifica che il file sia eseguito direttamente
if __name__ == "__main__":

    # Avvia l'esecuzione del programma
    main()