import pytest
from starlette.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_page_renders():
    response = client.get("/")
    assert response.status_code == 200
    assert "HSPT 로그인" in response.text
    assert "djkim" in response.text


def test_form_login_success():
    response = client.post(
        "/login",
        data={"userId": "djkim", "userPasswd": "core2020"},
    )
    assert response.status_code == 200
    assert "로그인 성공!" in response.text
    assert "김동진" in response.text
    assert "djkim" in response.text


def test_form_login_failure():
    response = client.post(
        "/login",
        data={"userId": "djkim", "userPasswd": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "아이디 또는 비밀번호가 올바르지 않습니다." in response.text


def test_api_login_success():
    response = client.post(
        "/api/login",
        json={"userId": "djkim", "userPasswd": "core2020"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user"]["userName"] == "김동진"
    assert data["user"]["userId"] == "djkim"
    assert data["user"]["userNo"] == 1


def test_api_login_failure():
    response = client.post(
        "/api/login",
        json={"userId": "djkim", "userPasswd": "invalid_pw"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


if __name__ == "__main__":
    test_login_page_renders()
    print("test_login_page_renders passed")
    test_form_login_success()
    print("test_form_login_success passed")
    test_form_login_failure()
    print("test_form_login_failure passed")
    test_api_login_success()
    print("test_api_login_success passed")
    test_api_login_failure()
    print("test_api_login_failure passed")
    print("All tests passed successfully!")

