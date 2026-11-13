CREATE TABLE customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id UUID NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0),
    order_status VARCHAR(20) NOT NULL
        CHECK (order_status IN (
            'PENDING', 'PAID', 'CANCELLED', 'REFUNDED'
        )),
    order_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_customer_id
    ON orders(customer_id);

CREATE INDEX idx_orders_order_date
    ON orders(order_date);

CREATE TABLE staging_orders (
    batch_id UUID NOT NULL,
    order_id INT,
    customer_id UUID,
    product_name VARCHAR(100),
    quantity INT,
    order_date TIMESTAMPTZ,
    unit_price NUMERIC(10, 2),
    order_status VARCHAR(20),
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ingestion_batches (
    batch_id UUID PRIMARY KEY,
    total_records INT NOT NULL,
    batch_status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
);