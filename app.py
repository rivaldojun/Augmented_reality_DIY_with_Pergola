from flask import Flask, render_template,request,jsonify,session,redirect,url_for,make_response,send_file
from api.edge import detection_de_bord
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func,and_
import numpy as np
import os
import subprocess
import datetime
from api.model_verification import get_existing_model,add_model
from api.optimisation import optimize,Item,Panel,Params
from api.prediction_de_ventes import predire
app = Flask(__name__)
app.secret_key = '123'

current_dir = os.getcwd()
# activate_this = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'activate_this.py')
# exec(open(activate_this).read())


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    age=db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    commandes = db.relationship("Commande", backref="client")

    def __repr__(self):
        return f'<User {self.username}>'
    


class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    statut = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False,default='Pas disponible')
    produits = db.relationship("CommandeProduit", backref="commande")
    adresse = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    date_com = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    montant = db.Column(db.Float)

    def mettre_a_jour_montant(self, nouveau_montant):
        self.montant = nouveau_montant
        db.session.commit()
    def valider_commande(self):
        self.statut = "valide"
        db.session.commit()

    def is_deliver(self):
        self.statut = "Livree"
        db.session.commit()
    def is_availible(self):
        self.state = "Disponible"
        db.session.commit()
    def en_cours(self):
        self.state = "En cours"
        db.session.commit()

    def __repr__(self):
        return f"<Commande {self.id}>"

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    width=db.Column(db.Float, nullable=True,default=0)
    height=db.Column(db.Float, nullable=True,default=0)
    couleur=db.Column(db.String(50), nullable=True,default="")
    def __repr__(self):
        return f"<Produit {self.nom}>"


class visiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    action = db.Column(db.String(50), unique=False, nullable=False,default="simple visite")
    date_visit = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    def mettre_a_jour_action(self):
        self.action = "Achat"
        db.session.commit()
    def __repr__(self):
        return f"<Produit {self.id}>"
    

class CommandeProduit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'))
    quantite = db.Column(db.Integer)
    couleur_c=db.Column(db.String(50))
    produit = db.relationship("Produit")

    def __repr__(self):
        return "<CommandeProduit(commande_id='%s', produit_id='%s', quantite='%s')>" % (
                                self.commande_id, self.produit_id, self.quantite)


with app.app_context():
  db.create_all()


@app.route('/dashboard/<int:client_id>')
def dashboard(client_id):
    # Récupérer l'utilisateur correspondant à l'ID donné
    utilisateur = User.query.get(client_id)
    # Récupérer toutes les commandes pour cet utilisateur
    commandes = utilisateur.commandes
    # Pour chaque commande, récupérer les produits associés et afficher leurs noms
    return render_template('dashboard.html', client=utilisateur, commandes=commandes)



@app.route('/register',methods=['GET', 'POST'])
def register():
    text=""
    textmdp=""
    if request.method == 'POST':
        
        username = request.form['username']
        email = request.form['email']
        age=request.form['age']
        password=request.form['password']
        passwordconf=request.form['Confirm password']
        session['email'] = email
        if username!='admin' and email!="":

            if password==passwordconf:
                password = generate_password_hash(request.form['password'])
                user = User(username=username, email=email,age=age, password=password)

                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                textmdp="Les mot de passe ne correspondent pas"
        else:
            text="Username deja utilise"
         
    text=text + ' '+ textmdp

            
    return render_template('register.html',text=text)

@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
    text=""
    if request.method == 'POST':
        username = request.form['username']
        
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user :
            if check_password_hash(user.password, password):
                session['username'] = username
                session['client_id'] = user.id
                v=visiteur(username=username,email=user.email)
                db.session.add(v)
                db.session.commit()
                session['visit']=int(v.id)
                return redirect(url_for('choix'))
                
            else:
                text='Invalid password'
            
        else:
            text='Invalid username'
    return render_template('login.html',text=text)



@app.route('/accueil', methods=['GET', 'POST'])
def choix():
    if request.method == 'POST':
        data = request.get_json()
        color = data['color']
        session['color']=color
        height = data['height']
        type=data['type']
        matrice=data['matrix']
        produits = [    {'nom': 'Joint de fixation', 'prix': 10,'width':20,'height':12},    {'nom': 'Joint a 3 entres', 'prix': 10,'width': 30,'height': 40},    {'nom': 'Joint a 4 entres', 'prix': 10,'width': 36,'height': 50},    {'nom': 'Joint a 5 entres', 'prix': 10,'width' :40,'height':57},    {'nom': 'Paquets de vis', 'prix':4,'width':0,'height':0},    {'nom': 'Voile', 'prix':10 ,'width':0,'height':0,'couleur':color}]
        for produit_info in produits:
            if not Produit.query.filter_by(nom=produit_info['nom']).first():
                produit = Produit(nom=produit_info['nom'], prix=produit_info['prix'],width=produit_info['width'],height=produit_info['height'])
                db.session.add(produit)
                
        db.session.commit()
        col=color
        color=os.path.join(current_dir,"api",col+".jpg")
        c=np.sum(matrice)
        _3entr,_4entr,_5entr=detection_de_bord(matrice)
        session['height']=int(height)
        session['_3entr'] = int(_3entr)
        session['_4entr'] = int(_4entr)
        session['_5entr'] = int(_5entr)
        session['type'] = type
        session['toit']=int(c)
        supp=_3entr+_4entr+_5entr
        nbvis=4*(3*_3entr+4*_4entr+5*_5entr+supp)+supp*4
        nbre_bois=int((2*_3entr+3*_4entr+4*_5entr)/2)
        session['supp']=int(supp)
        session['nbvis']=int(nbvis)
        session['nbre_bois']=int(nbre_bois)

        
         # Création du modèle FBX
        filename = "model_{}_{}_{}_{}.glb".format(height, col, type,matrice)
        fbx_path=os.path.join(current_dir,"static","model",filename)
        filenames = fbx_path.split('\\')[-1]
        filenames="static/model/{}".format(filenames)
        session['fbx']=filenames
        

        existing_model_filename = get_existing_model(matrice, height, col, type)
        if(existing_model_filename==None):
            add_model(matrice, height, col, type, filename,fbx_path)
            blender_path = os.path.join(os.getenv("PATH"), "blender", "blender.exe")
            p=subprocess.Popen([blender_path,"--background","--python",os.path.join(os.getcwd(), "generation.py"),"--", "construire", str(matrice), fbx_path,str(type),color,str(height)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            
        else:
            
            print("Le model existe deja")
            
        return redirect(url_for('result'))
    
    return render_template('choisir.html')
   
@app.route('/result', methods=['GET', 'POST'])
def result():
   
    _3entr = session.get('_3entr')
    _4entr = session.get('_4entr')
    _5entr = session.get('_5entr')
    toit=session.get('toit')
    supp=session.get('supp')
    nbvis=session.get('nbvis')
    nbre_bois=session.get('nbre_bois')
    type=session.get('type')
    color=session.get('color')
    if type=="ouvert":
            nbre_bois=nbre_bois+3*toit
            c=0
    else:
        c=toit
    produits = [    {'nom': 'Joint de fixation', 'prix': 10,'quantite':supp},    {'nom': 'Joint a 3 entres', 'prix': 10,'quantite':_3entr},    {'nom': 'Joint a 4 entres', 'prix': 10,'quantite':_4entr},    {'nom': 'Joint a 5 entres', 'prix': 10,'quantite':_5entr},    {'nom': 'Paquets de vis', 'prix':4/20 ,'quantite':nbvis},    {'nom': 'Voile', 'prix':10,'quantite':c ,'couleur':color}]
    montant_total = 0
    for produit in produits:
        montant_produit = produit['quantite'] * produit['prix']
        montant_total += montant_produit
    return render_template('List_mat.html',fix=supp ,_3entr=_3entr, _4entr=_4entr, _5entr=_5entr,supp=supp,bois=nbre_bois,vis=nbvis,toit=c,montant=montant_total)

@app.route('/execute_script',methods=['POST'])
def execute_script():
        client_id = session.get("client_id")
        statut = "en attente"
        _3entr = session.get('_3entr')
        _4entr = session.get('_4entr')
        _5entr = session.get('_5entr')
        color=session.get('color')
        toit=session.get('toit')
        supp=session.get('supp')
        nbvis=session.get('nbvis')
        nbre_bois=session.get('nbre_bois')
        address = request.form['address']
        tel = request.form['tel']
        # Créer une nouvelle commande avec un statut par défaut de 'en attente'
        nouvelle_commande = Commande(client_id=client_id, statut=statut,adresse=address,telephone=tel)
        db.session.add(nouvelle_commande)
        db.session.commit()
        type=session.get('type')
        if(type=="ouvert"):
            qte=0
            color=" "
        else:
            qte=toit
        # Ajouter des produits à la commande
        produits = [    {'produit_id': 1, 'quantite': supp,'couleur':" "},    {'produit_id': 2, 'quantite': _3entr,'couleur':" "},    {'produit_id': 3, 'quantite': _4entr,'couleur':" "},    {'produit_id': 4, 'quantite': _5entr,'couleur':" "},    {'produit_id': 5, 'quantite':int(nbvis/20),'couleur':" "},    {'produit_id': 6, 'quantite': qte,'couleur':color}]
        montant=0
        for produit in produits:
            mon_produit = Produit.query.get(produit['produit_id'])  # Récupérer le produit avec l'id 1
            prix_du_produit = mon_produit.prix  # Obtenir le prix du produit
            montant=montant+produit['quantite']*prix_du_produit 
            commande_produit = CommandeProduit(commande=nouvelle_commande, produit_id=produit['produit_id'], quantite=produit['quantite'],couleur_c=produit['couleur'])
            db.session.add(commande_produit)
        nouvelle_commande.mettre_a_jour_montant(montant)
        db.session.commit()
        visit_id=session.get('visit')
        v=visiteur.query.get(visit_id)
        v.mettre_a_jour_action()
        db.session.commit()
        
        return render_template('good.html')

@app.route('/mescommandes')
def mescommandes():
    client_id = session.get("client_id")
    return redirect(url_for('dashboard', client_id=client_id))


@app.route('/visualiser')
def visualiser():
    height=session.get('height')
    fbx_path=session.get('fbx')
    return render_template("index.html",height=height,fbx_path=fbx_path)

if __name__ == '__main__':
    app.run()