import bcrypt
import sys

print("Python Version:", sys.version)
print("bcrypt module loaded from:", bcrypt.__file__)

try:
    print("bcrypt version (from __about__):", bcrypt.__about__.__version__)
except AttributeError:
    print("AttributeError: bcrypt module does not have __about__.__version__ attribute.")
    print("This indicates a potential issue with how bcrypt is built or installed.")

try:
    # Test a simple hash to see if bcrypt is functional
    password = b"test_password"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print("bcrypt hash test successful. Hashed password:", hashed.decode('utf-8'))
except Exception as e:
    print(f"Error during bcrypt functionality test: {e}")

print("\n--- sys.path ---")
for p in sys.path:
    print(p)
