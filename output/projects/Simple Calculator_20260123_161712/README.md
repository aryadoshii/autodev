# Simple Calculator API

A RESTful API for a simple calculator application with full CRUD operations and persistent storage.

## Features

- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Clear functionality to reset the calculator
- Display of current input and results
- Handle decimal numbers
- Error handling for invalid operations (like division by zero)
- Keyboard support for input
- Persistent storage using SQLite
- Comprehensive API documentation

## Tech Stack

- Backend: FastAPI
- Database: SQLite (via SQLAlchemy)
- ORM: SQLAlchemy
- API Documentation: OpenAPI/Swagger

## Setup Instructions

1. **Clone the repository**
   bash
   git clone <repository-url>
   cd simple-calculator-api
   

2. **Install dependencies**
   bash
   pip install -r requirements.txt
   

3. **Run the application**
   bash
   python main.py
   

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Environment Variables

No environment variables required. The application uses a local SQLite database by default.

## Project Structure


.
├── main.py          # Main application file
├── database.py      # Database configuration
├── models.py        # SQLAlchemy models
├── requirements.txt # Dependencies
└── README.md        # This file



## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.