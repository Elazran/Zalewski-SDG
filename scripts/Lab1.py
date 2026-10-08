import numpy as np

#ZADANIE a)

x = np.random.randint(1, 10, size=15)
#print(x)
print(x.min())
print(x.max())
print(x.std())



#ZADANIE b)

macierz = np.random.randint(10, size=(4,4))
#print(macierz)
print(macierz.sum(axis=1))
print(macierz.sum(axis=0))



#ZADANIE c)

y = np.arange(0, 25*3, 3).reshape(5,5)
#print(y)
print(np.where((y % 2 == 0) & (y > 10 )))