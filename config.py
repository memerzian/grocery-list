import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error
    #postgresql pattern is postgresql://user:password@localhost:5432/database_name
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:db888@localhost:5432/Grocery"