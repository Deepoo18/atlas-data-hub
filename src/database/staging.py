from psycopg2.extras import execute_batch,register_uuid
from zmq import NULL
from src.database.connection import get_connection
import uuid
from datetime import datetime
from src.utils.logger import log
register_uuid()  # Register the UUID type with psycopg2

def staging_data_to_db(data, table_name):
    conn = get_connection()
    cursor = conn.cursor()
    batch_uuid = uuid.uuid4()  # Generate a unique UUID for this batch

    for row in data:
        row['batch_id']=batch_uuid  # Print each row to the console for debugging

    columns = data[0].keys()
    column_name = ",".join(columns)
    placeholders = ", ".join(f"%({column})s" for column in columns)

    insert_query = f"""
    INSERT INTO {table_name} ({column_name}) VALUES ({placeholders})
    """
    try:
        execute_batch(cursor, insert_query, data)
        log.INFO("Executed batch")
        print(f"Inserted {len(data)} records into {table_name} successfully.")

        batch_data={
            "batch_id": batch_uuid,
            "total_records": len(data),
            "batch_status": "COMPLETED",
            "created_at": datetime.today(),
            "error_message": NULL
        }
        insert_query_batch = f"""INSERT INTO ingestion_batches (batch_id, total_records, batch_status, created_at, error_message) VALUES (%(batch_id)s, %(total_records)s, %(batch_status)s, %(created_at)s, %(error_message)s)"""
    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        batch_data["batch_status"] = "FAILED"
        batch_data["error_message"] = str(e)
        insert_query_batch = f"""INSERT INTO ingestion_batches (batch_id, total_records, batch_status, created_at, error_message) VALUES (%(batch_id)s, %(total_records)s, %(batch_status)s, %(created_at)s, %(error_message)s)"""

    cursor.execute(insert_query_batch, batch_data)
    conn.commit()
    cursor.close()
    conn.close()
    return batch_uuid  # Return the batch UUID for reference

def validate_staging_data(batch_id):
    conn = get_connection()

    cursor = conn.cursor()
    invalid_query = """ 
        SELECT * from staging_orders s 
        WHERE s.batch_id = %s and 
        (s.customer_id is NULL
        or s.product_name is NULL
        or s.quantity is NULL
        or s.order_date is NULL
        or s.unit_price < 0
        or s.order_status not in ('PENDING', 'PAID', 'CANCELLED', 'REFUNDED'))
        or 
        NOT EXISTS (
        SELECT 1 
        FROM customers c
        WHERE c.customer_id = s.customer_id
        )
        or EXISTS(
        SELECT 1
        FROM orders o
        WHERE o.order_id = s.order_id
        )
        or s.order_id in (
        SELECT order_id
        from orders o
        group by order_id
        having count(*) > 1);
    """
    cursor.execute(invalid_query,(batch_id,))
    rows = cursor.fetchall()
    if rows:
        error_msg = (
            f"batch rejected: Invalid records found"
        )
        print("Invalid records")
        cursor.execute("""UPDATE ingestion_batches SET batch_status = 'REJECTED',error_message=%s WHERE batch_id = %s;""",(error_msg,batch_id))
        conn.commit()
        print(error_msg)

    else:
        cursor.execute("""INSERT INTO orders (
                order_id,
                customer_id,
                product_name,
                quantity,
                order_date,
                unit_price,
                order_status
            )
            SELECT
                order_id,
                customer_id,
                product_name,
                quantity,
                order_date,
                unit_price,
                order_status
            FROM staging_orders
            WHERE batch_id = %s
        """, (batch_id,))

    cursor.execute("""UPDATE ingestion_batches SET batch_status='ACCEPTED',error_message=NULL WHERE batch_id = %s""",(batch_id,))
    conn.commit()
    cursor.close()
    conn.close()
