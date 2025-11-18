# Predictive Maintenance Backend - Phase 2

A comprehensive FastAPI-based backend system for predictive maintenance with real-time monitoring, alarm management, and ticketing system.

## 🚀 Features Implemented in Phase 2

### ✅ Database & Alembic
- **Comprehensive Database Schema**: Users, machines, sensors, measurements, alarms, tickets, and audit logs
- **Alembic Migrations**: Automated database schema management with version control
- **TimescaleDB Support**: Optimized for time-series data storage
- **UUID Primary Keys**: Secure and scalable identifier system

### ✅ Authentication & User Management
- **JWT-based Authentication**: Secure token-based authentication
- **Role-based Access Control**: Admin, Operator, and Viewer roles
- **User Registration & Login**: Complete user management system
- **Password Hashing**: Secure bcrypt password hashing
- **User CRUD Operations**: Full user management for admins

### ✅ Core Features
- **Machines CRUD**: Complete machine management with validation
- **Sensors CRUD**: Sensor configuration with threshold management
- **Measurements Ingestion**: Real-time data ingestion with batch support
- **Alarm System**: Automatic alarm generation based on sensor thresholds
- **Ticket Management**: Issue tracking linked to alarms and machines
- **Audit Logging**: Comprehensive action logging for compliance

### ✅ API Documentation
- **Swagger UI**: Interactive API documentation at `/docs`
- **ReDoc**: Alternative API documentation at `/redoc`
- **Comprehensive Endpoints**: All CRUD operations with proper validation

### ✅ Monitoring & Logging
- **Structured Logging**: JSON-formatted logs for easy parsing
- **Request/Response Logging**: Complete API request tracking
- **Business Event Logging**: Custom event logging for business logic
- **Error Logging**: Comprehensive error tracking and reporting

### ✅ Deployment Ready
- **Docker Support**: Complete containerization with Dockerfile
- **Docker Compose**: Multi-service setup with PostgreSQL and pgAdmin
- **Environment Configuration**: Flexible configuration management
- **Health Checks**: Application and database health monitoring

### ✅ Testing
- **Unit Tests**: Comprehensive test coverage for all components
- **Integration Tests**: End-to-end workflow testing
- **Test Fixtures**: Reusable test data and setup
- **Authentication Testing**: Role-based access control testing

## 🏗️ Architecture

```
app/
├── api/
│   ├── routes/          # API endpoints
│   ├── deps.py         # Dependencies
│   └── core/           # Core API components
├── auth/               # Authentication logic
├── core/               # Core utilities (logging, etc.)
├── db/                 # Database configuration
├── middleware/         # Custom middleware
├── models/             # SQLAlchemy models
├── repositories/       # Data access layer
├── schemas/            # Pydantic schemas
└── services/           # Business logic services
```

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone and Setup**:
   ```bash
   git clone <repository>
   cd predictive_maintenance_backend
   cp env.example .env
   # Edit .env with your configuration
   ```

2. **Start Services**:
   ```bash
   docker-compose up -d
   ```

3. **Access the Application**:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - pgAdmin: http://localhost:5050 (admin@admin.com / admin)

### Manual Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**:
   ```bash
   # Create PostgreSQL database
   createdb predictive_maintenance
   
   # Run migrations
   alembic upgrade head
   ```

3. **Configure Environment**:
   ```bash
   cp env.example .env
   # Edit .env with your database URL and JWT secret
   ```

4. **Start Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `GET /auth/users` - List users (admin only)
- `PUT /auth/users/{id}` - Update user (admin only)
- `DELETE /auth/users/{id}` - Delete user (admin only)

### Machines
- `GET /machines/` - List machines
- `POST /machines/` - Create machine
- `GET /machines/{id}` - Get machine
- `PUT /machines/{id}` - Update machine
- `DELETE /machines/{id}` - Delete machine

### Sensors
- `GET /sensors/` - List sensors
- `POST /sensors/` - Create sensor
- `GET /sensors/{id}` - Get sensor
- `PUT /sensors/{id}` - Update sensor
- `DELETE /sensors/{id}` - Delete sensor

### Measurements
- `POST /ingest/measurement` - Ingest single measurement
- `POST /ingest/batch` - Ingest batch measurements
- `POST /ingest/query` - Query measurements
- `GET /ingest/latest` - Get latest measurements

### Alarms
- `GET /alarms/` - List alarms
- `GET /alarms/active` - Get active alarms
- `GET /alarms/statistics` - Get alarm statistics
- `POST /alarms/` - Create alarm
- `POST /alarms/{id}/acknowledge` - Acknowledge alarm
- `POST /alarms/{id}/clear` - Clear alarm

### Tickets
- `GET /tickets/` - List tickets
- `POST /tickets/` - Create ticket
- `GET /tickets/{id}` - Get ticket
- `PUT /tickets/{id}` - Update ticket
- `DELETE /tickets/{id}` - Delete ticket
- `GET /tickets/statistics/summary` - Get ticket statistics

### Audit
- `GET /audit/` - List audit logs
- `GET /audit/{id}` - Get audit log
- `GET /audit/user/{email}` - Get user audit logs
- `GET /audit/actions/{action}` - Get action audit logs

## 🔐 Authentication & Authorization

### User Roles
- **Admin**: Full system access, user management
- **Operator**: Machine/sensor management, alarm acknowledgment
- **Viewer**: Read-only access to all data

### JWT Token
Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run integration tests only
pytest -m integration
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Authentication Tests**: Role-based access control

## 📊 Monitoring & Logging

### Logging Configuration
- **Format**: JSON structured logging
- **Level**: Configurable (DEBUG, INFO, WARNING, ERROR)
- **Output**: Console with optional file output

### Health Checks
- `GET /health` - Application health status
- Database connectivity monitoring
- Service dependency checks

## 🐳 Docker Commands

```bash
# Build and start all services
make up

# View logs
make logs

# Run migrations
make migrate

# Create new migration
make migrate-create MESSAGE="description"

# Run tests
make test

# Clean up
make clean
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FORMAT`: Log format (json, text)
- `ALLOWED_ORIGINS`: CORS allowed origins

### Database Configuration
- **PostgreSQL 15+**: Primary database
- **TimescaleDB**: Optional time-series extension
- **Connection Pooling**: Optimized for concurrent requests

## 📈 Performance Features

- **Connection Pooling**: Efficient database connections
- **Batch Operations**: Bulk data ingestion
- **Indexed Queries**: Optimized database queries
- **Caching Ready**: Prepared for Redis integration
- **Async Support**: Non-blocking I/O operations

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt with salt
- **Role-based Access**: Granular permissions
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Configurable cross-origin policies

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set secure JWT secrets
2. **Database**: Use managed PostgreSQL service
3. **Logging**: Configure log aggregation
4. **Monitoring**: Set up application monitoring
5. **SSL/TLS**: Enable HTTPS in production
6. **Backup**: Regular database backups

### Scaling Options
- **Horizontal Scaling**: Multiple app instances
- **Database Scaling**: Read replicas, connection pooling
- **Caching**: Redis for session and data caching
- **Load Balancing**: Nginx or cloud load balancer

## 📝 API Documentation

Visit `/docs` for interactive API documentation with:
- Request/response schemas
- Authentication requirements
- Example requests
- Response codes and error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

## 🎯 Phase 2 Completion Checklist

- ✅ Database schema with Alembic migrations
- ✅ JWT authentication with role-based access
- ✅ Complete CRUD operations for all entities
- ✅ Real-time measurement ingestion
- ✅ Automatic alarm generation
- ✅ Ticket management system
- ✅ Comprehensive audit logging
- ✅ Structured logging and monitoring
- ✅ Docker containerization
- ✅ Unit and integration tests
- ✅ API documentation
- ✅ Production-ready configuration

**Phase 2 is complete and ready for production deployment!** 🚀