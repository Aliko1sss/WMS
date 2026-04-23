def test_full_warehouse_cycle(client):
    # 1. Создаем товар
    res = client.post("/products/", json={"sku": "TEST-01", "name": "Test Item", "quantity": 0})
    assert res.status_code == 201
    product_id = res.json()["id"]

    # 2. Приход (IN)
    res = client.post("/operations/", json={"product_id": product_id, "op_type": "IN", "amount": 10})
    assert res.status_code == 200
    assert res.json()["new_quantity"] == 10.0

    # 3. Расход (OUT)
    res = client.post("/operations/", json={"product_id": product_id, "op_type": "OUT", "amount": 4})
    assert res.status_code == 200
    assert res.json()["new_quantity"] == 6.0

    # 4. Проверка остатка через GET
    res = client.get(f"/products/{product_id}")
    assert res.json()["quantity"] == 6.0