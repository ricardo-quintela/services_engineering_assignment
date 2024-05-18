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
    
    # Executing SQL queries
    # lista: [['a', 'a', 10, 'a', 'a']]
    valores = connection.run(f"INSERT INTO CONSULTAS (username, data_appoitment, hora, especialidade, medico, estado) VALUES ('{user}', '{data}', {hora}, {especialidade}, '{medico}', 'Não Pago')")
    valores = connection.run(f"INSERT INTO MEDICOS (medico, data_appoitment, hora) VALUES ('{medico}', '{data}', {hora})")

    # Closing the cursor
    connection.close()
    
    # TODO implement
    return {
        'statusCode': 200,
    }

