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
        {'account_id': 2000, 'name': 'Кредиторська заборгованість', 'type': 'Пасив', 'category': 'Поточні зобов'язання'},
        {'account_id': 2100, 'name': 'Кредити', 'type': 'Пасив', 'category': 'Довгострокові зобов'язання'},
        
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
