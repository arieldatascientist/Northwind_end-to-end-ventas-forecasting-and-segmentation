################# Ánálisis EDA NorthWind ################

import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt

conn = sqlite3.connect("NorthWind.db")

#Monto de ventas por cliente
query1 = ''' 
        SELECT c.CustomerName AS NombreCliente, sum(od.Quantity * p.Price) AS Monto FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products P ON od.ProductID = p.ProductID
        GROUP BY c.CustomerName
        ORDER BY Monto DESC
             
           '''

clientes = pd.read_sql_query(query1, conn) 

#Limpieza y análisis
print(clientes.info)
print(clientes.describe())
print(clientes.index.duplicated().any())
print(clientes.isna().sum())

#Podemos destacar que el monto promedio gastado por cliente es $5221.94 USD, con un máximo de $35631.21USD
#y un mínimo de $62.46 USD.

#Top 10 mejores clientes en ventas gráfica
clientes_top10 = clientes.head(10)

clientes_top10.plot(x = 'NombreCliente', y = 'Monto', kind = 'bar', figsize=(10, 5))
plt.title("Top 10 mejores clientes")
plt.xlabel("Cliente")
plt.ylabel("Monto")
plt.xticks(rotation=45)
plt.grid()
plt.show()   

#El mejor cliente es Ernst Handel con $35631.21 USD 

#Top 10 peores clientes gráfica
clientes_peores = clientes.tail(10)

clientes_peores.plot(x = 'NombreCliente', y = 'Monto', kind = 'bar', figsize=(10, 5))
plt.title("Top 10 peores clientes")
plt.xlabel("Cliente")
plt.ylabel("Monto")
plt.xticks(rotation=65)
plt.grid()
plt.show()  

#El peor cliente es Franchi S.p.A. con $62.46 USD 

#Ventas por producto

query2 = '''
        SELECT p.ProductName as Producto, SUM(od.Quantity) as UnidadesVendidas, SUM(od.Quantity * p.Price) as MontoVendido FROM Products p
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        GROUP BY p.ProductName 
        ORDER BY MontoVendido DESC 
         '''


