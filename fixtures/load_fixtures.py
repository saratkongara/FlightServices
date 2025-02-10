from django.core.management import call_command

FIXTURE_ORDER = [
    "fixtures/users.json",
    "fixtures/tokens.json",
    "fixtures/flights.json",
    "fixtures/passengers.json"
]

def load_fixtures():
    for fixture in FIXTURE_ORDER:
        print(f"Loading {fixture}...")
        call_command("loaddata", fixture)

if __name__ == "__main__":
    load_fixtures()
