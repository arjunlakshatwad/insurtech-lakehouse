CREATE TABLE CUSTOMERS (
    customer_id NUMBER PRIMARY KEY, 
    name VARCHAR2(255), 
    dob DATE, 
    address VARCHAR2(255), 
    segment VARCHAR2(50), 
    created_at DATE, 
    updated_at DATE
);

CREATE TABLE POLICIES (
    policy_id NUMBER PRIMARY KEY, 
    customer_id NUMBER REFERENCES CUSTOMERS(customer_id), 
    product_code VARCHAR2(50), 
    premium NUMBER, 
    start_date DATE, 
    end_date DATE, 
    status VARCHAR2(50), 
    updated_at DATE
);

CREATE TABLE CLAIMS (
    claim_id NUMBER PRIMARY KEY, 
    policy_id NUMBER REFERENCES POLICIES(policy_id), 
    claim_date DATE, 
    amount NUMBER, 
    status VARCHAR2(50), 
    adjuster VARCHAR2(100), 
    updated_at DATE
);

CREATE TABLE GL_TRANSACTIONS (
    txn_id NUMBER PRIMARY KEY, 
    policy_id NUMBER REFERENCES POLICIES(policy_id), 
    txn_date DATE, 
    amount NUMBER, 
    gl_account VARCHAR2(50), 
    updated_at DATE
);

CREATE TABLE BRANCHES (
    branch_id NUMBER PRIMARY KEY, 
    branch_name VARCHAR2(100), 
    region VARCHAR2(100)
);