# Salesforce Access Lens

> An enterprise-grade Python application that analyzes and explains Salesforce user access through Profiles, Permission Sets, Permission Set Groups, Object Permissions, Field Permissions, and App Assignments.
>
> Built using Clean Architecture, SOLID principles, Object-Oriented Design, and exposed through the Model Context Protocol (MCP).

---

## Overview

Salesforce organizations often struggle to answer questions like:

- Why can this user access this object?
- Which Permission Set grants this field access?
- Does the Profile or a Permission Set Group provide this permission?
- Why can't this user see an application?
- Which Permission Set is responsible for a specific capability?

Salesforce Access Lens aims to provide a single source of truth for understanding and explaining Salesforce access by combining metadata, security assignments, and permission analysis into an easy-to-consume interface.

The application is designed to expose these capabilities through **Model Context Protocol (MCP)** so AI assistants and external applications can query Salesforce security intelligently.

---

# Goals

- Authenticate securely using Salesforce JWT Bearer Flow
- Build a reusable Salesforce API client
- Execute SOQL queries safely
- Retrieve Salesforce security metadata
- Resolve effective user permissions
- Explain *why* a user has a permission
- Expose security analysis through MCP tools
- Follow enterprise software engineering best practices

---

# Current Features

- JWT Bearer Authentication
- Salesforce OAuth Token Exchange
- Environment-based configuration
- Configuration Factory
- Typed Configuration Models
- Clean dependency injection
- Enterprise package structure

---

# Planned Features

## Authentication

- JWT Bearer Flow
- Session Management
- Automatic Token Refresh

## Salesforce Client

- REST API Client
- SOQL Query Executor
- Query Pagination
- Error Handling
- Retry Strategy

## Security Analysis

- User Lookup
- Profile Analysis
- Permission Set Analysis
- Permission Set Group Analysis
- Object Permissions
- Field Permissions
- Apex Class Access
- Visualforce Access
- Lightning App Access
- Tab Visibility
- Custom Permission Resolution

## Access Resolution Engine

- Effective Object Permissions
- Effective Field Permissions
- Permission Explanation Engine
- Permission Traceability

## MCP Server

- User Access Tool
- Object Access Tool
- Field Access Tool
- Permission Explanation Tool

---

# Project Architecture

```
salesforce-access-lens/
│
├── app/
│
│   ├── config/
│   │
│   ├── salesforce/
│   │   ├── auth/
│   │   ├── client/
│   │   ├── models/
│   │   ├── query/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── exceptions/
│   │
│   ├── mcp/
│   └── utils/
│
├── tests/
├── certs/
├── README.md
├── ARCHITECTURE.md
└── requirements.txt
```

---

# Architecture Principles

This project follows:

- SOLID Principles
- Clean Architecture
- Dependency Injection
- Repository Pattern
- Factory Pattern
- Single Responsibility Principle
- Composition over Inheritance
- Strong Encapsulation
- Type Hinting throughout the project

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application |
| Salesforce REST API | Metadata & Security |
| JWT Bearer Flow | Authentication |
| Requests | HTTP Communication |
| PyJWT | JWT Generation |
| python-dotenv | Environment Configuration |
| MCP | AI Integration |

---

# Getting Started

## Clone Repository

```bash
git clone <repository-url>
cd salesforce-access-lens
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment File

Create a `.env` file in the project root.

Example:

```env
SF_CONSUMER_KEY=
SF_USERNAME=
SF_LOGIN_URL=https://login.salesforce.com
SF_PRIVATE_KEY_PATH=
SF_API_VERSION=v64.0
```

---

## Run

```bash
python -m app.main
```

---

# Development Philosophy

Every component in this project is designed before implementation.

The project prioritizes:

- Readability
- Maintainability
- Extensibility
- Testability

Architecture decisions are documented in `ARCHITECTURE.md`.

---

# Roadmap

## Foundation
- [x] Project Setup
- [x] Environment Configuration
- [x] JWT Authentication
- [x] Salesforce REST Client
- [x] SOQL Query Executor

## Domain Layer
- [x] SalesforceUser Entity
- [x] Profile Entity
- [ ] PermissionSet Entity
- [ ] PermissionSetGroup Entity
- [ ] ObjectPermission Entity
- [ ] FieldPermission Entity

## Data Access Layer
- [x] User Repository
- [ ] Profile Repository
- [ ] Permission Set Repository
- [ ] Permission Set Group Repository
- [ ] Object Permission Repository
- [ ] Field Permission Repository

## Application Layer
- [ ] Access Resolution Engine
- [ ] Access Explanation Engine
- [ ] Permission Analysis Service

## MCP Integration
- [ ] MCP Server
- [ ] MCP Tools

## Quality
- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Documentation

---

# License

This project is licensed under the MIT License.

---

# Author

**Sidharth Pushp**

Salesforce Tech Lead

Building enterprise software with Python and Salesforce.