from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy import MetaData
import subprocess, re

# Taken from https://alembic.sqlalchemy.org/en/latest/naming.html
# This makes sure all constraints get created with names, so that they can be easily removed on downgrade
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# This is from the sqlalchemy documentation available at:
# https://docs.sqlalchemy.org/en/14/core/compiler.html#utc-timestamp-function
class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

def get_psql_version():
    versionResult = subprocess.run(['psql', '--version'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    version = re.search('^psql \(PostgreSQL\) (\d+\.\d+).*$', versionResult).group(1)
    return version
