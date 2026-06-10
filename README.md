# About Project

# Blog REST API

A complete Blog REST API built with Django REST Framework (DRF). This project provides authentication, blog post management, user management, comments, likes, search functionality, pagination, and API documentation.

## Features

### Authentication

* User registration
* JWT authentication using SimpleJWT
* Protected endpoints for authenticated users

### User Management

* List users (Admin only)
* Retrieve own profile
* Update own profile
* Delete users (Admin only)
* Search users by username

### Blog Posts

* Create blog posts
* Retrieve all posts
* Retrieve a specific post
* Update own posts
* Delete own posts
* Search posts by:

  * Title
  * Category
  * Tags

### Comments

* Add comments to posts
* Delete own comments
* Retrieve comments for a specific post
* Retrieve all comments (Admin only)
* Delete any comment (Admin only)

### Likes

* Like / Unlike posts using a toggle endpoint
* Retrieve likes for a specific post
* Prevent duplicate likes using database constraints

### Other Important Features
* PostgreSQL database
* Pagination
* Swagger/OpenAPI documentation
* Uses Viewsets & Router
* Nested serializers for cleaner API responses
* Category and Tags support for blog's posts
* Comment count per post
* Like count per post

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication (SimpleJWT)
* DRF Spectacular (Swagger)

---

## Database Setup

This project uses PostgreSQL.

Configure your PostgreSQL credentials inside your environment variables or settings.py file and then migrate.

---

## API Documentation

Swagger UI:

```text
/api/docs/
```

OpenAPI Schema:

```text
/api/schema/
```

Note: Since the project uses custom ViewSets and custom actions, Swagger may not fully infer some endpoints. For complete implementation details, please refer to the source code.

---

## JWT Authentication

Obtain JWT token:

```text
/api/users/login/
```

Refresh JWT token:

```text
/api/token/refresh/
```
Verify JWT token:

```text
/api/token/verify/
```

Include the token in request headers:

```text
Authorization: Bearer <access_token>
```

---

## Search Examples

Search users:

```text
/api/users/search/?username=danial
```

Search posts:

```text
/api/posts/search/?about=django
```

---

## Pagination

List endpoints support pagination.

Example:

```text
/api/posts/?page=2
```

## Project Purpose

This project was developed as a learning and portfolio project to practice building a complete RESTful API using Django REST Framework and PostgreSQL.

---
