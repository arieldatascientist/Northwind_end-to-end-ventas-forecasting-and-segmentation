################# Extracción de datos ################

import pandas as pd
import sqlite3 
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "Northwind.db"

DATA_PROCESSED.mkdir(exist_ok=True)

# Conexion
conn = sqlite3.connect(DB_PATH)



#Función de limpieza
def limpieza(df: pd.DataFrame):
        if df.empty:
                print("Data Frame vacío")
                return df 
        
        #Primer columna duplicada
        columna_clave = df.columns[0]
        df_sin_duplicados = df.drop_duplicates(subset=[columna_clave], keep='first')

        #Queremos imputar las columnas numericas excepto la primer columna pues nunca es numérica
        columnas_a_imputar = df_sin_duplicados.columns[1:]
        df_procesado = df_sin_duplicados.copy()

        #Imputamos valores nulos con la media
        for col in columnas_a_imputar:
                #Intentamos obtener la media. Esto funcionará solo si la columna es numérica.
                if pd.api.types.is_numeric_dtype(df_procesado[col]):
                        media = df_procesado[col].mean()
            
                        #Solo imputamos si hay valores nulos y si la media no es Na
                        if df_procesado[col].isna().any() and not np.isnan(media):
                                nulos_imputados = df_procesado[col].isna().sum()
                                df_procesado[col].fillna(media, inplace=True)
                                

        print("\n Proceso de limpieza y completado finalizado.")
        return df_procesado
#Nota: De momento imputaremos con la media pero de ser necesario en el futuro podemos probar con algún 
#método de regresión de ML.



#Clientes info
query1 = ''' 
    SELECT c.CustomerName as NombreCliente, SUM(od.Quantity) as UnidadesVendidas, sum(od.Quantity * p.Price) AS Monto, 
     count(DISTINCT o.OrderID) as NumeroDeOrdenes FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products P ON od.ProductID = p.ProductID
        GROUP BY c.CustomerName
        ORDER BY Monto DESC
'''

clientes = pd.read_sql_query(query1, conn) 
clientes_limpio = limpieza(clientes)
clientes_limpio.to_csv(DATA_PROCESSED / "Ventas_cliente.csv", index=False)

#Países info
query2 = '''
        SELECT c.Country as País, sum(od.Quantity * p.Price) as Monto, count(DISTINCT c.CustomerID) as NúmeroDeClientes FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID 
        jOIN OrderDetails od ON o.OrderID = od.OrderID
        jOIN Products p ON od.ProductID = p.ProductID
        GROUP BY c.Country
        ORDER BY Monto DESC
'''

pais_ventas = pd.read_sql_query(query2, conn)
pais_ventas_limpio = limpieza(pais_ventas)
pais_ventas_limpio.to_csv(DATA_PROCESSED / "Ventas_pais.csv", index=False)

#Productos info
query3 = ''' 
        SELECT p.ProductName as Producto, sum(od.Quantity) as UnidadesVendidas, p.Price as Precio, sum(p.Price * od.Quantity) as Monto FROM Products p
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        GROUP BY p.ProductName
        ORDER BY Monto DESC
'''
ventas_productos = pd.read_sql_query(query3, conn)
ventas_productos_limpio = limpieza(ventas_productos)
ventas_productos_limpio.to_csv(DATA_PROCESSED / "Productos_ventas.csv", index=False)

#Preferencia por país
query4 = ''' WITH ventas_por_pais as (
    SELECT c."Country" as Pais, p."ProductName" as Producto, SUM(od."Quantity") as Unidades, ROW_NUMBER() OVER (
            PARTITION BY c."Country"
            ORDER BY SUM(od."Quantity") DESC) as rn FROM "Customers" c
    JOIN "Orders" o ON c."CustomerID" = o."CustomerID"
    JOIN "OrderDetails" od ON o."OrderID" = od."OrderID"
    JOIN "Products" p ON od."ProductID" = p."ProductID"
    GROUP BY c."Country", p."ProductName")
SELECT Pais, Producto, Unidades FROM ventas_por_pais
WHERE rn = 1
ORDER BY Pais;
'''

pais_preferencia = pd.read_sql_query(query4, conn)
pais_preferencia_limpio = limpieza(ventas_productos)
pais_preferencia_limpio.to_csv(DATA_PROCESSED / "Paises_preferencias.csv", index=False)

#Empleados info
query5 = ''' 
        SELECT e.FirstName || ' ' || e.LastName as Empleado, count(o.OrderID) as Órdenes, sum(od.Quantity * p.Price) as Monto,
        sum(od.quantity) as UnidadesVendidas FROM Employees e
        JOIN Orders o ON e.EmployeeID = o.EmployeeID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        GROUP BY Empleado
        ORDER BY Órdenes DESC
'''

empleados = pd.read_sql_query(query5, conn)
empleados_limpio = limpieza(empleados)
empleados_limpio.to_csv(DATA_PROCESSED / "Empleados.csv", index=False)

query6 = ''' 
        SELECT o.OrderDate as Fecha, sum(od.Quantity * p.Price) as Monto FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        GROUP BY Fecha
        ORDER BY Fecha ASC
'''

ventas_dia = pd.read_sql_query(query6, conn)
ventas_dia_limpio = limpieza(ventas_dia)
ventas_dia_limpio["Fecha"] = pd.to_datetime(ventas_dia_limpio["Fecha"])
ventas_dia_limpio = ventas_dia_limpio.set_index("Fecha")
ventas_dia_limpio.to_csv(DATA_PROCESSED / "Ventas_dia.csv", index=True)

query7 = ''' 
        SELECT c.CustomerName as NombreCliente, SUM(od.Quantity) as UnidadesCompradas, sum(od.Quantity * p.Price) AS Monto, 
        count(DISTINCT o.OrderID) as NumeroDeOrdenes, AVG(od.Quantity * p.Price) AS TicketPromedio, 
        c.Country as Pais, COUNT(DISTINCT p.CategoryID) AS DiversidadCategorias FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products P ON od.ProductID = p.ProductID
        GROUP BY c.CustomerName
        ORDER BY Monto DESC 
'''
features_cluster = pd.read_sql_query(query7, conn)
features_cluster_limpio = limpieza(features_cluster)
features_cluster_limpio.to_csv(DATA_PROCESSED / "Features_clusters.csv", index=False)

conn.close()