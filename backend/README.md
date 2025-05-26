# Super App Backend

A banking-grade super-app backend built with FastAPI, featuring multi-service capabilities including instant messaging, shopping, payments, and a mini-app ecosystem.

## 🏦 Banking-Grade Security Features

- **JWT Authentication** with access/refresh token rotation
- **End-to-End Encryption** for sensitive PII data
- **Session Management** with device tracking
- **Rate Limiting** and failed attempt protection
- **Password Requirements** meeting banking standards
- **Audit Trails** for all operations
- **CORS and Security Headers** protection

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MySQL
- UV package manager

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd super-app-backend/backend

# Install dependencies with UV
uv sync

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Database Setup

```bash
# Create MySQL database
createdb superapp_db
```

### Running the Application

```bash
# Development mode
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
or 
cd backend/
uv run main.py

# Production mode
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🔐 Authentication Endpoints

### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

### Login User

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "user_id": "uuid-here",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "is_active": true,
    "is_verified": false,
    "kyc_status": "pending"
  },
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

### Get User Profile

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

### Logout

```http
POST /api/v1/auth/logout
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

## 📦 Postman Testing

### Setup Postman Environment

Create a new environment in Postman with:

```json
{
  "base_url": "http://localhost:8000/api/v1",
  "access_token": "",
  "refresh_token": ""
}
```

### Test Collection Examples

1. **Register User**
   ```
   POST {{base_url}}/auth/register
   Body: (JSON from examples above)
   ```

2. **Login User**
   ```
   POST {{base_url}}/auth/login
   Body: (JSON from examples above)
   
   Tests Script:
   ```javascript
   if (pm.response.code === 200) {
       const response = pm.response.json();
       pm.environment.set("access_token", response.tokens.access_token);
       pm.environment.set("refresh_token", response.tokens.refresh_token);
   }
   ```

3. **Get Profile**
   ```
   GET {{base_url}}/auth/me
   Authorization: Bearer {{access_token}}
   ```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── auth/                 # Authentication module
│   │   ├── router.py        # Auth endpoints
│   │   ├── service.py       # Business logic
│   │   └── dependencies.py  # Auth dependencies
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration
│   │   ├── security.py      # Security utilities
│   │   └── database.py      # Database setup
│   ├── models/              # Database models
│   │   └── user.py         # User models
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py         # User schemas
│   │   └── auth.py         # Auth schemas
│   ├── tests/               # Test suite
│   │   ├── conftest.py     # Test configuration
│   │   └── test_auth.py    # Auth tests
│   └── main.py             # FastAPI application
├── .env.example            # Environment template
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## 🔒 Security Considerations

### Data Encryption
- **PII Encryption**: First name, last name, and phone numbers are encrypted at rest
- **Password Hashing**: Bcrypt with configurable salt rounds (default: 12)
- **Token Security**: JWT with short-lived access tokens and rotating refresh tokens

### Session Management
- **Device Tracking**: Sessions are tied to device fingerprints
- **IP Logging**: All authentication attempts are logged with IP addresses
- **Session Expiry**: Configurable token expiration times
- **Concurrent Sessions**: Multiple device support with individual session management

### Banking-Grade Features
- **Failed Login Protection**: Account locking after 5 failed attempts
- **Audit Trails**: All operations are logged with timestamps
- **Data Privacy**: Sensitive data is encrypted and access-controlled
- **Secure Headers**: CORS, CSP, and other security headers

## 🚧 Next Steps

This authentication module provides the foundation for:

1. **KYC Module** - Document verification and face recognition
2. **Chat Module** - Real-time messaging with encryption
3. **Payment Module** - Razorpay integration for UPI/banking
4. **Mini-App Ecosystem** - Third-party app integration platform

## 🐛 Troubleshooting

1. **Token Validation Error**
   - Ensure `SECRET_KEY` is set and consistent
   - Check token expiration times
   - Verify token format in Authorization header

2. **Password Validation Error**
   - Review password requirements in schema
   - Check special character requirements

## 🔮 Future Enhancements

- [ ] OAuth2 integration (Google, Apple, Facebook)
- [ ] Two-Factor Authentication (2FA)
- [ ] Biometric authentication support
- [ ] Advanced rate limiting with Redis
- [ ] Microservices architecture
- [ ] GraphQL support
- [ ] Real-time notifications