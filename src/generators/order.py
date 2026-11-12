from src.database.connection import get_connection
from faker import Faker
from dotenv import load_dotenv

load_dotenv()

def generate_order(num_orders):
    conn = get_connection()

    cursor = conn.cursor()
    fake = Faker()
    cursor.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(num_orders):
        order_id = fake.random_number(digits=5)  # Generate a unique order ID
        customer_id = fake.random_element(elements=customer_ids)
        product_name = fake.word()  # Generate a unique product name
        quantity = fake.random_int(min=1, max=10)
        order_date = fake.date_this_year()  # Generate a random order date within this year
        
        unit_price = round(fake.random_number(digits=6), 2)  # Generate a random unit price
        order_status = fake.random_element(elements=('PENDING', 'PAID', 'CANCELLED', 'REFUNDED'))  # Random order status
        try:
            cursor.execute("INSERT INTO orders (order_id, customer_id, order_date, product_name, unit_price, quantity, order_status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (order_id, customer_id, order_date, product_name, unit_price, quantity, order_status))
        except Exception as e:
            conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error occurred while inserting order: {e}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    num_orders = 4415  # Specify the number of orders to generate
    generate_order(num_orders)  # Specify the number of orders to generate
