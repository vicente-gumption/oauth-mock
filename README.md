# OAuth Mock Server
This is a simple Flask python application that mimics the OAuth API of LinkedIn and FusionAuth with support for CORS.

## Local Setup
```bash
python -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run the application

```bash
python app.py
```

### Run from VS Code

Create a new run/debug configuration and set it as follows:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "args": ["run"],
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development"
            },
            "jinja": true
        }
    ]
}
```

## Test

Upon start, a server is ready listening in port 15000.

To see the list of routes available, execute:

```bash
python -m flask routes
```