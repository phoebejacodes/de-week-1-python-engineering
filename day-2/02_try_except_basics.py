# Basic structure of try-except block:
try:
    # Code that might fail
    result = 10 / 0
except ZeroDivisionError:
    # Handle the specific error
    print("Cannot divide by zero!")

print("Program continues...")

# Multiple exception handling types:
try:
    data = {"name": "Alice"}
    print(data["age"])  # KeyError
except KeyError:
    print("Key not found!")
except ZeroDivisionError:
    print("Cannot divide by zero!")

print("Program continues...")

# Catch all exceptions (not recommended for production code):
try:
    value = int("not_a_number")  # ValueError       
except Exception as e:
    print(f"An error occurred: {e}")    
print("Program continues...")

try:
    data = {"name": "Alice"}
    print(data["age"])
except Exception as e:
    print(f"An error occurred: {e}")
    print(f"Error type: {type(e).__name__}")