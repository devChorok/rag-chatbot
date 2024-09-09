import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db

# Initialize the database (creates 'responses' table if it doesn't exist)
init_db()
