import pytest
import csv


def pytest_addoption(parser):
    parser.addoption("--url", default='https://ya.ru', help="Request url", )

    parser.addoption("--status_code", default='200',
                     choices=['200', '201', '300', '301', '400', '402', '403', '404', '500', '502', '503', '504'],
                     help="Check status code")


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return int(request.config.getoption("--status_code"))


def pytest_generate_tests(metafunc):
    if "breed" in metafunc.fixturenames:
        with open("/test_data/all_breeds.csv") as file:
            reader = csv.reader(file)
            metafunc.parametrize("breed", reader)
