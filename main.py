from flask import Flask, request, render_template, redirect
from pymongo import MongoClient

#-------------------- Conexiones a la BD -------------------------

def get_connection():
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client['crud']
    collection = db['placas']
    return collection

def read_db():
    data = get_connection()
    read = data.find()
    return read

app = Flask(__name__)

#--------------------------Index ----------------------

@app.route("/")
def index():
    return render_template("index.html")

#-------------------------Home------------------------------
    
@app.route("/home")
def home():
    return render_template("home.html")

#---------------------------Registro--------------------------------
    
@app.route("/registro")
def ret_registro():
    return render_template("registro.html")

    
#--------------------------Create-----------------------------------
@app.route("/create", methods=['GET', 'POST'])
def create():
    
    marca = request.args['marca']
    modelo = request.args['modelo']
    color = request.args['color']
    placa = request.args['placa']
    
    nombre = request.args['nombre']
    apellido = request.args['apellido']
    cedula = request.args['cedula']
    casa = request.args['casa']
    
    data = {"placa":str(placa), "marca":str(marca),"modelo":str(modelo), "color":str(color),
                   "nombre":str(nombre), "apellido":str(apellido), "cedula":str(cedula), "casa":str(casa),
                   "estado":True}
        
    post = get_connection()
    save = post.insert_one(data).inserted_id
    print(save)
    
    return render_template("mensaje.html", placa=placa)


#----------------------------Read-------------------------------
    
@app.route("/buscar")
def ret_buscar():
    
    response = [] 
    read = read_db()    
    for data in read:
        response.append(data)
    
    return render_template("buscar.html", response=response)


#----------------------------Update-------------------------------
    

@app.route('/update/<string:placa>', methods=['GET'])
def update(placa):
    return render_template('update.html',placa=placa)

@app.route('/update/<string:placa>/upt', methods=['GET','POST'])
def update_carro(placa):
    
    color = request.args['color']
    nombre = request.args['nombre']
    apellido = request.args['apellido']
    cedula = request.args['cedula']
    casa = request.args['casa']
    
    
    data = get_connection()
    data.update_one({"placa":placa}, {"$set":{"color":color, "nombre":nombre, "apellido":apellido, "cedula":cedula, "casa":casa}})
    
    return redirect('/buscar')

#----------------------------Delete-------------------------------
    

@app.route('/delete/<string:placa>', methods=['GET','POST'])
def delete_carro(placa):
    
    data = get_connection()
    data.update_one({"placa":placa}, {"$set":{"estado":False}})
    
    return redirect('/buscar')



    
if __name__ == '__main__':
    app.run(debug=True)