import os
from app import create_app

env = os.environ.get('APP_ENV', 'DEV')
db_con = os.environ.get('SQLALCHEMY_DATABASE_URI')

app = create_app('app.settings.%sConfig' % env.capitalize(), env, db_con)

application = app
