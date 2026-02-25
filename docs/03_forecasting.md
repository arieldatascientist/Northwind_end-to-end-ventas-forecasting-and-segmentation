

# Forecasting de Ventas

## 1 Objetivo del Modelado

El objetivo es modelar y proyectar el comportamiento de las ventas diarias utilizando métodos estadísticos de series temporales, partiendo de los hallazgos del EDA:

- Serie estacionaria.
- Sin tendencia clara.
- Sin estacionalidad evidente.
- Alta volatilidad y presencia de outliers.

---

## 2 Preparación de la Serie Temporal

Aunque la serie era estacionaria (confirmado con Dickey-Fuller), se observó que:

- La varianza parecía aumentar ligeramente con el tiempo.
- Existían valores atípicos de ventas muy altas.

### Transformación Logarítmica

Se aplicó transformación logarítmica para estabilizar la varianza.

Después de la transformación:

- La varianza se estabilizó.
- ACF y PACF confirmaron ausencia de estacionalidad.
- No se observó correlación prolongada en el tiempo.

---

## 3 Modelo 1 — Suavización Exponencial Simple (SES)

Dado que:

- No hay tendencia.
- No hay estacionalidad.
- Dependencia temporal de corto plazo.

El modelo inicial seleccionado fue **Suavización Exponencial Simple**.

### Resultados

- MAE: 2658.38
- RMSE: 4605.38

### Interpretación

El error fue elevado debido a:

- Alta volatilidad diaria.
- Presencia de outliers extremos.

Aunque el modelo captura el nivel promedio, la serie es altamente ruidosa.

---

## 4 Modelo 2 — ARIMA

Se estimó un modelo ARIMA cuyos parámetros se definieron a partir de:

- Análisis de ACF
- Análisis de PACF
- Confirmación de estacionariedad con Dickey-Fuller

Aplicado sobre la serie con transformación logarítmica.

### Resultados

- MAE: 2591.99
- RMSE: 4734.51

### Interpretación

El rendimiento fue similar al SES.  
Los valores atípicos seguían afectando significativamente el error.

---

## 5 Tratamiento de Outliers — Winsorización

Dado que eliminar outliers podría distorsionar la realidad del negocio, se aplicó **Winsorización al percentil 95** para limitar valores extremos sin eliminarlos.

Esto permitió:

- Reducir el impacto de días excepcionalmente altos.
- Evitar sobreajuste.
- Preservar estructura general de la serie.

---

## 6 Modelo Final — ARIMA con Winsorización

Tras aplicar Winsorización y volver a entrenar el modelo ARIMA:

### Resultados

- MAE: 2578.31
- RMSE: 1410.45

La reducción significativa del RMSE indica una mejora sustancial en estabilidad del modelo.

El pronóstico ahora presenta:

- Oscilaciones realistas.
- Menor sensibilidad al ruido extremo.
- Mejor ajuste visual a la serie.

---

## 7 Diagnóstico de Residuos

Se analizaron los residuos del modelo final:

### ACF y PACF de Residuos

- La mayoría de los valores se mantienen dentro del intervalo de confianza.
- Un único lag (14) supera ligeramente el intervalo, pero no muestra patrón periódico.

### Prueba de Ljung-Box

- p-valor: 0.47

Dado que p > 0.05, no se rechaza la hipótesis nula de independencia.

**Conclusión:**  
Los residuos se comportan como ruido blanco.  
El modelo capturó adecuadamente la dependencia temporal de la serie.

---

## 8 Implementación en Producción (`src/ARIMA_ventas.py`)

El modelo final fue estructurado para:

- Reentrenamiento controlado.
- Registro de métricas.
- Versionado mediante MLflow.
- Exportación de pronósticos.

Se registran:

- MAE
- RMSE
- Parámetros del modelo
- Versiones del experimento

---

## 9 Consideraciones de Monitoreo

Aunque no se dispone de datos de producción en tiempo real, se contemplan estrategias como:

- Reentrenamiento periódico.
- Evaluación rolling-window.
- Monitoreo de degradación de métricas (model decay).

---

# Conclusión del Forecasting

El modelo ARIMA con transformación logarítmica y Winsorización logró:

- Capturar la estructura estacionaria de la serie.
- Reducir el impacto de valores extremos.
- Generar residuos compatibles con ruido blanco.
- Mejorar significativamente el RMSE.

Dado el carácter altamente volátil de la serie, el modelo logra un equilibrio adecuado entre estabilidad y capacidad de adaptación.

El siguiente paso del proyecto aborda la segmentación de clientes mediante técnicas de clustering.

---