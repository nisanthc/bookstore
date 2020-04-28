# bookstore

## STEPS for Installation

### Docker Installation

    1. Go to virutaul Machine or Host (centos)
            
    2. Install Docker using below commands
        1. sudo yum install -y yum-utils
        2. sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        3. sudo yum install docker-ce docker-ce-cli containerd.io
        4. sudo systemctl start docker
            
    3. Check the installation
        1. sudo docker run hello-world
        
    4. Download Book Store App
       Download zip file (https://github.com/nisanthc/bookstore/archive/master.zip) & unzip the same or Clone (https://github.com/nisanthc/bookstore.git) the bookstore project.

### MySQL

    1. Go to virutaul Machine or Host
            
    2. Create following folder
       sudo mkdir -p /media/book-mysql
    
    3. Run the below docker command to start MySQL
       docker run --name book-mysql -d -e MYSQL_ROOT_PASSWORD="admin123" -e MYSQL_DATABASE=book_store -e MYSQL_USER=book -e MYSQL_PASSWORD="book123" -e TZ=America/Pacific -p 3306:3306 -v /media/book-mysql:/var/lib/mysql mysql:5.7.29
       
    4. Check the MySQL 
       docker ps
       
    5. Run the MySQL command to set up database
       docker exec -i book-mysql mysql  -u book -p'book123' < bookstore/src/db/books_schema.sql

### Python Flask App

    1. Build the Book Store docker image
        1. Goto the bookstore folder
        2. Build the docker image
           docker build -t book_store_image .
     
    2. Start the Book Store App
        1. Create a log folder 
           sudo mkdir -p /media/book-app
        2. Run the Docker container
           docker run -d -p 5000:5000 --link book-mysql -e DB_HOST=book-mysql -e DB_USER=book -e DB_PASSWORD=book123 -e DB_DATABASE=book_store -e DB_PORT=3306 -v /media/book-app/:/logs --name book_store_app book_store_image
    
    3. Open the below URL in browser
         http://127.0.0.1:5000/api/external-books/  or 
         http://<<yourip>>:5000/api/external-books/
   

### Pytest for Unit Test

    1. Go into the Book Store container
        docker exec -it book_store_app /bin/sh 
       
    2. Run the below command
        py.test --cov books --cov-report html --html pytest_report.html    
      
