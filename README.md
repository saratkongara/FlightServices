# FlightServices

## Steps to run the API automation tests

### Clone the repository
```bash
    git clone https://github.com/saratkongara/FlightServices.git
    cd FlightServices
```

### Setup virtual environment and install the dependencies
```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
```

### Run the API automation tests
```bash
    behave
```

## Steps to run the dev server

# Run the migrations

```bash
    python3 manage.py makemigrations (only if you make changes to models)
    python3 manage.py migrate
```

# Create the super user to setup the api user and token
```bash
    python3 manage.py createsuperuser (superuser creation)
```

You can login as the superuser to the admin panel and create additional users.

# Start the server
```bash
    python3 manage.py runserver
```
