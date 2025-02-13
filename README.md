# Menu Voting System  

This is a backend service designed for company employees to collectively decide where to have lunch. Restaurants submit daily menus via API, and employees can vote for their preferred option through a mobile app. The system ensures backward compatibility with older app versions by recognizing the build version sent in request headers.

## Features  
- User authentication via JWT  
- Restaurant management (creation and retrieval)  
- Daily menu submission by restaurants  
- Employee voting system for lunch decisions  
- Daily results to determine the most popular restaurant  

## Technology Stack  
- **Backend Framework:** Django + Django REST Framework  
- **Database:** PostgreSQL  
- **Authentication:** JWT  
- **Containerization:** Docker + Docker Compose  
- **Testing:** PyTest  
- **Linting:** Flake8 

---

## Installation  

### Requirements
Ensure you have the following installed:  
- Python 3.10+  
- Docker (optional, for containerized deployment)  

### Setup Instructions  

**Clone the Repository**  
   ```bash
   cd your-folder
   git clone https://github.com/nretrorsum/inforce_python_task.git
   
   ```

**Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

**Database Configuration**  
   Update your database settings in `mealvote/settings.py`, then run:  
   ```bash
   python manage.py migrate
   ```

**Create an Admin User**  
   ```bash
   python manage.py createsuperuser
   ```

**Start the Server**  
   ```bash
   python manage.py runserver
   ```
Or

**Run with Docker**
   ```bash
   docker-compose up --build
   docker exec -it container-name sh
   python manage.py migrate
   ```
### Notice: Change the 'localhost' in menuvote/settings.py DATABASES to 'db' in case of installation via Docker
---

## API Overview  

### Authentication  

- **Register User**: `POST /users/register/`
- **Login**: `POST /users/login/`  
- **Token Refresh**: `POST /users/token/refresh/`
  
### Restaurant Management
- **Create a Restaurant**: `POST /restaurants/create/`  
- **List Restaurants**: `GET /restaurants/all/`  

### Menu Management  

- **Submit a Daily Menu**: `POST /restaurants/menu/upload/`  
- **Get Today’s Menus**: `GET /restaurants/menu/today/`  

### Voting  

- **Vote for a Restaurant**: `POST /voting/vote/`  
- **Get Daily Results**: `GET /voting/results/`  

---

## Testing  

Run tests to verify functionality:  

```bash
python manage.py test
```

For Docker users:  

```bash
docker-compose exec web python manage.py test
```

---




