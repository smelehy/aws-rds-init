#  converts an input json structure having table names, field names and data types into SQL that will create those tables
import pdb 
from pprint import pprint

def json_to_sql(**kwargs):
    tble = kwargs.get('table')
    flds = kwargs.get('fields')
    result = ''
    pkeydef   = 'INT AUTO_INCREMENT PRIMARY KEY'
    vc50      = 'VARCHAR(50)'
    vc100     = 'VARCHAR(100)'
    vc255     = 'VARCHAR(255)'
    d         = 'DATE'
    t         = 'TEXT'
    ti        = 'TINYINT'
    i         = 'INT'
    ts        = 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'

    sqltext = 'CREATE TABLE IF NOT EXISTS '+ tble + '('
    for fieldname,type in flds.items():
        sqltext += fieldname +' '+ type + ', '
    sqltext = sqltext[:-2]
    sqltext += ');'
    print('sql is:', sqltext)
    return sqltext

