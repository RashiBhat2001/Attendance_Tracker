# Student Attendance Viewer

## Overview

A Flask-based web application that allows students to view their attendance records by authenticating with their student credentials. The application integrates with Google Sheets to retrieve student credentials and attendance data, providing a clean Material Design interface for viewing current attendance statistics and historical records.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Design System**: Material Design with Tailwind CSS
- Mobile-first responsive approach using Tailwind utility classes
- Roboto font family via Google Fonts CDN
- Material Icons for consistent iconography
- Component spacing based on Tailwind primitives (2, 4, 6, 8 units)
- Responsive breakpoints: mobile (base), tablet (`md:`), desktop (`lg:`)

**Template Structure**: Jinja2 template inheritance pattern
- `base.html` - Base layout with common resources and styles
- `login.html` - Authentication interface
- `dashboard.html` - Main attendance overview
- `history.html` - Historical attendance records with date filtering
- `profile.html` - Account settings and password management

**Rationale**: Material Design provides excellent patterns for data-dense dashboards while maintaining clarity. The template inheritance pattern ensures DRY principles and consistent UI across pages.

### Backend Architecture

**Web Framework**: Flask with Flask-Login for session management
- ProxyFix middleware for handling reverse proxy headers
- Session-based authentication using Flask-Login
- In-memory user cache for authenticated students
- Environment-based configuration (secrets via environment variables)

**Authentication Flow**:
1. Student credentials stored and validated against Google Sheets
2. Custom `Student` class implements Flask-Login's UserMixin interface
3. In-memory cache (`students_cache`) maintains logged-in user objects
4. Password update capability through profile management

**Rationale**: Flask provides a lightweight, flexible foundation for this student-facing application. In-memory caching is appropriate given the expected user scale and session-based nature of the application.

### Data Storage Solutions

**Primary Data Source**: Google Sheets via Sheets API
- Attendance records stored in spreadsheet tabs/ranges
- Student credentials (ID, name, password) maintained in dedicated sheet
- Historical attendance data queryable by date ranges

**Integration Method**: Direct API calls using OAuth access tokens
- Replit Connectors system manages OAuth credentials
- Token refresh handled through Replit's connector infrastructure
- Environment variables specify spreadsheet ID and connector hostname

**Rationale**: Google Sheets serves as both database and administrative interface, allowing non-technical staff to manage student records and attendance data without requiring database expertise. This reduces operational complexity while maintaining flexibility.

### Authentication and Authorization

**Authentication Mechanism**: Credential-based login with session persistence
- Student ID and password validated against Google Sheets data
- Flask-Login manages session cookies and user state
- `login_required` decorator protects authenticated routes

**Session Management**:
- Secret key loaded from `SESSION_SECRET` environment variable
- User loader function retrieves student objects from in-memory cache
- Logout functionality clears session and redirects to login

**Security Considerations**: 
- Passwords currently stored in plaintext in Google Sheets (appropriate for low-security academic environment)
- Session secrets externalized to environment variables
- No role-based access control (all authenticated users are students with equal permissions)

**Rationale**: Simple credential-based authentication is appropriate for a student-facing attendance viewer where data sensitivity is low and administrative overhead must be minimal.

## External Dependencies

### Third-Party Services

**Google Sheets API (v4)**
- Purpose: Primary data storage and retrieval
- Authentication: OAuth 2.0 via Replit Connectors
- Endpoints used: `/spreadsheets/{id}/values/{range}` for data retrieval
- Configuration: Spreadsheet ID via `GOOGLE_SHEET_ID` environment variable

**Replit Connectors API**
- Purpose: Managed OAuth token retrieval and refresh
- Authentication: Replit identity tokens (`REPL_IDENTITY` or `WEB_REPL_RENEWAL`)
- Hostname: `REPLIT_CONNECTORS_HOSTNAME` environment variable
- Token types: Development (`repl`) and deployment (`depl`)

### Python Libraries

**Core Framework**:
- `Flask` - Web application framework
- `flask-login` - User session management
- `werkzeug.middleware.proxy_fix` - Reverse proxy support

**HTTP Client**:
- `requests` - Google Sheets API communication

### Frontend Resources (CDN)

**Styling & Typography**:
- Tailwind CSS (via CDN) - Utility-first CSS framework
- Google Fonts (Roboto) - Typography
- Material Icons - Iconography

### Environment Variables Required

- `SESSION_SECRET` - Flask session encryption key
- `GOOGLE_SHEET_ID` - Target spreadsheet identifier
- `REPLIT_CONNECTORS_HOSTNAME` - Connector API endpoint
- `REPL_IDENTITY` or `WEB_REPL_RENEWAL` - Replit authentication token

### Node.js Dependencies

**googleapis** (v148.0.0) - Google APIs client library
- Note: Package present in repository but not actively used in Python codebase
- May be intended for future Node.js-based extensions or utilities