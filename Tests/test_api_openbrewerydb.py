import pytest
import requests
from jsonschema import validate


@pytest.mark.list_breweries
def test_api_schema_breweries(base_url):
    res = requests.get(
        base_url + "/breweries"
    )
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "brewery_type": {"type": "string"},
            "street": {"type": ["null", "string"]},
            "address_2": {"type": ["null", "string"]},
            "address_3": {"type": ["null", "string"]},
            "city": {"type": "string"},
            "state": {"type": ["null", "string"]},
            "county_province": {"type": ["null", "string"]},
            "postal_code": {"type": "string"},
            "country": {"type": "string"},
            "longitude": {"type": ["null", "string"]},
            "latitude": {"type": ["null", "string"]},
            "phone": {"type": ["null", "string"]},
            "website_url": {"type": ["null", "string"]},
            "updated_at": {"type": "string"},
            "created_at": {"type": "string"}
        },
        "required": [
            "id",
            "name",
            "brewery_type",
            "street",
            "address_2",
            "address_3",
            "city",
            "state",
            "county_province",
            "postal_code",
            "country",
            "longitude",
            "latitude",
            "phone",
            "website_url",
            "updated_at",
            "created_at"
        ]
    }
    for i in range(len(res.json())):
        validate(instance=res.json()[i], schema=schema), 'Something wrong with validating schema'


@pytest.mark.page
@pytest.mark.parametrize('page', range(1, 51))
def test_api_counter_pages(base_url, page):
    """Check count pages from 1 to 50"""
    res = requests.get(
        base_url + "/breweries",
        params={'per_page': page}
    )
    assert len(res.json()) == page, f"Something wrong on page {page}"


@pytest.mark.list_breweries
@pytest.mark.parametrize("id_brewery", [9099, 0, 'A', 99999, -1],
                         ids=["valid_value", "zero", "letter", "out_of_range", "negative_value"])
def test_api_different_id_breweries(base_url, id_brewery):
    """Check different id breweries"""
    res = requests.get(
        base_url + f"/breweries/{id_brewery}"
    )
    if id_brewery == 9094:
        assert res.status_code == 200, f"Didn't get 200 status code"
    else:
        assert res.status_code == 404, f"Didn't get 404 status code"


@pytest.mark.list_breweries
@pytest.mark.parametrize("query, count", [("dog", 39), ("whale", 7), ("cow", 3), ("racoon", 0)])
def test_api_autocomplete(base_url, query, count):
    """Check autocomplete"""
    res = requests.get(
        base_url + "/breweries/autocomplete",
        params={'query': query}
    )
    assert len(res.json()) == count, f"Something wrong with autocomplete on query {query}"


@pytest.mark.list_breweries
@pytest.mark.parametrize("query", ["dog", "whale", "cow", "brain"])
def test_api_search_breweries(base_url, query):
    """Check search breweries"""
    res = requests.get(
        base_url + "/breweries/search",
        params={'query': query}
    )
    for i in range(len(res.json()) + 1):
        assert query.upper() in res.text.upper(), f"Incorrect searching for query {query} on {i} element"
