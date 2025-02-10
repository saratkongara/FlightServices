import json
import requests
from behave import given, when, then
from requests.auth import HTTPBasicAuth

@given('I make a {method} request to {endpoint}')
def step_make_request(context, method, endpoint):
    """ Initializes a request with method and endpoint. """
    context.method = method.upper()
    context.endpoint = endpoint
    context.headers = {}
    context.params = {}
    context.cookies = {}
    context.data = None
    context.files = None
    context.response = None
    context.stored_values = {}  # Store dynamic values from responses

@given('I set header {key} to {value}')
def step_set_header(context, key, value):
    """ Adds a header to the request. """
    context.headers[key] = value

@given('I set query param {key} to {value}')
def step_set_query_param(context, key, value):
    """ Adds a query parameter to the request. """
    context.params[key] = value

@given('I set cookie {key} to {value}')
def step_set_cookie(context, key, value):
    """ Sets a cookie in the request. """
    context.cookies[key] = value

@given('I set Basic Auth with username {username} and password {password}')
def step_set_basic_auth(context, username, password):
    """ Configures Basic Authentication. """
    context.auth = HTTPBasicAuth(username, password)

@given('I set Bearer Token from stored value {key}')
def step_set_bearer_token(context, key):
    """ Sets Authorization header using a previously stored value. """
    token = context.stored_values.get(key, "")
    context.headers["Authorization"] = f"Bearer {token}"

@given('I set Token from stored value {key}')
def step_set_bearer_token(context, key):
    """ Sets Authorization header using a previously stored value. """
    token = context.stored_values.get(key, "")
    context.headers["Authorization"] = f"Token {token}"

@given('I set body to')
def step_set_body(context):
    """ Sets JSON body from the step input. """
    try:
        context.data = json.loads(context.text)
    except json.JSONDecodeError:
        context.data = context.text

@given('I upload file {filename} for form param {param}')
def step_upload_file(context, filename, param):
    """ Uploads a file as multipart form data. """
    context.files = {param: open(filename, 'rb')}

@when('I send the request')
def step_send_request(context):
    """ Sends the API request and stores the response. """
    context.response = requests.request(
        method=context.method,
        url=context.endpoint,
        headers=context.headers,
        params=context.params,
        cookies=context.cookies,
        json=context.data,
        auth=getattr(context, "auth", None),
        files=context.files
    )
    if context.files:
        for file in context.files.values():
            file.close()  # Ensure files are properly closed

@then('I expect response status to be {status_code:d}')
def step_expect_status(context, status_code):
    """ Validates response status code. """
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"

@then('I expect response header {key} to be {value}')
def step_expect_header(context, key, value):
    """ Validates a response header. """
    assert context.response.headers.get(key) == value, f"Expected {key}: {value}, got {context.response.headers.get(key)}"

@then('I expect response to have a cookie {key}')
def step_expect_cookie(context, key):
    """ Checks if a response contains a specific cookie. """
    assert key in context.response.cookies, f"Cookie {key} not found"

@then('I expect response should have JSON')
def step_expect_json(context):
    """ Validates the JSON response body. """
    expected_json = json.loads(context.text)
    actual_json = context.response.json()
    assert actual_json == expected_json, f"Expected {expected_json}, got {actual_json}"

@then('I expect JSON response at {path} to be {value}')
def step_expect_json_path(context, path, value):
    """ Validates a specific JSON path in the response. """
    keys = path.split('.')
    json_data = context.response.json()
    for key in keys:
        json_data = json_data.get(key, {})
    assert json_data == json.loads(value), f"Expected {path} to be {value}, but got {json_data}"

@then('I store JSON response at {path} as {key}')
def step_store_json_value(context, path, key):
    """ Stores a JSON response value for later use. """
    keys = path.split('.')
    json_data = context.response.json()
    for key_part in keys:
        json_data = json_data.get(key_part, {})
    context.stored_values[key] = json_data

@then('I expect response time to be less than {ms:d} ms')
def step_expect_response_time(context, ms):
    """ Validates that response time is within a limit. """
    actual_time = context.response.elapsed.total_seconds() * 1000  # Convert to ms
    assert actual_time < ms, f"Expected response time < {ms}ms, but got {actual_time:.2f}ms"
