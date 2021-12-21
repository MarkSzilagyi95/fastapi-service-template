import pandas as pd
from hdbcli import dbapi


class SqlHana:
    conn = None

    def __init__(self, hostname, username, password, database, port=3306):
        self.conn = dbapi.connect(address=hostname, port=port, user=username, password=password, databasename=database)

    def _query(self, query):
        return pd.read_sql_query(query, self.conn)

    def __call__(self, cls):
        def wrapper(*args, **kwargs):
            setattr(cls, '_query', self._query)

            return cls(*args, **kwargs)

        return wrapper
