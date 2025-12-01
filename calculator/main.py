import sys
from pkg.calculator import Calculator

print(sys.argv)

if len(sys.argv) > 1:
    expression = sys.argv[1]
    calculator = Calculator()
    result = calculator.evaluate(expression)
    print(result)
else:
    print("No expression provided.")