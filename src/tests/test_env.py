import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("host", os.getenv('host'))
print("database", os.getenv('database'))
print("user", os.getenv('user'))
print("password", os.getenv('password'))