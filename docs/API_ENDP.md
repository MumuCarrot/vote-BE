# API Endpoints Documentation

This document provides comprehensive documentation for all API endpoints in the Election Backend system.

## Base URL

All endpoints are prefixed with `/api/v1`.

## Authentication

Most endpoints require authentication via JWT tokens. Tokens are stored in httpOnly cookies:
- `access_token`: Used for authenticating requests
- `refresh_token`: Used for refreshing the access token

Endpoints that require authentication will return `401 Unauthorized` if the token is missing or invalid.

---

## Health Check Endpoints

### GET `/api/v1/health/`

Root health check endpoint.

**Authentication:** Not required

**Response:**
```json
{
  "status_code": 200,
  "detail": "ok",
  "result": "working"
}
```

---

### GET `/api/v1/health/postgresql`

PostgreSQL database health check endpoint.

**Authentication:** Not required

**Response:**
```json
{
  "status": "ok"
}
```

**Error Response:**
```json
{
  "status": "error",
  "detail": "Error message"
}
```

---

### GET `/api/v1/health/redis`

Redis database health check endpoint.

**Authentication:** Not required

**Response:**
```json
{
  "status": "ok",
  "detail": "Redis is healthy"
}
```

**Error Response:**
```json
{
  "status": "error",
  "detail": "Error message"
}
```

---

### GET `/api/v1/health/protected`

Protected endpoint that requires a valid JWT token.

**Authentication:** Required

**Response:**
```json
{
  "message": "Authentication successful!",
  "authenticated": true,
  "user_id": "user-uuid",
  "user_login": "user@example.com"
}
```

---

## Authentication Endpoints

### POST `/api/v1/auth/register`

Register a new user. Tokens are set in httpOnly cookies.

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Fields:**
- `email` (required): User email address (must be valid email format)
- `password` (required): User password (minimum 8 characters)
- `phone` (optional): User phone number
- `first_name` (optional): User first name
- `last_name` (optional): User last name

**Response:** `201 Created`
```json
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Cookies Set:**
- `access_token`: JWT access token
- `refresh_token`: JWT refresh token

**Note:** A user profile is automatically created when a user registers.

---

### POST `/api/v1/auth/login`

Authenticate user. Tokens are set in httpOnly cookies.

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Fields:**
- `email` (required): User email address
- `password` (required): User password (minimum 8 characters)

**Response:** `200 OK`
```json
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Cookies Set:**
- `access_token`: JWT access token
- `refresh_token`: JWT refresh token

---

### POST `/api/v1/auth/refresh`

Refresh access token using refresh token. New tokens are set in httpOnly cookies.

**Authentication:** Required (refresh token in cookie)

**Request Body:** None (refresh token is read from cookie)

**Response:** `200 OK`
```json
{
  "detail": "Tokens refreshed successfully"
}
```

**Cookies Set:**
- `access_token`: New JWT access token
- `refresh_token`: New JWT refresh token

---

### POST `/api/v1/auth/logout`

Logout user by blacklisting tokens.

**Authentication:** Required

**Request Body:** None

**Response:** `200 OK`
```json
{
  "detail": "Logged out successfully"
}
```

**Cookies Cleared:**
- `access_token`
- `refresh_token`

---

### GET `/api/v1/auth/me`

Get current authenticated user information.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

---

## User Endpoints

### POST `/api/v1/users`

Create a new user.

**Authentication:** Not required (may vary based on your security requirements)

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Fields:**
- `email` (required): User email address
- `password` (required): User password (minimum 8 characters)
- `phone` (optional): User phone number
- `first_name` (optional): User first name
- `last_name` (optional): User last name

**Response:** `201 Created`
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

**Note:** A user profile is automatically created when a user is created.

---

### GET `/api/v1/users`

Get all users with pagination.

**Authentication:** Not required (may vary based on your security requirements)

**Query Parameters:**
- `page` (optional, default: 1): Page number (minimum: 1)
- `page_size` (optional, default: 10): Number of items per page (minimum: 1, maximum: 100)

**Response:** `200 OK`
```json
[
  {
    "id": "user-uuid-1",
    "email": "user1@example.com",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": "user-uuid-2",
    "email": "user2@example.com",
    "phone": "+0987654321",
    "first_name": "Jane",
    "last_name": "Smith",
    "created_at": "2024-01-02T00:00:00"
  }
]
```

---

### GET `/api/v1/users/{user_id}`

Get user by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Response:** `200 OK`
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User with id {user_id} not found"
}
```

---

### PUT `/api/v1/users/{user_id}`

Update user information.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "password": "newpassword123"
}
```

**Fields (all optional):**
- `email`: User email address
- `phone`: User phone number
- `first_name`: User first name
- `last_name`: User last name
- `password`: User password (minimum 8 characters)

**Response:** `200 OK`
```json
{
  "id": "user-uuid",
  "email": "newemail@example.com",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### DELETE `/api/v1/users/{user_id}`

Delete user by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Response:** `200 OK`
```json
{
  "detail": "User with id {user_id} deleted successfully"
}
```

---

## User Profile Endpoints

### POST `/api/v1/user-profiles`

Create a new user profile.

**Authentication:** Not required (may vary based on your security requirements)

**Request Body:**
```json
{
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/avatar.jpg",
  "address": "123 Main St, City, Country"
}
```

**Fields:**
- `user_id` (required): User UUID
- `birth_date` (optional): User birth date (YYYY-MM-DD format)
- `avatar_url` (optional): URL to user's avatar image
- `address` (optional): User's address

**Response:** `201 Created`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/avatar.jpg",
  "address": "123 Main St, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "detail": "User profile for user {user_id} already exists"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User with id {user_id} not found"
}
```

---

### GET `/api/v1/user-profiles`

Get all user profiles with pagination.

**Authentication:** Not required (may vary based on your security requirements)

**Query Parameters:**
- `page` (optional, default: 1): Page number (minimum: 1)
- `page_size` (optional, default: 10): Number of items per page (minimum: 1, maximum: 100)

**Response:** `200 OK`
```json
[
  {
    "id": "profile-uuid-1",
    "user_id": "user-uuid-1",
    "birth_date": "1990-01-01",
    "avatar_url": "https://example.com/avatar1.jpg",
    "address": "123 Main St, City, Country",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": "profile-uuid-2",
    "user_id": "user-uuid-2",
    "birth_date": "1992-05-15",
    "avatar_url": "https://example.com/avatar2.jpg",
    "address": "456 Oak Ave, City, Country",
    "created_at": "2024-01-02T00:00:00"
  }
]
```

---

### GET `/api/v1/user-profiles/me/profile`

Get current user's profile.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/avatar.jpg",
  "address": "123 Main St, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile for user {user_id} not found"
}
```

---

### GET `/api/v1/user-profiles/user/{user_id}`

Get user profile by user ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Response:** `200 OK`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/avatar.jpg",
  "address": "123 Main St, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile for user {user_id} not found"
}
```

---

### GET `/api/v1/user-profiles/{profile_id}`

Get user profile by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `profile_id` (required): User profile UUID

**Response:** `200 OK`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/avatar.jpg",
  "address": "123 Main St, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile with id {profile_id} not found"
}
```

---

### PUT `/api/v1/user-profiles/me/profile`

Update current user's profile.

**Authentication:** Required

**Request Body:**
```json
{
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "address": "789 Pine Rd, City, Country"
}
```

**Fields (all optional):**
- `birth_date`: User birth date (YYYY-MM-DD format)
- `avatar_url`: URL to user's avatar image
- `address`: User's address

**Response:** `200 OK`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "address": "789 Pine Rd, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile for user {user_id} not found"
}
```

---

### PUT `/api/v1/user-profiles/user/{user_id}`

Update user profile by user ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Request Body:**
```json
{
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "address": "789 Pine Rd, City, Country"
}
```

**Fields (all optional):**
- `birth_date`: User birth date (YYYY-MM-DD format)
- `avatar_url`: URL to user's avatar image
- `address`: User's address

**Response:** `200 OK`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "address": "789 Pine Rd, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile for user {user_id} not found"
}
```

---

### PUT `/api/v1/user-profiles/{profile_id}`

Update user profile information.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `profile_id` (required): User profile UUID

**Request Body:**
```json
{
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "address": "789 Pine Rd, City, Country"
}
```

**Fields (all optional):**
- `birth_date`: User birth date (YYYY-MM-DD format)
- `avatar_url`: URL to user's avatar image
- `address`: User's address

**Response:** `200 OK`
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "birth_date": "1990-01-01",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "address": "789 Pine Rd, City, Country",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile with id {profile_id} not found"
}
```

---

### DELETE `/api/v1/user-profiles/me/profile`

Delete current user's profile.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "detail": "User profile for user {user_id} deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile for user {user_id} not found"
}
```

---

### DELETE `/api/v1/user-profiles/user/{user_id}`

Delete user profile by user ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Response:** `200 OK`
```json
{
  "detail": "User profile for user {user_id} deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile for user {user_id} not found"
}
```

---

### DELETE `/api/v1/user-profiles/{profile_id}`

Delete user profile by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `profile_id` (required): User profile UUID

**Response:** `200 OK`
```json
{
  "detail": "User profile with id {profile_id} deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User profile with id {profile_id} not found"
}
```

---

## Election Endpoints

### POST `/api/v1/elections`

Create a new election with candidates and settings.

**Authentication:** Required

**Request Body:**
```json
{
  "title": "Presidential Election 2024",
  "description": "Annual presidential election",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "is_public": true,
  "candidates": [
    {
      "name": "Candidate A",
      "description": "Candidate A description"
    },
    {
      "name": "Candidate B",
      "description": "Candidate B description"
    }
  ],
  "settings": {
    "allow_revoting": true,
    "max_votes": 1,
    "require_auth": true
  },
  "attachments": []
}
```

**Fields:**
- `title` (required): Election title (minimum 1 character)
- `description` (optional): Election description
- `start_date` (required): Election start date (ISO 8601 format)
- `end_date` (required): Election end date (ISO 8601 format)
- `is_public` (optional, default: true): Whether the election is public
- `candidates` (required): List of candidates (minimum 2 candidates)
  - `name` (required): Candidate name (minimum 1 character)
  - `description` (optional): Candidate description
- `settings` (optional): Election settings
  - `allow_revoting` (optional, default: true): Whether revoting is allowed
  - `max_votes` (optional, default: 1): Maximum number of votes allowed (minimum: 1)
  - `require_auth` (optional, default: true): Whether authentication is required
- `attachments` (optional): List of PDF file attachments

**Response:** `201 Created`
```json
{
  "id": "election-uuid",
  "title": "Presidential Election 2024",
  "description": "Annual presidential election",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "is_public": true,
  "created_at": "2024-01-01T00:00:00",
  "candidates": [
    {
      "id": "candidate-uuid-1",
      "election_id": "election-uuid",
      "name": "Candidate A",
      "description": "Candidate A description"
    },
    {
      "id": "candidate-uuid-2",
      "election_id": "election-uuid",
      "name": "Candidate B",
      "description": "Candidate B description"
    }
  ],
  "settings": {
    "id": "setting-uuid",
    "election_id": "election-uuid",
    "allow_revoting": true,
    "max_votes": 1,
    "require_auth": true
  },
  "attachments": []
}
```

---

### GET `/api/v1/elections`

Get all elections with pagination.

**Authentication:** Not required (may vary based on your security requirements)

**Query Parameters:**
- `page` (optional, default: 1): Page number (minimum: 1)
- `page_size` (optional, default: 10): Number of items per page (minimum: 1, maximum: 100)

**Response:** `200 OK`
```json
[
  {
    "id": "election-uuid-1",
    "title": "Presidential Election 2024",
    "description": "Annual presidential election",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59",
    "is_public": true,
    "created_at": "2024-01-01T00:00:00",
    "candidates": [],
    "settings": null,
    "attachments": []
  }
]
```

---

### GET `/api/v1/elections/{election_id}`

Get election by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `election_id` (required): Election UUID

**Response:** `200 OK`
```json
{
  "id": "election-uuid",
  "title": "Presidential Election 2024",
  "description": "Annual presidential election",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "is_public": true,
  "created_at": "2024-01-01T00:00:00",
  "candidates": [],
  "settings": null,
  "attachments": []
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Election with id {election_id} not found"
}
```

---

### PUT `/api/v1/elections/{election_id}`

Update election information.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `election_id` (required): Election UUID

**Request Body:**
```json
{
  "title": "Updated Election Title",
  "description": "Updated description",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "is_public": false,
  "candidates": [
    {
      "name": "Updated Candidate A",
      "description": "Updated description"
    }
  ],
  "settings": {
    "allow_revoting": false,
    "max_votes": 2,
    "require_auth": true
  },
  "attachments": []
}
```

**Fields (all optional):**
- `title`: Election title (minimum 1 character)
- `description`: Election description
- `start_date`: Election start date (ISO 8601 format)
- `end_date`: Election end date (ISO 8601 format)
- `is_public`: Whether the election is public
- `candidates`: List of candidates (minimum 2 if provided)
- `settings`: Election settings
- `attachments`: List of PDF file attachments

**Response:** `200 OK`
```json
{
  "id": "election-uuid",
  "title": "Updated Election Title",
  "description": "Updated description",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "is_public": false,
  "created_at": "2024-01-01T00:00:00",
  "candidates": [],
  "settings": null,
  "attachments": []
}
```

---

### DELETE `/api/v1/elections/{election_id}`

Delete election by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `election_id` (required): Election UUID

**Response:** `200 OK`
```json
{
  "detail": "Election with id {election_id} deleted successfully"
}
```

---

## Vote Endpoints

### POST `/api/v1/votes`

Create a new vote.

**Authentication:** Required

**Request Body:**
```json
{
  "election_id": "election-uuid",
  "candidate_id": "candidate-uuid"
}
```

**Fields:**
- `election_id` (required): Election UUID
- `candidate_id` (required): Candidate UUID

**Response:** `201 Created`
```json
{
  "id": "vote-uuid",
  "election_id": "election-uuid",
  "voter_id": "user-uuid",
  "candidate_id": "candidate-uuid",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### GET `/api/v1/votes`

Get all votes with pagination.

**Authentication:** Not required (may vary based on your security requirements)

**Query Parameters:**
- `page` (optional, default: 1): Page number (minimum: 1)
- `page_size` (optional, default: 10): Number of items per page (minimum: 1, maximum: 100)

**Response:** `200 OK`
```json
[
  {
    "id": "vote-uuid-1",
    "election_id": "election-uuid",
    "voter_id": "user-uuid-1",
    "candidate_id": "candidate-uuid",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": "vote-uuid-2",
    "election_id": "election-uuid",
    "voter_id": "user-uuid-2",
    "candidate_id": "candidate-uuid",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### GET `/api/v1/votes/{vote_id}`

Get vote by ID.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `vote_id` (required): Vote UUID

**Response:** `200 OK`
```json
{
  "id": "vote-uuid",
  "election_id": "election-uuid",
  "voter_id": "user-uuid",
  "candidate_id": "candidate-uuid",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Vote with id {vote_id} not found"
}
```

---

### GET `/api/v1/votes/election/{election_id}`

Get all votes for a specific election.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `election_id` (required): Election UUID

**Response:** `200 OK`
```json
[
  {
    "id": "vote-uuid-1",
    "election_id": "election-uuid",
    "voter_id": "user-uuid-1",
    "candidate_id": "candidate-uuid",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": "vote-uuid-2",
    "election_id": "election-uuid",
    "voter_id": "user-uuid-2",
    "candidate_id": "candidate-uuid",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### GET `/api/v1/votes/user/{user_id}`

Get all votes by a specific user.

**Authentication:** Not required (may vary based on your security requirements)

**Path Parameters:**
- `user_id` (required): User UUID

**Response:** `200 OK`
```json
[
  {
    "id": "vote-uuid-1",
    "election_id": "election-uuid-1",
    "voter_id": "user-uuid",
    "candidate_id": "candidate-uuid-1",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": "vote-uuid-2",
    "election_id": "election-uuid-2",
    "voter_id": "user-uuid",
    "candidate_id": "candidate-uuid-2",
    "created_at": "2024-01-02T00:00:00"
  }
]
```

---

### GET `/api/v1/votes/election/{election_id}/my-vote`

Get current user's vote for a specific election.

**Authentication:** Required

**Path Parameters:**
- `election_id` (required): Election UUID

**Response:** `200 OK`
```json
{
  "id": "vote-uuid",
  "election_id": "election-uuid",
  "voter_id": "user-uuid",
  "candidate_id": "candidate-uuid",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Vote for election {election_id} by user {user_id} not found"
}
```

---

### PUT `/api/v1/votes/{vote_id}`

Update vote information.

**Authentication:** Required

**Path Parameters:**
- `vote_id` (required): Vote UUID

**Request Body:**
```json
{
  "election_id": "election-uuid",
  "voter_id": "user-uuid",
  "candidate_id": "new-candidate-uuid"
}
```

**Fields (all optional):**
- `election_id`: Election UUID
- `voter_id`: User UUID
- `candidate_id`: Candidate UUID

**Response:** `200 OK`
```json
{
  "id": "vote-uuid",
  "election_id": "election-uuid",
  "voter_id": "user-uuid",
  "candidate_id": "new-candidate-uuid",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### DELETE `/api/v1/votes/{vote_id}`

Delete vote by ID.

**Authentication:** Required

**Path Parameters:**
- `vote_id` (required): Vote UUID

**Response:** `200 OK`
```json
{
  "detail": "Vote with id {vote_id} deleted successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Notes

- All timestamps are in ISO 8601 format (e.g., `2024-01-01T00:00:00`)
- All UUIDs are in standard UUID format (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- Pagination parameters apply to list endpoints
- Authentication tokens are stored in httpOnly cookies and are automatically sent with requests
- When authentication is required, include the `access_token` cookie in the request

