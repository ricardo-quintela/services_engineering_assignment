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
    
    # Executing SQL queries
    # lista: [['a', 'a', 10, 'a', 'a']]
    valores = connection.run("SELECT * FROM Consultas")

    # Closing the cursor
    connection.close()
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(valores)
    }


connection = pg8000.native.Connection(
        host="clinic.chmlmnyewbda.us-east-1.rds.amazonaws.com", 
        port="5432", 
        user="postgres", 
        password="postgres", 
        database="Consultas"
    )
user = "a"
hora = "10"
data = "b"
especialidade = 10
medico = "aaaa"

# cursor = connection.cursor()
valores = connection.run(f"INSERT INTO CONSULTAS (username, data_appoitment, hora, especialidade, medico, estado) VALUES ('{user}', '{data}', {hora}, {especialidade}, '{medico}', 'Não Pago')")
valores = connection.run(f"INSERT INTO MEDICOS (medico, data_appoitment, hora) VALUES ('{medico}', '{data}', {hora})")
# connection.commit()
connection.close()
