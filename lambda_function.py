import os
import sys
import pymysql
import json
from pprint import pprint 
import boto3
from botocore.exceptions import ClientError
from json_to_sql import json_to_sql

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
print('**********dbsecrets***********')
pprint(dbsecrets)
print('*****************************')
rds_host  = 'hlw-database-1.csmymcm2btd4.us-east-2.rds.amazonaws.com'
name      = dbsecrets.get('username')
password  = dbsecrets.get('password')
db_name   = 'hlw_database_1'
pkeydef   = 'INT AUTO_INCREMENT PRIMARY KEY'
vc50      = 'VARCHAR(50)'
vc100     = 'VARCHAR(100)'
vc255     = 'VARCHAR(255)'
d         = 'DATE'
t         = 'TEXT'
ti        = 'TINYINT'
i         = 'INT'
ts        = 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
print('lambda-init.......')
def lambda_handler(event, context):
    #result = {**dbsecrets, **dbparams}
    #This function fetches content from MySQL RDS instance
    print('before connect')
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    print('after connect')
    cur  = conn.cursor()
    sqltables = {
        'application' : {
            'id'         : pkeydef,
            'appid'      : i,
            'appname'    : vc100,
            'description': vc255,
            'created'    : ts,
        },
        'contacts' : {
            'id'    : pkeydef,
            'first' : vc100,
            'last'  : vc100,
            'phone' : vc100,
            'created'    : ts,
        },
        'requests'  : {
            'id'    : pkeydef,
            'requestedfrom'  : i,
            'subject' : vc100,
            'requestdate' : d,
            'created'    : ts,
        },
    }
    for table,fields in sqltables.items():
        sqlres = json_to_sql(table = table, fields = fields)
        print(sqlres)
        cur.execute(sqlres)

    return 1
