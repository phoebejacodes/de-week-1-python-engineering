import argparse

parser = argparse.ArgumentParser(description="Multiply a number")

parser.add_argument("number", type=int, help="Number to multiply")
parser.add_argument("--times", type=int, default=2, help="Multiplier")

args = parser.parse_args()

result = args.number * args.times
print(f"{args.number} × {args.times} = {result}")