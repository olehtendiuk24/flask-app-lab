import io
import unittest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from app import app
from app.products import views as product_views


class ProductCrudTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        self.test_db = TinyDB(storage=MemoryStorage)
        product_views.products_table = self.test_db.table('products')

    def test_create_and_read_product(self):
        data = {
            "name": "Test Laptop",
            "content": "Опис тестового ноутбука для перевірки CRUD",
            "price": "1500.50",
            "category": "Laptops",
            "quantity": "5",
            "image": (io.BytesIO(b"fake image bytes"), "laptop.png")
        }
        res = self.client.post("/product/add", data=data, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Test Laptop".encode("utf-8"), res.data)

        detail_res = self.client.get("/product/1")
        self.assertEqual(detail_res.status_code, 200)
        self.assertIn("1500.50".encode("utf-8"), detail_res.data)

    def test_update_product(self):

        product_views.products_table.insert({
            "id": 1,
            "name": "Old Phone",
            "content": "Старий опис",
            "price": 500.00,
            "category": "Smartphones",
            "quantity": 2,
            "image": None,
            "created_at": "2026-11-23 12:00:00"
        })

        update_data = {
            "name": "Updated Phone Pro",
            "content": "Оновлений опис смартфона",
            "price": "799.99",
            "category": "Smartphones",
            "quantity": "10"
        }
        res = self.client.post("/product/1/edit", data=update_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Updated Phone Pro".encode("utf-8"), res.data)
        self.assertIn(b"799.99", res.data)

    def test_delete_product(self):
        product_views.products_table.insert({
            "id": 1,
            "name": "To Delete",
            "content": "Буде видалено",
            "price": 100.00,
            "category": "PC",
            "quantity": 1,
            "image": None,
            "created_at": "2026-11-23 12:00:00"
        })

        res = self.client.post("/product/1/delete", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("було видалено".encode("utf-8"), res.data)
        self.assertEqual(len(product_views.products_table.all()), 0)

    def test_product_not_found(self):
        res = self.client.get("/product/999")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()