from app.utils.connectors.SqlServer import SqlServer
from app.utils.helpers.ConfigReader import Config


@SqlServer(hostname=Config('mssql.host').get(), username=Config('mssql.user').get(),
           password=Config('mssql.pass').get(), database=Config('mssql.database').get())
class DemoModel:

    def __init__(self):
        pass

    def mandant(self):
        return self._query("select * from analytics.Dim_Mandant")
