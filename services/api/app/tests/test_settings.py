"""Tests for user settings synchronization."""

def test_get_default_settings(client, auth_headers):
    response = client.get("/api/v1/me/settings", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["theme"] == "dark"
    assert "table_layout_json" in data


def test_update_settings(client, auth_headers):
    payload = {
        "theme": "light",
        "table_layout_json": {
            "first_name_width": 150,
            "phone_width": 200,
            "sort_column": "last_name",
            "sort_order": "asc"
        }
    }
    response = client.put("/api/v1/me/settings", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["theme"] == "light"
    assert data["table_layout_json"]["first_name_width"] == 150

    # Verify retrieval preserves settings
    get_res = client.get("/api/v1/me/settings", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["theme"] == "light"
    assert get_res.json()["table_layout_json"]["sort_column"] == "last_name"
