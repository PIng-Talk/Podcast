#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSD_calculator.py

Calcolatore grafico per stimare l'impatto di Fast Startup (Avvio rapido)
sull'usura di un SSD su un orizzonte temporale (default 2 anni).

Requisiti:
- Python 3.8+
- Tkinter (incluso nella maggior parte delle distribuzioni Python)
- matplotlib
- pandas
- numpy

Installazione dipendenze:
pip install matplotlib pandas numpy

Uso:
Salva questo file come SSD_calculator.py ed esegui:
python SSD_calculator.py

Note tecniche:
- TBW (Terabytes Written) è considerato in TB (1 TB = 1024 GB).
- GB per spegnimento è la stima della quantità di dati scritti su disco ad ogni spegnimento
  quando Fast Startup è attivo. Microsoft non fornisce un valore fisso; qui si usano stime.
- Percentuale di usura = (GB_totali / (TBW_in_TB * 1024)) * 100
  dove GB_totali è la somma delle scritture logiche in GB su tutto l'orizzonte.
- Il calcolatore è pensato per fornire ordini di grandezza e confronti, non misure assolute.
"""

# ---------- Importazioni ----------

# importa il modulo tkinter con alias 'tk' per costruire l'interfaccia grafica
import tkinter as tk
# importa ttk (themed widgets) da tkinter per widget con stile moderno
from tkinter import ttk, messagebox, filedialog
# importa matplotlib e imposta il backend per l'integrazione con Tkinter
import matplotlib
matplotlib.use('TkAgg')
# importa il canvas per incorporare i grafici matplotlib in Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# importa pyplot per creare i grafici
import matplotlib.pyplot as plt
# importa pandas per gestire i dati in DataFrame
import pandas as pd
# importa numpy per operazioni numeriche e generazione di range
import numpy as np
# importa csv per eventuali operazioni CSV (non strettamente necessarie qui)
import csv
# importa sys per eventuali interazioni con il sistema (non usato esplicitamente)
import sys
# importa formatter per formattare l'asse y in percentuali personalizzate
from matplotlib.ticker import FuncFormatter

# ---------- Funzioni di calcolo ----------

# definisce una funzione che calcola i GB totali scritti in un orizzonte temporale
def gb_totali_per_orizzonte(gb_per_spegnimento, spegnamenti_giorno, giorni_per_anno, anni):
    """
    Calcola i GB totali scritti in un orizzonte temporale.
    """
    # moltiplica GB per spegnimento per il numero di spegnimenti giornalieri, giorni per anno e anni
    return gb_per_spegnimento * spegnamenti_giorno * giorni_per_anno * anni

# definisce una funzione che calcola la percentuale di usura rispetto al TBW dichiarato
def percentuale_usura(gb_totali, tbw_tb):
    """
    Calcola la percentuale di usura rispetto al TBW dichiarato.
    TBW è in TB; 1 TB = 1024 GB.
    """
    # se il TBW è zero o negativo, restituisce NaN per evitare divisione per zero
    if tbw_tb <= 0:
        return np.nan
    # converte TBW da TB a GB (1 TB = 1024 GB)
    tbw_gb = tbw_tb * 1024.0
    # calcola la percentuale come rapporto tra GB totali e TBW in GB, moltiplicato per 100
    return (gb_totali / tbw_gb) * 100.0

# ---------- GUI e logica ----------

# definisce la classe principale dell'applicazione ereditando da tk.Tk
class SSDWearCalculatorApp(tk.Tk):
    # costruttore della classe
    def __init__(self):
        # chiama il costruttore della classe base
        super().__init__()
        # imposta il titolo della finestra principale
        self.title("Calcolatore usura SSD - Fast Startup")
        # imposta la dimensione iniziale della finestra
        self.geometry("1100x700")
        # crea i widget dell'interfaccia
        self.create_widgets()
        # inizializza un DataFrame vuoto per memorizzare i risultati
        self.results_df = pd.DataFrame()

    # metodo per creare e disporre i widget nell'interfaccia
    def create_widgets(self):
        # crea un frame etichettato per i parametri di input
        frm_inputs = ttk.LabelFrame(self, text="Parametri di input")
        # posiziona il frame nella finestra principale
        frm_inputs.pack(fill='x', padx=10, pady=6)

        # etichetta e campo per TBW minimo
        ttk.Label(frm_inputs, text="TBW minimo (TB):").grid(row=0, column=0, sticky='w', padx=6, pady=4)
        # variabile di testo per il TBW minimo con valore di default "150"
        self.tbw_min_var = tk.StringVar(value="150")
        # campo di input per TBW minimo
        ttk.Entry(frm_inputs, textvariable=self.tbw_min_var, width=10).grid(row=0, column=1, padx=6)

        # etichetta e campo per TBW massimo
        ttk.Label(frm_inputs, text="TBW massimo (TB):").grid(row=0, column=2, sticky='w', padx=6)
        # variabile di testo per il TBW massimo con valore di default "600"
        self.tbw_max_var = tk.StringVar(value="600")
        # campo di input per TBW massimo
        ttk.Entry(frm_inputs, textvariable=self.tbw_max_var, width=10).grid(row=0, column=3, padx=6)

        # etichetta e campo per il passo TBW
        ttk.Label(frm_inputs, text="Passo TBW (TB):").grid(row=0, column=4, sticky='w', padx=6)
        # variabile di testo per il passo TBW con valore di default "150"
        self.tbw_step_var = tk.StringVar(value="150")
        # campo di input per il passo TBW
        ttk.Entry(frm_inputs, textvariable=self.tbw_step_var, width=10).grid(row=0, column=5, padx=6)

        # etichetta e campo per GB per spegnimento minimo
        ttk.Label(frm_inputs, text="GB/spegnimento min:").grid(row=1, column=0, sticky='w', padx=6, pady=4)
        # variabile di testo per GB min con valore di default "0.5"
        self.gb_min_var = tk.StringVar(value="0.5")
        # campo di input per GB min
        ttk.Entry(frm_inputs, textvariable=self.gb_min_var, width=10).grid(row=1, column=1, padx=6)

        # etichetta e campo per GB per spegnimento massimo
        ttk.Label(frm_inputs, text="GB/spegnimento max:").grid(row=1, column=2, sticky='w', padx=6)
        # variabile di testo per GB max con valore di default "4"
        self.gb_max_var = tk.StringVar(value="4")
        # campo di input per GB max
        ttk.Entry(frm_inputs, textvariable=self.gb_max_var, width=10).grid(row=1, column=3, padx=6)

        # etichetta e campo per il passo GB
        ttk.Label(frm_inputs, text="Passo GB (GB):").grid(row=1, column=4, sticky='w', padx=6)
        # variabile di testo per il passo GB con valore di default "0.5"
        self.gb_step_var = tk.StringVar(value="0.5")
        # campo di input per il passo GB
        ttk.Entry(frm_inputs, textvariable=self.gb_step_var, width=10).grid(row=1, column=5, padx=6)

        # etichetta e campo per gli spegnimenti per giorno (accetta lista)
        ttk.Label(frm_inputs, text="Spegnimenti/giorno (es. 1 o 1,2,4):").grid(row=2, column=0, sticky='w', padx=6, pady=4)
        # variabile di testo per spegnimenti con valore di default "1,2,4"
        self.shutdowns_var = tk.StringVar(value="1,2,4")
        # campo di input per spegnimenti
        ttk.Entry(frm_inputs, textvariable=self.shutdowns_var, width=20).grid(row=2, column=1, padx=6)

        # etichetta e campo per l'orizzonte in anni
        ttk.Label(frm_inputs, text="Orizzonte (anni):").grid(row=2, column=2, sticky='w', padx=6)
        # variabile di testo per anni con valore di default "2"
        self.years_var = tk.StringVar(value="2")
        # campo di input per anni
        ttk.Entry(frm_inputs, textvariable=self.years_var, width=8).grid(row=2, column=3, padx=6)

        # etichetta e campo per i giorni per anno (default 365)
        ttk.Label(frm_inputs, text="Giorni/anno:").grid(row=2, column=4, sticky='w', padx=6)
        # variabile di testo per giorni per anno con valore di default "365"
        self.days_var = tk.StringVar(value="365")
        # campo di input per giorni per anno
        ttk.Entry(frm_inputs, textvariable=self.days_var, width=8).grid(row=2, column=5, padx=6)

        # crea un frame per i preset (casi preimpostati)
        frm_presets = ttk.LabelFrame(self, text="Casi preimpostati (GB per spegnimento)")
        # posiziona il frame dei preset
        frm_presets.pack(fill='x', padx=10, pady=6)
        # bottone per preset conservativo che imposta 0.5 GB
        ttk.Button(frm_presets, text="Conservativo (0.5 GB)", command=lambda: self.set_preset(0.5)).pack(side='left', padx=6, pady=6)
        # bottone per preset centrale che imposta 1.5 GB
        ttk.Button(frm_presets, text="Centrale (1.5 GB)", command=lambda: self.set_preset(1.5)).pack(side='left', padx=6, pady=6)
        # bottone per preset alto che imposta 4 GB
        ttk.Button(frm_presets, text="Alto (4 GB)", command=lambda: self.set_preset(4.0)).pack(side='left', padx=6, pady=6)

        # frame per i pulsanti di azione (Calcola, Esporta, Pulisci, Guida)
        frm_actions = ttk.Frame(self)
        # posiziona il frame dei pulsanti
        frm_actions.pack(fill='x', padx=10, pady=6)
        # bottone per eseguire il calcolo
        ttk.Button(frm_actions, text="Calcola", command=self.on_calcola).pack(side='left', padx=6)
        # bottone per esportare i risultati in CSV
        ttk.Button(frm_actions, text="Esporta CSV", command=self.on_export_csv).pack(side='left', padx=6)
        # bottone per esportare il grafico come immagine
        ttk.Button(frm_actions, text="Esporta grafico", command=self.on_export_plot).pack(side='left', padx=6)
        # bottone per pulire i risultati
        ttk.Button(frm_actions, text="Pulisci risultati", command=self.on_clear).pack(side='left', padx=6)
        # bottone per mostrare la guida e le assunzioni
        ttk.Button(frm_actions, text="Guida e assunzioni", command=self.on_help).pack(side='right', padx=6)

        # frame che conterrà la tabella dei risultati e il grafico
        frm_results = ttk.Frame(self)
        # posiziona il frame dei risultati
        frm_results.pack(fill='both', expand=True, padx=10, pady=6)

        # crea una Treeview per mostrare i risultati in forma tabellare
        self.tree = ttk.Treeview(frm_results, columns=("TBW_TB","GB_per_shut","shut_per_day","GB_tot_TB","percent_2y"), show='headings')
        # definisce le intestazioni delle colonne
        self.tree.heading("TBW_TB", text="TBW (TB)")
        self.tree.heading("GB_per_shut", text="GB/spegn.")
        self.tree.heading("shut_per_day", text="Spegn./giorno")
        self.tree.heading("GB_tot_TB", text="GB totali (TB)")
        self.tree.heading("percent_2y", text="% usura (orizz. selez.)")
        # imposta larghezze e allineamento delle colonne
        self.tree.column("TBW_TB", width=80, anchor='center')
        self.tree.column("GB_per_shut", width=100, anchor='center')
        self.tree.column("shut_per_day", width=100, anchor='center')
        self.tree.column("GB_tot_TB", width=120, anchor='center')
        self.tree.column("percent_2y", width=140, anchor='center')
        # posiziona la Treeview nel frame dei risultati
        self.tree.pack(side='left', fill='both', expand=True)

        # crea una scrollbar verticale per la tabella
        scrollbar = ttk.Scrollbar(frm_results, orient="vertical", command=self.tree.yview)
        # collega la scrollbar alla Treeview
        self.tree.configure(yscroll=scrollbar.set)
        # posiziona la scrollbar accanto alla tabella
        scrollbar.pack(side='left', fill='y')

        # crea una figura matplotlib e un asse per il grafico
        self.fig, self.ax = plt.subplots(figsize=(6,4))
        # crea il canvas che incorpora la figura matplotlib in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm_results)
        # posiziona il canvas nel frame dei risultati
        self.canvas.get_tk_widget().pack(side='right', fill='both', expand=True)

        # variabile di stato per mostrare messaggi all'utente
        self.status_var = tk.StringVar(value="Pronto")
        # etichetta che mostra lo stato corrente
        ttk.Label(self, textvariable=self.status_var).pack(fill='x', padx=10, pady=4)

    # metodo che imposta i preset per GB per spegnimento
    def set_preset(self, gb_value):
        # imposta il valore minimo di GB per spegnimento
        self.gb_min_var.set(str(gb_value))
        # imposta il valore massimo di GB per spegnimento
        self.gb_max_var.set(str(gb_value))
        # imposta un passo piccolo per permettere variazioni minime
        self.gb_step_var.set("0.1")
        # aggiorna la label di stato per informare l'utente
        self.status_var.set(f"Preset impostato: {gb_value} GB per spegnimento")

    # funzione di utilità per convertire stringhe in float con gestione errori
    def parse_float(self, s, name):
        try:
            # prova a convertire la stringa in float
            return float(s)
        except Exception:
            # solleva un ValueError con messaggio descrittivo in caso di errore
            raise ValueError(f"Valore non valido per {name}: '{s}'")

    # funzione di utilità per convertire stringhe in int con gestione errori
    def parse_int(self, s, name):
        try:
            # prova a convertire la stringa in int
            return int(s)
        except Exception:
            # solleva un ValueError con messaggio descrittivo in caso di errore
            raise ValueError(f"Valore non valido per {name}: '{s}'")

    # funzione per interpretare il campo spegnimenti che può contenere una lista separata da virgole
    def parse_shutdowns(self, s):
        # divide la stringa sulle virgole e rimuove spazi vuoti
        parts = [p.strip() for p in s.split(',') if p.strip()!='']
        # lista che conterrà i valori numerici validi
        vals = []
        # itera ogni elemento parsato
        for p in parts:
            try:
                # prova a convertire in float (accetta anche valori non interi)
                v = float(p)
                # rifiuta valori non positivi
                if v <= 0:
                    raise ValueError
                # aggiunge il valore valido alla lista
                vals.append(v)
            except Exception:
                # solleva un errore descrittivo se uno degli elementi non è valido
                raise ValueError(f"Valore non valido in Spegnimenti/giorno: '{p}'")
        # restituisce la lista di spegnimenti/giorno
        return vals

    # metodo chiamato quando l'utente preme "Calcola"
    def on_calcola(self):
        # validazione degli input con gestione degli errori
        try:
            tbw_min = self.parse_float(self.tbw_min_var.get(), "TBW minimo")
            tbw_max = self.parse_float(self.tbw_max_var.get(), "TBW massimo")
            tbw_step = self.parse_float(self.tbw_step_var.get(), "Passo TBW")
            gb_min = self.parse_float(self.gb_min_var.get(), "GB min")
            gb_max = self.parse_float(self.gb_max_var.get(), "GB max")
            gb_step = self.parse_float(self.gb_step_var.get(), "Passo GB")
            shutdowns = self.parse_shutdowns(self.shutdowns_var.get())
            years = self.parse_float(self.years_var.get(), "Anni")
            days = self.parse_int(self.days_var.get(), "Giorni/anno")
        except ValueError as e:
            # mostra un messaggio di errore se la validazione fallisce
            messagebox.showerror("Errore input", str(e))
            return

        # controlli addizionali sui valori numerici
        if tbw_min <= 0 or tbw_max <= 0 or tbw_step <= 0:
            messagebox.showerror("Errore input", "TBW e passo devono essere > 0")
            return
        if gb_min < 0 or gb_max < 0 or gb_step <= 0:
            messagebox.showerror("Errore input", "GB devono essere >= 0 e passo > 0")
            return
        if tbw_max < tbw_min:
            messagebox.showerror("Errore input", "TBW massimo deve essere >= TBW minimo")
            return
        if gb_max < gb_min:
            messagebox.showerror("Errore input", "GB max deve essere >= GB min")
            return

        # genera un array di valori TBW usando numpy.arange con passo specificato
        tbw_values = np.arange(tbw_min, tbw_max + 1e-9, tbw_step)
        # genera un array di valori GB per spegnimento usando numpy.arange
        gb_values = np.arange(gb_min, gb_max + 1e-9, gb_step)

        # pulisce la tabella Treeview rimuovendo eventuali righe precedenti
        for i in self.tree.get_children():
            self.tree.delete(i)

        # prepara una lista per raccogliere le righe dei risultati
        rows = []
        # ciclo su ogni combinazione di TBW, GB per spegnimento e spegnimenti/giorno
        for tbw in tbw_values:
            for gb in gb_values:
                for shut in shutdowns:
                    # calcola i GB totali per l'orizzonte usando la funzione definita sopra
                    gb_tot = gb_totali_per_orizzonte(gb, shut, days, years)
                    # calcola la percentuale di usura rispetto al TBW
                    pct = percentuale_usura(gb_tot, tbw)
                    # converte GB totali in TB per visualizzazione nella tabella
                    gb_tot_tb = gb_tot / 1024.0
                    # aggiunge un dizionario con i valori calcolati alla lista rows
                    rows.append({
                        "TBW_TB": round(tbw,3),
                        "GB_per_shut": round(gb,3),
                        "shut_per_day": round(shut,3),
                        "GB_tot_TB": round(gb_tot_tb,3),
                        "percent_2y": round(pct,6)
                    })

        # crea un DataFrame pandas dai risultati raccolti
        self.results_df = pd.DataFrame(rows)
        # ordina il DataFrame per TBW, GB per spegnimento e spegnimenti/giorno
        self.results_df.sort_values(by=["TBW_TB","GB_per_shut","shut_per_day"], inplace=True)

        # popola la Treeview con i risultati del DataFrame
        for _, r in self.results_df.iterrows():
            self.tree.insert("", "end", values=(r["TBW_TB"], r["GB_per_shut"], r["shut_per_day"], r["GB_tot_TB"], f'{r["percent_2y"]:.6f}'))

        # aggiorna il grafico: per ogni TBW traccia percentuale vs GB_per_shut per il primo profilo di spegnimenti
        self.update_plot(tbw_values, gb_values, shutdowns)

        # aggiorna la label di stato con il numero di combinazioni calcolate
        self.status_var.set(f"Calcolo completato: {len(self.results_df)} combinazioni")

    # metodo per aggiornare il grafico matplotlib incorporato
    def update_plot(self, tbw_values, gb_values, shutdowns):
        # pulisce l'asse corrente
        self.ax.clear()

        # palette colori per TBW
        tbw_colors = plt.cm.viridis(np.linspace(0,1,len(tbw_values)))

        # palette colori per spegnimenti/giorno
        shut_colors = plt.cm.plasma(np.linspace(0,1,len(shutdowns)))

        # raccoglie tutte le percentuali per calcolare limiti dinamici
        all_pct_values = []

        # ciclo su TBW e su spegnimenti/giorno
        for i, tbw in enumerate(tbw_values):
            for j, shut in enumerate(shutdowns):

                pct_list = []
                for gb in gb_values:
                    gb_tot = gb_totali_per_orizzonte(
                        gb,
                        shut,
                        int(self.days_var.get()),
                        float(self.years_var.get())
                    )
                    pct = percentuale_usura(gb_tot, tbw)
                    pct_list.append(pct)

                    if pct is not None and not (isinstance(pct, float) and np.isnan(pct)):
                        all_pct_values.append(pct)

                # nome della curva
                label = f"TBW {tbw} TB – {shut} spegn./giorno"

                # colore combinato TBW + spegnimenti
                color_mix = (tbw_colors[i] * 0.6) + (shut_colors[j] * 0.4)

                # se un solo valore X → scatter
                if len(gb_values) == 1:
                    self.ax.scatter(gb_values, pct_list, label=label, color=color_mix)
                else:
                    self.ax.plot(gb_values, pct_list, label=label, color=color_mix)

        # Impostazioni dinamiche asse X
        try:
            min_gb = float(np.min(gb_values))
            max_gb = float(np.max(gb_values))
            gb_range = max_gb - min_gb
            gb_margin = gb_range * 0.05 if gb_range > 0 else 0.5
            self.ax.set_xlim(min_gb - gb_margin, max_gb + gb_margin)
        except Exception:
            pass

        # Impostazioni dinamiche asse Y
        if len(all_pct_values) == 0:
            self.ax.set_ylim(0.0, 1.0)
        else:
            min_pct = float(np.min(all_pct_values))
            max_pct = float(np.max(all_pct_values))
            y_min = 0.0
            y_max = max(max_pct * 1.20, max_pct + 0.01)
            self.ax.set_ylim(y_min, y_max)

        # formattatore percentuale
        def percent_formatter(x, pos):
            return f"{x:.3f}%"

        self.ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

        # etichette
        self.ax.set_xlabel("GB per spegnimento")
        self.ax.set_ylabel("Percentuale di usura (%)")
        self.ax.set_title(f"Percentuale usura su {self.years_var.get()} anni")

        # griglia e legenda
        self.ax.grid(True)
        self.ax.legend(fontsize=8)

        # layout
        self.fig.tight_layout()

        # aggiorna grafico
        self.canvas.draw()

    # metodo per esportare i risultati in CSV
    def on_export_csv(self):
        # controlla che ci siano risultati da esportare
        if self.results_df is None or self.results_df.empty:
            # informa l'utente che non ci sono dati
            messagebox.showinfo("Nessun dato", "Esegui il calcolo prima di esportare.")
            return
        # apre una finestra di dialogo per scegliere il percorso di salvataggio
        fpath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv"),("All files","*.*")])
        # se l'utente annulla la finestra di dialogo, esce
        if not fpath:
            return
        try:
            # salva il DataFrame in CSV senza l'indice
            self.results_df.to_csv(fpath, index=False)
            # mostra un messaggio di conferma
            messagebox.showinfo("Esportazione completata", f"Risultati esportati in {fpath}")
        except Exception as e:
            # mostra un messaggio di errore in caso di eccezione durante il salvataggio
            messagebox.showerror("Errore esportazione", str(e))

    # metodo per esportare il grafico come immagine
    def on_export_plot(self):
        # finestra di dialogo per scegliere dove salvare il grafico
        fpath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All files", "*.*")]
        )

        # se l'utente annulla, esci
        if not fpath:
            return

        try:
            # salva la figura matplotlib nel percorso scelto
            self.fig.savefig(fpath, dpi=300)
            messagebox.showinfo("Esportazione completata", f"Grafico salvato in:\n{fpath}")
        except Exception as e:
            messagebox.showerror("Errore esportazione grafico", str(e))

    # metodo per pulire i risultati e resettare il grafico
    def on_clear(self):
        # rimuove tutte le righe dalla Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # pulisce l'asse del grafico
        self.ax.clear()
        # ridisegna il canvas vuoto
        self.canvas.draw()
        # resetta il DataFrame dei risultati a vuoto
        self.results_df = pd.DataFrame()
        # aggiorna lo stato
        self.status_var.set("Risultati puliti")

    # metodo che mostra una finestra di aiuto con le assunzioni del calcolatore
    def on_help(self):
        # testo di aiuto che spiega le assunzioni e i limiti del calcolatore
        help_text = (
            "Guida e assunzioni:\n\n"
            "- TBW (Terabytes Written) è espresso in TB. 1 TB = 1024 GB.\n"
            "- GB per spegnimento è una stima della quantità di dati scritti su disco\n"
            "  quando Fast Startup salva lo stato del kernel in hiberfil.sys.\n"
            "- Le percentuali calcolate sono indicative e servono a confrontare ordini di grandezza.\n"
            "- Per una stima precisa misurare il valore reale di Host Writes del vostro SSD\n"
            "  e usare il TBW dichiarato dal produttore.\n"
            "- Esempi preimpostati: Conservativo 0.5 GB, Centrale 1.5 GB, Alto 4 GB.\n"
            "- Se usi Modern Standby (S0 Low Power Idle) su portatili, disattivare l'ibernazione\n"
            "  può comportare rischi di perdita dati in caso di batteria scarica.\n"
        )
        # mostra il testo di aiuto in una finestra informativa
        messagebox.showinfo("Guida e assunzioni", help_text)

# ---------- Main ----------

# funzione principale che avvia l'applicazione
def main():
    # crea un'istanza dell'applicazione
    app = SSDWearCalculatorApp()
    # avvia il loop principale di Tkinter (gestione eventi)
    app.mainloop()

# se il file è eseguito come script principale, chiama main()
if __name__ == "__main__":
    main()
