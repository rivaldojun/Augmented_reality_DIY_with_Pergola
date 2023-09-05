import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

import datetime

# Entrée des commandes et de leurs dates
# commandes = [
#     {"date": "2022-04-01", "produits": {"A": 10, "B": 20, "C": 30, "D": 40, "E": 50, "F": 60}},
#     {"date": "2022-04-02", "produits": {"A": 15, "B": 25, "C": 35, "D": 45, "E": 55, "F": 65}},
#     {"date": "2022-04-03", "produits": {"A": 20, "B": 30, "C": 40, "D": 50, "E": 60, "F": 70}},
#     {"date": "2022-04-04", "produits": {"A": 25, "B": 35, "C": 45, "D": 55, "E": 65, "F": 75}},
#     {"date": "2022-04-05", "produits": {"A": 30, "B": 40, "C": 50, "D": 60, "E": 70, "F": 80}},
#     {"date": "2022-04-06", "produits": {"A": 35, "B": 45, "C": 55, "D": 65, "E": 75, "F": 85}},
#     {"date": "2022-04-07", "produits": {"A": 40, "B": 50, "C": 60, "D": 70, "E": 80, "F": 90}},
#     # {"date": "2022-04-08", "produits": {"A": 45, "B": 55, "C": 65, "D": 75, "E": 85, "F": 95}},
#     # {"date": "2022-04-09", "produits": {"A": 10, "B": 20, "C": 30, "D": 40, "E": 50, "F": 60}},
#     # {"date": "2022-04-10", "produits": {"A": 15, "B": 25, "C": 35, "D": 45, "E": 55, "F": 65}},
#     # {"date": "2022-04-11", "produits": {"A": 20, "B": 30, "C": 40, "D": 50, "E": 60, "F": 70}},
#     # {"date": "2022-04-12", "produits": {"A": 25, "B": 35, "C": 45, "D": 55, "E": 65, "F": 75}},
#     # {"date": "2022-04-13", "produits": {"A": 30, "B": 40, "C": 50, "D": 60, "E": 70, "F": 80}},
#     # {"date": "2022-04-14", "produits": {"A": 35, "B": 45, "C": 55, "D": 65, "E": 75, "F": 85}},
#     # {"date": "2022-04-15", "produits": {"A": 40, "B": 50, "C": 60, "D": 70, "E": 80, "F": 90}},
#     # {"date": "2022-04-16", "produits": {"A": 45, "B": 55, "C": 65, "D": 75, "E": 85, "F": 95}},
#     #  {"date": "2022-04-17", "produits": {"A": 10, "B": 20, "C": 30, "D": 40, "E": 50, "F": 60}},
#     # {"date": "2022-04-18", "produits": {"A": 15, "B": 25, "C": 35, "D": 45, "E": 55, "F": 65}},
#     # {"date": "2022-04-19", "produits": {"A": 20, "B": 30, "C": 40, "D": 50, "E": 60, "F": 70}},
#     # {"date": "2022-04-20", "produits": {"A": 25, "B": 35, "C": 45, "D": 55, "E": 65, "F": 75}},
#     # {"date": "2022-04-21", "produits": {"A": 30, "B": 40, "C": 50, "D": 60, "E": 70, "F": 80}},
#     # {"date": "2022-04-22", "produits": {"A": 35, "B": 45, "C": 55, "D": 65, "E": 75, "F": 85}},
#     # {"date": "2022-04-23", "produits": {"A": 40, "B": 50, "C": 60, "D": 70, "E": 80, "F": 90}},
#     # {"date": "2022-04-24", "produits": {"A": 45, "B": 55, "C": 65, "D": 75, "E": 85, "F": 95}},
#     #  {"date": "2022-04-25", "produits": {"A": 10, "B": 20, "C": 30, "D": 40, "E": 50, "F": 60}},
#     # {"date": "2022-04-26", "produits": {"A": 15, "B": 25, "C": 35, "D": 45, "E": 55, "F": 65}},
#     # {"date": "2022-04-27", "produits": {"A": 20, "B": 30, "C": 40, "D": 50, "E": 60, "F": 70}},
#     # {"date": "2022-04-28", "produits": {"A": 25, "B": 35, "C": 45, "D": 55, "E": 65, "F": 75}},
#     # {"date": "2022-04-29", "produits": {"A": 30, "B": 40, "C": 50, "D": 60, "E": 70, "F": 80}},
#     # {"date": "2022-04-30", "produits": {"A": 35, "B": 45, "C": 55, "D": 65, "E": 75, "F": 85}},
# ]
def predire(commandes):
# Initialisation des ensembles de données
    donnees = {}

    # Conversion des dates en objets datetime pour les manipuler plus facilement
    for commande in commandes:
        date_commande = datetime.datetime.strptime(commande["date"], "%Y-%m-%d")
        semaine_commande = date_commande.isocalendar()[1]  # Récupération du numéro de semaine de l'année
        if semaine_commande not in donnees:
            donnees[semaine_commande] = []
        donnees[semaine_commande].append(commande["produits"])

    # Calcul des ventes pour chaque semaine
    ventes_par_semaine = []
    for semaine, commandes in donnees.items():
        ventes = [0] * len(commandes[0])
        for commande in commandes:
            for i, quantite in enumerate(commande.values()):
                ventes[i] += quantite
        ventes_par_semaine.append(ventes)

    # Transformation des ventes en un tableau numpy pour l'entraînement du modèle LSTM
    ventes = np.array(ventes_par_semaine)

    # print(ventes)
    # Ventes des articles pour la semaine courante (dont on ne se sert pas)
    ventes_courante = np.array([50, 60, 70, 80, 90, 100])

    # Nombre d'étapes de temps pour l'entraînement du modèle
    n_steps = 1

    # Préparation des données d'entraînement pour le modèle LSTM
    X_train, y_train = [], []
    for i in range(n_steps, ventes.shape[0]):
        X_train.append(ventes[i-n_steps:i, :])
        y_train.append(ventes[i, :])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Création du modèle LSTM
    inputs = Input(shape=(n_steps, ventes.shape[1]))
    x = LSTM(32, activation='relu')(inputs)
    outputs = Dense(ventes.shape[1])(x)
    model = Model(inputs=inputs, outputs=outputs)

    # Fonction de récompense (reward) pour le renforcement learning
    def reward(y_true, y_pred):
        return tf.keras.losses.mean_squared_error(y_true, y_pred)

    # Compilation du modèle avec l'algorithme d'optimisation Adam et la fonction de récompense définie précédemment
    model.compile(optimizer=Adam(), loss=reward)

    # Entraînement du modèle avec le renforcement learning
    model.fit(X_train, y_train, epochs=100, verbose=0)

    # Prédiction des ventes des 6 articles pour la semaine suivante
    ventes_prevues = model.predict(np.array([X_train[-1, :, :]]))
    # print("La semaine prochaine, on vendra :", ventes_prevues[0])
    return ventes_prevues[0]

