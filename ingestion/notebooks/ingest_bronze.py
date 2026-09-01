from pyspark.sql.functions import current_timestamp, lit

# Database Connections
jdbc_oracle = "jdbc:oracle:thin:@//localhost:1521/XEPDB1"
jdbc_pg = "jdbc:postgresql://localhost:5432/lending"

# Target Environment
catalog = "dev"

# Metadata-driven source configuration
source_tables = [
    {"system": "oracle", "table": "CUSTOMERS", "url": jdbc_oracle, "user": "migration_demo", "secret_key": "oracle-password"},
    {"system": "oracle", "table": "POLICIES", "url": jdbc_oracle, "user": "migration_demo", "secret_key": "oracle-password"},
    {"system": "oracle", "table": "CLAIMS", "url": jdbc_oracle, "user": "migration_demo", "secret_key": "oracle-password"},
    {"system": "pg", "table": "customers", "url": jdbc_pg, "user": "migration_demo", "secret_key": "postgres-password"},
    {"system": "pg", "table": "loans", "url": jdbc_pg, "user": "migration_demo", "secret_key": "postgres-password"},
    {"system": "pg", "table": "loan_payments", "url": jdbc_pg, "user": "migration_demo", "secret_key": "postgres-password"}
]

def full_load(spark, jdbc_url, table, target, user, password_secret):
    password = dbutils.secrets.get(scope="migration-demo", key=password_secret)
    
    print(f"Extracting {table} via JDBC...")
    df = (spark.read.format("jdbc")
          .option("url", jdbc_url)
          .option("dbtable", table)
          .option("user", user)
          .option("password", password)
          .option("driver", "oracle.jdbc.driver.OracleDriver" if "oracle" in jdbc_url else "org.postgresql.Driver")
          .load())
    
    # Append audit column required for dbt freshness checks
    df = df.withColumn("_ingested_at", current_timestamp())
    
    print(f"Loading into Bronze Delta table: {target}")
    df.write.format("delta").mode("overwrite").saveAsTable(target)

# Execute the ingestion loop
for config in source_tables:
    target_table = f"{catalog}.bronze.{config['system']}_{config['table'].lower()}"
    full_load(spark, config["url"], config["table"], target_table, config["user"], config["secret_key"])