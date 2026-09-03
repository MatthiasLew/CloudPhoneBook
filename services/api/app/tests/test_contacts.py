"""Tests for contact CRUD operations and searching."""

def test_create_and_get_contact(client, auth_headers):
    payload = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "phone": "+48 123 456 789",
        "email": "jan@example.com",
        "address": "Warszawa",
        "notes": "Test contact",
    }
    # Create
    create_res = client.post("/api/v1/contacts", json=payload, headers=auth_headers)
    assert create_res.status_code == 201
    contact = create_res.json()
    assert contact["first_name"] == "Jan"
    assert contact["last_name"] == "Kowalski"
    contact_id = contact["id"]

    # Get single
    get_res = client.get(f"/api/v1/contacts/{contact_id}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == contact_id


def test_list_contacts_and_search(client, auth_headers):
    # Add 2 contacts
    client.post(
        "/api/v1/contacts",
        json={"first_name": "Jan", "last_name": "Kowalski", "phone": "111222333"},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/contacts",
        json={"first_name": "Anna", "last_name": "Nowak", "phone": "999888777"},
        headers=auth_headers,
    )

    # List all
    res = client.get("/api/v1/contacts", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

    # Search by first name
    res_search = client.get("/api/v1/contacts?query=Anna", headers=auth_headers)
    assert res_search.status_code == 200
    search_data = res_search.json()
    assert search_data["total"] == 1
    assert search_data["items"][0]["first_name"] == "Anna"

    # Search by phone
    res_phone = client.get("/api/v1/contacts?query=111222", headers=auth_headers)
    assert res_phone.status_code == 200
    assert res_phone.json()["total"] == 1
    assert res_phone.json()["items"][0]["first_name"] == "Jan"


def test_update_contact(client, auth_headers):
    create_res = client.post(
        "/api/v1/contacts",
        json={"first_name": "StareImie", "last_name": "Kowalski", "phone": "123456"},
        headers=auth_headers,
    )
    contact_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/v1/contacts/{contact_id}",
        json={"first_name": "NoweImie", "phone": "654321"},
        headers=auth_headers,
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["first_name"] == "NoweImie"
    assert updated["phone"] == "654321"
    assert updated["last_name"] == "Kowalski"


def test_delete_contact(client, auth_headers):
    create_res = client.post(
        "/api/v1/contacts",
        json={"first_name": "DoUsuniecia", "last_name": "Test", "phone": "000000"},
        headers=auth_headers,
    )
    contact_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/contacts/{contact_id}", headers=auth_headers)
    assert delete_res.status_code == 204

    get_res = client.get(f"/api/v1/contacts/{contact_id}", headers=auth_headers)
    assert get_res.status_code == 404
