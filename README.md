# The Grumpy Tracker

A web application designed for VFX Matchmove Artists, providing centralized access to camera technical specifications based on make, model, or film/tv project.

## Live Demo

https://www.thegrumpytracker.xyz

## Overview

The Grumpy Tracker serves the VFX community by offering accurate camera technical data essential for shot tracking and matchmoving work. Users can browse camera manufacturers, search for specific models, and access project-specific camera information sourced from verified industry data.

## Features

- **Camera Database**: Comprehensive catalog of camera makes and models with detailed technical specifications
- **Project Integration**: Search cameras by film/TV projects with TMDB integration
- **Format Tracking**: Camera format specifications with community voting system
- **User Authentication**: Secure user accounts with role-based access
- **Community Features**: User-contributed data with source verification
- **Advanced Search**: Search by manufacturer, model, format, or project

## Technical Stack

### Backend

- **Framework**: Django 5.2
- **Database**: PostgreSQL
- **Authentication**: Custom JWT middleware
- **Testing**: Pytest with Django integration
- **API Documentation**: Bruno collections included

### Frontend

- **Framework**: React 19 with Vite
- **UI Library**: React Bootstrap
- **State Management**: React Context API
- **HTTP Client**: Axios with automatic camelCase conversion
- **Testing**: Vitest with React Testing Library
- **Styling**: Bootstrap 5 with custom CSS

## Project Structure

```
capstone2/
├── backend/
│   ├── grumpytracker/          # Django project
│   │   ├── cameras/            # Camera models and views
│   │   ├── makes/             # Manufacturer data
│   │   ├── formats/           # Format specifications
│   │   ├── projects/          # Film/TV project data
│   │   ├── sources/           # Data source tracking
│   │   └── users/             # User management
│   └── grumpy/                # Bruno API tests
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Route components
│   │   ├── context/          # React contexts
│   │   ├── services/         # API client
│   │   └── hooks/            # Custom React hooks
│   └── public/               # Static assets
```

## Installation & Setup

### Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL
- Git

### Backend Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd capstone2/backend
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e .
```

4. Set up environment variables:
   Create a `.env` file in the backend directory:

```env
DB_NAME=grumpy_tracker
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

5. Set up database:

```bash
cd grumpytracker
python manage.py migrate
python manage.py createsuperuser
```

6. Start development server:

```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd ../frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create environment file:
   Create a `.env` file in the frontend directory:

```env
VITE_BASE_URL=http://127.0.0.1:8000
```

4. Start development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Development

### Running Tests

Backend tests:

```bash
cd backend/grumpytracker
pytest
```

Frontend tests:

```bash
cd frontend
npm test
```

### Code Quality

Backend linting:

```bash
cd backend
ruff check .
```

Frontend linting:

```bash
cd frontend
npm run lint
```

## Data Models

### Core Models

- **Make**: Camera manufacturers (ARRI, RED, Sony, etc.)
- **Camera**: Individual camera models with technical specifications
- **Format**: Recording formats with resolution and codec details
- **Project**: Film/TV projects with associated cameras and formats
- **Source**: Data source tracking for verification
- **User**: User accounts with role-based permissions

### Key Relationships

- Cameras belong to Makes (many-to-one)
- Projects can use multiple Cameras (many-to-many)
- Projects have Formats with voting system (many-to-many through ProjectFormat)
- Users can vote on Project-Format combinations

## API Endpoints

### Authentication

- `POST /api/v1/users/auth` - User login
- `DELETE /api/v1/users/auth` - User logout
- `POST /api/v1/users/` - User registration

### Core Resources

- `GET /api/v1/makes/` - List all manufacturers
- `GET /api/v1/cameras/` - List all cameras
- `GET /api/v1/formats/` - List all formats
- `GET /api/v1/projects/` - List all projects
- `GET /api/v1/sources/` - List all data sources

### Search Endpoints

- `GET /api/v1/cameras/search?q=<query>` - Search cameras
- `GET /api/v1/formats/search` - Search formats
- `GET /api/v1/projects/search?q=<query>` - Search projects

## Testing Status

- **Backend**: 14 test files covering models and views for all apps
- **Frontend**: 9 test files with component and page tests
- **API Testing**: Complete Bruno collection for all endpoints

---

_Built with ❤️ for the VFX community_
