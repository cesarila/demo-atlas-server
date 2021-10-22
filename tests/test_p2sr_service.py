import pytest
from app.services import p2sr

def test_fetch_new_display_name():
    my_steam_id = 76561198084554697
    my_display_name = "Luke"
    assert my_display_name == p2sr.get_display_name(my_steam_id)