from datetime import datetime
from unittest import TestCase

from src.adapters.db.sqlite import SQLiteDBAdapter
from src.schemas.common import EnvType
from src.schemas.product import Product
from src.tests.integration import TEST_SQLITE_DB_PATH


class TestSQLiteDBAdapter(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = SQLiteDBAdapter(EnvType.TEST, None, TEST_SQLITE_DB_PATH)
        cls.adapter.table = "products"

    def setUp(self):
        self.adapter.drop_table("products")
        self.adapter.cursor.execute("""
            CREATE TABLE products (
                _id TEXT PRIMARY KEY,
                name TEXT,
                created_at TEXT,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT,
                deleted_at TEXT,
                deleted_by TEXT
            )
            """)

    def test_create_one(self):
        product = Product(
            id="test-_id",
            name="test product",
            created_at=datetime.now(),
            created_by="admin",
        )
        product_id = self.adapter.create_one(product.model_dump())
        self.assertEqual(product_id, "test-_id")

    def test_read_one(self):
        product = Product(
            id="test-_id-read",
            name="test product",
            created_at=datetime.now(),
            created_by="admin",
        )
        self.adapter.create_one(product.model_dump())
        retrieved_product = self.adapter.read_one("test-_id-read")
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product["_id"], "test-_id-read")

    def test_update_one(self):
        product_id = "test-_id-update"
        product = Product(
            id=product_id,
            name="test product",
            created_at=datetime.now(),
            created_by="admin",
        )
        self.adapter.create_one(product.model_dump())

        # update_one expects data to update
        update_data = {
            "name": "updated product",
            "updated_at": datetime.now(),
            "updated_by": "admin",
        }
        self.assertTrue(self.adapter.update_one(product_id, update_data))

        retrieved = self.adapter.read_one(product_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "updated product")

    def test_delete_one(self):
        product_id = "test-_id-delete"
        product = Product(
            id=product_id,
            name="test product",
            created_at=datetime.now(),
            created_by="admin",
        )
        self.adapter.create_one(product.model_dump())
        self.assertTrue(self.adapter.delete_one(product_id))
        self.assertIsNone(self.adapter.read_one(product_id))
