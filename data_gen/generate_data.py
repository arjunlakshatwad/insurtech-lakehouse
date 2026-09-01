import oracledb
import psycopg2
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

# Database Connections
oracle_dsn = "10.88.0.2:1521/XEPDB1"
oracle_user = "migration_demo"
oracle_pass = "DemoPass123"

pg_host = "10.88.0.3"
pg_db = "lending"
pg_user = "migration_demo"
pg_pass = "DemoPass123"

def generate_and_load():
    print("Connecting to databases and cleaning old data...")
    conn_oracle = oracledb.connect(user=oracle_user, password=oracle_pass, dsn=oracle_dsn)
    cur_oracle = conn_oracle.cursor()
    
    conn_pg = psycopg2.connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host, port="5432")
    cur_pg = conn_pg.cursor()

    # Clean previous partial runs to prevent Primary Key errors
    cur_oracle.execute("DELETE FROM CLAIMS")
    cur_oracle.execute("DELETE FROM POLICIES")
    cur_oracle.execute("DELETE FROM CUSTOMERS")
    conn_oracle.commit()
    
    cur_pg.execute("TRUNCATE TABLE support_tickets, loan_payments, loans, loan_applications, customers CASCADE;")
    conn_pg.commit()

    # 1. Oracle Customers
    print("Generating 50,000 Oracle Customers...")
    oracle_customers = []
    oracle_emails = []
    for i in range(1, 50001):
        email = fake.email() if random.random() > 0.05 else None
        oracle_emails.append(email)
        created = fake.date_time_between(start_date="-10y", end_date="-1y")
        oracle_customers.append((i, fake.name(), fake.date_of_birth(minimum_age=18, maximum_age=80), fake.address()[:250], random.choice(['Retail', 'Commercial', 'VIP']), created, fake.date_time_between(start_date=created, end_date="now")))
    cur_oracle.executemany("INSERT INTO CUSTOMERS (customer_id, name, dob, address, segment, created_at, updated_at) VALUES (:1, :2, :3, :4, :5, :6, :7)", oracle_customers)
    conn_oracle.commit()

    # 2. Oracle Policies
    print("Generating 120,000 Oracle Policies...")
    oracle_policies = []
    for i in range(1, 120001):
        start = fake.date_time_between(start_date="-5y", end_date="now")
        oracle_policies.append((i, random.randint(1, 50000), random.choice(['AUTO', 'HOME', 'LIFE']), round(random.uniform(500, 5000), 2), start, start + timedelta(days=365), random.choice(['ACTIVE', 'EXPIRED']), fake.date_time_between(start_date=start, end_date="now")))
    cur_oracle.executemany("INSERT INTO POLICIES (policy_id, customer_id, product_code, premium, start_date, end_date, status, updated_at) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", oracle_policies)
    conn_oracle.commit()

    # 3. Postgres Customers (15% overlap)
    print("Generating 20,000 Postgres Customers (with identity overlap)...")
    pg_customers = []
    valid_emails = [e for e in oracle_emails if e]
    overlap = random.sample(valid_emails, 7500)
    for i in range(1, 20001):
        email = overlap[i-1] if i <= len(overlap) else fake.email()
        signup = fake.date_time_between(start_date="-3y", end_date="now")
        pg_customers.append((i, email, signup, random.choice(['APPROVED', 'PENDING']), fake.date_time_between(start_date=signup, end_date="now")))
    cur_pg.executemany("INSERT INTO customers (customer_id, email, signup_date, kyc_status, updated_at) VALUES (%s, %s, %s, %s, %s)", pg_customers)
    conn_pg.commit()

    # 4. Postgres Loan Applications & Loans
    print("Generating 60,000 Postgres Loan Applications & Loans...")
    pg_apps = []
    pg_loans = []
    for i in range(1, 60001):
        sub_date = fake.date_time_between(start_date="-3y", end_date="now")
        pg_apps.append((i, random.randint(1, 20000), round(random.uniform(1000, 50000), 2), 'APPROVED', sub_date, sub_date))
        pg_loans.append((i, i, round(random.uniform(1000, 50000), 2), round(random.uniform(3.5, 12.0), 2), sub_date, 'ACTIVE', fake.date_time_between(start_date=sub_date, end_date="now")))
        
    cur_pg.executemany("INSERT INTO loan_applications (application_id, customer_id, amount_requested, status, submitted_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", pg_apps)
    cur_pg.executemany("INSERT INTO loans (loan_id, application_id, principal, interest_rate, origination_date, status, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)", pg_loans)
    conn_pg.commit()

    print("Data generation complete!")
    cur_oracle.close(); conn_oracle.close()
    cur_pg.close(); conn_pg.close()

if __name__ == "__main__":
    generate_and_load()