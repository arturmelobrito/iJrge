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
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Create a virtual environment:**
   ```shell
   python3 -m venv venv
   ```
   or
   ```shell
   pipenv shell
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

   OBS: If you used `pipenv` to manage the project there is no need to activate the environment

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```
   or
   ```shell
   pipenv install # After using pipenv shell
   ```

4. **Run the application:**
   ```
   python src/app.py
   ```

## Usage

Once the application is running, you can access the health check endpoint at:

```
http://localhost:5000/api/health
```

This will return a JSON response indicating the health status of the application:

```json
{
  "status": "healthy"
}
```

## Contributing

Feel free to submit issues or pull requests for any improvements or features you would like to see in this project.