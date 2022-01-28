import requests


def test_api_entered_status_code(base_url, status_code):
    res = requests.get(base_url)
    assert res.status_code == status_code
