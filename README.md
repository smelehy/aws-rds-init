# aws-rds-init
Initializes an RDS MYSQL database by creating new tables

set up directory on C drive C:\my-directory
open debian window on windows subsystem

install pip:
  - sudo apt-get install pip

install package dependencies
  - pip install --target ./packages packagename

install zip
  - sudo apt-get install zip 

create a lambda deployment package
  - cd packages
  - zip -r ../deployment-package.zip .
  - cd ..
  - zip deployment-pacakge.zip lambda_function.py  (python file name has to be 'lambda_function.py')

connect to RDS via Cloud9
  - myawl -u[username] -p -h [rds endpoint]
  - mysql -uadmin -p -h hlw-database-1.csmymcm2btd4.us-east-2.rds.amazonaws.com
  - (enter pwd when prompted)