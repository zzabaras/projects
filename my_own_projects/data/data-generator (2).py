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
