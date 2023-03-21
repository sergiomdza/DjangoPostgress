# 1) Para correr el projecto primero ejecute el siguiente comando en la carpeta root:

docker network create odoo-network

# 2) Después ejecute el docker compose de la Carpeta Odoo
DjangoPostgres\Odoo> docker-compose up

# 3.1) Si se abre el http://localhost:8069/ y se tiene que crear una base de datos, asegurese de crearla
# con la información que aparece en la foto Config.png

# 3.2) Si no, si le pide hacer Login refierase a la foto Config.png para obtener los valores

# 4) Acceda a la consola de Django del contenedor de docker y ejecute los siguientes comandos
python3 manage.py makemigrations
python3 manage.py migrate

# 5) Ejecute el comando para crear un nuevo superusuario
python3 manage.py createsuperuser

# 6) Ponga los siguientes datos:
*UserName:* admin
*Password:* adminpassword
