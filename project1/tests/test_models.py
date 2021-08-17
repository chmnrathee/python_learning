from django.test import TestCase
from project1.models import empinfo

def test_basic():
    assert 1 == 1

test_basic()

class TestEmpinfo(TestCase):
    # Test class to verify EmpInfo table is working or not.
    # Checking by adding some data in table and flush it later on. 
    def setUp(self):
        self.empinfo = empinfo.objects.create(
            name="Rathee",
            title="Engineer",
            age=10
        )

    def test_empmodel(self):
        row1 = empinfo.objects.get(age=10)
        self.assertEquals(row1.name, 'Rathee'),
    
    def tearDown(self):
        try:
            employee_name = empinfo.objects.get(name="Raman")
            employee_name.delete()
        except empinfo.DoesNotExist:
            pass