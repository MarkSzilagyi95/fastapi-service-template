import sys
import pyodbc
import pandas as pd


class SqlServer:
    conn = None

    def __init__(self, hostname, username, password, database, port=3306, driver=None):
        driver = driver if driver is not None else self.__default_sql_driver_based_on_operating_system()
        self.conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + hostname + ';PORT=' +
                                   str(port) + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    @classmethod
    def __default_sql_driver_based_on_operating_system(cls):
        if sys.platform == 'win32':
            return '{SQL Server}'
        else:
            return '{ODBC Driver 17 for SQL Server}'

    def _query(self, query):
        return pd.read_sql_query(query, self.conn)

    def __call__(self, cls):
        def wrapper(*args, **kwargs):
            setattr(cls, '_query', self._query)

            return cls(*args, **kwargs)

        return wrapper
