import pytest
import os

@pytest.fixture
def sample_dict():
    return {"name": "Uliana", "age": 23}


def test_one(sample_dict):
    assert 'name' in sample_dict


def test_two(sample_dict):
    assert sample_dict['age'] > 18


@pytest.fixture
def temporary_file():
    filename = 'test_file.txt'
    with open(filename, 'w') as file:
        file.write('Hello!')
    yield filename
    os.remove(filename)

def test_check_file(temporary_file):
    with open('test_file.txt', 'r') as file:
        assert file.read() == 'Hello!'

@pytest.fixture
def base_url():
    return "https://example.com"

@pytest.fixture
def endpoint():
    return "/users"

@pytest.fixture
def full_url(base_url, endpoint):
    return f'{base_url}{endpoint}'

def test_full_url(full_url):
    assert full_url == "https://example.com/users"
