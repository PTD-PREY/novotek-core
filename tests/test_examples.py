def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

def calculate_total(prices):
    return sum(prices)

# Pytest test functions in ./tests/test_functions/test_math_numbers.py
def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(3, 2) == 1

def test_multiply():
    assert multiply(2, 3) == 6
    
def test_divide():
    assert divide(6, 3) == 2

def test_calculate_total():
    items = [10, 20, 30, 40]
    assert calculate_total(items) == 100