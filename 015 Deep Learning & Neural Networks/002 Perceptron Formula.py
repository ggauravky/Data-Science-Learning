def step(x):
    return 1 if x >= 0 else 0

def perceptron(x1, x2, w1, w2, b):
    z = x1 * w1 + x2 * w2 + b
    return step(z)

# Try different weights and bias to match the AND logic
print(perceptron(0, 0, 1, 1, -1.5))  # Expected: 0
print(perceptron(0, 1, 1, 1, -1.5))  # Expected: 0
print(perceptron(1, 0, 1, 1, -1.5))  # Expected: 0
print(perceptron(1, 1, 1, 1, -1.5))  # Expected: 1