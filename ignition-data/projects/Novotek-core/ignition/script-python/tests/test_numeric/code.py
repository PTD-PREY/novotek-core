import numeric 

def test_add():
    assert numeric.add(2, 3) == 5

def test_subtract():
    assert numeric.subtract(3, 2) == 1

def test_multiply():
    assert numeric.multiply(2, 3) == 6

def test_divide():
    assert numeric.divide(6, 3) == 2

def test_calculate_total():
    items = [10, 20, 30, 40]
    assert numeric.calculate_total(items) == 100