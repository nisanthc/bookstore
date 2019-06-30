# bookstore

**This project is created in Windows 10**

## STEPS for Installation

### MySQL Installation

    1. Download MySQL using below URL
        https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.26-winx64.zip
    
    2. Extract the zip file (mysql-5.7.26-winx64)
    
    3. Copy the mysql-5.7.26-winx64 into E:
    
    4. Rename the folder mysql-5.7.26-winx64 to Mysql
    
    5. Open command prompt and GoTO the E:\Mysql\bin folder
    
    6. Run the below commands to Start the Mysql
    
        1. mysqld --initialize-insecure
        
        2. mysqld --console
        Note: Don't close this cmd shell, because Mysql is running in this console
    
    7. Open another command prompt and GoTo the E:\Mysql\bin and run the below command to check
        mysql -u root --skip-password

### Python Installation

    1. Download Python using below link
        https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe

    2. Install the downloaded python-3.6.5-amd64.exe
    
    3. Go to command prompt and type python to check the version
        E:\> python --version
            Python 3.6.5
        Note: If you are getting below error, then need to the python path into environment variable
        E:\> python --version
            'python' is not recognized as an internal or external command,operable program or batch file.
        Please go through this video to setup python path to environment variable
            https://www.youtube.com/watch?v=OS5EgtMQrmQ
    
    4. Installing required python package for this project
    
        1. Create requirements.txt & add the below lines in it. And save it under E: drive
            Flask==0.10.1
            flask-restful==0.3.7
            requests==2.22.0
            jsonschema==3.0.1
            mysql-connector-python==8.0.16
            pytest==5.0.0
            pytest-cov==2.7.1
            pytest-html==1.21.1
            
        2. Open command prompt and goto the requirement.txt folder (E:)
        
        3. Run the below command
           pip install -r requirements.txt

### Setup Project

Download zip file (https://github.com/nisanthc/bookstore/archive/master.zip) & unzip the same 
or
Clone (https://github.com/nisanthc/bookstore.git) the bookstore project.

Assuming downloaded bookstore project is available under following location
E:\workplace\bookstore-master

    1. Setting up databases
        
        1. Open command prompt, and Go to E:\Mysql\bin folder
        
        2. Run the below command to restore
            mysql -u root <  E:\workplace\bookstore-master\src\db\books_schema.sql
    
    2. Setup and Run project
        
        1. Add project path to PYTHONPATH in environment variable(either by using GUI or command prompt)
           If you are adding command prompt, it is temporary. PYTHONPATH variable is available only
           to that cmd shell.
        
        2. Open command prompt
        
        3. Run the below command
            set PYTHONPATH=E:\workplace\bookstore-master\src
        
        4. Start the project by running routes.py
            python E:\workplace\bookstore-master\src\routes.py
        
            Note: Don't close this cmd shell, because flask application is running
        
        5. Open browser and type the below URL to check
                http://127.0.0.1:8080/api/external-books/?name=The Hedge Knight
