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

# Додаємо нові параметри
n_inventory = 2000
n_logistics = 1200
n_quality = 800

def generate_inventory(products_df):
    """Генерує дані про складські запаси"""
    inventory = []
    warehouses = ['Головний склад', 'Склад сировини', 'Склад готової продукції', 'Склад матеріалів']
    
    for i in range(n_inventory):
        record_date = random_date(start_date, end_date)
        
        # Вибираємо тільки активні продукти
        active_products = products_df[products_df['is_active'] == True]
        if not len(active_products):
            continue
            
        product = active_products.sample(1).iloc[0]
        min_stock = random.randint(10, 50)
        max_stock = min_stock * 3
        
        inventory.append({
            'inventory_id': i + 1,
            'product_id': product['product_id'],
            'warehouse': random.choice(warehouses),
            'record_date': record_date,
            'quantity_on_hand': random.randint(0, max_stock),
            'min_stock_level': min_stock,
            'max_stock_level': max_stock,
            'reorder_point': min_stock * 1.5,
            'unit_cost': product['standard_cost'],
            'total_value': 0,  # заповнимо пізніше
            'last_count_date': record_date - timedelta(days=random.randint(1, 30)),
            'storage_location': f'Ряд {random.randint(1,20)}-Стелаж {random.randint(1,50)}-Позиція {random.randint(1,10)}',
            'status': random.choice(['В наявності', 'Низький запас', 'Критичний запас', 'Надлишок'])
        })
    
    inventory_df = pd.DataFrame(inventory)
    # Розраховуємо загальну вартість
    inventory_df['total_value'] = inventory_df['quantity_on_hand'] * inventory_df['unit_cost']
    return inventory_df

def generate_logistics(sales_df, production_df):
    """Генерує дані про логістику"""
    logistics = []
    transport_types = ['Вантажівка', 'Мікроавтобус', 'Фура', 'Легковий автомобіль']
    destinations = ['Клієнт', 'Склад', 'Виробництво', 'Постачальник']
    
    for i in range(n_logistics):
        transport_date = random_date(start_date, end_date)
        destination = random.choice(destinations)
        
        # Пов'язуємо з продажами або виробництвом
        if destination == 'Клієнт':
            related_sale = sales_df.sample(1).iloc[0] if len(sales_df) else None
            related_id = related_sale['sale_id'] if related_sale is not None else None
        else:
            related_production = production_df.sample(1).iloc[0] if len(production_df) else None
            related_id = related_production['production_id'] if related_production is not None else None
            
        logistics.append({
            'logistics_id': i + 1,
            'transport_date': transport_date,
            'transport_type': random.choice(transport_types),
            'destination_type': destination,
            'related_id': related_id,
            'distance_km': random.randint(1, 1000),
            'fuel_consumption': round(random.uniform(5, 30), 2),
            'transport_cost': round(random.uniform(500, 5000), 2),
            'driver_name': fake.name(),
            'vehicle_number': f'AA{random.randint(1000, 9999)}AA',
            'start_time': transport_date + timedelta(hours=random.randint(0, 23)),
            'estimated_arrival': None,  # заповнимо пізніше
            'actual_arrival': None,  # заповнимо пізніше
            'status': random.choice(['Заплановано', 'В дорозі', 'Доставлено', 'Затримка'])
        })
    
    logistics_df = pd.DataFrame(logistics)
    # Додаємо часи прибуття
    for idx, row in logistics_df.iterrows():
        travel_hours = row['distance_km'] / 60  # Середня швидкість 60 км/год
        logistics_df.at[idx, 'estimated_arrival'] = row['start_time'] + timedelta(hours=travel_hours)
        # Додаємо випадкове відхилення для фактичного часу прибуття
        delay = random.uniform(-0.5, 2) if row['status'] != 'Затримка' else random.uniform(2, 5)
        logistics_df.at[idx, 'actual_arrival'] = row['start_time'] + timedelta(hours=travel_hours + delay)
    
    return logistics_df

def generate_quality(production_df, products_df):
    """Генерує дані про контроль якості"""
    quality = []
    test_types = ['Візуальний контроль', 'Розмірний контроль', 'Функціональний тест', 
                 'Хімічний аналіз', 'Механічні випробування', 'Електричні випробування']
    
    for i in range(n_quality):
        # Беремо випадкове виробництво та пов'язаний продукт
        if len(production_df) and len(products_df):
            production = production_df.sample(1).iloc[0]
            product = products_df[products_df['product_id'] == production['product_id']].iloc[0]
            
            test_date = production['end_date']
            
            # Визначаємо тести залежно від категорії продукту
            category_tests = {
                'Металовироби': ['Механічні випробування', 'Розмірний контроль', 'Візуальний контроль'],
                'Електроніка': ['Електричні випробування', 'Функціональний тест', 'Візуальний контроль'],
                'Пластикові вироби': ['Хімічний аналіз', 'Розмірний контроль', 'Візуальний контроль'],
                'Меблі': ['Механічні випробування', 'Розмірний контроль', 'Візуальний контроль']
            }
            
            available_tests = category_tests.get(product['category'], test_types)
            test_type = random.choice(available_tests)
            
            # Генеруємо результати тестів
            is_passed = random.random() > 0.1  # 90% тестів проходять успішно
            
            quality.append({
                'quality_check_id': i + 1,
                'production_id': production['production_id'],
                'product_id': product['product_id'],
                'test_date': test_date,
                'test_type': test_type,
                'test_result': 'Пройдено' if is_passed else 'Не пройдено',
                'measured_value': round(random.uniform(95, 105), 2),  # відсоток від норми
                'standard_value': 100,
                'deviation': 0,  # заповнимо пізніше
                'inspector_name': fake.name(),
                'equipment_used': f'Обладнання {random.randint(1,10)}',
                'notes': fake.text(max_nb_chars=200) if not is_passed else None,
                'requires_rework': not is_passed,
                'batch_size_tested': random.randint(5, 50),
                'defects_found': random.randint(0, 5) if not is_passed else 0
            })
    
    quality_df = pd.DataFrame(quality)
    # Розраховуємо відхилення
    quality_df['deviation'] = quality_df['measured_value'] - quality_df['standard_value']
    
    return quality_df

# Генеруємо нові дані
inventory_df = generate_inventory(products_df)
logistics_df = generate_logistics(sales_df, production_df)
quality_df = generate_quality(production_df, products_df)

# Зберігаємо нові дані в CSV
inventory_df.to_csv('fact_inventory.csv', index=False)
logistics_df.to_csv('fact_logistics.csv', index=False)
quality_df.to_csv('fact_quality.csv', index=False)

# Додаємо нові параметри
n_equipment = 50  # кількість одиниць обладнання
n_maintenance = 1000  # кількість записів про ремонти
n_spare_parts = 200  # кількість типів запчастин

def generate_equipment():
    """Генерує дані про обладнання підприємства"""
    equipment_types = {
        'Верстат': ['Токарний', 'Фрезерний', 'Свердлильний', 'Шліфувальний'],
        'Конвеєр': ['Стрічковий', 'Роликовий', 'Пластинчастий'],
        'Прес': ['Гідравлічний', 'Механічний', 'Пневматичний'],
        'Робот': ['Зварювальний', 'Пакувальний', 'Складальний'],
        'Піч': ['Термічна', 'Плавильна', 'Сушильна']
    }
    
    equipment = []
    for i in range(n_equipment):
        equip_type = random.choice(list(equipment_types.keys()))
        purchase_date = random_date(start_date - timedelta(days=365*5), start_date)
        
        equipment.append({
            'equipment_id': i + 1,
            'equipment_code': f'EQ{str(i+1).zfill(4)}',
            'equipment_name': f'{random.choice(equipment_types[equip_type])} {equip_type} #{i+1}',
            'equipment_type': equip_type,
            'manufacturer': fake.company(),
            'model': f'Model-{fake.lexify(text="????")}-{random.randint(100,999)}',
            'serial_number': fake.uuid4()[:10],
            'purchase_date': purchase_date,
            'installation_date': purchase_date + timedelta(days=random.randint(5,20)),
            'warranty_end': purchase_date + timedelta(days=365*2),
            'location': f'Цех {random.randint(1,5)}, Дільниця {random.randint(1,10)}',
            'status': random.choice(['Працює', 'В ремонті', 'Очікує обслуговування', 'Резерв']),
            'last_maintenance': random_date(start_date, end_date),
            'maintenance_interval_days': random.choice([30, 60, 90, 180, 365]),
            'power_consumption_kwh': round(random.uniform(5, 50), 2),
            'operating_hours': random.randint(1000, 20000)
        })
    return pd.DataFrame(equipment)

def generate_spare_parts():
    """Генерує дані про запчастини"""
    categories = ['Механічні', 'Електричні', 'Гідравлічні', 'Пневматичні', 'Електронні']
    spare_parts = []
    
    for i in range(n_spare_parts):
        spare_parts.append({
            'part_id': i + 1,
            'part_code': f'SP{str(i+1).zfill(4)}',
            'part_name': fake.word() + ' ' + random.choice(['Датчик', 'Клапан', 'Підшипник', 'Вал', 'Двигун', 'Насос']),
            'category': random.choice(categories),
            'description': fake.text(max_nb_chars=100),
            'supplier': fake.company(),
            'unit_price': round(random.uniform(100, 5000), 2),
            'min_stock': random.randint(1, 10),
            'current_stock': random.randint(0, 20),
            'lead_time_days': random.randint(1, 30),
            'last_order_date': random_date(start_date, end_date),
            'shelf_life_months': random.randint(12, 60)
        })
    return pd.DataFrame(spare_parts)

def generate_maintenance(equipment_df, employees_df, spare_parts_df):
    """Генерує дані про ремонти та обслуговування"""
    maintenance_types = {
        'Планове обслуговування': {
            'duration_hours': (2, 8),
            'cost_range': (500, 2000),
            'parts_needed': (1, 3)
        },
        'Поточний ремонт': {
            'duration_hours': (4, 16),
            'cost_range': (1000, 5000),
            'parts_needed': (2, 5)
        },
        'Капітальний ремонт': {
            'duration_hours': (24, 72),
            'cost_range': (5000, 20000),
            'parts_needed': (5, 10)
        },
        'Аварійний ремонт': {
            'duration_hours': (1, 24),
            'cost_range': (2000, 10000),
            'parts_needed': (1, 7)
        }
    }
    
    maintenance = []
    
    # Відбираємо технічний персонал
    tech_employees = employees_df[
        (employees_df['department_id'] == 6) & 
        (employees_df['is_active'] == True)
    ]
    
    for i in range(n_maintenance):
        # Вибираємо випадкове обладнання
        equipment = equipment_df.sample(1).iloc[0]
        maint_type = random.choice(list(maintenance_types.keys()))
        type_params = maintenance_types[maint_type]
        
        start_datetime = random_date(start_date, end_date)
        duration = random.uniform(*type_params['duration_hours'])
        end_datetime = start_datetime + timedelta(hours=duration)
        
        # Вибираємо випадкові запчастини
        n_parts = random.randint(*type_params['parts_needed'])
        used_parts = spare_parts_df.sample(n=min(n_parts, len(spare_parts_df)))
        parts_cost = sum(used_parts['unit_price'])
        
        maintenance_record = {
            'maintenance_id': i + 1,
            'equipment_id': equipment['equipment_id'],
            'maintenance_type': maint_type,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'duration_hours': duration,
            'status': random.choice(['Заплановано', 'В процесі', 'Завершено', 'Відкладено']),
            'technician_id': tech_employees.sample(1).iloc[0]['employee_id'] if len(tech_employees) else None,
            'description': fake.text(max_nb_chars=200),
            'parts_cost': parts_cost,
            'labor_cost': round(random.uniform(*type_params['cost_range']), 2),
            'total_cost': 0,  # заповнимо пізніше
            'next_maintenance_date': end_datetime + timedelta(days=equipment['maintenance_interval_days']),
            'breakdown_cause': None,
            'resolution': None,
            'quality_check_status': random.choice(['Очікує', 'Пройдено', 'Потребує перевірки'])
        }
        
        # Додаємо причину поломки та рішення для аварійних ремонтів
        if maint_type == 'Аварійний ремонт':
            maintenance_record['breakdown_cause'] = random.choice([
                'Знос деталей', 'Перевантаження', 'Збій електроніки', 
                'Людський фактор', 'Відмова системи охолодження'
            ])
            maintenance_record['resolution'] = random.choice([
                'Заміна компонентів', 'Регулювання', 'Перепрограмування', 
                'Очистка системи', 'Модернізація вузла'
            ])
        
        # Розраховуємо загальну вартість
        maintenance_record['total_cost'] = maintenance_record['parts_cost'] + maintenance_record['labor_cost']
        
        maintenance.append(maintenance_record)
    
    return pd.DataFrame(maintenance)

# Генеруємо нові дані
equipment_df = generate_equipment()
spare_parts_df = generate_spare_parts()
maintenance_df = generate_maintenance(equipment_df, employees_df, spare_parts_df)

# Зберігаємо нові дані в CSV
equipment_df.to_csv('dim_equipment.csv', index=False)
spare_parts_df.to_csv('dim_spare_parts.csv', index=False)
maintenance_df.to_csv('fact_maintenance.csv', index=False)

# Додаємо нові параметри
n_transactions = 5000  # кількість фінансових транзакцій
n_budgets = 100  # кількість бюджетів по відділам
n_invoices = 2000  # кількість рахунків

def generate_chart_of_accounts():
    """Генерує план рахунків"""
    accounts = [
        # Активи
        {'account_id': 1000, 'name': 'Грошові кошти', 'type': 'Актив', 'category': 'Оборотні активи'},
        {'account_id': 1100, 'name': 'Дебіторська заборгованість', 'type': 'Актив', 'category': 'Оборотні активи'},
        {'account_id': 1200, 'name': 'Запаси', 'type': 'Актив', 'category': 'Оборотні активи'},
        {'account_id': 1300, 'name': 'Основні засоби', 'type': 'Актив', 'category': 'Необоротні активи'},
        
        # Зобов'язання
        {'account_id': 2000, 'name': 'Кредиторська заборгованість', 'type': 'Пасив', 'category': 'Поточні зобов\'язання'},
        {'account_id': 2100, 'name': 'Кредити', 'type': 'Пасив', 'category': 'Довгострокові зобов\'язання'},
        
        # Доходи
        {'account_id': 3000, 'name': 'Дохід від реалізації', 'type': 'Дохід', 'category': 'Операційні доходи'},
        {'account_id': 3100, 'name': 'Інші доходи', 'type': 'Дохід', 'category': 'Інші доходи'},
        
        # Витрати
        {'account_id': 4000, 'name': 'Собівартість реалізації', 'type': 'Витрати', 'category': 'Операційні витрати'},
        {'account_id': 4100, 'name': 'Заробітна плата', 'type': 'Витрати', 'category': 'Операційні витрати'},
        {'account_id': 4200, 'name': 'Комунальні послуги', 'type': 'Витрати', 'category': 'Операційні витрати'},
        {'account_id': 4300, 'name': 'Амортизація', 'type': 'Витрати', 'category': 'Операційні витрати'},
        {'account_id': 4400, 'name': 'Ремонт та обслуговування', 'type': 'Витрати', 'category': 'Операційні витрати'},
        {'account_id': 4500, 'name': 'Маркетинг та реклама', 'type': 'Витрати', 'category': 'Операційні витрати'}
    ]
    return pd.DataFrame(accounts)

def generate_transactions(accounts_df, sales_df, maintenance_df):
    """Генерує фінансові транзакції"""
    transactions = []
    
    for i in range(n_transactions):
        transaction_date = random_date(start_date, end_date)
        
        # Визначаємо тип транзакції
        transaction_type = random.choice(['Продаж', 'Закупівля', 'Зарплата', 'Комунальні', 'Ремонт', 'Інше'])
        
        if transaction_type == 'Продаж' and len(sales_df):
            # Беремо дані з реальних продажів
            sale = sales_df.sample(1).iloc[0]
            amount = sale['quantity'] * sale['unit_price'] * (1 - sale['discount'])
            debit_account = accounts_df[accounts_df['name'] == 'Грошові кошти']['account_id'].iloc[0]
            credit_account = accounts_df[accounts_df['name'] == 'Дохід від реалізації']['account_id'].iloc[0]
            reference_id = f'SALE-{sale["sale_id"]}'
            description = f'Продаж товару {sale["product_id"]}'
            
        elif transaction_type == 'Ремонт' and len(maintenance_df):
            # Беремо дані з реальних ремонтів
            maintenance = maintenance_df.sample(1).iloc[0]
            amount = maintenance['total_cost']
            debit_account = accounts_df[accounts_df['name'] == 'Ремонт та обслуговування']['account_id'].iloc[0]
            credit_account = accounts_df[accounts_df['name'] == 'Грошові кошти']['account_id'].iloc[0]
            reference_id = f'MAINT-{maintenance["maintenance_id"]}'
            description = f'Ремонт обладнання {maintenance["equipment_id"]}'
            
        else:
            # Генеруємо випадкові транзакції
            amount = round(random.uniform(1000, 100000), 2)
            if transaction_type == 'Зарплата':
                debit_account = accounts_df[accounts_df['name'] == 'Заробітна плата']['account_id'].iloc[0]
                description = 'Виплата заробітної плати'
            elif transaction_type == 'Комунальні':
                debit_account = accounts_df[accounts_df['name'] == 'Комунальні послуги']['account_id'].iloc[0]
                description = 'Оплата комунальних послуг'
            else:
                debit_account = accounts_df.sample(1).iloc[0]['account_id']
                description = fake.text(max_nb_chars=50)
            
            credit_account = accounts_df[accounts_df['name'] == 'Грошові кошти']['account_id'].iloc[0]
            reference_id = f'TRX-{i+1}'
        
        transactions.append({
            'transaction_id': i + 1,
            'date': transaction_date,
            'type': transaction_type,
            'debit_account': debit_account,
            'credit_account': credit_account,
            'amount': amount,
            'description': description,
            'reference_id': reference_id,
            'status': random.choice(['Проведено', 'Очікує', 'Відхилено']),
            'created_by': fake.name(),
            'created_at': transaction_date,
            'approved_by': fake.name() if random.random() > 0.1 else None,
            'approved_at': transaction_date + timedelta(hours=random.randint(1, 48)) if random.random() > 0.1 else None,
            'currency': 'UAH',
            'exchange_rate': 1.0,
        })
    
    return pd.DataFrame(transactions)

def generate_budgets(departments_df, accounts_df):
    """Генерує бюджети по відділам"""
    budgets = []
    
    for i in range(n_budgets):
        department = departments_df.sample(1).iloc[0]
        account = accounts_df[accounts_df['type'] == 'Витрати'].sample(1).iloc[0]
        
        # Визначаємо період бюджету
        year = random.choice([2023, 2024])
        month = random.randint(1, 12)
        period = f'{year}-{str(month).zfill(2)}'
        
        # Генеруємо планові показники
        planned_amount = round(random.uniform(10000, 1000000), 2)
        actual_amount = round(planned_amount * random.uniform(0.8, 1.2), 2)
        
        budgets.append({
            'budget_id': i + 1,
            'department_id': department['department_id'],
            'account_id': account['account_id'],
            'period': period,
            'planned_amount': planned_amount,
            'actual_amount': actual_amount,
            'variance': actual_amount - planned_amount,
            'variance_percentage': ((actual_amount - planned_amount) / planned_amount * 100).round(2),
            'status': random.choice(['Затверджено', 'Проект', 'На перегляді']),
            'notes': fake.text(max_nb_chars=100) if random.random() > 0.7 else None,
            'created_at': random_date(start_date, end_date),
            'approved_by': fake.name() if random.random() > 0.1 else None,
            'last_modified': random_date(start_date, end_date)
        })
    
    return pd.DataFrame(budgets)

def generate_invoices(sales_df, customers_df):
    """Генерує рахунки"""
    invoices = []
    payment_terms = ['30 днів', '45 днів', '60 днів', 'Передоплата']
    
    for i in range(n_invoices):
        # Беремо дані з реальних продажів якщо можливо
        if len(sales_df) and len(customers_df):
            sale = sales_df.sample(1).iloc[0]
            customer = customers_df[customers_df['customer_id'] == sale['customer_id']].iloc[0]
            amount = sale['quantity'] * sale['unit_price'] * (1 - sale['discount'])
            
            issue_date = sale['order_date']
            due_days = int(random.choice(payment_terms).split()[0])
            due_date = issue_date + timedelta(days=due_days)
            
            # Визначаємо статус оплати
            if random.random() > 0.2:  # 80% рахунків оплачені
                payment_date = issue_date + timedelta(days=random.randint(1, due_days))
                status = 'Оплачено'
            else:
                payment_date = None
                if due_date > datetime.now():
                    status = 'Очікує оплати'
                else:
                    status = 'Прострочено'
        else:
            # Генеруємо випадкові дані
            issue_date = random_date(start_date, end_date)
            due_days = int(random.choice(payment_terms).split()[0])
            due_date = issue_date + timedelta(days=due_days)
            amount = round(random.uniform(1000, 100000), 2)
            
            if random.random() > 0.2:
                payment_date = issue_date + timedelta(days=random.randint(1, due_days))
                status = 'Оплачено'
            else:
                payment_date = None
                status = 'Очікує оплати' if due_date > datetime.now() else 'Прострочено'
        
        invoices.append({
            'invoice_id': i + 1,
            'invoice_number': f'INV-{str(i+1).zfill(6)}',
            'sale_id': sale['sale_id'] if 'sale' in locals() else None,
            'customer_id': customer['customer_id'] if 'customer' in locals() else None,
            'issue_date': issue_date,
            'due_date': due_date,
            'amount': amount,
            'payment_terms': random.choice(payment_terms),
            'status': status,
            'payment_date': payment_date,
            'payment_method': random.choice(['Банківський переказ', 'Готівка', 'Картка']) if payment_date else None,
            'notes': fake.text(max_nb_chars=100) if random.random() > 0.8 else None
        })
    
    return pd.DataFrame(invoices)

# Генеруємо нові дані
accounts_df = generate_chart_of_accounts()
transactions_df = generate_transactions(accounts_df, sales_df, maintenance_df)
budgets_df = generate_budgets(departments_df, accounts_df)
invoices_df = generate_invoices(sales_df, customers_df)

# Зберігаємо нові дані в CSV
accounts_df.to_csv('dim_accounts.csv', index=False)
transactions_df.to_csv('fact_transactions.csv', index=False)
budgets_df.to_csv('fact_budgets.csv', index=False)
invoices_df.to_csv('fact_invoices.csv', index=False)

# Додаємо нові параметри
n_vacancies = 100  # кількість вакансій
n_applications = 500  # кількість заявок на роботу
n_trainings = 200  # кількість навчальних програм
n_attendance = 5000  # кількість записів відвідуваності
n_performance = 400  # кількість оцінок продуктивності

def generate_employee_details(employees_df):
    """Генерує додаткову інформацію про співробітників"""
    education_levels = ['Середня', 'Бакалавр', 'Магістр', 'PhD']
    marital_statuses = ['Неодружений/а', 'Одружений/а', 'Розлучений/а']
    
    employee_details = []
    
    for _, employee in employees_df.iterrows():
        # Генеруємо базову зарплату в залежності від позиції
        if 'Керівник' in employee['position']:
            base_salary = random.uniform(50000, 80000)
        elif 'Старший' in employee['position']:
            base_salary = random.uniform(30000, 50000)
        else:
            base_salary = random.uniform(15000, 30000)
            
        details = {
            'employee_id': employee['employee_id'],
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=65),
            'gender': random.choice(['Ч', 'Ж']),
            'marital_status': random.choice(marital_statuses),
            'education_level': random.choice(education_levels),
            'university': fake.university() if random.random() > 0.3 else None,
            'specialization': fake.job() if random.random() > 0.3 else None,
            'languages': random.sample(['Українська', 'Англійська', 'Німецька', 'Польська'], 
                                    random.randint(1, 3)),
            'address': fake.address(),
            'emergency_contact': fake.name(),
            'emergency_phone': fake.phone_number(),
            'base_salary': round(base_salary, 2),
            'bonus_rate': round(random.uniform(0.05, 0.20), 2),
            'vacation_days': random.randint(18, 24),
            'sick_days': random.randint(0, 10),
            'probation_end': employee['hire_date'] + timedelta(days=90),
            'last_review_date': random_date(employee['hire_date'], end_date),
            'next_review_date': random_date(datetime.now(), end_date + timedelta(days=180))
        }
        employee_details.append(details)
    
    return pd.DataFrame(employee_details)

def generate_vacancies(departments_df):
    """Генерує дані про вакансії"""
    status_options = ['Відкрита', 'Закрита', 'На паузі']
    experience_levels = ['Початковий', 'Середній', 'Високий', 'Експерт']
    
    vacancies = []
    
    for i in range(n_vacancies):
        department = departments_df.sample(1).iloc[0]
        posting_date = random_date(start_date, end_date)
        status = random.choice(status_options)
        
        if status == 'Закрита':
            closing_date = posting_date + timedelta(days=random.randint(14, 90))
        else:
            closing_date = None
            
        vacancies.append({
            'vacancy_id': i + 1,
            'department_id': department['department_id'],
            'position_name': fake.job(),
            'experience_level': random.choice(experience_levels),
            'description': fake.text(max_nb_chars=500),
            'requirements': fake.text(max_nb_chars=300),
            'salary_min': round(random.uniform(15000, 40000), 2),
            'salary_max': round(random.uniform(40000, 80000), 2),
            'posting_date': posting_date,
            'closing_date': closing_date,
            'status': status,
            'applications_count': random.randint(0, 50),
            'hired_count': random.randint(0, 3) if status == 'Закрита' else 0,
            'priority_level': random.choice(['Низький', 'Середній', 'Високий']),
            'remote_work': random.choice(['Ні', 'Частково', 'Так'])
        })
        
    return pd.DataFrame(vacancies)

def generate_applications(vacancies_df):
    """Генерує дані про заявки на роботу"""
    status_options = ['Нова', 'Розглядається', 'Співбесіда', 'Пропозиція', 'Прийнято', 'Відхилено']
    
    applications = []
    
    for i in range(n_applications):
        vacancy = vacancies_df.sample(1).iloc[0]
        application_date = random_date(vacancy['posting_date'], 
                                     vacancy['closing_date'] if pd.notna(vacancy['closing_date']) else end_date)
        
        status = random.choice(status_options)
        current_salary = round(random.uniform(10000, 50000), 2)
        expected_salary = round(current_salary * random.uniform(1.1, 1.5), 2)
        
        applications.append({
            'application_id': i + 1,
            'vacancy_id': vacancy['vacancy_id'],
            'candidate_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'current_position': fake.job(),
            'current_company': fake.company(),
            'current_salary': current_salary,
            'expected_salary': expected_salary,
            'experience_years': random.randint(0, 15),
            'education_level': random.choice(['Середня', 'Бакалавр', 'Магістр', 'PhD']),
            'application_date': application_date,
            'status': status,
            'interview_date': application_date + timedelta(days=random.randint(3, 14)) if status in ['Співбесіда', 'Пропозиція', 'Прийнято', 'Відхилено'] else None,
            'feedback': fake.text(max_nb_chars=200) if status in ['Пропозиція', 'Прийнято', 'Відхилено'] else None,
            'source': random.choice(['LinkedIn', 'Work.ua', 'Рекомендація', 'Сайт компанії', 'Інше'])
        })
        
    return pd.DataFrame(applications)

def generate_trainings():
    """Генерує дані про навчальні програми"""
    training_types = ['Технічне навчання', 'Soft skills', 'Безпека праці', 'Управління', 'Мовні курси']
    
    trainings = []
    
    for i in range(n_trainings):
        start_date_training = random_date(start_date, end_date)
        duration_days = random.randint(1, 5)
        
        trainings.append({
            'training_id': i + 1,
            'training_name': fake.text(max_nb_chars=50),
            'training_type': random.choice(training_types),
            'description': fake.text(max_nb_chars=200),
            'start_date': start_date_training,
            'end_date': start_date_training + timedelta(days=duration_days),
            'duration_hours': duration_days * 8,
            'trainer': fake.name(),
            'max_participants': random.randint(10, 30),
            'actual_participants': 0,  # заповнимо пізніше
            'status': random.choice(['Заплановано', 'В процесі', 'Завершено', 'Скасовано']),
            'location': random.choice(['Офіс', 'Онлайн', 'Зовнішній центр']),
            'cost_per_person': round(random.uniform(1000, 5000), 2),
            'required_level': random.choice(['Початковий', 'Середній', 'Просунутий']),
            'certification': random.choice([True, False])
        })
        
    return pd.DataFrame(trainings)

def generate_attendance(employees_df):
    """Генерує дані про відвідуваність"""
    attendance = []
    
    for i in range(n_attendance):
        employee = employees_df.sample(1).iloc[0]
        attendance_date = random_date(employee['hire_date'], end_date)
        
        # Визначаємо тип дня
        if attendance_date.weekday() >= 5:  # вихідні
            status = 'Вихідний'
            hours_worked = 0
        else:
            rand = random.random()
            if rand > 0.9:  # 10% відпусток/лікарняних
                status = random.choice(['Відпустка', 'Лікарняний'])
                hours_worked = 0
            elif rand > 0.85:  # 5% запізнень
                status = 'Запізнення'
                hours_worked = round(random.uniform(6, 7.5), 2)
            else:  # 85% звичайних робочих днів
                status = 'Присутній'
                hours_worked = round(random.uniform(7.5, 8.5), 2)
        
        attendance.append({
            'attendance_id': i + 1,
            'employee_id': employee['employee_id'],
            'date': attendance_date,
            'status': status,
            'time_in': datetime.combine(attendance_date, 
                                      datetime.strptime(f"{random.randint(8,10)}:{random.randint(0,59)}", 
                                                      "%H:%M").time()) if status not in ['Вихідний', 'Відпустка', 'Лікарняний'] else None,
            'time_out': datetime.combine(attendance_date, 
                                       datetime.strptime(f"{random.randint(17,19)}:{random.randint(0,59)}", 
                                                       "%H:%M").time()) if status not in ['Вихідний', 'Відпустка', 'Лікарняний'] else None,
            'hours_worked': hours_worked,
            'overtime_hours': round(max(0, hours_worked - 8), 2),
            'notes': fake.text(max_nb_chars=100) if random.random() > 0.8 else None
        })
        
    return pd.DataFrame(attendance)

def generate_performance(employees_df):
    """Генерує дані про оцінку продуктивності"""
    performance = []
    evaluation_criteria = ['Якість роботи', 'Продуктивність', 'Командна робота', 
                         'Ініціативність', 'Дотримання дедлайнів']
    
    for i in range(n_performance):
        employee = employees_df.sample(1).iloc[0]
        evaluation_date = random_date(employee['hire_date'], end_date)
        
        # Генеруємо оцінки по кожному критерію
        criteria_scores = {criterion: random.randint(1, 5) for criterion in evaluation_criteria}
        average_score = sum(criteria_scores.values()) / len(criteria_scores)
        
        performance.append({
            'performance_id': i + 1,
            'employee_id': employee['employee_id'],
            'evaluation_date': evaluation_date,
            'evaluator_id': employees_df[employees_df['position'].str.contains('Керівник')].sample(1).iloc[0]['employee_id'],
            'period': f"{evaluation_date.year}-{str(((evaluation_date.month-1)//3)+1).zfill(2)}",  # квартал
            **criteria_scores,  # додаємо всі оцінки по критеріям
            'average_score': round(average_score, 2),
            'comments': fake.text(max_nb_chars=200),
            'goals_achieved': random.randint(60, 100),
            'improvement_areas': fake.text(max_nb_chars=100),
            'training_recommendations': fake.text(max_nb_chars=100) if random.random() > 0.7 else None,
            'next_review_date': evaluation_date + timedelta(days=90),
            'status': random.choice(['Чернетка', 'На розгляді', 'Затверджено'])
        })
        
    return pd.DataFrame(performance)

# Генеруємо нові дані
employee_details_df = generate_employee_details(employees_df)
vacancies_df = generate_vacancies(departments_df)
applications_df = generate_applications(vacancies_df)
trainings_df = generate_trainings()
attendance_df = generate_attendance(employees_df)
performance_df = generate_performance(employees_df)

# Зберігаємо нові дані в CSV
employee_details_df.to_csv('dim_employee_details.csv', index=False)
vacancies_df.to_csv('fact_vacancies.csv', index=False)
applications_df.to_csv('fact_applications.csv', index=False)
trainings_df.to_csv('dim_trainings.csv', index=False)
attendance_df.to_csv('fact_attendance.csv', index=False)
performance_df.to_csv('fact_performance.csv', index=False)
