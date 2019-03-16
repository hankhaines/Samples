from core.models.security.Security import *


class TenantRepository:

    @staticmethod
    def find_by_id(id):
        tenant = Tenant.get_by_id(id)
        return tenant

    @staticmethod
    def find_by_name(name):
        tenants = Tenant.select().where(Tenant.name == name)
        return tenants

    @staticmethod
    def find_where_contains_name(name):
        tenants = Tenant.select().where(Tenant.name.contains(name))
        return tenants

    @staticmethod
    def find_where_startswith_name(name):
        tenants = Tenant.select().where(Tenant.name.startswith(name))
        return tenants
