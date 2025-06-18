# Manufacturing REST API Server

A comprehensive Flask-based server that serves **two distinct purposes**:

1. **HTML/Web Interface** for database management and demonstration
2. **REST API Endpoints** for Komax IT system integration

## 🎯 **Dual Purpose Architecture**

### Purpose 1: HTML/Web Interface for Database Management
- **Target Users**: Operators, technicians, demonstration purposes
- **Access**: Web browser interface at `http://localhost:5000/interface`
- **Functionality**: 
  - View all manufacturing data in HTML tables
  - Add new contacts, wires, processes, recipes via web forms
  - Edit existing data through user-friendly forms
  - Delete records with confirmation
  - Real-time database updates

### Purpose 2: REST API for Komax IT System Integration
- **Target Users**: Customer IT systems, automation, integration
- **Access**: REST API endpoints at `/api/v1/*`
- **Functionality**:
  - Full CRUD operations via JSON API
  - Machine control commands
  - Programmatic access to manufacturing data
  - Integration with customer MES/ERP systems

## 🚀 Features

- **Dual Interface Support**: 
  - Web interface for human operators
  - REST API for system integration
- **Complete CRUD Operations**: Full Create, Read, Update, Delete support for all entities
- **Database Integration**: SQLite database with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing enabled for API endpoints
- **Device Control**: Machine control commands via REST API
- **Comprehensive Documentation**: Built-in API documentation endpoint

## 📊 Data Entities

The server manages the following manufacturing entities:

- **Contacts**: Terminal contacts with specifications
- **Wires**: Wire specifications and properties
- **Processes**: Manufacturing process parameters
- **Recipes**: Assembly recipes combining contacts, wires, and processes
- **Jobs**: Manufacturing job management
- **Setups**: Machine setup configurations
- **Commands**: Device control commands

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd lab_http_server
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database** (optional - will be created automatically):
   ```bash
   python populate_db.py
   ```

4. **Run the server**:
   ```bash
   python main.py
   ```

The server will start on `http://localhost:5000/interface`

## 📖 Usage

### Purpose 1: HTML/Web Interface for Database Management

#### Web Interface Endpoints

- **Home Page**: `http://localhost:5000/interface` - Main dashboard with all data tables
- **Add Data Forms**:
  - `http://localhost:5000/add_contact` - Add new contacts
  - `http://localhost:5000/add_wire` - Add new wires
  - `http://localhost:5000/add_process` - Add new processes
  - `http://localhost:5000/add_recipe` - Add new recipes
- **Edit Data Forms**:
  - `http://localhost:5000/edit_contact?id=1` - Edit contact
  - `http://localhost:5000/edit_wire?id=1` - Edit wire
  - `http://localhost:5000/edit_process?id=1` - Edit process
  - `http://localhost:5000/edit_recipe?id=1` - Edit recipe
- **Demo API**: `http://localhost:5000/api/demo` - JSON overview of current data

#### Web Interface Features
- **User-friendly forms** for data entry
- **Real-time validation** and error handling
- **Automatic redirects** after operations
- **Responsive design** for different screen sizes
- **Direct database access** through web forms

### Purpose 2: REST API for Komax IT System Integration

#### REST API Endpoints

All API endpoints follow the pattern: `/api/v1/{entity}`

##### Base URL
```
http://localhost:5000/api/v1
```

##### Available Resources

| Entity | Endpoints | Description |
|--------|-----------|-------------|
| `contacts` | GET, POST, PUT, DELETE | Terminal contacts management |
| `wires` | GET, POST, PUT, DELETE | Wire specifications |
| `processes` | GET, POST, PUT, DELETE | Manufacturing processes |
| `recipes` | GET, POST, PUT, DELETE | Assembly recipes (with full details) |
| `jobs` | GET, POST, PUT, DELETE | Job management |
| `setups` | GET, POST, PUT, DELETE | Machine setups |
| `commands` | GET, POST, PUT, DELETE | Device commands |

##### API Documentation

- **API Docs**: `GET /api/v1/docs` - Complete API documentation

##### Device Control

- **Device Commands**: `POST /api/v1/device/commands` - Execute machine commands

#### REST API Features
- **JSON-based communication** for system integration
- **Standard HTTP methods** (GET, POST, PUT, DELETE)
- **CORS enabled** for cross-origin requests
- **Error handling** with proper HTTP status codes
- **Data validation** and integrity checks

## 🔧 API Examples for Komax IT Integration

### Get All Contacts
```bash
curl -X GET http://localhost:5000/api/v1/contacts
```

### Get Specific Contact
```bash
curl -X GET http://localhost:5000/api/v1/contacts/1
```

### Create New Contact
```bash
curl -X POST http://localhost:5000/api/v1/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "Description": "New Contact",
    "Diameter": "15.0",
    "Insertdepth": "25.0",
    "Name": "NC001",
    "ZF_ContNumb": "10.0"
  }'
```

### Update Contact
```bash
curl -X PUT http://localhost:5000/api/v1/contacts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "Description": "Updated Contact"
  }'
```

### Delete Contact
```bash
curl -X DELETE http://localhost:5000/api/v1/contacts/1
```

### Start Recipe (Machine Control)
```bash
curl -X POST http://localhost:5000/api/v1/device/commands \
  -H "Content-Type: application/json" \
  -d '{
    "command": "start_recipe",
    "parameters": {
      "recipe_id": 1
    }
  }'
```

### Reset Machine
```bash
curl -X POST http://localhost:5000/api/v1/device/commands \
  -H "Content-Type: application/json" \
  -d '{
    "command": "reset",
    "parameters": {}
  }'
```

## 🧪 Testing

### Test Web Interface
1. Open browser and navigate to `http://localhost:5000/interface`
2. Use the web forms to add, edit, and delete data
3. Verify changes are reflected in the database

### Test REST API
Run the comprehensive test suite:

```bash
python test_api.py
```

This will test all API endpoints and demonstrate functionality.

## 📁 Project Structure

```
lab_http_server/
├── main.py              # Main Flask application (both interfaces)
├── populate_db.py       # Database population script
├── test_api.py          # API test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── instance/
│   └── manufacturing.db # SQLite database (shared by both interfaces)
└── templates/          # HTML templates for web interface
    ├── index.html      # Main dashboard
    ├── add_contact.html
    ├── add_wire.html
    ├── add_process.html
    ├── add_recipe.html
    ├── edit_contact.html
    ├── edit_wire.html
    ├── edit_process.html
    └── edit_recipe.html
```

## 🔒 Security Notes

- **Authentication**: Currently disabled for demonstration purposes
- **CORS**: Enabled for all origins on API endpoints
- **Database**: SQLite file-based database (shared by both interfaces)
- **Production Use**: Add authentication and proper security measures for production deployment

## 🌐 Response Formats

### Web Interface
- **HTML pages** for human interaction
- **Form-based data entry** and validation
- **Redirect responses** after operations

### REST API
- **JSON responses** for system integration
- **Standard HTTP status codes**
- **Error messages** in JSON format

#### Success Response
```json
{
  "id": 1,
  "name": "Example",
  "description": "Example description"
}
```

#### Error Response
```json
{
  "error": "Error description"
}
```

#### List Response
```json
[
  {
    "id": 1,
    "name": "Item 1"
  },
  {
    "id": 2,
    "name": "Item 2"
  }
]
```

## 🚀 Deployment

### Development
```bash
python main.py
```

### Production
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Adding authentication and authorization
- Implementing rate limiting
- Using a production database (PostgreSQL, MySQL)
- Setting up proper logging and monitoring

## 📞 Support

### For Web Interface Users
- Access the main dashboard at `http://localhost:5000/interface`
- Use the navigation links to add, edit, or delete data
- Check the demo endpoint at `/api/demo` for data overview

### For Komax IT System Integration
- Check the API documentation at `/api/v1/docs`
- Use the REST API endpoints at `/api/v1/*`
- Run the test suite with `python test_api.py`
- Review the API examples in this README

## 📄 License

This project is for demonstration and educational purposes.

## 🔄 Version History

- **v1.0**: Initial release with dual interface implementation
  - HTML/Web interface for database management
  - REST API endpoints for Komax IT system integration
  - Complete CRUD operations for all entities
  - Device control endpoints
  - Comprehensive documentation and testing
