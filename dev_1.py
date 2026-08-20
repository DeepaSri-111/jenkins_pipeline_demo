"""
OrderManagement.py
E-Commerce Order Processing System
Development Code
"""

from dataclasses import dataclass


class OrderProcessingError(Exception):
    """Custom exception for order processing errors."""
    pass


@dataclass
class Product:
    product_id: str
    category: str
    quantity: int
    unit_price: float
    discount: float = 0.0
    tax: float = 18.0
    in_stock: bool = True


@dataclass
class OrderResult:
    subtotal: float
    category_discount: float
    coupon_discount: float
    bulk_discount: float
    total_discount: float
    taxable_amount: float
    gst: float
    shipping_charge: float
    final_amount: float


# Category-specific discount percentages
CATEGORY_DISCOUNTS = {
    "electronics": 5.0,
    "clothing": 10.0,
    "grocery": 3.0,
    "books": 8.0
}

# Valid coupon codes
COUPONS = {
    "SAVE10": 10.0,
    "SAVE15": 15.0,
    "WELCOME5": 5.0
}

# Maximum total discount allowed
MAX_DISCOUNT_PERCENT = 20.0

# Free shipping threshold
FREE_SHIPPING_THRESHOLD = 500.0

# Shipping charge below threshold
SHIPPING_CHARGE = 50.0

# Bulk order quantity
BULK_QUANTITY = 10

# Bulk discount
BULK_DISCOUNT_PERCENT = 5.0


def validate_product(product):
    """Validate product information."""

    if not product.product_id:
        raise OrderProcessingError("Invalid product ID.")

    if product.quantity <= 0:
        raise OrderProcessingError(
            f"Invalid quantity for {product.product_id}."
        )

    if product.unit_price < 0:
        raise OrderProcessingError(
            f"Invalid price for {product.product_id}."
        )

    if not product.in_stock:
        raise OrderProcessingError(
            f"Product {product.product_id} is out of stock."
        )

    if product.tax < 0:
        raise OrderProcessingError(
            f"Invalid tax for {product.product_id}."
        )


def calculate_order(products, coupon_code=None):
    """
    Process an order containing multiple products.
    """

    if not products:
        raise OrderProcessingError("Order cannot be empty.")

    # Validate every product
    for product in products:
        validate_product(product)

    # ------------------------------------------------
    # 1. Calculate subtotal
    # ------------------------------------------------
    subtotal = sum(
        product.quantity * product.unit_price
        for product in products
    )

    # ------------------------------------------------
    # 2. Category-specific discount
    # ------------------------------------------------
    category_discount = 0.0

    for product in products:
        category_rate = CATEGORY_DISCOUNTS.get(
            product.category.lower(), 0.0
        )

        product_discount = (
            product.quantity
            * product.unit_price
            * category_rate
            / 100
        )

        category_discount += product_discount

    # ------------------------------------------------
    # 3. Product-specific discount
    # ------------------------------------------------
    product_discount_total = 0.0

    for product in products:
        if product.discount < 0 or product.discount > 100:
            raise OrderProcessingError(
                f"Invalid discount for {product.product_id}."
            )

        product_discount_total += (
            product.quantity
            * product.unit_price
            * product.discount
            / 100
        )

    # ------------------------------------------------
    # 4. Bulk order discount
    # ------------------------------------------------
    bulk_discount = 0.0

    for product in products:
        if product.quantity >= BULK_QUANTITY:
            bulk_discount += (
                product.quantity
                * product.unit_price
                * BULK_DISCOUNT_PERCENT
                / 100
            )

    # ------------------------------------------------
    # 5. Coupon discount
    # ------------------------------------------------
    coupon_discount = 0.0

    if coupon_code is not None:

        coupon_code = coupon_code.upper()

        if coupon_code not in COUPONS:
            raise OrderProcessingError(
                f"Invalid coupon code: {coupon_code}"
            )

        coupon_rate = COUPONS[coupon_code]

        coupon_discount = subtotal * coupon_rate / 100

    # ------------------------------------------------
    # 6. Apply maximum discount limit
    # ------------------------------------------------
    total_discount_before_limit = (
        category_discount
        + product_discount_total
        + bulk_discount
        + coupon_discount
    )

    maximum_discount = (
        subtotal * MAX_DISCOUNT_PERCENT / 100
    )

    total_discount = min(
        total_discount_before_limit,
        maximum_discount
    )

    # Keep discounts proportionally limited
    if total_discount_before_limit > 0:
        reduction_factor = (
            total_discount / total_discount_before_limit
        )

        category_discount *= reduction_factor
        product_discount_total *= reduction_factor
        bulk_discount *= reduction_factor
        coupon_discount *= reduction_factor

    # ------------------------------------------------
    # 7. Taxable amount
    # ------------------------------------------------
    taxable_amount = subtotal - total_discount

    # ------------------------------------------------
    # 8. GST calculation
    # ------------------------------------------------
    # Use average tax rate from products.
    weighted_tax = 0.0

    for product in products:
        product_value = (
            product.quantity * product.unit_price
        )

        weighted_tax += product_value * product.tax

    average_tax_rate = (
        weighted_tax / subtotal
        if subtotal > 0
        else 0
    )

    gst = taxable_amount * average_tax_rate / 100

    # ------------------------------------------------
    # 9. Shipping charge
    # ------------------------------------------------
    if taxable_amount >= FREE_SHIPPING_THRESHOLD:
        shipping_charge = 0.0
    else:
        shipping_charge = SHIPPING_CHARGE

    # ------------------------------------------------
    # 10. Final amount
    # ------------------------------------------------
    final_amount = (
        taxable_amount
        + gst
        + shipping_charge
    )

    return OrderResult(
        subtotal=round(subtotal, 2),
        category_discount=round(category_discount, 2),
        coupon_discount=round(coupon_discount, 2),
        bulk_discount=round(bulk_discount, 2),
        total_discount=round(total_discount, 2),
        taxable_amount=round(taxable_amount, 2),
        gst=round(gst, 2),
        shipping_charge=round(shipping_charge, 2),
        final_amount=round(final_amount, 2)
    )


def display_result(result):
    """Display order calculation."""

    print("\n========== ORDER SUMMARY ==========")
    print(f"Subtotal           : ₹{result.subtotal:.2f}")
    print(f"Category Discount  : ₹{result.category_discount:.2f}")
    print(f"Coupon Discount    : ₹{result.coupon_discount:.2f}")
    print(f"Bulk Discount      : ₹{result.bulk_discount:.2f}")
    print(f"Total Discount     : ₹{result.total_discount:.2f}")
    print(f"Taxable Amount     : ₹{result.taxable_amount:.2f}")
    print(f"GST                : ₹{result.gst:.2f}")
    print(f"Shipping Charge    : ₹{result.shipping_charge:.2f}")
    print("----------------------------------")
    print(f"FINAL AMOUNT       : ₹{result.final_amount:.2f}")
    print("==================================\n")


# ------------------------------------------------
# Main program
# ------------------------------------------------

if __name__ == "__main__":

    products = [
        Product(
            product_id="P001",
            category="electronics",
            quantity=2,
            unit_price=1000,
            discount=2,
            tax=18
        ),
        Product(
            product_id="P002",
            category="clothing",
            quantity=3,
            unit_price=500,
            discount=0,
            tax=5
        )
    ]

    try:
        result = calculate_order(
            products,
            coupon_code="SAVE10"
        )

        display_result(result)

    except OrderProcessingError as error:
        print(f"ERROR: {error}")
