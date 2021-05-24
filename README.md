# Programing Project Databases TEAM 3 #
This project is created for the course Programming project databases. This repository is the remote repository of our web application and is created by Mohamed Darkoui, Mounir Madmar, Khalil Ouailb and Ferit Murad

### Configure and run our web application:

#### 1. Postgres database and Python interface
```bash
sudo apt install postgresql python-psycopg2
```

#### 2. Create the database
First configure the database with `postgres` user:
```bash
sudo su postgres
psql
```
Then create the database with owner postgres:
```sql
CREATE DATABASE ppdb OWNER postgres;
```


the default password for the postgres user is **postgres**, in the case that you have a different password then you have to edit the file
`src/config.py` (change the assignment of config_data['dbpassword'] to your own password), you can also change the name of the
database or the user if needed.

```
# database access information

config_data = {
    'dbname' : 'ppdb',
    'dbuser' : 'postgres',
    'dbpassword' : 'thisismypassword'
}
```
You need to 'trust' the role to be able to login. Add the following line to `/etc/postgresql/9.6/main/pg_hba.conf` (you need root access, version may vary). __It needs to be the first rule (above local all all peer)__.
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# app
local   	ppdb                  postgres                                       	 trust
```

and restart the service. Then initialize the database:
```bash
sudo systemctl restart postgresql
psql ppdb -U postgres -f sql/schema.sql
```


#### 3. Download Dependencies

```bash
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
```


#### 4. Run development server
```bash
chmod +x run.sh
./run.sh
```
Then visit http://localhost:5000


### Programma Design:
**Here we will give a brief explanation of the source files.**

##### src/appCreator.py
- Creates the flask application that will be used.
- Makes the necessary connections with the database.
- Registers all necessary blueprints for the application.
- Creates a login manager.

##### src/models.py
- The model of our database is defined in a .sql file but we need an object relational mapper to be able to use
the login_manager from flask-login. We dont really need to the define the whole model in the object relational mapper
but only the Users table that is used in the login manager. This file defines the class (table) Users.

##### src/auth.py
- Provides functionality for the registration page.

##### src/views.py
- Provides functionality for the home, users and profile pages.

##### src/datasets.py 
- Provides functionality for the datasets page.

##### src/scenarios.py 
- Provides functionality for the scenarios page.

##### src/_models.py 
- Provides functionality for the models page.

##### src/experiments.py 
- Provides functionality for the experiments page.

##### src/database/*.py
- All the files in the src/database folder contain utility and classes that provide functionality with the database.

##### src/Algorithms
- Library of recommendation algorithms from course assistant Joey De Pauw.

##### src/algorithm.py
- Contains functions to be able to create algorithms from the library of the recommendation algorithms and run them.

##### src/config.py
- Configuration of the database (name, user and password).

##### src/templates/*.html
- All the files in the src/templates folder contain html templates for our web application.

##### src/static/*
- All the files in the src/static folder contain images, css files and javascript files for our web application.

\
**The following schema shows how the source files are linked with each other.**

![alt text](https://i.ibb.co/v36mpMn/programma-Design.png)
