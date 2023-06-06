import pytest
from fastapi.testclient import TestClient
from cid_resolver.main import app
from cid_resolver.routers.cid import redis_client


client = TestClient(app)

def test_get_cid_not_found():
    redis_client.delete("bafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi")
    response = client.get(f"/entry/cid?cid=bafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi")
    assert response.status_code == 404
    
def test_post_cid_unauth():
    response = client.post(f"/entry/?cid=bafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi&url=%20https%3A%2F%2Fbafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi.ipfs.w3s.link")
    assert response.status_code == 403


def test_post_cid_outdated_bearer():
    bearer = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODU5NzA3MDIsInB1YmxpY19rZXkiOiJHdGJpNldRREI2d1VlUGlabThhWXM1WFo1cFVxeDlqTU1MdlJWSFBFU1RqVSJ9.TujsqB9lpybvtfWc5SakXXjQ_kFM8jvpnYDH5V_z4gc'
    response = client.post('/entry/?cid=bafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi&url=%20https%3A%2F%2Fbafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi.ipfs.w3s.link',
                           headers={ 'accept': 'application/json' f'Authorization: Bearer {bearer}'})
    assert response.status_code == 403

def test_post_cid_proper_bearer(get_bearer2):
    bearer = get_bearer2
    response = client.post('/entry/?cid=bafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi&url=%20https%3A%2F%2Fbafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi.ipfs.w3s.link',
                           headers={ "Authorization": f"Bearer {bearer}"})
    assert response.status_code == 200

def test_get_cid_found():
    response = client.get(f"/entry/cid?cid=bafkreibklq6s67jlcni2alpkqmxuyz4kh65uefp6vltoglnrr6riezs4qi")
    assert response.status_code == 200
