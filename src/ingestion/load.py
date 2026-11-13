from src.generators.order import generate_order
from src.database.connection import load_data_to_db, get_connection
from src.database.staging import staging_data_to_db,validate_staging_data

if __name__ == "__main__":
    num_orders = 100
    orders = generate_order(num_orders)
    batch_id=staging_data_to_db(orders, "staging_orders")
    validate_staging_data(batch_id)

