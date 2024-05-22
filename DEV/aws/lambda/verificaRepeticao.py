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
    medico = event["medico"]
    
    user_id = connection.run(f"SELECT id from auth_user where username = '{user}'")
    user_id = user_id[0][0]
    
    # Executing SQL queries
    # lista: [['a', 'a', 10, 'a', 'a']]
    valores = connection.run(f"SELECT count(*) FROM CONSULTAS where user_id = '{user_id}' and data_appointment = '{data}' and hora = {hora};")
    
    if valores[0][0] > 0:
        response = "Já tem uma consulta nesse dia nessa hora"
        statusCode = 500
    else:
        valores = connection.run(f"SELECT count(*) FROM MEDICOS where medico = '{medico}' and data_appointment = '{data}' and hora = {hora};")
        
        if valores[0][0] > 0:
            response = "Médico ocupado"
            statusCode = 500
        else:
            response = "Okk"
            statusCode = 200
            
    # Closing the cursor
    connection.close()
    
    # TODO implement
    return {
        'statusCode': statusCode,
        'body': json.dumps(valores)
    }