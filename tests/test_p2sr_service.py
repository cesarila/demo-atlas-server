import pytest, json
from app.services import p2sr, p2sr_response

def test_get_display_name():
    my_steam_id = 76561198084554697
    my_display_name = "Luke"
    response = p2sr.get_display_name(my_steam_id)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['displayName'] == my_display_name