# Docker Notes:

1. Build and run the containers: `$ docker-compose up -d --build`
2. Create the DB `$ docker-compose exec web python manage.py create_db`
3. (Optional) Inpect volume `$ docker volume inspect sailogy_postgres_data`
4. (Optional) Connect to DB `$ docker-compose exec db psql --username=flask_user --dbname=sailogy_dev`
