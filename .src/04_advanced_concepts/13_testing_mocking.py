# %% [markdown]
# # Tutorial 08: Modern Testing & Mocking
#
# Testing code isolates modules to guarantee changes do not break existing behavior. In modern Python, this is achieved by pairing `pytest` (a powerful, flexible test runner) with `unittest.mock` (standard library mock tool for dependency isolation).
#
# In this notebook, we look at:
# 1. Isolating objects with `Mock` and `MagicMock`
# 2. Dynamic mocking with `side_effect` and patching modules using `patch`
# 3. Clean test suites using `pytest.fixture`
# 4. Data-driven testing using `@pytest.mark.parametrize`

# %%
import unittest.mock as mock
import pytest

# %% [markdown]
# ## 1. Mocks and MagicMocks
# Mocks replace system components with dummy objects that assert how they were called.
#
# - `Mock`: Basic mock object.
# - `MagicMock`: A subclass of `Mock` that automatically implements magic methods (like `__len__`, `__str__`, `__iter__`, and context managers).

# %%
# 1. Basic Mock with return_value
calculator = mock.Mock()
calculator.add.return_value = 10

result = calculator.add(4, 6)
print("Mock Return Value:", result)

# Assert that add was called with correct parameters
calculator.add.assert_called_once_with(4, 6)
print("Add was verified to have been called with (4, 6) once.")


# 2. MagicMock supporting magic methods
mock_list = mock.MagicMock()
mock_list.__len__.return_value = 42

print("\nMagicMock length:", len(mock_list))
print("Calling MagicMock string representation:", str(mock_list))

# %% [markdown]
# ## 2. Side Effects & Patching
#
# - `side_effect`: Simulates exceptions, dynamic return values, or iterators.
# - `patch`: Temporarily replaces a function or class in another module during execution (can be used as decorator or context manager).

# %%
# 1. Using side_effect to raise an exception or cycle through values
api_client = mock.Mock()

# First call returns 200, second raises TimeoutError
api_client.fetch_data.side_effect = [200, TimeoutError("Service unavailable")]

print("First API response:", api_client.fetch_data())
try:
    api_client.fetch_data()
except TimeoutError as e:
    print("Second API call timed out as expected:", e)


# 2. Using patch.object to patch functions on objects
class PaymentProcessor:
    def charge(self, amount):
        print(f"Charging ${amount} to actual bank gateway...")
        return "SUCCESS_TX_123"

processor = PaymentProcessor()

# Patch the 'charge' method to bypass live bank gateway during tests
with mock.patch.object(processor, 'charge', return_value="MOCKED_TX_999") as mocked_charge:
    result = processor.charge(50)
    print("\nResult of transaction:", result)
    mocked_charge.assert_called_once_with(50)

# %% [markdown]
# ## 3. Pytest Fixtures & Assertions
# Pytest uses regular Python `assert` statements instead of verbose self.assertEqual wrapper methods.
#
# `pytest.fixture` functions setup resources required by multiple test cases.

# %%
# A sample system under test (SUT)
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item: str):
        self.items.append(item)

    @property
    def total_items(self):
        return len(self.items)

# Pytest tests are regular functions prefixed with test_
@pytest.fixture
def empty_cart():
    """Fixture that initializes a fresh ShoppingCart before each test"""
    return ShoppingCart()

def test_new_cart_is_empty(empty_cart):
    assert empty_cart.total_items == 0

def test_add_item_to_cart(empty_cart):
    empty_cart.add_item("Python Book")
    assert empty_cart.total_items == 1
    assert "Python Book" in empty_cart.items

# Run tests inline in the notebook to demonstrate pytest execution
# (This runs pytest programmatically on this file)
print("--- Programmatic Pytest Execution ---")
pytest.main(["-v", "--tb=short", "-c", "/dev/null", __file__])

# %% [markdown]
# ## 4. Parameterized Testing
# Rather than duplicate test functions for different inputs, `@pytest.mark.parametrize` allows running the same test against different sets of arguments.

# %%
def is_even(n):
    return n % 2 == 0

@pytest.mark.parametrize("number, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-1, False),
    (102, True)
])
def test_is_even(number, expected):
    assert is_even(number) == expected
