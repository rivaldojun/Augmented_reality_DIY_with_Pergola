from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db,User, Commande, Produit, visiteur, CommandeProduit
from flask import Flask, render_template,request,jsonify,session,redirect,url_for,make_response,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,and_
import numpy as np
from api.optimisation import optimize,Item,Panel,Params
from api.prediction_de_ventes import predire

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# Crée un contexte d'application pour le code dans ce fichier
app.app_context().push()

# Utilise la base de données définie dans app.py
db.init_app(app)

# Utilisation des modèles définis dans le fichier app.py
users = User.query.all()
commandes = Commande.query.all()
produits = Produit.query.all()
visiteurs = visiteur.query.all()
commande_produits = CommandeProduit.query.all()


@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
    text=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username=="admin" and password=="rivaldo" :
            return redirect (url_for('gestion'))
              
        else:
                text='Informations incorrectes'
            
    return render_template('login.html',text=text)

@app.route('/gestion')
def gestion():
    commande=Commande.query.all()
    return render_template('gestioncommande.html',commande=commande)


@app.route('/visiteur')
def visiteurs():
    visit=visiteur.query.all()
    return render_template('visiteur.html',visit=visit)

@app.route('/details/<int:command_id>')
def details(command_id):
    commande = Commande.query.get(command_id)
    return render_template('Detailcommande.html',commande=commande)

@app.route('/details_admin/<int:command_id>')
def details_adimn(command_id):
    commande = Commande.query.get(command_id)
    return render_template('detailscom_admin.html',commande=commande)

@app.route('/valider/<int:command_id>')
def valider(command_id):
    commande = Commande.query.get(command_id)
    commande.valider_commande()
    return redirect(request.referrer)

@app.route('/disponible/<int:command_id>')
def disponible(command_id):
    commande = Commande.query.get(command_id)
    commande.is_availible()
    return redirect(request.referrer)

@app.route('/livree/<int:command_id>')
def livree(command_id):
    commande = Commande.query.get(command_id)
    commande.is_deliver()
    return redirect(request.referrer)


@app.route('/filtre_valide')
def filtre_valide():
    commande = Commande.query.filter_by(statut='valide').order_by(Commande.date_com.asc()).all()
    return render_template('filtre_valide.html',commande=commande)

@app.route('/filtre_attente')
def filtre_attente():
    commande = Commande.query.filter_by(statut='en attente').order_by(Commande.date_com.asc()).all()

    return render_template('filtre_attente.html',commande=commande)
@app.route('/besoin')
def besoin():
    besoin=db.session.query(Produit.nom,Produit.width,Produit.height,func.sum(CommandeProduit.quantite).label('total_quantite')).join(CommandeProduit).join(Commande).filter(Commande.state == 'Pas disponible',and_(Commande.statut=='valide')).group_by(Produit.nom).all()
    return render_template('besoin.html',besoin=besoin)


@app.route('/coupe')
def plandecoupe():
    item=[]
    panel=[]
    k=1
    l=1
    p=Panel(l,200,200)
    l=l+1
    panel.append(p)
    

    besoin=db.session.query(Produit.nom,Produit.width,Produit.height,func.sum(CommandeProduit.quantite).label('total_quantite')).join(CommandeProduit).join(Commande).filter(Commande.state == 'Pas disponible',and_(Commande.statut=='valide')).group_by(Produit.nom).all()
    for nom_produit,width,height,total_quantite in besoin:
        if (width!=0 and height!=0):
            for j in range(total_quantite):
                item.append(Item(k,width,height,True,nom_produit))
                k=k+1
    params=Params(panel,item,2,False)
    sorti=optimize(params)
    while sorti=="pas possible":  
        p=Panel(l,200,200)
        l=l+1
        panel.append(p)
        params=Params(panel,item,2,False)
        sorti=optimize(params)
    cmd = Commande.query.filter(Commande.state == 'Pas disponible',and_(Commande.statut=='valide')).order_by(Commande.date_com.asc()).all()
    for com in cmd:
        com.en_cours()
    db.session.commit()
    return send_file('static/output.pdf', as_attachment=False)
    
@app.route('/pred')
def pred():
    commande = Commande.query.filter_by(statut='valide').all()
    commandes=[]
    for c in commande:
        date=c.date_com
        date = date.strftime('%Y-%m-%d')
        l=[]
        for list in c.produits:
            l.append((str(list.produit_id),list.quantite))
        prod=dict(l)
        com = {"date": date, "produits": prod}
        commandes.append(com)
    commander = [
    {"date": "2023-04-27", "produits": {"1": 10, "2": 27, "3": 13, "4": 13, "5": 10, "6": 12}},
    {"date": "2023-04-29", "produits": {"1": 30, "2": 21, "3": 14, "4": 13, "5": 37, "6": 10}},
    {"date": "2023-04-30", "produits": {"1": 16, "2": 17, "3": 17, "4": 11, "5": 42, "6": 12}},
    {"date": "2023-05-02", "produits": {"1": 27, "2": 16, "3": 12, "4": 13, "5": 45, "6": 13}},
    {"date": "2023-05-03", "produits": {"1": 11, "2": 29, "3": 14, "4": 12, "5": 41, "6": 12}},
    {"date": "2023-05-05", "produits": {"1": 27, "2": 12, "3": 14, "4": 12, "5": 44, "6": 11}},
    {"date": "2023-05-10", "produits": {"1": 36, "2": 27, "3": 17, "4": 13, "5": 52, "6": 10}},
    {"date": "2023-05-12", "produits": {"1": 39, "2": 16, "3": 12, "4": 14, "5": 48, "6": 12}},
    {"date": "2023-05-13", "produits": {"1": 32, "2": 29, "3": 14, "4": 12, "5": 44, "6": 11}},
    {"date": "2023-05-14", "produits": {"1": 33, "2": 18, "3": 14, "4": 15, "5": 37, "6": 12}},
    {"date": "2023-05-15", "produits": {"1": 34, "2": 16, "3": 17, "4": 10, "5": 46, "6": 13}},
    {"date": "2023-05-16", "produits": {"1": 39, "2": 14, "3": 22, "4": 11, "5": 45, "6": 11}},
    {"date": "2023-05-19", "produits": {"1": 10, "2": 29, "3": 24, "4": 14, "5": 41, "6": 14}},
    {"date": "2023-05-25", "produits": {"1": 35, "2": 30, "3": 26, "4": 13, "5": 44, "6": 13}},
    {"date": "2023-05-26", "produits": {"1": 34, "2": 10, "3": 25, "4": 12, "5": 43, "6": 13}},
    {"date": "2023-05-27", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-02", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-07", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-07", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}}
    ,{"date": "2023-06-08", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-09", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-10", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-12", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}},
    {"date": "2023-06-17", "produits": {"1": 33, "2": 14, "3": 24, "4": 12, "5": 45, "6": 20}}]
    for m in commander:
        commandes.append(m)
  
    p=predire(commandes=commandes)
    
   
    session['pred']=p.tolist()
    return render_template("prediction.html",p=p)

@app.route('/coupe_pred')
def plandecoupe_pred():
    item=[]
    panel=[]
    k=1
    l=1
    p=Panel(l,200,200)
    l=l+1
    panel.append(p)
    pred=session.get('pred',[])
    for ind,total_quantite in enumerate(pred):
        print(ind)
        print(total_quantite)
        if (ind==0):
            nom_produit='Joint de fixation'
            width=20
            height=12
        if (ind==1):
            nom_produit='Joint a 3 entres'
            width=30
            height=40
        if (ind==2):
            nom_produit='Joint a 4 entres'
            width=36
            height=50
        if (ind==3):
            nom_produit='Joint a 5 entres'
            width=40
            height=57
        if ind==0 or ind==1 or ind==2 or ind==3:

            for j in range(int(total_quantite)):
                
                    item.append(Item(k,width,height,True,nom_produit))
                    k=k+1
    params=Params(panel,item,2,False)
    sorti=optimize(params)
    while sorti=="pas possible":  
        p=Panel(l,200,200)
        l=l+1
        panel.append(p)
        params=Params(panel,item,2,False)
        sorti=optimize(params)
   
    return send_file('static/output.pdf', as_attachment=False)



if __name__ == '__main__':
    app.run()
