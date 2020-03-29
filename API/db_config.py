from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gopi'
app.config['MYSQL_DATABASE_DB'] = 'vtrips'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)