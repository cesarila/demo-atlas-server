import os, pytest
from pytest_postgresql.janitor import DatabaseJanitor
from pytest_postgresql.config import get_config
from dbUtils import get_psql_version
from unittest.mock import patch
from app import create_app, db
from app.models import Player
from datetime import datetime
from globals import *
from app.services import p2sr, p2sr_response

pytest_plugins = ['pytest-flask-sqlalchemy']

@pytest.fixture(scope='session')
def database(request):
    config = get_config(request)
    pg_host = config["host"]
    pg_port = config["port"] or 5432
    pg_user = config["user"]
    pg_pass = config["password"] or "password"
    pg_db = config["dbname"] or "demoatlas_app_test"
    pg_version = get_psql_version()

    janitor = DatabaseJanitor(
        user=pg_user,
        password=pg_pass,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=pg_version
    )
    janitor.init()
    yield
    janitor.drop()

    @request.addfinalizer
    def drop_database():
        try:
            janitor.drop()
        except:
            return


@pytest.fixture(scope='session')
def app(database):
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()

@pytest.fixture(scope='session')
def _db(app):
    db.create_all()
    return db


@pytest.fixture()
def mocked_newname():
    with patch(
            'app.services.p2sr.get_display_name',
            return_value=p2sr_response.success('verycoolupdatedname')):
        yield

@pytest.fixture()
def mocked_player_does_not_exist():
    with patch('app.services.p2sr.get_display_name', side_effect=mocked_player_does_not_exist_side_effect):
        yield


@pytest.fixture()
def mocked_p2sr_down():
    with patch('app.services.p2sr.get_display_name', return_value=p2sr_response.bad_gateway()):
        yield

@pytest.fixture()
def mocked_p2sr_breaking_api_change():
    with patch('app.services.p2sr.get_display_name', return_value=p2sr_response.internal_server_error()):
        yield


@pytest.fixture()
def force_update_condition():
    with patch('app.services.time.utc_now', return_value=datetime.utcnow()+MINIMUM_TIME_BEFORE_UPDATE*2):
        yield

    
def generate_test_player(db_session=None, steam_id=38903245, display_name='testerman'):
    test_player = Player(steam_id=steam_id, display_name=display_name)
    if db_session:
        db_session.add(test_player)
        db_session.commit()
    return test_player

def mocked_player_does_not_exist_side_effect(steam_id):
    return p2sr_response.not_found(steam_id)

