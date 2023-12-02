import matplotlib.pyplot as plt
import random


squares = [1, 4, 9, 16, 25]
wildcard = random.randint(27, 50)

squares.append(wildcard)

print(wildcard)

fig, ax = plt.subplots()
ax.plot(squares)

plt.show()
