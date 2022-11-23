from flask import Flask
from flask import render_template,request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

app=Flask(__name__)
app.secret_key="daniel"
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)

    return render_template('sitio/index.html', libros=libros)

#Adjuntar la imagen a la tabla de datos de la Pagina web Adm
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)
#Adjuntar la imagen a la tabla de datos de la Pagina web Adm

#Acceder a la informacion de la hoja de estilo de CSS
@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'), archivocss)



@app.route('/libros')
def libros():
#Actualizar los productos o libros creados por el ADMIN en el sitio
    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)

    return render_template('sitio/libros.html', libros=libros)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/ropa')
def ropa():
    return render_template('sitio/ropa.html')

@app.route('/tecnologia')
def tecnologia():
    return render_template('sitio/tecnologia.html')

@app.route('/salud&belleza')
def salud_belleza():
    return render_template('sitio/salud&belleza.html')



@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

#DIRECCION INGRESO DE LOS ADMIN
@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')


@app.route('/admin/login', methods=['POST'])
def admin_login_post():

    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    #Con estos prints se imprime el usuario y password digitado por el admin en la pagina
    print(_usuario)
    print(_password)
    #Comparativa de datos

    #VALIDAR CON BD (if tabla usuarios where usuario= "admin" and password="123")
    if _usuario=="admin" and _password=="123":
        session["login"]=True
        session["usuario"]="Administrador"
        return redirect("/admin")

    return render_template("admin/login.html", mensaje="Acceso denegado")

@app.route('/admin/login/registro')
def admin_login_registro():
    return render_template('admin/registro.html')
#######
@app.route('/registro/guardar', methods=['POST'])
def registro_guardar():
    _nombre=request.form['txtNombreR']
    _apellido=request.form['txtApellidoR']
    _correo=request.form['txtCorreoR']
    _localComercial=request.form['txtLocalcomercialR']
    _ubicacion=request.form['txtUbicacionR']
    _producto= request.form['txtProductoR']
    _contraseña= request.form['txtPasswordR']

    sql= "INSERT INTO `administradores`(`ID`, `Nombre`, `Apellido`, `Email`, `LocalComercial`, `Ubicacion`, `Producto`, `Contraseña` ) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s);"
    datos=(_nombre,_apellido,_correo,_localComercial,_ubicacion,_producto,_contraseña)

    conexion= mysql.connect()
    cursor= conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_nombre)
    print(_apellido)
    print(_correo)
    print(_localComercial)
    print(_ubicacion)
    print(_producto)
    print(_contraseña)

    return redirect('/admin/login')
#####

#Direccion para cuadno el admin cierre sesion
@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')
#Direccion para cuadno el admin cierre sesion

@app.route('/admin/libros')
def admin_libros():

    #Bloqueo cuando se cierra sesion
    if not 'login' in session:
        return redirect("/admin/login")

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)

    return render_template('admin/libros.html', libros=libros)

@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():

    #Bloqueo cuando se cierra sesion
    if not 'login' in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _precioreal=request.form['txtPrecioreal']
    _preciodesc=request.form['txtPreciodesc']
    _finaldescuento=request.form['txtCulminacion']
    _archivo1=request.files['txtImagen1']
    _archivo2=request.files['txtImagen2']
    _url=request.form['txtURL']


#Adjuntar la imagen a la BD
    tiempo= datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo1.filename!="":
        nuevoNombre=horaActual+"_"+_archivo1.filename
        _archivo1.save("templates/sitio/img/"+nuevoNombre)
    
    if _archivo2.filename!="":
        nuevoNombre2=horaActual+"_"+_archivo2.filename
        _archivo2.save("templates/sitio/img/"+nuevoNombre2)
#Adjuntar la imagen a la BD


    sql= "INSERT INTO `libros` (`ID`, `Nombre`, `Precio-real`,`Precio-descuento`,`Final-descuento`,`Imagen-1ra`,`Imagen-2da`, `url`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s);"
    datos=(_nombre,_precioreal,_preciodesc,_finaldescuento,nuevoNombre,nuevoNombre2,_url)


    conexion= mysql.connect()
    cursor= conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_nombre)
    print(_precioreal)
    print(_preciodesc)
    print(_finaldescuento)
    print(_archivo1)
    print(_archivo2)
    print(_url)
    return redirect('/admin/libros')
    
#REDIRECCIONAMIENTO PARA CUANDOS SE BORRE UN DATO DE LA BD
@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():

    #Bloqueo cuando se cierra sesion
    if not 'login' in session:
        return redirect("/admin/login")

    _id=request.form['txtID']
    print(_id)
#Aqui busca la imagen y la almacena en libros
    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT imagen FROM `libros` WHERE id=%s",(_id))
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)
#Aqui busca la imagen
#Validar si existe la imagen para borrarla en la bd
    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
        os.unlink("templates/sitio/img/"+str(libro[0][0]))
#Validar si existe la imagen para borrarla

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s",(_id))
    conexion.commit()

    return redirect('/admin/libros')


if __name__ == '__main__':
    app.run(debug=True)