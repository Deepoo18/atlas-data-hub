from src.database.connection import get_connection
from faker import Faker
from typing import List, Dict, Any

def generate_order(num_orders)->List[Dict[str,Any]]:
    orders = []
    conn = get_connection()
    cursor = conn.cursor()
    fake = Faker()

    cursor.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("select order_id from orders")
    order_ids = [row[0] for row in cursor.fetchall()]


    for i in range(num_orders):
        order_id = i+10000
        if order_id in order_ids:
            order_id = fake.random_number(digits=5)  # Generate a new order_id if it already exists
        customer_id = fake.random_element(elements=customer_ids)
        product_name = fake.word()  # Generate a unique product name
        quantity = fake.random_int(min=1, max=10)
        order_date = fake.date_this_year()  # Generate a random order date within this year
        
        unit_price = round(fake.random_number(digits=6), 2)  # Generate a random unit price
        order_status = fake.random_element(elements=('PENDING', 'PAID', 'CANCELLED', 'REFUNDED'))  # Random order status
        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "product_name": product_name,
            "quantity": quantity,
            "order_date": order_date,
            "unit_price": unit_price,
            "order_status": order_status
        }
        orders.append(order)

    cursor.close()
    conn.close()
    return orders
