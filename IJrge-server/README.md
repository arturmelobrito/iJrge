# Flask API Project

This is a simple Flask API project that includes a health check endpoint. 

## Project Structure

```
flask-api-project
├── src
│   ├── app.py
│   ├── config.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── routes.py
│   ├── models
│   │   └── __init__.py
│   ├── services
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_health.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python src/app.py
   ```

## Usage

Once the application is running, you can access the health check endpoint at:

```
http://localhost:5000/health
```

This will return a JSON response indicating the health status of the application:

```json
{
  "status": "healthy"
}
```

## Contributing

Feel free to submit issues or pull requests for any improvements or features you would like to see in this project.