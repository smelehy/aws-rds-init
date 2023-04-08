import os
import sys
import pymysql
import json
from pprint import pprint 
import boto3
from botocore.exceptions import ClientError

def get_secret(sname,sregion):

    secret_name = sname 
    region_name = sregion 
    # Create a Secrets Manager client
    session     = boto3.session.Session()
    client   = session.client(
        service_name = 'secretsmanager',
        region_name  = region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId              = secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    pprint(get_secret_value_response)
    secret = get_secret_value_response['SecretString']
    return secret

dbsecrets = json.loads(get_secret('rds!db-065d633a-5436-4451-9248-d79bc059450a','us-east-2'))
print('********************* dbsecrets *********************')
pprint(dbsecrets)
print('***************************************************')
#dbparams  = json.loads(get_secret('hlw-db1-credentials','us-east-2'))
#pprint(dbparams)
#print('*****************************')
rds_host  = 'hlw-database-1.csmymcm2btd4.us-east-2.rds.amazonaws.com'
#rds_host  = dbparams.get('host')
name      = dbsecrets.get('username')
password  = dbsecrets.get('password')
#db_name   = dbparams.get('dbClusterIdentifier')
db_name   = 'hlw_database_1'
sqltables = {
    'sysconfig' : {
        'id'      : 
        'appname' : {'type': 'varchar(100)', 'value'    : 'hellow-lamdba-app'},
        'sysid'   : {'type': 'int'         , 'value'    : 123876             },
        'country' : {'type': 'varchar(10)' , 'value'    : "USA"              },
        'created' : 
    },
}

def lambda_handler(event, context):
    #result = {**dbsecrets, **dbparams}
    #This function fetches content from MySQL RDS instance
    print('before connect')
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    print('after connect')
    cur  = conn.cursor()
    sqltext = 'CREATE TABLE IF NOT EXISTS sysconfig (id INT AUTO_INCREMENT PRIMARY KEY,
    appname VARCHAR(255) DEFAULT 'hello-world-lambda-app',
    sysid AUTO_INCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT DEFAULT 'This is the first lambda serverless app',
    last_update DATE
);'
    cur.execute(sqltext)
    cur.execute('select * from sysconfig')
    for row in cur:
        print(row,row[0],row[1],row[2])
        result[row[0]] = row[1]

    return result


    # Your code goes here.
