import json
import os

class ProjetManager:
    def __init__(self, chemin_db="database.json"):
        self.chemin_db = chemin_db
        if not os.path.exists(self.chemin_db):
            with open(self.chemin_db, 'w') as f:
                json.dump({}, f)
        self._charger()

    def _charger(self):
        with open(self.chemin_db, 'r') as f:
            self.donnees = json.load(f)

    def _sauver(self):
        with open(self.chemin_db, 'w') as f:
            json.dump(self.donnees, f, indent=4)

    def creer_projet(self, pseudo, nom, description="", pays="", ville=""):
        self._charger()
        if pseudo not in self.donnees:
            self.donnees[pseudo] = {}
        if nom in self.donnees[pseudo]:
            return False, "Projet déjà existant."
        self.donnees[pseudo][nom] = {
            "description": description,
            "pays": pays,
            "ville": ville,
            "resultats": {}
        }
        self._sauver()
        return True, "Projet créé."

    def lister_projets(self, pseudo):
        self._charger()
        return list(self.donnees.get(pseudo, {}).keys())

    def maj_resultats(self, pseudo, projet, resultats):
        self._charger()
        self.donnees[pseudo][projet]["resultats"] = resultats
        self._sauver()

    def get_resultats(self, pseudo, projet):
        self._charger()
        return self.donnees.get(pseudo, {}).get(projet, {}).get("resultats", {})
