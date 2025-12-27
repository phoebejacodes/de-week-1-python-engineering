import argparse


parser = argparse.ArgumentParser(description="Greet a user")

# Add required positional argument
parser.add_argument("name", help="Name of person to greet")

args = parser.parse_args()

print(f"Hello, {args.name}!")