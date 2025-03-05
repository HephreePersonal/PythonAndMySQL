import mysql.connector
import json
from datetime import datetime, date, time
from decimal import Decimal
import os  # Add this to help with file paths

# Define your export path
export_path = r"C:\Users\JReic\GitHub_Personal\PythonAndMySQL\7342_ILKane\exports"  # Example path
file_name = "airlines.json"
full_path = os.path.join(export_path, file_name)

# Create the directory if it doesn't exist
os.makedirs(export_path, exist_ok=True)

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="VeryKnies23!",
        database="hephreeair"
    )
    
    # Create cursor and execute query
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from airlines")
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Custom JSON encoder to handle special data types
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            if isinstance(obj, time):
                return obj.strftime('%H:%M:%S')
            if isinstance(obj, Decimal):
                return float(obj)
            return super().default(obj)
    
    # Write to JSON file
    with open(full_path, 'w') as f:
        json.dump(results, f, cls=CustomJSONEncoder, indent=2)
        
    print(f"Data exported successfully to {full_path}")
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    if 'conn' in locals():
        cursor.close()
        conn.close()
