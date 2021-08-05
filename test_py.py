## Python Program to print consective numbers

# def test_f1():
#     for i in range(10):
#         print(i)
# test_f1()

import pytest

def chmn1(x):
    return x + 2

# In below line, i'm marking test as a name so that i can run all respective mark with same name. 
@pytest.mark.chmntest
def test_chmn1():
    assert chmn1(3) == 5

# Above test cases are in function, now we can have how to combine all these functions in a class.

class TestClass:
    def test_one(self):
        string = "Rathee"
        assert 'thee' in string
    def test_two(self):
        string = "Chaman"
        assert 'thee' in string

#Assert is nothing just a check which returns either true or false. 

# Run pytest
#  Use -m option for markers like "pytest -m chmntest"