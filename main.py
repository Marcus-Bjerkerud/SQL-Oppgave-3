import sqlite3
import pandas as pd
from tkinter import *

# Funksjon for å opprette databasen og tabellene
def create_database_and_tables():
    # Koble til databasen
    conn = sqlite3.connect('kundeliste.db')
    c = conn.cursor()

    # Slett tabellene hvis de eksisterer
    c.execute('DROP TABLE IF EXISTS kundeinfo')
    c.execute('DROP TABLE IF EXISTS postnummer_tabell')

    # Opprett tabellene
    c.execute('''
        CREATE TABLE postnummer_tabell (
            postnummer TEXT PRIMARY KEY,
            sted TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE kundeinfo (
            kundenummer INTEGER PRIMARY KEY AUTOINCREMENT,
            fnavn TEXT NOT NULL,
            enavn TEXT NOT NULL,
            epost TEXT NOT NULL,
            tlf TEXT NOT NULL,
            postnr TEXT,
            FOREIGN KEY(postnr) REFERENCES postnummer_tabell(postnummer)
        )
    ''')

    # Lagre endringene og lukk tilkoblingen
    conn.commit()
    conn.close()

# Funksjon for å fylle tabellene med data fra CSV-filene
def fill_tables():
    # Koble til databasen
    conn = sqlite3.connect('kundeliste.db')

    # Les CSV-filene
    df_kundeinfo = pd.read_csv('kundeinfo.csv', sep=';')
    df_postnummer_tabell = pd.read_csv('postnummer.csv')

    # Skriv dataframes til databasen
    df_kundeinfo.to_sql('kundeinfo', conn, if_exists='replace', index=False)
    df_postnummer_tabell.to_sql('postnummer_tabell', conn, if_exists='replace', index=False)

    # Lukk tilkoblingen
    conn.close()

# Funksjon for å hente kundeinformasjon basert på kundenummer
def get_customer_info(customer_number):
    # Koble til databasen
    conn = sqlite3.connect('kundeliste.db')
    c = conn.cursor()

    # Utfør SQL-spørringen
    c.execute("SELECT * FROM kundeinfo WHERE kundenummer=?", (customer_number,))

    # Hent resultatet
    data = c.fetchone()

    # Lukk tilkoblingen og returner resultatet
    conn.close()
    return data

# Funksjon for å opprette GUI-en
def create_gui():
    # Opprett hovedvinduet
    root = Tk()
    root.title("Kundeliste")
    root.geometry("400x400")

    # Legg til en inndatafelt for kundenummer
    Label(root, text="Skriv inn kundenummer:").grid(row=0, column=0, padx=10, pady=10)
    customer_number_entry = Entry(root)
    customer_number_entry.grid(row=0, column=1, padx=10, pady=10)

    # Legg til en tekstboks for å vise kundeinformasjon
    Label(root, text="Kundeinformasjon:").grid(row=1, column=0, padx=10, pady=10)
    customer_info_text = Text(root, width=50, height=10)
    customer_info_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Legg til en knapp som henter og viser kundeinformasjonen når den klikkes
    def show_customer_info():
        # Hent kundenummeret fra inndatafeltet
        customer_number = customer_number_entry.get()

        # Hent kundeinformasjonen fra databasen
        customer_info = get_customer_info(customer_number)

        # Slett eksisterende tekst i tekstboksen
        customer_info_text.delete(1.0, END)

        # Sjekk om kundeinformasjonen ble funnet
        if customer_info is not None:
            # Formater kundeinformasjonen
            formatted_info = f"Kundenummer: {customer_info[0]}\nFornavn: {customer_info[1]}\nEtternavn: {customer_info[2]}\nEpost: {customer_info[3]}\nTelefon: {customer_info[4]}\nPostnummer: {customer_info[5]}"

            # Sett inn den formaterte kundeinformasjonen i tekstboksen
            customer_info_text.insert(END, formatted_info)
        else:
            # Hvis ingen kunde ble funnet, vis en feilmelding
            customer_info_text.insert(END, "Ingen kunde funnet med det kundenummeret.")

    Button(root, text="Vis kundeinfo", command=show_customer_info).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Start hovedløkken for GUI-en
    root.mainloop()

# Hovedfunksjonen
def main():
    # Opprett databasen og tabellene
    create_database_and_tables()

    # Fyll tabellene med data fra CSV-filene
    fill_tables()

    # Opprett og vis GUI-en
    create_gui()

# Hvis dette scriptet kjøres direkte (i stedet for å bli importert), kall hovedfunksjonen
if __name__ == "__main__":
    main()