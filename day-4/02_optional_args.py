import argparse

parser = argparse.ArgumentParser(description="Greeting tool with options")

# Positional (required)
parser.add_argument("name", help="Name to greet")

# Optional (starts with --)
parser.add_argument("--greeting", default="Hello", help="Greeting to use")
parser.add_argument("--excited", action="store_true", help="Add exclamation marks")

args = parser.parse_args()

message = f"{args.greeting}, {args.name}"

if args.excited:
    message = message.upper() + "!!!"

print(message)