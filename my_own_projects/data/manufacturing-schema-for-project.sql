-- Довідники (dimension tables)

-- Товари/продукція
CREATE TABLE dim_products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) UNIQUE,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    unit_of_measure VARCHAR(20),
    standard_cost DECIMAL(10,2),
    list_price DECIMAL(10,2),
    created_date DATE,
    discontinued_date DATE,
    is_active BOOLEAN DEFAULT true
);

-- Співробітники
CREATE TABLE dim_employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    department_id INTEGER,
    position VARCHAR(100),
    hire_date DATE,
    termination_date DATE,
    salary DECIMAL(10,2),
    manager_id INTEGER,
    is_active BOOLEAN DEFAULT true
);

-- Підрозділи
CREATE TABLE dim_departments (
    department_id SERIAL PRIMARY KEY,
    department_code VARCHAR(50) UNIQUE,
    department_name VARCHAR(100),
    parent_department_id INTEGER,
    manager_id INTEGER,
    cost_center VARCHAR(50),
    created_date DATE,
    is_active BOOLEAN DEFAULT true
);

-- Клієнти
CREATE TABLE dim_customers (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(50) UNIQUE,
    company_name VARCHAR(200),
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    customer_category VARCHAR(50),
    created_date DATE,
    is_active BOOLEAN DEFAULT true
);

-- Таблиці фактів (fact tables)

-- Продажі
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    order_date DATE,
    delivery_date DATE,
    product_id INTEGER REFERENCES dim_products(product_id),
    customer_id INTEGER REFERENCES dim_customers(customer_id),
    employee_id INTEGER REFERENCES dim_employees(employee_id),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    discount DECIMAL(5,2),
    total_amount DECIMAL(12,2),
    order_status VARCHAR(50),
    payment_terms VARCHAR(50),
    shipping_method VARCHAR(50)
);

-- Виробництво
CREATE TABLE fact_production (
    production_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES dim_products(product_id),
    batch_number VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    planned_quantity INTEGER,
    produced_quantity INTEGER,
    defect_quantity INTEGER,
    employee_id INTEGER REFERENCES dim_employees(employee_id),
    machine_id INTEGER,
    production_line VARCHAR(50),
    production_cost DECIMAL(12,2),
    energy_consumption DECIMAL(10,2),
    production_status VARCHAR(50),
    quality_check_status VARCHAR(50)
);

-- Індекси для оптимізації запитів
CREATE INDEX idx_sales_date ON fact_sales(order_date);
CREATE INDEX idx_production_date ON fact_production(start_date);
CREATE INDEX idx_product_category ON dim_products(category);
CREATE INDEX idx_employee_department ON dim_employees(department_id);
