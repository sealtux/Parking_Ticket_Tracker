import mysql.connector
from mysql.connector import Error

# Function to create a connection to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("✅ Connection to MySQL DB successful")
    except Error as e:
        print(f"❌ The error '{e}' occurred")
    return connection

# Function to execute SQL queries (e.g., create tables)
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("✅ Query executed successfully")
    except Error as e:
        print(f"❌ The error '{e}' occurred")

# Function to initialize table creation
def table_creation(connection):
    table_queries = [

        # Vehicle table
        """
        CREATE TABLE IF NOT EXISTS Vehicle (
            LicensePlate VARCHAR(6) NOT NULL PRIMARY KEY,
            TypeOfVehicle VARCHAR(20) NOT NULL
        );
        """,

        # Ticket table
        """
        CREATE TABLE IF NOT EXISTS Ticket (
            TicketID VARCHAR(9) NOT NULL PRIMARY KEY,
            IssuedDate DATETIME NOT NULL,
            LicensePlate VARCHAR(6) NOT NULL,
            FOREIGN KEY (LicensePlate) REFERENCES Vehicle(LicensePlate)
        );
        """,

        # ParkingSpace table
        """
        CREATE TABLE IF NOT EXISTS ParkingSpace (
            SpaceID VARCHAR(6) NOT NULL PRIMARY KEY,
            TicketID VARCHAR(9) NOT NULL,
            Floor INT NOT NULL,
            VehicleType VARCHAR(20) NOT NULL,
            AvailabilityStatus ENUM('Available', 'Occupied') NOT NULL,
            FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
        );
        """,

        # Acquires table
        """
        CREATE TABLE IF NOT EXISTS Acquires (
            Acquires_ID VARCHAR(6) NOT NULL PRIMARY KEY,
            LicensePlate VARCHAR(6) NOT NULL,
            TicketID VARCHAR(9) NOT NULL,
            EntryTime DATETIME NOT NULL,
            FOREIGN KEY (LicensePlate) REFERENCES Vehicle(LicensePlate),
            FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
        );
        """,

        # Pays_for table
        """
        CREATE TABLE IF NOT EXISTS Pays_for (
            Pays_for_ID VARCHAR(6) NOT NULL PRIMARY KEY,
            LicensePlate VARCHAR(6) NOT NULL,
            TicketID VARCHAR(9) NOT NULL,
            AmountPaid DECIMAL(10,2) NOT NULL,
            Penalties DECIMAL(10,2) NOT NULL,
            PaymentDate DATETIME NOT NULL,
            FOREIGN KEY (LicensePlate) REFERENCES Vehicle(LicensePlate),
            FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
        );
        """
    ]

    for query in table_queries:
        execute_query(connection, query)
