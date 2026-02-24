# Análisis Exploratorio de Datos (EDA)

## Objetivo

Comprender la estructura de los datos, identificar patrones iniciales y detectar posibles anomalías antes del modelado.

El análisis exploratorio permitió establecer una base sólida para la segmentación de clientes y el modelo de pronóstico.

Extraer información clave sobre el estado del negocio.
---

## Descripción General del Dataset

La base de datos Northwind contiene información sobre:

- Órdenes
- Clientes
- Productos
- Empleados
- Regiones / Países
- Fechas de transacción

Se trabajó principalmente con información histórica de ventas para construir métricas agregadas y series temporales.

---

## Limpieza y Preparación Inicial

Durante el proceso de src/Datos_procesados_eda se realizaron las siguientes acciones:

- Verificación de valores nulos
- Revisión de duplicados
- imputación 
- Conversión de fechas
- Creación de variables agregadas (ventas totales, unidades vendidas, etc.)
- Agrupaciones temporales (diarias / mensuales)
- Creación de archivos CSV

---

## Hallazgos Clave

### 1. Tendencia Temporal

Se identificó el comportamiento histórico de ventas y posibles patrones de crecimiento o estabilidad.

### 2. Concentración de Ventas

Se observó concentración en ciertos países y productos, lo que sugiere dependencia de mercados específicos.

### 3. Distribución de Clientes

Se detectó variabilidad significativa en el comportamiento de compra entre clientes.

### 4. Variabilidad de Ventas

La volatilidad en ciertos periodos justificó el uso de técnicas de suavizado como media móvil para analizar tendencia.

---

## Impacto del EDA en el Modelado

Los resultados del análisis exploratorio permitieron:

- Definir la frecuencia adecuada para forecasting.
- Justificar el uso de ARIMA.
- Seleccionar variables relevantes para clustering.
- Detectar posibles problemas de drift en la distribución de ventas.
- Extraer Kpis clave para la compañía.