from fastapi import Request

data_user = {
    "email": "nikita@kar.ru",
    "password": "12345678"
}
stats_code_200 = 200

async def test_user_flow(ac, request: Request):

    # /register
    auth_reg = await ac.post(
        url="/auth/register",
        json={**data_user}
    )

    assert auth_reg.status_code == stats_code_200

    # /login
    auth_login = await ac.post(
        url="/auth/login",
        json={**data_user}
    )
    assert auth_login.status_code == stats_code_200
    res_login = auth_login.json()
    assert "access_token" in res_login

    # /me
    res_get_me = await ac.get(
        url="/auth/me"
    )
    assert res_get_me.status_code == stats_code_200
    assert isinstance(res_get_me.json(), dict)
    user = res_get_me.json()
    assert user["email"] == "nikita@kar.ru"
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    res_log_out = await ac.post(
        url="/auth/logout"
    )
    assert res_log_out.status_code == stats_code_200
    assert "access_token" not in ac.cookies