import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, Any

app=FastAPI(title='FastAPI CRUD API')

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

db_dependency=Annotated[Any, Depends(get_db)]

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
def insert_students(db:db_dependency, id_estudiante:int, nombre_estudiante:str, apellido_estudiante:str, id_grado:int, seccion:str):
    try:
        cursor=db.cursor()
        cursor.execute(f"INSERT INTO estudiantes(id_estudiante, nombre_estudiante, apellido_estudiante, id_grado, seccion) VALUES ( '{id_estudiante}', '{nombre_estudiante}', '{apellido_estudiante}', '{id_grado}', '{ seccion}' )" )
        db.commit()
        return {'status': 'query inserted correctly'}
    except Error as e:
        return {'Error insertando valores:' : str(e)}

@app.get('/courses')
def show_courses(db:db_dependency):
    try:
        cursor=db.cursor()
        cursor.execute('SELECT nombre_curso, id_curso AS codigo_curso FROM cursos')
        rows= cursor.fetchall()
        return{'cursos:' : rows}
    except Error as e:
        return {'error': str(e)}


