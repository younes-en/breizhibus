from flask import Flask, render_template, request
from connexion import Connexion

app = Flask(__name__)

@app.route('/')
def index():
    ligne = Connexion.lister_lignes()
    return render_template('index.html', ligne = ligne)


@app.route('/client', methods = ['POST', 'GET'])
def client():
    lignes = Connexion.lister_lignes()
    return render_template("client.html", lignes = lignes)

@app.route('/arret/<int:id_ligne>')
def afficher_arrets(id_ligne):
    arrets= Connexion.lister_arrets(id_ligne)
    return render_template("arret.html", arrets=arrets)

@app.route('/identifier')
def identifier():
    
    return render_template("form_identifier.html")


@app.route('/autoriser', methods=['POST'])
def autoriser():
    pseudo_saisie = request.values.get("pseudo")
    mdp_saisie = request.values.get("mdp")
    oui = Connexion.identifier(pseudo_saisie, mdp_saisie)

    return render_template("identifier.html", qui = pseudo_saisie, reponse = oui)

@app.route('/autoriser/ajouter', methods = ['GET', 'POST'])
def ajouter():
    id_ligne_input = Connexion.select_lignes()

    if request.method == 'POST':
        immatriculation = request.values.get('immatriculation')
        numero = request.values.get('numero')
        nombre_place = request.values.get('nombre_place')
        id_ligne = request.values.get('id_ligne')

        print(immatriculation, numero, nombre_place, id_ligne)
        Connexion.ajouter(numero,immatriculation, nombre_place, id_ligne)
    return render_template("ajouter.html", id_ligne=id_ligne_input)


@app.route('/autoriser/modifier', methods = ['GET', 'POST'])
def modifier():
    id_bus = Connexion.select_id_bus()
    id_ligne = Connexion.select_lignes()

    if request.method == 'POST':
        immatriculation = request.values.get('immatriculation')
        numero = request.values.get('numero')
        nombre_place = request.values.get('nombre_place')
        id_ligne = request.values.get('id_ligne')
        id_bus = request.values.get('id_bus')

        print(immatriculation, numero, nombre_place, id_ligne, id_bus)
        Connexion.modifier(id_bus, numero, immatriculation, nombre_place, id_ligne)

    return render_template("modifier.html", id_bus=id_bus, id_ligne=id_ligne)

@app.route('/autoriser/supprimer', methods = ['GET', 'POST'])
def supprimer():

    if request.method == 'POST':
        id_bus = request.values.get('id_bus')
        Connexion.supprimer(id_bus)

    id_bus = Connexion.select_id_bus()
    return render_template("supprimer.html", id_bus=id_bus)


@app.route ('/formuler')
def formuler():
    return render_template("form_identifier.html")






if __name__ == "__main__":
    app.run(debug=True)
