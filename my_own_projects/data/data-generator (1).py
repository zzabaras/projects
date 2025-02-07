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
