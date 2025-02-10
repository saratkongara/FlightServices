# from fixtures.load_fixtures import load_fixtures

# def before_all(context):
#     """
#     Runs once before all tests.
#     """
#     load_fixtures()

import os
import django
import time
import subprocess
from django.test.runner import DiscoverRunner
from django.conf import settings

# ✅ Set Django settings module before anything else
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightServices.settings")

# ✅ Force test database before initializing Django
os.environ["TEST_DB"] = "true"

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

        # ✅ Start Django test server
    print("🚀 Starting Django test server...")
    test_server_process = subprocess.Popen(
        ["python3", "manage.py", "runserver", "8000"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # ⏳ Give the server time to start

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
    test_runner.teardown_databases(context.old_config)
    print("🧹 Database cleaned up!")

    # ✅ Stop Django test server
    if test_server_process:
        print("🛑 Stopping Django test server...")
        test_server_process.terminate()
        test_server_process.wait()
        print("✅ Django test server stopped!")

    print("🧹 Database cleaned up!")