HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'wqm120312'
DATABASE = 'ckgl'
DB_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SECRET_KEY = '2019212853'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

KEY = "d5a3db3a36******56d4c31cee0" #高德地图api-key
default_no="sa"
default_password="123"