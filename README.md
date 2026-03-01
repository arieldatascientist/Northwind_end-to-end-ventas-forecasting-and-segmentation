# Northwind_end-to-end-ventas-forecasting-and-segmentation

## Descripción

Este proyecto tiene como objetivo analizar el desempeño del negocio utilizando la base de datos Northwind, extrayendo insights clave para la toma de decisiones, segmentando clientes mediante Machine Learning y generando pronósticos de ventas.

Se integran técnicas de análisis exploratorio, modelado predictivo, clustering y visualización en Power BI.

- Dashnoard preview

![Dashboard](docs/Dashboard%20imagenes/2026-02-24%20(1).png)

- Mlflow preview

![Mlflow](docs/Mlflow%20runs%20imagenes/DBSCAN/2026-01-27%20(9).png)

---

## Objetivos

- Analizar el comportamiento del negocio
- Identificar patrones en clientes, productos y mercados
- Segmentar clientes mediante clustering
- Generar pronósticos de ventas a corto plazo
- Construir un dashboard interactivo para toma de decisiones

---

## Componentes del Proyecto

### 1. Análisis Exploratorio (EDA)
- Querys SQL a la base de datos
- Identificación de outliers
- Distribución de ventas por cliente, país y producto
- Análisis de correlaciones
- KPIs clave del negocio

Ver: `docs/02_eda.md`

---

### 2. Forecasting
- Análisis de estacionariedad (Dickey-Fuller)
- Estabilizar varianza
- Evaluación de modelos:
  - Suavización exponencial
  - ARIMA
- Manejo de outliers (Winsorización)
- Evaluación con MAE y RMSE
- Analizar residuos (Ljung-Box)

Ver: `docs/03_forecasting.md`

---

### 3. Clustering de Clientes
- Análisis de colinealidad de variables
- Escalamiento
- Reducción de dimensionalidad con PCA
- Segmentación con DBSCAN
- Evaluación con Silhouette Score
- Tracking mlflow
- Identificación de clientes de alto valor (outliers)
- Análisis chi-cuadrado clusters/mercado

Ver: `docs/04_clustering.md`

---

### 4. Pipeline en Producción (src/)
- Extracción (Querys)
- Limpieza y transformación de datos
- Modelos modulares y escalables
- Registro automático con MLflow
- Medición de data drift (KS-test)

---

### 5. Dashboard (Power BI)
- Visualización de KPIs
- Segmentación de clientes
- Análisis de productos y empleados
- Pronóstico de ventas

Ver: `docs/05_dashboard.md`

---

## Principales Insights

- El **51% de las ventas** proviene del top 10 de clientes
- El **86% de las ventas** se concentra en los principales 10 países
- Existen clientes altamente valiosos (outliers)
- No hay estacionalidad en las ventas
- Alta volatilidad en la serie temporal
- Productos caros generan gran parte de los ingresos

---

## Tecnologías Utilizadas

- Python 3.11.9
- SQL
- Pandas 
- NumPy
- Matplotlib
- Scipy
- Seaborn
- Plotly
- Scikit-learn
- Statsmodels
- MLflow
- Power BI

---

##  Estructura del Proyecto

```text
Northwind_end-to-end-ventas-forecasting-and-segmentation/
│
├── notebooks/
│   ├── EDA_Morthwind.ipynb
│   ├── Forecasting_ventas_Northwind.ipynb
│   └── Clustering_Northwind.ipynb
│
├── src/
│   ├── Datos_procesados_eda.py
│   ├── ARIMA_ventas.py
│   └── Clustering_clientes.py
│   
│
├── dashboard/
│   └── Northwind_dashboard.pbix
│
├── docs/
│   ├── 01_arquitectura.md
│   ├── 02_eda.md
│   ├── 03_forecasting.md
│   ├── 04_clustering.md
│   ├── 05_conclusiones.md
│   ├── 06_dashboard.md
│   ├── Dashboard imágenes
│   └── Mlflow runs imagenes
│
├── data/
│   ├── northwind.zip
│   └── diagrama_Northwind.png
│
├── requirements.txt
│
└── README.md
```

---

## Resultados

Este proyecto demuestra la capacidad de:

- Transformar datos en insights accionables
- Aplicar modelos de machine learning en problemas reales
- Diseñar pipelines reproducibles
- Comunicar resultados mediante visualización

---

## Autor

**Ariel Martínez González**  
Proyecto enfocado en análisis de datos, machine learning y generación de valor de negocio.