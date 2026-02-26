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

- Extracción (Querys)
- Verificación de valores nulos
- Revisión de duplicados
- imputación 
- Conversión de fechas
- Creación de variables agregadas (ventas totales, unidades vendidas, etc.)
- Agrupaciones temporales (diarias / mensuales)
- Creación de archivos CSV

---

## Hallazgos Clave

## 1 Concentración de ingresos

Se identificó una fuerte concentración en la generación de ingresos:

- El **51.1%** de las ventas proviene de los **10 mejores clientes**.
- El **47.6%** del ingreso total es generado por los **10 productos más rentables**.
- El **86.2%** de las ventas se concentra en los **10 países con mayor facturación**.
- El **77% de los clientes** se encuentra en esos mismos países.

 **Implicación:**  
El negocio presenta una estructura tipo *Pareto*, donde una fracción reducida de entidades genera la mayor parte del ingreso. Esto implica riesgo de dependencia y oportunidad de optimización estratégica.

---

## 2 Alta dispersión y presencia de outliers

Se observó una dispersión considerable en:

- Monto por cliente
- Monto por país
- Unidades vendidas por producto
- Ventas diarias

Las desviaciones estándar elevadas y amplias distancias intercuartiles confirman heterogeneidad significativa en el comportamiento de compra.

 **Implicación:**  
Existen clientes corporativos de alto valor coexistiendo con clientes ocasionales, lo que sugiere potencial para segmentación futura.

---

## 3 Precio vs Volumen

La correlación de Spearman entre precio y unidades vendidas fue **0.131**, indicando ausencia de relación significativa.

- Productos caros pueden vender altos volúmenes.
- Productos baratos no garantizan alta rotación.
- Los ingresos dependen más del posicionamiento que del precio absoluto.

 **Implicación:**  
Las decisiones de pricing deben evaluarse junto con margen y estrategia comercial, no únicamente con base en volumen.

---

## 4 Desempeño comercial

Se detectó alta variabilidad entre empleados en:

- Número de órdenes
- Unidades vendidas
- Ingresos generados

 **Implicación:**  
Podría existir oportunidad de análisis adicional sobre asignación de cuentas, experiencia o estrategias comerciales diferenciadas.

---

## 5 Comportamiento temporal de las ventas

El análisis de la serie diaria mostró:

- Ausencia de estacionalidad clara.
- Sin tendencia marcada.
- Alta varianza
- ACF con caída rápida.
- PACF de corto alcance.
- Estacionariedad confirmada mediante prueba de Dickey-Fuller.
- Diferenciación requerida: 0.

 **Conclusión técnica:**  
La serie es estacionaria y compatible con modelos de bajo orden como:

- Suavización Exponencial Simple
- ARIMA con componentes mínimos

---

## Impacto del EDA en el Modelado

Los resultados del análisis exploratorio permitieron:

- Definir la frecuencia adecuada para forecasting.
- Justificar el uso de ARIMA.
- Seleccionar variables relevantes para clustering.
- Detectar posibles problemas de drift en la distribución de ventas.
- Extraer Kpis clave para la compañía.