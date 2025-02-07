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
