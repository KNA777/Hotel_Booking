async def test_post_facilities(ac):
    facility_title = "WI_FI"
    response = await ac.post(
        url="/facilities",
        json={
            "title": facility_title
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert result["data"]["title"] == facility_title
    assert "data" in result



async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)




