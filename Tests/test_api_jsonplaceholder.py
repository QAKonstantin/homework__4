import pytest
import requests
from jsonschema import validate


@pytest.mark.posts
@pytest.mark.parametrize('posts', range(1, 101))
def test_api_counter_posts(base_url, posts):
    """Check count posts from 1 to 100"""
    res = requests.get(
        base_url + f"/posts/{posts}"
    )
    assert res.json()["id"] == posts, f'Something wrong with count post {posts}'


@pytest.mark.posts
@pytest.mark.parametrize("postid", [0, 'ABC', 1231122312, -1],
                         ids=["zero", "letter", "out_of_range", "negative_value"])
def test_api_post_id(base_url, postid):
    """Check different post id"""
    assert requests.get(base_url + "/comments",
                        params={"postId": postid}).json() == [], f'Something wrong with post_id {postid}'


@pytest.mark.users
def test_api_schema_users(base_url):
    res = requests.get(
        base_url + "/users"
    )
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "username": {"type": "string"},
            "email": {"type": "string"},
            "address": {"type": "object",
                        "properties": {
                            "street": {"type": "string"},
                            "suite": {"type": "string"},
                            "city": {"type": "string"},
                            "zipcode": {"type": "string"},
                            "geo": {"type": "object",
                                    "properties": {
                                        "lat": {"type": "string"},
                                        "lng": {"type": "string"}
                                    },
                                    "required": ["lat", "lng"]
                                    }
                        },
                        "required": ["street", "suite", "city", "zipcode", "geo"]
                        },
            "phone": {"type": "string"},
            "website": {"type": "string"},
            "company": {"type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "catchPhrase": {"type": "string"},
                            "bs": {"type": "string"}
                        },
                        "required": ["name", "catchPhrase", "bs"]
                        }
        },
        "required": ["id", "name", "username", "email", "address", "phone", "website", "company"]
    }

    for i in range(len(res.json())):
        validate(instance=res.json()[i], schema=schema), 'Something wrong with validating schema'


@pytest.mark.posts
def test_api_create_post(base_url):
    """Check creating post"""
    payload = {'title': 'foo', 'body': 'bar', 'userId': 1}
    res = requests.post(base_url + '/posts', data=payload)
    assert res.json()['title'] == 'foo' and res.json()['body'] == 'bar' and res.json()['userId'] == str(1) \
           and res.json()['id'] == 101, 'Something wrong with creating post'


@pytest.mark.posts
def test_api_delete_post(base_url):
    """Check delete post"""
    res = requests.delete(
        base_url + "/posts/7"
    )
    assert res.json() == {}, 'Something wrong with deleting post'
