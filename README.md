# FlightServices

## Steps to run the API automation tests

### Clone the repository
git clone https://github.com/saratkongara/FlightServices.git
cd FlightServices

### Setup virtual environment and install the dependencies
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

### Run the API automation tests
behave

## Steps to run the dev server

# Run the migrations
python3 manage.py makemigrations (only if you make changes to models)
python3 manage.py migrate

# Create the super user to setup the api user and token
python3 manage.py createsuperuser (superuser creation)

You can login as the superuser to the admin panel and create additional users.

# Start the server
python3 manage.py runserver