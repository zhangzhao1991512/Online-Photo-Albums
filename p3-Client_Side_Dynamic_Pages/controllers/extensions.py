import MySQLdb
import MySQLdb.cursors
import config
#from flask.ext.mysqldb import MYSQL

def connect_to_database():
  options = {
    'host': config.env['host'],
    'user': config.env['user'],
    'passwd': config.env['password'],
    'db': config.env['db'],
    'cursorclass' : MySQLdb.cursors.DictCursor
  }
  
  db = MySQLdb.connect(**options)
  db.autocommit(True)
  return db

#mysql = MYSQL()  
#db = MySQLdb.connect_to_database()
