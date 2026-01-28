from datetime import datetime
from unittest import TestCase

from schemas.product import Product


class TestProduct(TestCase):
    def setUp(self):
        date_format = "%Y-%m-%d"
        self.datetime1 = datetime.strptime("2021-05-01", date_format)
        self.datetime2 = datetime.strptime("2022-05-01", date_format)
        self.datetime3 = datetime.strptime("2023-05-01", date_format)
        self.id = "1"
        self.name = "test product"
        self.user1 = "user1"
        self.user2 = "user2"
        self.user3 = "user3"
        self.product = Product(
            id=self.id,
            name=self.name,
            created_at=self.datetime1,
            created_by=self.user1,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.id, self.id)
        self.assertEqual(self.product.name, self.name)
        self.assertIsInstance(self.product.created_at, datetime)
        self.assertEqual(self.product.created_by, self.user1)
        self.assertIsNone(self.product.updated_at)
        self.assertIsNone(self.product.updated_by)
        self.assertIsNone(self.product.deleted_at)
        self.assertIsNone(self.product.deleted_by)

    def test_product_update(self):
        self.product.updated_at = self.datetime2
        self.product.updated_by = self.user2
        self.assertEqual(self.product.updated_at, self.datetime2)
        self.assertEqual(self.product.updated_by, self.user2)

    def test_product_deletion(self):
        self.product.deleted_at = self.datetime3
        self.product.deleted_by = self.user3
        self.assertEqual(self.product.deleted_at, self.datetime3)
        self.assertEqual(self.product.deleted_by, self.user3)

    def test_id_required(self):
        with self.assertRaises(TypeError):
            Product(name=self.name, created_by=self.user1, created_at=self.datetime1)

    def test_name_required(self):
        with self.assertRaises(TypeError):
            Product(id=self.id, created_by=self.user1, created_at=self.datetime1)

    def test_created_at_required(self):
        with self.assertRaises(TypeError):
            Product(id=self.id, name=self.name, created_by=self.user1)

    def test_created_by_required(self):
        with self.assertRaises(TypeError):
            Product(id=self.id, name=self.name, created_at=self.datetime1)
