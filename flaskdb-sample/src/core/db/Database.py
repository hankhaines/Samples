from peewee import *
from playhouse.mysql_ext import MySQLConnectorDatabase
from playhouse.dataset import DataSet


dbInstance = MySQLConnectorDatabase('sample', host='localhost', user='admin', password='admpass')
dbDataSet = DataSet(dbInstance)


class BaseModel(Model):
    create_timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], null=True)
    update_timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')],
                                     null=True)

    class Meta:
        database = dbInstance


class ConflictDetectedException(Exception):
    pass


class BaseVersionedModel(BaseModel):
    version = IntegerField(constraints=[SQL('DEFAULT 1')], index=True)

    def __init__(self, *args, **kwargs):
        self._current_version = 1
        super(BaseModel, self).__init__(*args, **kwargs)

    def _pk_expr(self):
        model_class = type(self)
        return (model_class.version == self._current_version) & (self._meta.primary_key == self._pk)

    def save(self, *args, **kwargs):
        if not self.id:
            return super(BaseVersionedModel, self).save(*args, **kwargs)

        self._current_version = self.version
        self.version += 1

        rows = super(BaseVersionedModel, self).save(*args, **kwargs)
        if rows == 0:
            raise ConflictDetectedException()
        else:
            # Increment local version to match what is now in the db and return rows as base class
            return rows
