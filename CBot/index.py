from flask import Flask, render_template, request
import re

app = Flask(__name__)

def cargar_postulados():
    diccionario = {}
    with open("NIF.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if ":" in linea:
                clave, valor = linea.strip().split(":", 1)
                diccionario[clave.strip()] = valor.strip()
    return diccionario

postulados = cargar_postulados()

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = ""
    if request.method == "POST":
        mensaje = request.form["message"].lower()
        respuesta = "Hmm... No encontré respuesta a la pregunta"
        for clave in postulados:
            if clave in mensaje:
                respuesta = formatear_respuesta(postulados[clave])
                break

    return render_template("index.html", respuesta=respuesta)

def formatear_respuesta(texto):
    texto = re.sub(r"\s*-\s*", r"\n- ", texto.strip())

    lineas = texto.split('\n')
    resultado = []
    en_lista = False

    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("-"):
            if not en_lista:
                resultado.append("<ul>")
                en_lista = True
            resultado.append(f"<li>{linea[1:].strip()}</li>")
        else:
            if en_lista:
                resultado.append("</ul>")
                en_lista = False
            if linea:
                resultado.append(f"<p>{linea}</p>")

    if en_lista:
        resultado.append("</ul>")

    return "\n".join(resultado)

if __name__ == "__main__":
    app.run(debug=True)
