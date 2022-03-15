import mysql.connector as mysql


# création d'une classe
class Connexion :
    __user = 'root'
    __password = 'root'
    __host = 'localhost'
    __port = '8081'
    __database = 'breizhibus'
    __cursor = None 

# méthode pour ouvrir la connexion à la bdd
    @classmethod
    def ouvrir_connexion(cls):
        if cls.__cursor == None :
            cls.__bdd = mysql.connect(user = cls.__user, password = cls.__password, host = cls.__host, port = cls.__port, database = cls.__database)
            cls.__cursor = cls.__bdd.cursor()




# insertion des futures méthodes

    @classmethod
    def select_lignes(cls):
        cls.ouvrir_connexion()
        query = "SELECT id_ligne FROM lignes"
        cls.__cursor.execute(query)
        result = cls.__cursor.fetchall()

        cls.fermer_connexion()
        return result

    @classmethod
    def select_id_bus(cls):
        cls.ouvrir_connexion()
        query = "SELECT id_bus FROM bus"
        cls.__cursor.execute(query)
        result = cls.__cursor.fetchall()

        cls.fermer_connexion()
        return result

    @classmethod
    def lister_lignes(cls):
        cls.ouvrir_connexion()

        query = "SELECT l.nom, a.nom, a.adresse  \
                FROM lignes l\
                JOIN arrets_lignes al ON al.id_ligne = l.id_ligne\
                JOIN arrets a ON al.id_arret = a.id_arret;"
        cls.__cursor.execute(query)
        result = cls.__cursor.fetchall()
        cls.fermer_connexion()
        return result
    
    # méthode pour retrouver tous les arrêts d'une ligne précise
    @classmethod
    def lister_arrets(cls, id_ligne):
        cls.ouvrir_connexion()

        query = "SELECT a.id_arret, a.nom, a.adresse, l.nom \
                 FROM lignes l \
                 JOIN arrets_lignes al ON al.id_ligne = l.id_ligne \
                 JOIN arrets a ON al.id_arret = a.id_arret \
                 WHERE l.id_ligne = %s ;"
        param = (id_ligne)
        cls.__cursor.execute(query, param)
        result = cls.__cursor.fetchall()
        cls.fermer_connexion()
        return result

    # méthode pour identifier l'utilisateur (identifiant + mdp)
    @classmethod
    def identifier(cls, pseudo_saisie, mdp_saisie):
        
        ok = False
        cls.ouvrir_connexion()
        query = "SELECT pseudo, mdp FROM utilisateurs WHERE pseudo = %s AND mdp = %s"
        vals = (pseudo_saisie, mdp_saisie)
        cls.__cursor.execute(query, vals)

        if cls.__cursor.fetchone() != None:
            ok = True

        cls.fermer_connexion()

        return ok
    # méthode pour ajouter un bus
    @classmethod
    def ajouter(cls, numero_saisie, immatriculation_bus, places_saisie, ligne_saisie):
        
        cls.ouvrir_connexion()

        query = "INSERT INTO bus (numero, immatriculation, nombre_place, id_ligne) VALUES (%s, %s, %s, %s)"
        param = (numero_saisie, immatriculation_bus, places_saisie, ligne_saisie)
        cls.__cursor.execute(query, param)
        cls.__bdd.commit()

        cls.fermer_connexion()
    


    # méthode pour modifier un bus
    @classmethod
    def modifier(cls, numero, immatriculation, ligne, id_bus, nombre_place):
        cls.ouvrir_connexion()

        cls.__cursor.execute(f"UPDATE bus SET numero = '{numero}', immatriculation = '{immatriculation}', nombre_place = '{nombre_place}', id_ligne = '{ligne}' WHERE id_bus = '{id_bus}'")
        cls.__bdd.commit()

        cls.fermer_connexion()


    # méthode pour supprimer un bus
    @classmethod
    def supprimer(cls, id_bus):
        cls.ouvrir_connexion()

        query = (f'DELETE FROM bus WHERE id_bus = "{id_bus}"')
        cls.__cursor.execute(query)
        cls.__bdd.commit()

        cls.fermer_connexion()


# méthode pour fermer la connexion à la bdd
    @classmethod
    def fermer_connexion(cls):
        cls.__cursor.close()
        cls.__bdd.close()
        cls.__cursor = None
