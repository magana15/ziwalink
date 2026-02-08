# Ziwalink API


**Ziwalink** is a Dockerized Django + GraphQL backend for a social platform for farmers.  
Farmers can post updates, images of livestock, and interact through likes and comments.  


## Features

- Custom user roles: **Farmer** and **Admin**
- GraphQL API with **JWT authentication**
- Image uploads with Pillow
- Dockerized **PostgreSQL + Django + Gunicorn**
- Production-ready and deployable


## Tech Stack

- **Backend:** Django
- **API:** GraphQL (Graphene)  
- **Auth:** JWT (SimpleJWT)  
- **Database:** PostgreSQL  
- **Containerization:** Docker & Docker Compose  


## Quick Setup

```bash
# Clone repo
git clone https://github.com/yourusername/ziwalink.git
cd ziwalink

# Create .env (production or local)
cp .env.example .env

# Build & start containers
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

