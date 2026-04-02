import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated

app=FastAPI(title='FastAPI CRUD API')

def create_connection(host, user, password, database):
    try:
        conn=mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=database )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f'Error de conexion: {e}')

@app.post('/users')
def insert_students(db:db_dependency, id_estudiante, nombre_estudiante, apellido_estudiante, id_grado, seccion):
    try:
        db_conn=db.cursor()
        db_conn.execute('INSERT INTO estudiantes(id_estudiante, nombre_estudiante, apellido_estudiante, id_grado, seccion) VALUES (' + id_estudiante + nombre_estudiante+ apellido_estudiante+ id_grado + seccion + ');' )
        db_conn.commit()
        return {'status': 'query inserted correctly'}
    except Error as e:
        return {'Error insertando valores:' : str(e)}

@app.get('/courses')
def show_courses(db:db_dependency):
    try:
        db_conn=db.cursor()
        db_conn.execute('SELECT nombre_curso, id_curso AS codigo_curso FROM cursos')
        rows= db_conn.fetchall()
        return{'cursos:' : rows}
    except Error as e:
        return {'error': str(e)}

def get_db():
    host='10.10.10.26'
    user='user'
    password='katty2023'
    database='vuln_db'
    db=create_connection(host, user, password, database)
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
