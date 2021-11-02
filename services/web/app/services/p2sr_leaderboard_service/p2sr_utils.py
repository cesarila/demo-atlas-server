import json

def is_ok(response):
    return response.status_code == 200

def extract_display_name(response):
    return json.loads(response.data)['displayName']