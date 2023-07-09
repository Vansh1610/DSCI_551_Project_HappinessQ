import psycopg2

def connect_sql():
    conn = psycopg2.connect(database="add_your_database_name",
                            host="add_your_host_name",
                            user="add_your_username",
                            password="add_your_password",
                            port="add_your_port_number")
        
    return conn
    

