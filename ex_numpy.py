import matplotlib.pyplot as plt
import numpy as np

vendas = np.random.randint(1000,3000,50)
meses = np.arange(1,51)

print(vendas)
print(meses)

plt.plot(meses, vendas)
plt.ylabel("Vendas")
plt.xlabel("Meses")
plt.axis([0, 50, 0,  max(vendas) + 200 ])    

plt.show()