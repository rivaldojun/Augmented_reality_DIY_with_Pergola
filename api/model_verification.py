import os
import json
current_dir = os.getcwd()
MODELS_FILE =os.path.join(current_dir,"static","json","models.json")


def get_existing_model(matrice, height, color, type):
    """
    Recherche un modèle existant qui correspond aux paramètres donnés.
    Si un modèle existe, retourne le nom du fichier. Sinon, retourne None.
    """
    with open(MODELS_FILE,'r+') as f:
        models_data = json.load(f)
        for model in models_data:
                model=models_data[model]
                if (model['color'] == color and
                        model['height'] == height and
                        model['type'] == type and
                        model['matrice'] == matrice):

                    return model["fbx_path"]
        return None

def add_model(matrice, height, color, type, filename,fbx_path):
    """
    Ajoute un modèle à la liste des modèles dans le fichier JSON.
    """
    
    with open(MODELS_FILE, "r+") as f:
        models = json.load(f)
    entree={
            "matrice": matrice,
            "height": height,
            "color": color,
            "type": type,
            "fbx_path": fbx_path
        }
    models[filename]=entree
    with open(MODELS_FILE, "r+") as f:
        f.seek(0)
        json.dump(models, f)