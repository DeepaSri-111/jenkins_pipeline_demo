"""
OrderManagementQA.py
E-Commerce Order Processing System
QA Test Program

Tests more than 20 combinations.
"""

import unittest

from OrderManagementQA import (
    Product,
    calculate_order,
    OrderProcessingError
)


class TestOrderManagement(unittest.TestCase):

    # ------------------------------------------------
    # 1. Single product
    # ------------------------------------------------
    def test_01_single_product(self):
        product = Product("P001", "electronics", 1, 1000)
        result = calculate_order([product])
        self.assertGreater(result.final_amount, 0)

    # ------------------------------------------------
    # 2. Multiple products
    # ------------------------------------------------
    def test_02_multiple_products(self):
        products = [
            Product("P001", "electronics", 2, 1000),
            Product("P002", "clothing", 2, 500)
        ]

        result = calculate_order(products)
        self.assertGreater(result.subtotal, 0)

    # ------------------------------------------------
    # 3. Zero quantity
    # ------------------------------------------------
    def test_03_zero_quantity(self):
        product = Product("P001", "electronics", 0, 1000)

        with self.assertRaises(OrderProcessingError):
            calculate_order([product])

    # ------------------------------------------------
    # 4. Negative quantity
    # ------------------------------------------------
    def test_04_negative_quantity(self):
        product = Product("P001", "electronics", -2, 1000)

        with self.assertRaises(OrderProcessingError):
            calculate_order([product])

    # ------------------------------------------------
    # 5. Invalid product ID
    # ------------------------------------------------
    def test_05_invalid_product(self):
        product = Product("", "electronics", 1, 1000)

        with self.assertRaises(OrderProcessingError):
            calculate_order([product])

    # ------------------------------------------------
    # 6. Out of stock
    # ------------------------------------------------
    def test_06_out_of_stock(self):
        product = Product(
            "P001",
            "electronics",
            1,
            1000,
            in_stock=False
        )

        with self.assertRaises(OrderProcessingError):
            calculate_order([product])

    # ------------------------------------------------
    # 7. Invalid coupon
    # ------------------------------------------------
    def test_07_invalid_coupon(self):
        product = Product("P001", "electronics", 1, 1000)

        with self.assertRaises(OrderProcessingError):
            calculate_order(
                [product],
                coupon_code="INVALID"
            )

    # ------------------------------------------------
    # 8. Valid coupon
    # ------------------------------------------------
    def test_08_valid_coupon(self):
        product = Product("P001", "electronics", 1, 1000)

        result = calculate_order(
            [product],
            coupon_code="SAVE10"
        )

        self.assertGreater(result.coupon_discount, 0)

    # ------------------------------------------------
    # 9. Maximum discount limit
    # ------------------------------------------------
    def test_09_maximum_discount(self):
        product = Product(
            "P001",
            "electronics",
            1,
            10000,
            discount=50
        )

        result = calculate_order(
            [product],
            coupon_code="SAVE15"
        )

        # Maximum discount should not exceed 20%
        self.assertLessEqual(
            result.total_discount,
            result.subtotal * 0.20
        )

    # ------------------------------------------------
    # 10. Tax calculation
    # ------------------------------------------------
    def test_10_tax_calculation(self):
        product = Product(
            "P001",
            "electronics",
            1,
            1000,
            tax=18
        )

        result = calculate_order([product])

        self.assertGreater(result.gst, 0)

    # ------------------------------------------------
    # 11. Free shipping
    # ------------------------------------------------
    def test_11_free_shipping(self):
        product = Product(
            "P001",
            "electronics",
            1,
            2000
        )

        result = calculate_order([product])

        self.assertEqual(result.shipping_charge, 0)

    # ------------------------------------------------
    # 12. Paid shipping
    # ------------------------------------------------
    def test_12_paid_shipping(self):
        product = Product(
            "P001",
            "electronics",
            1,
            100
        )

        result = calculate_order([product])

        self.assertEqual(result.shipping_charge, 50)

    # ------------------------------------------------
    # 13. Bulk order
    # ------------------------------------------------
    def test_13_bulk_order(self):
        product = Product(
            "P001",
            "electronics",
            10,
            100
        )

        result = calculate_order([product])

        self.assertGreater(result.bulk_discount, 0)

    # ------------------------------------------------
    # 14. Small quantity
    # ------------------------------------------------
    def test_14_small_quantity(self):
        product = Product(
            "P001",
            "electronics",
            2,
            100
        )

        result = calculate_order([product])

        self.assertEqual(result.bulk_discount, 0)

    # ------------------------------------------------
    # 15. Clothing discount
    # ------------------------------------------------
    def test_15_clothing_discount(self):
        product = Product(
            "P002",
            "clothing",
            1,
            1000
        )

        result = calculate_order([product])

        self.assertGreater(result.category_discount, 0)

    # ------------------------------------------------
    # 16. Grocery discount
    # ------------------------------------------------
    def test_16_grocery_discount(self):
        product = Product(
            "P003",
            "grocery",
            1,
            1000
        )

        result = calculate_order([product])

        self.assertGreater(result.category_discount, 0)

    # ------------------------------------------------
    # 17. Books discount
    # ------------------------------------------------
    def test_17_books_discount(self):
        product = Product(
            "P004",
            "books",
            1,
            1000
        )

        result = calculate_order([product])

        self.assertGreater(result.category_discount, 0)

    # ------------------------------------------------
    # 18. Negative price
    # ------------------------------------------------
    def test_18_negative_price(self):
        product = Product(
            "P001",
            "electronics",
            1,
            -100
        )

        with self.assertRaises(OrderProcessingError):
            calculate_order([product])

    # ------------------------------------------------
    # 19. Invalid product discount
    # ------------------------------------------------
    def test_19_invalid_discount(self):
        product = Product(
            "P001",
            "electronics",
            1,
            1000,
            discount=110
        )

        with self.assertRaises(OrderProcessingError):
            calculate_order([product])

    # ------------------------------------------------
    # 20. Empty order
    # ------------------------------------------------
    def test_20_empty_order(self):

        with self.assertRaises(OrderProcessingError):
            calculate_order([])

    # ------------------------------------------------
    # 21. Multiple categories
    # ------------------------------------------------
    def test_21_multiple_categories(self):

        products = [
            Product("P001", "electronics", 1, 1000),
            Product("P002", "clothing", 2, 500),
            Product("P003", "grocery", 3, 200),
            Product("P004", "books", 2, 300)
        ]

        result = calculate_order(
            products,
            coupon_code="WELCOME5"
        )

        self.assertGreater(result.final_amount, 0)

    # ------------------------------------------------
    # 22. Bulk + coupon
    # ------------------------------------------------
    def test_22_bulk_and_coupon(self):

        product = Product(
            "P001",
            "electronics",
            20,
            100
        )

        result = calculate_order(
            [product],
            coupon_code="SAVE10"
        )

        self.assertGreater(result.bulk_discount, 0)
        self.assertGreater(result.coupon_discount, 0)

    # ------------------------------------------------
    # 23. Different tax
    # ------------------------------------------------
    def test_23_different_tax(self):

        product = Product(
            "P001",
            "electronics",
            2,
            1000,
            tax=12
        )

        result = calculate_order([product])

        self.assertGreater(result.gst, 0)

    # ------------------------------------------------
    # 24. Zero tax
    # ------------------------------------------------
    def test_24_zero_tax(self):

        product = Product(
            "P001",
            "books",
            1,
            500,
            tax=0
        )

        result = calculate_order([product])

        self.assertEqual(result.gst, 0)

    # ------------------------------------------------
    # 25. Large order
    # ------------------------------------------------
    def test_25_large_order(self):

        products = [
            Product("P001", "electronics", 50, 1000),
            Product("P002", "clothing", 30, 500)
        ]

        result = calculate_order(
            products,
            coupon_code="SAVE15"
        )

        self.assertGreater(result.final_amount, 0)


if __name__ == "__main__":

    print("\n======================================")
    print(" E-COMMERCE ORDER MANAGEMENT QA")
    print("======================================\n")

    unittest.main(verbosity=2)
