from database import Session
from models import Turno
from datetime import datetime, timedelta
from calendar import monthrange

def aggiungi_turno(session, data, orario_inizio, orario_fine, note=None):
    try:
        data_format = datetime.strptime(data, "%Y-%m-%d")
        orario_inizio_format = datetime.strptime(orario_inizio, "%H:%M")
        orario_fine_format = datetime.strptime(orario_fine, "%H:%M")

        turno = Turno(
            data=data_format,
            orario_inizio=orario_inizio_format,
            orario_fine=orario_fine_format,
            note=note
        )
        session.add(turno)
        session.commit()
        print("Turno aggiunto con successo.")
    except Exception as e:
        print(f"Errore durante l'aggiunta del turno: {e}")


def visualizza_turno(session):
    turni = session.query(Turno).order_by(Turno.data.asc()).all()

    if not turni:
        print("Nessun turno trovato.")
        return []

    for turno in turni:
        data = turno.data.date() if turno.data else None

        orario_inizio = turno.orario_inizio.strftime('%H:%M') if turno.orario_inizio else "Non specificato"
        orario_fine = turno.orario_fine.strftime('%H:%M') if turno.orario_fine else "Non specificato"

        print(f"ID turno: {turno.id}, Giorno: {data}, "
              f"Orario Inizio: {orario_inizio}, Orario Fine: {orario_fine}, Note: {turno.note}")
        return turni

def modifica_turno(session):
    visualizza_turno(session)
    id_turno = input("Inserisci l'id del turno che vuoi modificare: ")

    turno = session.query(Turno).filter_by(id=id_turno).first()
    if not turno:
        print("Turno non trovato")
        return

    print(f"\nModifichiamo il turno con ID {turno.id}")
    data = input(f"Inserisci la nuova data (YYYY-MM-DD) [{turno.data.strftime('%Y-%m-%d')}]: ")
    orario_inizio = input(f"Inserisci il nuovo orario di inizio (HH:MM) [{turno.orario_inizio}]: ")
    orario_fine = input(f"Inserisci l'orario di fine turno (HH:MM) [{turno.orario_fine}]: ")
    note = input(f"Inserisci le eventuali note [{turno.note}]: ")

    turno.data = datetime.strptime(data, "%Y-%m-%d")
    turno.orario_inizio = orario_inizio
    turno.orario_fine = orario_fine
    turno.note = note

    session.commit()
    print("Turno modificato con successo.")

def calcola_monte_ore_mensile(session):
    try:
        mese = input("Inserisci il mese di cui vuoi sapere le ore (YYYY-MM): ")
        data_inizio = datetime.strptime(mese + "-01", "%Y-%m-%d")
        giorni_nel_mese = monthrange(data_inizio.year, data_inizio.month)[1]
        data_fine = data_inizio + timedelta(days=giorni_nel_mese)

        turni = session.query(Turno).filter(Turno.data >= data_inizio, Turno.data < data_fine).all()

        totale_ore = 0.0

        for turno in turni:
            ora_inizio = turno.orario_inizio
            ora_fine = turno.orario_fine

            if ora_inizio and ora_fine: 
                delta = datetime.combine(datetime.min, ora_fine) - datetime.combine(datetime.min, ora_inizio)
                ore = delta.total_seconds() / 3600
                totale_ore += ore
            else:
                print(f"Turno ID {turno.id} ha orari mancanti. Ignorato.")

        print(f"Le ore totali per il mese di {mese} sono {totale_ore:.2f} ore.")
    except ValueError:
        print("Formato del mese non valido. Usa il formato YYYY-MM.")
    except Exception as e:
        print(f"Errore durante il calcolo del monte ore: {e}")


def elimina_turno(session):
    id_turno = int(input("Inserisci l'ID del turno che vuoi eliminare: "))
    turno = session.query(Turno).filter(Turno.id == id_turno).first()
    if turno:
        session.delete(turno)
        session.commit()
        print(f"Il turno {id_turno} è stato eliminato con successo.")
    else:
        print("Non è stato trovato l'id del turno.")

def esci():
    exit()

def Main():
    session = Session()
    while True:
        print("1. Aggiungi un turno")
        print("2. Visualizza i turni")
        print("3. Apporta una modifica a un turno")
        print("4. Elimina un turno")
        print("5. Calcola il monte ore di un mese")
        print("6. Esci")
        scelta = int(input("Scegli l'azione da svolgere: "))

        if scelta == 1:
            aggiungi_turno(session)
        elif scelta == 2:
            visualizza_turno(session)
        elif scelta == 3:
            modifica_turno(session)
        elif scelta == 4:
            elimina_turno(session)
        elif scelta == 5:
            calcola_monte_ore_mensile(session)
        elif scelta == 6:
            exit()
        else:
            print("Inserisci un'azione valida, grazie.")
    
    session.close()

if __name__ == "__main__":
    Main()
