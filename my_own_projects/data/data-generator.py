import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Налаштування
fake = Faker('uk_UA')
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
n_products = 100
n_employees = 200
n_customers = 150
n_sales = 1000
n_production = 1500

def random_date(start_date, end_date):
    """Генерує випадкову дату в заданому діапазоні"""
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

def generate_products():
    """Генерує дані про продукцію"""
    categories = ['Металовироби', 'Електроніка', 'Пластикові вироби', 'Меблі']
    subcategories = {
        'Металовироби': ['Труби', 'Листовий метал', 'Металоконструкції'],
        'Електроніка': ['Плати', 'Кабелі', 'Датчики'],
        'Пластикові вироби': ['Контейнери', 'Труби ПВХ', 'Деталі'],
        'Меблі': ['Офісні меблі', 'Промислові меблі', 'Спецзамовлення']
    }
    
    products = []
    for i in range(n_products):
        category = random.choice(categories)
        products.append({
            'product_id': i + 1,
            'product_code': f'P{str(i+1).zfill(4)}',
            'product_name': fake.word().title() + ' ' + fake.word(),
            'category': category,
            'subcategory': random.choice(subcategories[category]),
            'unit_of_measure': random.choice(['шт', 'кг', 'м', 'м2', 'м3']),
            'standard_cost': round(random.uniform(100, 5000), 2),
            'list_price': round(random.uniform(150, 7500), 2),
            'created_date': random_date(start_date, end_date),
            'is_active': random.choice([True, True, True, False])  # 75% активних
        })
    return pd.DataFrame(products)

def generate_employees():
    """Генерує дані про співробітників"""
    departments = {
        1: 'Виробництво',
        2: 'Продажі',
        3: 'Фінанси',
        4: 'Склад',
        5: 'Логістика',
        6: 'Якість'
    }
    
    positions = {
        'Виробництво': ['Оператор', 'Майстер', 'Начальник цеху'],
        'Продажі': ['Менеджер з продажу', 'Старший менеджер', 'Керівник відділу'],
        'Фінанси': ['Бухгалтер', 'Економіст', 'Фінансовий директор'],
        'Склад': ['Комірник', 'Завідувач складу', 'Логіст'],
        'Логістика': ['Водій', 'Диспетчер', 'Керівник відділу'],
        'Якість': ['Контролер якості', 'Інженер з якості', 'Керівник відділу']
    }
    
    employees = []
    for i in range(n_employees):
        dept_id = random.randint(1, len(departments))
        dept_name = departments[dept_id]
        
        employees.append({
            'employee_id': i + 1,
            'employee_code': f'E{str(i+1).zfill(4)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'department_id': dept_id,
            'position': random.choice(positions[dept_name]),
            'hire_date': random_date(start_date - timedelta(days=365*3), end_date),
            'salary': round(random.uniform(10000, 50000), 2),
            'is_active': random.choice([True, True, True, False])
        })
    return pd.DataFrame(employees)

def generate_customers():
    """Генерує дані про клієнтів"""
    customers = []
    for i in range(n_customers):
        customers.append({
            'customer_id': i + 1,
            'customer_code': f'C{str(i+1).zfill(4)}',
            'company_name': fake.company(),
            'contact_person': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'city': fake.city(),
            'country': 'Україна',
            'customer_category': random.choice(['A', 'B', 'C']),
            'created_date': random_date(start_date, end_date),
            'is_active': random.choice([True, True, True, False])
        })
    return pd.DataFrame(customers)

def generate_sales(products_df, customers_df, employees_df):
    """Генерує дані про продажі"""
    sales = []
    for i in range(n_sales):
        order_date = random_date(start_date, end_date)
        
        # Вибираємо тільки активних співробітників відділу продажів
        sales_employees = employees_df[
            (employees_df['department_id'] == 2) & 
            (employees_df['is_active'] == True)
        ]
        
        # Вибираємо тільки активних клієнтів та продукти
        active_customers = customers_df[customers_df['is_active'] == True]
        active_products = products_df[products_df['is_active'] == True]
        
        if not len(sales_employees) or not len(active_customers) or not len(active_products):
            continue
            
        product = active_products.sample(1).iloc[0]
        
        sales.append({
            'sale_id': i + 1,
            'order_date': order_date,
            'delivery_date': order_date + timedelta(days=random.randint(1, 14)),
            'product_id': product['product_id'],
            'customer_id': active_customers.sample(1).iloc[0]['customer_id'],
            'employee_id': sales_employees.sample(1).iloc[0]['employee_id'],
            'quantity': random.randint(1, 100),
            'unit_price': product['list_price'],
            'discount': round(random.uniform(0, 0.15), 2),
            'order_status': random.choice(['Новий', 'В обробці', 'Відвантажено', 'Завершено']),
            'payment_terms': random.choice(['Передоплата', 'Часткова оплата', 'Післяплата']),
            'shipping_method': random.choice(['Самовивіз', 'Доставка', 'Нова пошта'])
        })
    return pd.DataFrame(sales)

def generate_production(products_df, employees_df):
    """Генерує дані про виробництво"""
    production = []
    for i in range(n_production):
        start_date_prod = random_date(start_date, end_date)
        planned_qty = random.randint(50, 1000)
        
        # Вибираємо тільки активних співробітників виробництва
        prod_employees = employees_df[
            (employees_df['department_id'] == 1) & 
            (employees_df['is_active'] == True)
        ]
        
        # Вибираємо тільки активні продукти
        active_products = products_df[products_df['is_active'] == True]
        
        if not len(prod_employees) or not len(active_products):
            continue
            
        produced_qty = round(planned_qty * random.uniform(0.9, 1.1))
        defect_qty = round(produced_qty * random.uniform(0, 0.05))
        
        production.append({
            'production_id': i + 1,
            'product_id': active_products.sample(1).iloc[0]['product_id'],
            'batch_number': f'B{str(i+1).zfill(6)}',
            'start_date': start_date_prod,
            'end_date': start_date_prod + timedelta(hours=random.randint(4, 72)),
            'planned_quantity': planned_qty,
            'produced_quantity': produced_qty,
            'defect_quantity': defect_qty,
            'employee_id': prod_employees.sample(1).iloc[0]['employee_id'],
            'machine_id': random.randint(1, 10),
            'production_line': f'Лінія {random.randint(1, 5)}',
            'production_cost': round(random.uniform(1000, 50000), 2),
            'energy_consumption': round(random.uniform(100, 1000), 2),
            'production_status': random.choice(['Заплановано', 'В процесі', 'Завершено']),
            'quality_check_status': random.choice(['Очікує', 'Пройдено', 'Відхилено'])
        })
    return pd.DataFrame(production)

# Генеруємо дані
products_df = generate_products()
employees_df = generate_employees()
customers_df = generate_customers()
sales_df = generate_sales(products_df, customers_df, employees_df)
production_df = generate_production(products_df, employees_df)

# Зберігаємо дані в CSV
products_df.to_csv('dim_products.csv', index=False)
employees_df.to_csv('dim_employees.csv', index=False)
customers_df.to_csv('dim_customers.csv', index=False)
sales_df.to_csv('fact_sales.csv', index=False)
production_df.to_csv('fact_production.csv', index=False)
