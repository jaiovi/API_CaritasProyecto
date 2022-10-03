from flask import Flask, jsonify, make_response, request, send_file
import json
import sys
import mysql.connector

import os

# Connect to MySQL dB from start
mysql_params = {}
mysql_params['DB_HOST'] = '100.80.80.6'
mysql_params['DB_NAME'] = 'base_datos_caritas'
mysql_params['DB_USER'] = 'caritas'
mysql_params['DB_password'] = 'MejorProyecto'

try:
    cnx = mysql.connector.connect(
        user=mysql_params['DB_USER'],
        password=mysql_params['DB_password'],
        host=mysql_params['DB_HOST'],
        database=mysql_params['DB_NAME'], 
        auth_plugin='mysql_native_password'
        )
except Exception as e:
    print("Cannot connect to MySQL server!: {}".format(e))
    sys.exit()

def module_path():
    import sys
    import os
    if (hasattr(sys, "frozen")):
        return os.path.dirname(sys.executable)
    if os.path.dirname(__file__) == "":
        return "."
    return os.path.dirname(__file__)


def mysql_connect():
    global mysql_params
    cnx = mysql.connector.connect(
        user=mysql_params['DB_USER'],
        password=mysql_params['DB_password'],
        host=mysql_params['DB_HOST'],
        database=mysql_params['DB_NAME'], 
        auth_plugin='mysql_native_password'
        )
    return cnx

def read_user_data(table_name, curpUsuarios):
    global cnx
    try:
        try:
            cnx.ping(reconnect=False, attempts=1, delay=3)
        except:
            cnx = mysql_connect()
        cursor = cnx.cursor(dictionary=True)
        #read = 'SELECT * FROM {} WHERE curpUsuarios = "{}"'.format(table_name, curpUsuarios)
        #cursor.execute(read)
        read = 'SELECT * FROM {} WHERE idUsuarios = %s'.format(table_name)
        #tabla = request.args.get('table_name')
        #curpcito = request.args.get('curpUsuarios')
        #table_name % curpUsuarios (tabla, curpcito)
        cursor.execute(read, (curpUsuarios,))
        a = cursor.fetchall()
        cnx.commit()
        cursor.close()
        return a
    except Exception as e:
        raise TypeError("read_user_data:%s" % e)


def mysql_read_where(table_name, d_where):
    global cnx
    try:
        try:
            cnx.ping(reconnect=False, attempts=1, delay=3)
        except:
            cnx = mysql_connect()
        cursor = cnx.cursor(dictionary=True)
        read = 'SELECT * FROM %s WHERE ' % table_name
        read += '('
        for k,v in d_where.items():
            if v is not None:
                if isinstance(v,bool):
                    v = int(v == True)
                    read += '%s = "%s" AND ' % (k,v)
                elif isinstance(v,str):
                    if '"' in v:
                        read += "%s = '%s' AND " % (k,v)
                    else:
                        read += '%s = "%s" AND ' % (k,v)
                else:
                    read += '%s = "%s" AND ' % (k,v)
            else:
                read += '%s is NULL AND ' % (k)
        # Remove last "AND "
        read = read[:-4]
        read += ')'
        #print(read)
        cursor.execute(read)
        a = cursor.fetchall()
        cnx.commit()
        cursor.close()
        return a
    except Exception as e:
        raise TypeError("mysql_read_where:%s" % e)


def mysql_insert_row_into(table_name, d):
    global cnx
    try:
        try:
            cnx.ping(reconnect=False, attempts=1, delay=3)
        except:
            cnx = mysql_connect()
        cursor = cnx.cursor()
        keys = ""
        values = ""
        data = []
        for k in d:
            keys += k + ','
            values += "%s,"
            if isinstance(d[k],bool):
                d[k] = int(d[k] == True)
            data.append(d[k])
        keys = keys[:-1]
        values = values[:-1]
        insert = 'INSERT INTO %s (%s) VALUES (%s)'  % (table_name, keys, values)
        #print(insert)
        #print(data)
        a= cursor.execute(insert,data)
        id_new = cursor.lastrowid #me va a devolver el id autogenerado del registro
        cnx.commit()
        cursor.close()
        return id_new
    except Exception as e:
        raise TypeError("mysql_insert_row_into:%s" % e)


def mysql_update_where(table_name, d_field, d_where):
    global cnx
    try:
        try:
            cnx.ping(reconnect=False, attempts=1, delay=3)
        except:
            cnx = mysql_connect()
        cursor = cnx.cursor()
        update = 'UPDATE `%s` SET ' % table_name
        for k,v in d_field.items():
            if v is None:
                update +='`%s` = NULL, ' % (k)
            elif isinstance(v,bool):
                update +='`%s` = %s, ' % (k,int(v == True))
            elif isinstance(v,str):
                if '"' in v:
                    update +="`%s` = '%s', " % (k,v)
                else:
                    update +='`%s` = "%s", ' % (k,v)
            else:
                update +='`%s` = %s, ' % (k,v)
        # Remove last ", "
        update = update[:-2]
        update += ' WHERE ( '
        for k,v in d_where.items():
            if v is not None:
                if isinstance(v,bool):
                    v = int(v == True)
                elif isinstance(v,str):
                    if '"' in v:
                        update += "%s = '%s' AND " % (k,v)
                    else:
                        update += '%s = "%s" AND ' % (k,v)
                else:
                    update += '%s = %s AND ' % (k,v)
            else:
                update += '%s is NULL AND ' % (k)
        # Remove last "AND "
        update = update[:-4]
        update += ")"
        #print(update)
        a = cursor.execute(update)
        cnx.commit()
        cursor.close()
        return a
    except Exception as e:
        raise TypeError("mysql_update_where:%s" % e)

def mysql_delete_where(table_name, d_where):
    global cnx
    try:
        try:
            cnx.ping(reconnect=False, attempts=1, delay=3)
        except:
            cnx = mysql_connect()
        cursor = cnx.cursor()
        delete = 'DELETE FROM %s ' % table_name
        delete += ' WHERE ( '
        for k,v in d_where.items():
            if v is not None:
                if isinstance(v,bool):
                    v = int(v == True)
                elif isinstance(v,str):
                    if '"' in v:
                        delete += "%s = '%s' AND " % (k,v)
                    else:
                        delete += '%s = "%s" AND ' % (k,v)
                else:
                    delete += '%s = "%s" AND ' % (k,v)
            else:
                delete += '%s is NULL AND ' % (k)
        # Remove last "AND "
        delete = delete[:-4]
        delete += ")"
        #print(delete)
        a = cursor.execute(delete)
        cnx.commit()
        cursor.close()
        return a
    except Exception as e:
        raise TypeError("mysql_delete_where:%s" % e)


app = Flask(__name__)

##ESTANDAR DE TODOS 
@app.route("/hello")
def hello():
    return "Caritas de Monterrey!\n"

@app.route("/docker_logo")
def docker_logo():
    my_path =  module_path()
    fname = "{}/dockerBlue.png".format(my_path)
    return send_file(fname, as_attachment=False)

@app.route("/usuario") #### BUSQUEDA POR ID
def user():
    idUsuarios = request.args.get('idUsuarios', None)
    d_user = read_user_data('usuarios', idUsuarios)
    return make_response(jsonify(d_user))

@app.route("/usuarios/crear", methods=['POST']) # Crear usuario general "/crud/create"
def crud_create():
    d = request.json
    idUser = mysql_insert_row_into('usuarios', d)
    return make_response(jsonify(idUser))

@app.route("/usuarios/login", methods=['GET']) # BUSQUEDA DE EMAIL /crud/read
def crud_read():
    idUsuarios = request.args.get('emailUsuarios', None)
    #curpUsuarios = request.args.get('curpUsuarios', None)
    d_user = mysql_read_where('usuarios', {'emailUsuarios': idUsuarios})
    return make_response(jsonify(d_user))

@app.route("/usuarios/actualizarContra", methods=['PUT']) ##ACTUALIZAR LA CONTRASEÑA /crud/update
def crud_update():
    d = request.json
    d_field = {'passUsuarios': d['passUsuarios']}
    d_where = {'emailUsuarios': d['emailUsuarios']} #antes era id
    mysql_update_where('usuarios', d_field, d_where)
    return make_response(jsonify('ok'))


@app.route("/crud/delete", methods=['DELETE'])
def crud_delete():
    d = request.json
    d_where = {'idUsuarios': d['idUsuarios']}
    mysql_delete_where('usuarios', d_where)
    return make_response(jsonify('ok'))


## PERSONALIZADO
@app.route("/voluntarios/create", methods=['POST'])
def voluntarios_create():
    d = request.json
    idUser = mysql_insert_row_into('voluntarios', d)
    return make_response(jsonify(idUser))

@app.route("/admin/create", methods=['POST'])
def admin_create():
    d = request.json
    idUser = mysql_insert_row_into('admin', d)
    return make_response(jsonify(idUser))

@app.route("/usuarios/eliminar", methods=['DELETE'])
def usuarios_delete():
    d = request.json
    d_where = {'idUsuarios': d['idUsuarios']}
    mysql_delete_where('usuarios', d_where)
    return make_response(jsonify('ok'))
    

## AñADIDO PARA VALIDAR SSL
API_CERT = '{}/.SSL/equipo05.tc2007b.tec.mx.cer'.format(module_path())
API_KEY = '{}/.SSL/equipo05.tc2007b.tec.mx.key'.format(module_path())
CA = '{}/.SSL/ca.tc2007b.tec.mx.cer'.format(module_path())

if __name__ == '__main__':
    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_verify_locations(CA)
    context.load_cert_chain(API_CERT, API_KEY)
    app.run(host='0.0.0.0', port=10210, ssl_context=context, debug=True)
