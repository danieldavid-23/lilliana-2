from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures as MySQLDatabaseFeatures

class DatabaseFeatures(MySQLDatabaseFeatures):
    @property
    def can_return_columns_from_insert(self):
        if self.connection.mysql_is_mariadb:
            return self.connection.mysql_version >= (10, 6)
        return True

    @property
    def can_return_rows_from_bulk_insert(self):
        if self.connection.mysql_is_mariadb:
            return self.connection.mysql_version >= (10, 6)
        return True

class DatabaseWrapper(MySQLDatabaseWrapper):
    features_class = DatabaseFeatures

    def check_database_version_supported(self):
        pass
