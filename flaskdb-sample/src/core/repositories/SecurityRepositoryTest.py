import unittest
from core.repositories.SecurityRepository import *


class TestSum(unittest.TestCase):

    def test_00_add_tenant(self):
        tenant = Tenant(name='Test Tenant')
        rows = tenant.save()
        self.assertEqual(rows, 1)

    def test_01_find_tenant(self):
        results = TenantRepository.find_by_name('Test Tenant')
        for tenant in results:
            self.assertEqual(tenant.name, 'Test Tenant')

    def test_02_delete_tenant(self):
        rows = Tenant.delete().where(Tenant.name == 'Test Tenant').execute()
        self.assertLessEqual(1, rows)


if __name__ == '__main__':
    unittest.main()
