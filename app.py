from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

ARCHIVO_JSON = "reservas.json"

# Cargar reservas desde el archivo JSON
def cargar_reservas():
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):  # Verifica que sea una lista
                    return data
                else:
                    return []  # Si no es lista, retorna vacío
            except json.JSONDecodeError:
                return []  # Si hay error, retorna vacío
    return []  # Si el archivo no existe, retorna vacío

# Guardar reservas en el archivo JSON
def guardar_reservas(reservas):
    with open(ARCHIVO_JSON, "w") as f:
        json.dump(reservas, f, indent=4)

@app.route("/")
def home():
    reservas = cargar_reservas()
    return render_template("index.html", reservas=reservas)

@app.route("/agregar", methods=["POST"])
def agregar_reserva():
    reservas = cargar_reservas()
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    habitacion = request.form["habitacion"]
    
    nueva_reserva = {
        "id": len(reservas) + 1,
        "nombre": nombre,
        "fecha": fecha,
        "habitacion": habitacion
    }
    
    reservas.append(nueva_reserva)
    guardar_reservas(reservas)
    
    return redirect(url_for("home"))

@app.route("/eliminar/<int:id>")
def eliminar_reserva(id):
    reservas = cargar_reservas()
    reservas = [r for r in reservas if r["id"] != id]
    guardar_reservas(reservas)
    
    return redirect(url_for("home"))

@app.route("/editar/<int:id>", methods=["POST"])
def editar_reserva(id):
    reservas = cargar_reservas()
    for r in reservas:
        if r["id"] == id:
            r["nombre"] = request.form["nombre"]
            r["fecha"] = request.form["fecha"]
            r["habitacion"] = request.form["habitacion"]
            break
    
    guardar_reservas(reservas)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

