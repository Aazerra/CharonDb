import sqlite3
import pymysql
from pymysql.cursors import DictCursor
import logging


class DbManagerException(Exception):
    pass


class LiteManager:
    def __init__(self, database):
        self.con = sqlite3.connect(database)
        self.cursor = self.con.cursor()

    def show_databases(self):
        query = ".databases"
        self.cursor.execute(query)
        return self.cursor.fetchall()


class MySQLManager:
    DB_CREATE = 'CREATE DATABASE %s'
    DB_DROP = 'DROP DATABASE IF EXISTS %s'
    DB_USE = "USE '%(dbname)s'"
    DB_EXISTS = "SELECT EXISTS(SELECT * from %(table_name)s WHERE %(where)s)"
    DB_CREATE_TABLE = 'CREATE TABLE %s (%s) DEFAULT CHARSET=utf8'
    DB_INSERT = "INSERT INTO %(table_name)s (%(cols)s) VALUES (%(values)s)"
    DB_SELECT = "SELECT %(cols)s FROM %(table_name)s"
    DB_SEARCH = 'SELECT %s FROM %s WHERE %s'
    DB_LIKE = 'SELECT %s FROM %s WHERE %s LIKE %s'

    def __init__(self, database: str, password: str, username: str = "root", host: str = "localhost", port: int = 3306, debug=False):
        self.con = None
        self.cursor = None
        self._init_logger(debug)
        self._init_con(database, host, username, password)
        self._init_cursor()

    def _init_logger(self, debug):
        self.logger = logging.Logger("Database")
        formater = logging.Formatter('%(asctime)s -> %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formater)
        self.logger.addHandler(handler)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def _init_con(self, database, host, username, password):
        self.logger.debug("Connecting to MySQL database")
        self.con = pymysql.connect(host=host, user=username,
                                   password=password, db=database,
                                   charset="utf8")

    def _init_cursor(self):
        self.logger.debug("Creating cursor instance")
        self.cursor = self.con.cursor(DictCursor)

    def import_database(self, sql_file):
        self.logger.debug("Importing .Sql File")
        self.cursor.execute(sql_file.read())
        self.commit()

    def commit(self):
        self.logger.debug("Commit changes")
        try:
            self.con.commit()
        except AttributeError as e:
            raise DbManagerException(
                'Connection to database is closed', str(e))
        except pymysql.err.InterfaceError as e:
            raise DbManagerException(
                'Connection to database is closed', str(e))

    def use_db(self, dbname):
        self.logger.debug(f"Current db: {dbname}")
        try:
            print(type(dbname))
            self.cursor.execute(MySQLManager.DB_USE, {"dbname": dbname})
        except pymysql.err.InterfaceError as e:
            raise DbManagerException(
                "Connection to database is closed", str(e))

    def show_databases(self):
        self.cursor.execute("SHOW TABLES")
        return self.cursor.fetchall()

    def select(self, table_name, cols):
        self.logger.debug('Select values from %s', table_name)
        cols = ', '.join([f'{i}' for i in cols])
        try:
            self.cursor.execute(MySQLManager.DB_SELECT % {
                                "table_name": table_name, "cols": cols})
            return self.cursor.fetchall()
        except pymysql.err.InterfaceError as e:
            raise DbManagerException(
                'Connection to database is closed', str(e))

    def insert(self, table_name, cols, values):
        self.logger.debug('Insert data to %s', table_name)
        cols = ', '.join([f'`{i}`' for i in cols])
        values = ', '.join([f'"{i}"' if isinstance(
            i, str) else f'{i}' for i in values])
        try:
            self.cursor.execute(MySQLManager.DB_INSERT % {
                                "table_name": f"`{table_name}`", "cols": cols, "values": values})
        except pymysql.err.IntegrityError as e:
            raise DbManagerException('Duplicate entry ', str(e))
        except pymysql.err.InterfaceError as e:
            raise DbManagerException('Connection to database is closed', str(e))
        self.commit()

    def exists(self, table_name, where):
        self.logger.debug('Check data is exists or not %s', where)
        try:
            self.cursor.execute(MySQLManager.DB_EXISTS %
                                {"table_name": f"`{table_name}`", "where": where})
            if list(self.cursor.fetchone().values())[0]:
                return True
            return False
        except pymysql.err.InterfaceError as e:
            raise DbManagerException(
                'Connection to database is closed', str(e))
