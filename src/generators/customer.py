from src.database.connection import get_connection
from faker import Faker

def generate_customers(num_customers):
    conn = get_connection()
    cursor = conn.cursor()
    fake = Faker()

    for i in range(num_customers):
        customer_id = fake.uuid4() 
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.random_number(digits=10)
        created_at = fake.date_time_this_year()  # Generate a random creation date within this year
         # Generate a unique customer ID
        try:
            cursor.execute("INSERT INTO customers (customer_id, first_name, last_name, email, phone_number, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                       (customer_id, first_name, last_name, email, phone_number, created_at))
        except Exception as e:
            conn.rollback()
            print(f"Error occurred while inserting customer: {e}")
        if i % 500 == 0:
            print(f"Inserted {i} customers...")
            conn.commit()  # Commit every 500 inserts to avoid large transactions

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    num_customers = 10000  # Specify the number of customers to generate
    generate_customers(num_customers)