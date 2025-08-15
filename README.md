
![SM-Backend](https://socialify.git.ci/An-Array/SM-Backend/image?font=Raleway&language=1&name=1&owner=1&pattern=Brick+Wall&theme=Dark)
A modern social media backend API built with FastAPI, PostgreSQL, and SQLAlchemy. This project provides a robust foundation for social media applications with user authentication, post management, and secure API endpoints.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Overview

SM-Backend is a RESTful API service designed for social media applications. Built with FastAPI for high performance and automatic API documentation, it provides essential features like user management, post creation, and JWT-based authentication.

## ✨ Features

- **User Management**
  - User registration and authentication
  - Secure password hashing with bcrypt
  - Email validation
  - User profile management

- **Post Management**
  - Create, read, update, and delete posts
  - Post ownership and permissions
  - Published/unpublished post states
  - Automatic timestamps

- **Authentication & Security**
  - JWT token-based authentication
  - OAuth2 password bearer flow
  - Secure password hashing
  - Token expiration management

- **API Features**
  - Automatic API documentation with Swagger UI
  - Pydantic data validation
  - SQLAlchemy ORM with PostgreSQL
  - Environment-based configuration

## 🛠 Tech Stack

| Component       | Technology |
|-----------------|------------|
| Framework       | FastAPI    |
| Database        | PostgreSQL |
| ORM             | SQLAlchemy |
| Authentication  | JWT/OAuth2 |
| Password Hashing| Bcrypt     |
| Validation      | Pydantic   |
| Configuration   | pydantic-settings|
| Python Version  |  3.7+      |

## 📁 Project Structure

```
SM-Backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for request/response
│   ├── oauth2.py            # JWT authentication logic
│   ├── utils.py             # Utility functions (password hashing)
│   └── routers/             # API route modules
│       ├── auth.py          # Authentication routes
│       ├── post.py          # Post management routes
│       └── user.py          # User management routes
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 📋 Prerequisites

Before running this application, ensure you have:

- Python 3.7 or higher
- PostgreSQL database
- pip (Python package manager)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/An-Array/SM-Backend.git
   cd SM-Backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Configure your environment variables** (see [Configuration](#configuration))

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_HOSTNAME=your_db_host
DATABASE_PORT=your_db_port
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_db_user

# JWT Configuration
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configuration Details

- **Database Settings**: PostgreSQL connection parameters
- **JWT Settings**: 
  - `SECRET_KEY`: Used for signing JWT tokens (keep this secure!)
  - `ALGORITHM`: Hashing algorithm for JWT (HS256 recommended)
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`

### Main Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login` | Get access token |

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "yourpassword"
}
```

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Create new user |
| `GET`  | `/users/{id}` | Get user by ID |

**Create User Request:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Posts
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET`  | `/posts/` | Get all posts | Yes |
| `POST` | `/posts/` | Create new post | Yes |
| `GET`  | `/posts/{id}` | Get post by ID | Yes |
| `PUT`  | `/posts/{id}` | Update post | Yes |
| `DELETE`| `/posts/{id}` | Delete post | Yes |

**Post Request Body:**
```json
{
  "title": "Post Title",
  "content": "Post content here...",
  "published": true
}
```


## 🗃 Database Models

### User Model
```python
class User(Base):
    id: int (Primary Key)
    email: str (Unique, Required)
    password: str (Hashed, Required)
    created_at: datetime (Auto-generated)
```

### Post Model
```python
class Post(Base):
    id: int (Primary Key)
    title: str (Required)
    content: str (Required)
    published: bool (Default: True)
    created_at: datetime (Auto-generated)
    user_id: int (Foreign Key to User)
    created_by: User (Relationship)
```

## 🔐 Authentication

This API uses JWT (JSON Web Tokens) for authentication following the OAuth2 password bearer flow.

### Authentication Flow
1. User logs in with credentials at `/login`
2. Server returns JWT access token
3. Client includes token in Authorization header:
   ```
   Authorization: Bearer <token>
   ```
4. Protected endpoints verify token validity
5. Token expires after 30 minutes (configurable)

### Token Details
- **Type**: Bearer Token
- **Expiration**: Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Algorithm**: HS256 (configurable)

## 💻 Usage Examples

### Register a New User
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "securepassword123"
     }'
```

### Login
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=securepassword123"
```

### Create a Post (Authenticated)
```bash
curl -X POST "http://localhost:8000/posts" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_jwt_token>" \
     -d '{
       "title": "My First Post",
       "content": "This is the content of my first post!",
       "published": true
     }'
```

### Get All Posts
```bash
curl -X GET "http://localhost:8000/posts"
```

## 🔧 Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations
The application automatically creates tables on startup using SQLAlchemy's `create_all()` method.

### Adding New Features
1. Define database models in `models.py`
2. Create Pydantic schemas in `schemas.py`
3. Implement route logic in appropriate router files
4. Register routers in `main.py`

## 🧪 Testing

### Manual Testing
Use the interactive documentation at `/docs` to test endpoints directly from your browser.

### Example Test Scenarios
1. Register a new user
2. Login with user credentials
3. Create posts with authentication
4. Try accessing protected endpoints without tokens
5. Test data validation with invalid inputs

## 🚀 Deployment

### Production Considerations
- Use environment variables for all sensitive configuration
- Set up proper PostgreSQL database with backups
- Configure HTTPS/SSL certificates
- Set up proper logging and monitoring
- Consider using a production WSGI server like Gunicorn

### Docker Deployment (Example)
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add appropriate error handling
- Include docstrings for functions
- Test new features before submitting

## 📄 Dependencies

### Main Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - Database ORM
- `psycopg2-binary` - PostgreSQL adapter
- `pydantic[email]` - Data validation
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data support

## 📞 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/docs) when running locally
2. Review the configuration settings in your `.env` file
3. Open an issue on GitHub with detailed information
4. Check existing issues for similar problems

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using FastAPI and modern Python tools**
