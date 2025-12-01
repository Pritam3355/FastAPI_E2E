python -m venv virtualenv

.\virtualenv\Scripts\activate 

docker compose -f <full-path> up -d

docker exec -it postgres15 psql -U "test_user" -d "test_db"

\l              -- list databases
\du             -- list users

# Initalize new migration
alembic init alembic 

# Check if .env files are loaded properly
docker-compose config

# Stop containers but keep all data
docker-compose stop

# Start the stopped containers
docker-compose start

# Or use down (stops and removes containers, but keeps volumes)
docker-compose down

# Or use down (stops and removes containers,also removes volumes)
docker-compose down -v

# Or if you used 'down', use up
docker-compose up -d

# Clean up any old containers
docker system prune -f
docker volume rm fastapi_db_postgres_data

# Restart fresh
docker-compose up --build -d

# Run the migration creation inside a temporary container
docker-compose run --rm api alembic revision --autogenerate -m "create users table"

or 

alembic revision --autogenerate -m "create users table"

 
### this will create xxxx_create_users_table.py if not create them manually

then migrate using

# Access the running container
docker exec -it fastapi_app bash

# Inside the container, run:
alembic revision --autogenerate -m "create users table"
# To Run Upgrade Part (Create Table)
alembic upgrade head
# To Run Relative Downgrade Part (Downgrade to previous version)
alembic downgrade -1
# To Run Relative Upgrade
alembic upgrade +1
# To Reverse Everything &  Back to no Table
alembic upgrade base

# Check Current version
alembic current

# Exit the container
exit

# Filter Logs
docker-compose logs -f api

docker-compose logs -f postgres

# Doesn't support on windows
uvloop==0.21.0 
