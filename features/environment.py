import os
import django
import time
import subprocess
from django.test.runner import DiscoverRunner
from django.conf import settings

# ✅ Set Django settings module before anything else
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightServices.settings")

# ✅ Force test database before initializing Django
os.environ["DJANGO_ENV"] = "test"

# ✅ Initialize Django
django.setup()

print(f"✅ Django is using database: {settings.DATABASES['default']['NAME']}")

# ✅ Use Django test runner to set up test database
class TestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        return super().teardown_databases(old_config, **kwargs)

# ✅ Load fixtures before all tests
from fixtures.load_fixtures import load_fixtures

# Global variable to store the test server process
test_server_process = None

def before_all(context):
    """Set up the test environment and load fixtures before all tests."""
    global test_server_process
    test_runner = TestRunner()
    context.old_config = test_runner.setup_databases()
    
    print("📥 Loading test fixtures...")
    load_fixtures()
    print("✅ Fixtures loaded successfully!")

    # ✅ Print user credentials and tokens
    # print_users_and_tokens()

    # ✅ Start Django test server
    print("🚀 Starting Django test server...")
    test_server_process = subprocess.Popen(
        ["python3", "manage.py", "runserver", "9000", "--nothreading", "--noreload"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # ⏳ Give the server time to start

    # ✅ Check if the server is running
    if test_server_process.poll() is None:
        print("✅ Django test server started successfully!")
    else:
        print("❌ Failed to start Django test server!")
        exit(1)

def after_all(context):
    """Clean up after all tests."""
    global test_server_process
    test_runner = TestRunner()

    # ✅ Clean up test database
    test_runner.teardown_databases(context.old_config)
    print("🧹 Database cleaned up!")

    # ✅ Stop Django test server
    if test_server_process:
        print("🛑 Stopping Django test server...")
        test_server_process.terminate()
        test_server_process.wait()
        print("✅ Django test server stopped!")

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.db import connection

def print_users_and_tokens():
    """Fetch and print users' login details and authentication tokens."""
    User = get_user_model()

    print("\n👤 User Credentials and Tokens:")
    print("=" * 50)

    with connection.cursor() as cursor:
        # Fetch users
        cursor.execute("SELECT id, username, password FROM auth_user;")
        users = cursor.fetchall()

        # Fetch tokens
        cursor.execute("SELECT user_id, key FROM authtoken_token;")
        tokens = dict(cursor.fetchall())  # Convert token results to a dictionary {user_id: token}

    for user_id, username, password_hash in users:
        token = tokens.get(user_id, "No Token Found")
        print(f"📌 Username: {username}")
        print(f"🔑 Password Hash: {password_hash}")
        print(f"🆔 Token: {token}")
        print("-" * 50)

import sqlite3

def dump_test_db():
    # ✅ Get test database path (assuming SQLite)
    test_db_path = settings.DATABASES["default"]["NAME"]
    dump_file = "test_db_dump.sql"
    print(f'test_db_path: {test_db_path}')

    # ✅ Dump the database
    if os.path.exists(test_db_path):
        print(f"📦 Dumping test database to {dump_file}...")
        with open(dump_file, "w") as f:
            conn = sqlite3.connect(test_db_path)
            for line in conn.iterdump():
                f.write(f"{line}\n")
            conn.close()
        print(f"✅ Test database dumped successfully to {dump_file}!")