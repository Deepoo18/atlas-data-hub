import os
from dotenv import load_dotenv
load_dotenv()

print("host", os.getenv('host'))