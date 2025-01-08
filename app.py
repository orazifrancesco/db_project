from flask import Flask, jsonify, request, render_template
from database import Session
from models import Turno
from datetime import datetime

app = Flask(__name__)


@app.before_request
def create_session():
    app.session = Session()

@app.teardown_request
def close_session(exception=None):
    app.session.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/turni', methods=['GET'])
def get_turni():
    session = app.session
    turni = session.query(Turno).order_by(Turno.data.asc()).all()
    turni_json = [
        {
            "id": turno.id,
            "data": turno.data.strftime("%Y-%m-%d") if turno.data else None,
            "orario_inizio": turno.orario_inizio.strftime("%H:%M") if turno.orario_inizio else None,
            "orario_fine": turno.orario_fine.strftime("%H:%M") if turno.orario_fine else None,
            "note": turno.note
        }
        for turno in turni
    ]
    return jsonify(turni_json)


@app.route('/turni', methods=['POST'])
def aggiungi_turno():
    session = app.session
    data = request.json.get("data")
    orario_inizio = request.json.get("orario_inizio")
    orario_fine = request.json.get("orario_fine")
    note = request.json.get("note", None)

    try:
        turno = Turno(
            data=datetime.strptime(data, "%Y-%m-%d"),
            orario_inizio=datetime.strptime(orario_inizio, "%H:%M"),
            orario_fine=datetime.strptime(orario_fine, "%H:%M"),
            note=note
        )
        session.add(turno)
        session.commit()
        return jsonify({"message": "Turno aggiunto con successo."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/turni/<int:id>', methods=['DELETE'])
def elimina_turno(id):
    session = app.session
    turno = session.query(Turno).filter_by(id=id).first()
    if turno:
        session.delete(turno)
        session.commit()
        return jsonify({"message": f"Turno con ID {id} eliminato con successo."}), 200
    else:
        return jsonify({"error": "Turno non trovato"}), 404

@app.route('/monte-ore', methods=['GET'])
def calcola_monte_ore():
    session = app.session
    mese = request.args.get("mese")  # Esempio: "2025-01"
    if not mese:
        return jsonify({"error": "Parametro 'mese' richiesto nel formato YYYY-MM."}), 400

    try:
        data_inizio = datetime.strptime(mese + "-01", "%Y-%m-%d")
        giorni_nel_mese = monthrange(data_inizio.year, data_inizio.month)[1]
        data_fine = data_inizio + timedelta(days=giorni_nel_mese)

        turni = session.query(Turno).filter(Turno.data >= data_inizio, Turno.data < data_fine).all()

        totale_ore = 0.0

        for turno in turni:
            if turno.orario_inizio and turno.orario_fine:
                delta = datetime.combine(datetime.min, turno.orario_fine) - datetime.combine(datetime.min, turno.orario_inizio)
                totale_ore += delta.total_seconds() / 3600

        return jsonify({"mese": mese, "totale_ore": round(totale_ore, 2)}), 200
    except ValueError:
        return jsonify({"error": "Formato del mese non valido. Usa il formato YYYY-MM."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)