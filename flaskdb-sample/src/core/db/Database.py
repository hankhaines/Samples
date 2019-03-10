import datetime

from peewee import *
from playhouse.signals import pre_save
from playhouse.mysql_ext import MySQLConnectorDatabase
from playhouse.dataset import DataSet


dbInstance = MySQLConnectorDatabase('sample', host='localhost', user='admin', password='admpass')
dbDataSet = DataSet(dbInstance)


class BaseModel(Model):
    create_timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], null=True)
    update_timestamp = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.update_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = dbInstance


class ConflictDetectedException(Exception):
    pass


class BaseVersionedModel(BaseModel):
    version = IntegerField(default=1, index=True)

    def save_optimistic(self):
        if not self.id:
            # This is a new record, so the default logic is to perform an
            # INSERT. Ideally your model would also have a unique
            # constraint that made it impossible for two INSERTs to happen
            # at the same time.
            return self.save()

        # Update any data that has changed and bump the version counter.
        field_data = dict(self._data)
        current_version = field_data.pop('version', 1)

        field_data = self._prune_fields(field_data, self.dirty_fields)
        if not field_data:
            # No changes were found, so lets not do anything leaving the version as is
            return True

        model_class = type(self)
        field_data['version'] = model_class.version + 1  # Atomic increment.

        query = model_class.update(**field_data).where(
            (model_class.version == current_version) &
            (model_class.id == self.id))
        if query.execute() == 0:
            # No rows were updated, indicating another process has saved
            # a new version. How you handle this situation is up to you,
            # but for simplicity I'm just raising an exception.
            raise ConflictDetectedException()
        else:
            # Increment local version to match what is now in the db.
            self.version += 1
            return True


@pre_save(sender=BaseModel)
def on_save_handler(model_class, instance, created):
    if hasattr(instance, 'update_timestamp'):
        if created is None:
            instance.updated_timestamp = datetime.datetime.now()
