# bookstore

**This project is created in Windows 10**

## STEPS for Installation

### MySQL Installation
-------------------
    1. Download MySQL using below URL
         https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.26-winx64.zip
    2. Extract the zip file (mysql-5.7.26-winx64)
    3. Copy the mysql-5.7.26-winx64 into any drive C: or E:
    4. Rename the folder to Mysql
    5. Open command prompt and GoTO the Mysql/bin folder
    6. Run the below commands to Start the Mysql
        1. mysqld --initialize-insecure
        2. mysqld --console
        Note: Don't Close this cmd shell, because Mysql is running in console
    7. Open another command prompt and GoTo the Mysql/bin and run the below command to check
        1. mysql -u root --skip-password
-------------------

### Python Installation
-------------------
    1. Download Python using below link
        https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe
    2. Install the downloaded python exe
    3. Go to cmd and type python to check the version
        E:\>python --version
            Python 3.6.5

        Note: If you are getting below error, then need to the python path into environment variable
              E:\>python --version
                'python' is not recognized as an internal or external command,operable program or batch file.
        Please go through this video to setup python path toenvironment
            https://www.youtube.com/watch?v=OS5EgtMQrmQ
    4. Installing required python package for this project
        1. Create requirements.txt and add the below lines in it
            pip install Flask==0.10.1
            pip install flask-restful==0.3.7
            pip install requests==2.22.0
            pip install jsonschema==3.0.1
            pip install mysql-connector-python==8.0.16
            pip install pytest==5.0.0
            pip install pytest-cov==2.7.1
            pip install pytest-html==1.21.1
        2. Run the below command in command prompt
           E:\> pip install -r requirements.txt

### Setup Project
------------------------------------
Assuming downloaded bookstore project is available under following location
E:\workplace\bookstore

1. Setting up databases
    1. Open command prompt, and Go to Mysql/bin folder
    2. Run the below command to restore
        E:\Mysql\bin>mysql -u root <  E:\workplace\bookstore\src\db\books_schema.sql
2. Setup and Run project

    1. Add project path to PYTHONPATH in environment(either by using GUI or command prompt)
       If you are adding command prompt, it is temporary. PYTHONPATH variable is available only
       to that cmd shell.
    2) Open command prompt
    3) Run the below command
        E:\> set PYTHONPATH=E:\workplace\bookstore\src
    4) Goto the folder E:\workplace\bookstore\src
    5) Start the project by running routes.py
        E:\workplace\bookstore\src> python routes.py
    6) Open browser and type the below URL to check
            http://127.0.0.1:8080/api/external-books/?name=The Hedge Knight
-------------------------------------










