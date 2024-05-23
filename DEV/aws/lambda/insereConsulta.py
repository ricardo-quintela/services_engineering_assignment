import pg8000.native
import json


def lambda_handler(event, context):
    
    # Building the database connection
    connection = pg8000.native.Connection(
        host="clinic.chmlmnyewbda.us-east-1.rds.amazonaws.com", 
        port="5432", 
        user="postgres", 
        password="postgres", 
        database="Consultas"
    )
    
    user = event["cliente"]
    data = event["data"]
    hora = event["hora"]
    especialidade = event["especialidade"]
    medico = event["medico"]
    estado = event["estado"]
    
    user_id = connection.run(f"SELECT id from auth_user where username = '{user}'")
    user_id = user_id[0][0]
    
    # Executing SQL queries
    # lista: [['a', 'a', 10, 'a', 'a']]
    valores = connection.run(f"INSERT INTO CONSULTAS (user_id, data_appointment, hora, especialidade, medico, estado) VALUES ({user_id}, '{data}', {hora}, {especialidade}, '{medico}', '{estado}')")
    valores = connection.run(f"INSERT INTO MEDICOS (medico, data_appointment, hora) VALUES ('{medico}', '{data}', {hora})")

    # Closing the cursor
    connection.close()
    
    # TODO implement
    return {
        'statusCode': 200,
    }
