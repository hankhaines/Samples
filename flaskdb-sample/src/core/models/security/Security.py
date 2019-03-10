from core.db.Database import *


class Tenant(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'appTenant'


class Alias(BaseModel):
    lookup = CharField()
    tenant = ForeignKeyField(Tenant, backref='aliases')

    class Meta:
        table_name = 'appAlias'


class User(BaseVersionedModel):
    name = CharField()
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    phone = CharField(null=True)
    title = CharField(null=True)
    question = CharField()
    answer = CharField()
    timezone = CharField(default='US/Central')

    class Meta:
        table_name = 'secUser'


class TenantUser(BaseModel):
    user = ForeignKeyField(Tenant, backref='tenants')
    tenant = ForeignKeyField(User, backref='users')

    class Meta:
        table_name = 'appTenantUser'


class Role(BaseModel):
    name = CharField()
    display = CharField(null=True)

    class Meta:
        table_name = 'secRole'


class UserRole(BaseModel):
    user = ForeignKeyField(User, backref='roles')
    role = ForeignKeyField(Role, backref='users')

    class Meta:
        table_name = 'secUserRole'


class Group(BaseVersionedModel):
    name = CharField()
    display = CharField(null=True)

    class Meta:
        table_name = 'secGroup'


class UserGroup(BaseModel):
    user = ForeignKeyField(User, backref='groups')
    group = ForeignKeyField(Group, backref='users')

    class Meta:
        table_name = 'secUserGroup'


class GroupRole(BaseModel):
    group = ForeignKeyField(User, backref='roles')
    role = ForeignKeyField(Role, backref='groups')

    class Meta:
        table_name = 'secGroupRole'


def create_tables():
    with dbInstance:
        dbInstance.create_tables([Tenant, Alias, User, Role, Group, UserRole, UserGroup, GroupRole, TenantUser])


def drop_tables():
    with dbInstance:
        dbInstance.drop_tables([Tenant, Alias, User, Role, Group, UserRole, UserGroup, GroupRole, TenantUser])


def load_data():
    tenants = dbDataSet['appTenant']
    tenants.thaw(filename='tenants.json', format='json')
