CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY, 
    email VARCHAR(255), 
    signup_date TIMESTAMP, 
    kyc_status VARCHAR(50), 
    updated_at TIMESTAMP
);

CREATE TABLE loan_applications (
    application_id SERIAL PRIMARY KEY, 
    customer_id INT REFERENCES customers(customer_id), 
    amount_requested NUMERIC, 
    status VARCHAR(50), 
    submitted_at TIMESTAMP, 
    updated_at TIMESTAMP
);

CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY, 
    application_id INT REFERENCES loan_applications(application_id), 
    principal NUMERIC, 
    interest_rate NUMERIC, 
    origination_date TIMESTAMP, 
    status VARCHAR(50), 
    updated_at TIMESTAMP
);

CREATE TABLE loan_payments (
    payment_id SERIAL PRIMARY KEY, 
    loan_id INT REFERENCES loans(loan_id), 
    payment_date TIMESTAMP, 
    amount NUMERIC, 
    updated_at TIMESTAMP
);

CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY, 
    customer_id INT REFERENCES customers(customer_id), 
    opened_at TIMESTAMP, 
    closed_at TIMESTAMP, 
    category VARCHAR(100), 
    csat_score INT
);