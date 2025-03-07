import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
JWT_SECRET_KEY = 'my precious'
JWT_BLACKLIST_ENABLED = True
# TODO: This is temp
JWT_ACCESS_TOKEN_EXPIRES = False

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
