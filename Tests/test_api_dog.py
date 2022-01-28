import pytest
import requests
from jsonschema import validate


@pytest.mark.regress_dogs
def test_api_list_all_breeds(base_url, status_code):
    """Check status code"""
    res = requests.get(
        base_url + "/api/breeds/list/all"
    )
    assert res.status_code == status_code, 'Something wrong with status_code'


@pytest.mark.image
def test_api_json_schema_random_image(base_url):
    res = requests.get(
        base_url + "/api/breeds/image/random"
    )
    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"}
        },
        "required": ["message", "status"]
    }
    validate(instance=res.json(), schema=schema), 'Something wrong with validating schema'


@pytest.mark.image
@pytest.mark.parametrize('image_id', range(1, 51))
def test_api_multiple_random_images(base_url, image_id):
    """Check count images from 1 to 50"""
    res = requests.get(
        base_url + f"/api/breeds/image/random/{image_id}"
    )
    assert len(res.json().get("message")) == image_id, f'Something wrong with image_id {image_id}'


@pytest.mark.image
def test_api_type_all_images(base_url):
    """Check type of all images"""
    res = requests.get(
        base_url + f"/api/breed/hound/images"
    )
    for i in range(len(res.json().get("message"))):
        assert res.json().get("message")[i][-4:].lower() == '.jpg' \
               or res.json().get("message")[i][-4:].lower() == 'jpeg', \
            f'Something wrong with type image_id {res.json().get("message")[i]}'


@pytest.mark.image
def test_api_image_each_breed(base_url, breed):
    """Check the image of each breed"""
    res = requests.get(
        base_url + "/api/breed/" + ''.join(breed) + "/images/random"
    )
    assert (res.json().get("message")[-4:].lower() == '.jpg'
            or res.json().get("message")[-4:].lower() == 'jpeg'
            or res.json().get("message")[-4:].lower() == '.png') \
           and res.json().get(
        "status") == "success" and res.status_code == 200, f'Something wrong with image bread_id {breed}'


@pytest.mark.regression
def test_api_list_all_sub_breeds(base_url, breed):
    """Check list all sub-breeds"""
    res = requests.get(
        base_url + "/api/breed/" + ''.join(breed).split('/')[0] + "/list"
    )
    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"}
        },
        "required": ["message", "status"]
    }
    validate(instance=res.json(), schema=schema), 'Something wrong with validating schema'
