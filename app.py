from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)


#CONFIG VALUES FOR MYTSQL
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_ADDON_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_ADDON_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_ADDON_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_ADDON_DB")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #PARA MOSTRAR DATOS EN FORMATO DICCIONARIO

#TABLE tarea
mysql =MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tarea(
                        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        description VARCHAR(255) NOT NULL,
                        estado VARCHAR(100) DEFAULT 'pendiente'
                    );
                    """)
    mysql.connection.commit()
    print("TABLA CREADA !!!")
    cursor.close()
    context ={
        'status' : True, 
        'content' : '',
        'message' : 'Bienvenido a mi apirest con Flask'
    }
    return jsonify(context)

@app.route('/tarea')
def getTarea() :
    cursor = mysql.connection.cursor()
    cursor.execute("select id,description,estado from tarea")
    data = cursor.fetchall()
    print(data)
    context = {
        'status':True,
        'content':data
    }
    return jsonify(context)

@app.route('/tarea',methods=['POST'])
def setTarea():
    description = request.json['description']

    cursor = mysql.connection.cursor()
    cursor.execute("""
                    insert into tarea(description)
                    values('"""+description+"""');  
                  """)
    mysql.connection.commit()
    cursor.close()

    context = {
        'status' : True,
        'content' : '',
        'message' : 'registro exitoso'}
    
    return jsonify(context)

@app.route('/tarea/<id>')
def getTareaById(id):
    cursor = mysql.connection.cursor()
    cursor.execute("select id,description,estado from tarea where id='"+id+"'")
    data = cursor.fetchall()
    cursor.close()

    context = {
        'status' : True,
        'content' : data
    }

    return jsonify(context)


@app.route('/tarea/<id>',methods=['PUT'])
def updateTareaById(id):
    description = request.json['description']
    estado = request.json['estado']
    cursor = mysql.connection.cursor()

    cursor.execute("update tarea set description = '"+description+"', estado = '"+estado+"' where id='"+id+"'")

    mysql.connection.commit()
    cursor.close()

    context = {
        'status' : True,
        'content' : '',
        'message' : 'registro actualizado'
    }

    return jsonify(context)

@app.route('/tarea/<id>',methods=['DELETE'])
def deleteTareaById(id):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from tarea where id='"+id+"'")
    mysql.connection.commit()
    cursor.close()

    context={
        'status' :  True,
        'content' : '',
        'message' : 'registro Eliminado'
    }
    return jsonify(context)

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
