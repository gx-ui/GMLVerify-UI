# GMLVerify-UI Data Validation Platform

A data validation platform based on front-end and back-end separation architecture, supporting multiple data source connections and data quality expectation management.

## Project Overview

GMLVerify-UI is a modern data validation platform designed to help users manage and validate data quality. The platform provides an intuitive user interface for creating data assets, setting data expectations, and performing data validation.

### Key Features

- 🔗 **Multi-Data Source Connection**: Support for PostgreSQL and other database connections
- 📊 **Data Asset Management**: Create and manage data assets
- ✅ **Data Expectation Setting**: Flexible data quality expectation configuration
- 🎯 **Data Validation**: Automated data quality checks
- 👤 **User Management**: Complete user authentication and authorization system
- 📈 **Data Metrics**: Data quality metrics monitoring

## Technology Stack

### Frontend
- **Framework**: Vue 3.5.13
- **UI Component Library**: Element Plus 2.9.9
- **Build Tool**: Vite 6.x
- **State Management**: Pinia 3.0.2
- **Routing**: Vue Router 4.5.0
- **HTTP Client**: Axios 1.9.0
- **Icons**: Element Plus Icons Vue 2.0.0

### Backend
- **Framework**: FastAPI 0.112.2
- **ASGI Server**: Uvicorn
- **ORM**: Tortoise ORM
- **Database Driver**: asyncpg (PostgreSQL)
- **Data Validation**: Great Expectations
- **Database Migration**: Aerich

## Project Structure
GMLVerify-UI/
├── backend/                     # Backend project
│   ├── api/                     # API interface modules
│   │   ├── db_connect/          # Database connection module
│   │   │   ├── pgsql/           # PostgreSQL connection
│   │   │   └── table_info.py    # Table information retrieval
│   │   ├── expectations/        # Expectation management module
│   │   │   ├── expectation.py   # Expectation definitions
│   │   │   ├── gx_router.py     # Expectation routing
│   │   │   └── gx_service.py    # Expectation services
│   │   ├── user/               # User management module
│   │   │   ├── login.py        # Login interface
│   │   │   └── user.py         # User interface
│   │   ├── utils/              # Utility modules
│   │   └── models.py           # Data models
│   ├── migrations/             # Database migration files
│   ├── main.py                 # FastAPI application entry
│   ├── setting.py              # Configuration file
│   ├── requirements.txt        # Python dependencies
│   └── pyproject.toml          # Project configuration
└── frontend/                   # Frontend project
└── gx-project/
├── src/
│   ├── components/      # Vue components
│   │   ├── expectationForms/  # Expectation form components
│   │   │   ├── Completeness.vue  # Completeness expectations
│   │   │   ├── Numeric.vue      # Numeric expectations
│   │   │   ├── Schema.vue       # Schema expectations
│   │   │   ├── Uniqueness.vue   # Uniqueness expectations
│   │   │   ├── Validity.vue     # Validity expectations
│   │   │   └── Volume.vue       # Volume expectations
│   │   ├── Login.vue           # Login component
│   │   ├── NewDataAsset.vue    # New data asset
│   │   ├── CreateExpectations.vue  # Create expectations
│   │   ├── HeaderBar.vue       # Header navigation
│   │   └── LeftSidebar.vue     # Left sidebar
│   ├── views/              # Page views
│   │   ├── Home.vue           # Home page
│   │   ├── CreateDataAssets.vue   # Create data assets page
│   │   ├── ExistingDataAssets.vue # Existing data assets page
│   │   ├── AssetDetail.vue    # Asset detail page
│   │   └── detail/            # Detail sub-pages
│   │       ├── Expectations.vue   # Expectation management
│   │       ├── Validation.vue     # Validation results
│   │       └── Metric.vue         # Data metrics
│   ├── router/             # Router configuration
│   ├── config.js           # Configuration file
│   └── main.js             # Application entry
├── package.json            # Frontend dependencies
└── vite.config.js          # Vite configuration


## Quick Start

### Requirements

- **Node.js**: >= 16.0.0
- **Python**: >= 3.7.7
- **PostgreSQL**: >= 12.0

### Backend Setup

1. **Clone the project**
```bash
git clone <repository-url>
cd GMLVerify-UI
cd backend
pip install -r requirements.txt

2.Configure database
Edit the backend/setting.py file and modify the database connection information:
```
## API Documentation
After starting the backend service, you can access the API documentation at:

- Swagger UI : http://localhost:8080/docs
## Main Functional Modules
### 1. User Authentication
- User login/registration
- User information management
- Session management
### 2. Data Source Management
- PostgreSQL database connection
- Connection testing and validation
- Data source configuration management
- Table structure information retrieval
### 3. Data Asset Management
- Create and manage data assets
- Data table selection and configuration
- Asset metadata management
- Asset detail viewing
### 4. Data Expectation Management
- Completeness Expectations : Check data completeness
- Numeric Expectations : Numeric range and statistical validation
- Schema Expectations : Data structure validation
- Uniqueness Expectations : Data uniqueness checks
- Validity Expectations : Data format and rule validation
- Volume Expectations : Data volume statistical validation
### 5. Data Validation
- Automated data quality checks
- Validation result display
- Failure case analysis
- Historical validation records
### 6. Data Metrics
- Data quality metrics monitoring
- Trend analysis
- Report generation
## Data Models
The project uses the following main data models:

- User : User information
- DataSource : Data source configuration
- DataAsset : Data assets
- ExpectationSuite : Expectation suites
- ValidationResult : Validation results
## Development Guide
### Frontend Development
- Use Vue 3 Composition API
- Follow Element Plus design specifications
- Component-based development for improved code reusability
- Use Pinia for state management
### Backend Development
- Use FastAPI asynchronous framework
- Tortoise ORM for database operations
- RESTful API design principles
- Integrate Great Expectations for data validation
## Contact
For questions or suggestions, please contact:

- Email: guoxuan@gml.ac.cn
## Changelog
### v1.0 (Current Version)
- Initial project setup
- Basic user authentication functionality
- PostgreSQL data source connection
- Basic data asset and expectation management functionality
- Data validation and metrics display
- Multiple expectation type support