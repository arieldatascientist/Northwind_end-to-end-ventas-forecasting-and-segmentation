
# 04  Segmentación de Clientes (Clustering)

## 1 Objetivo

El objetivo es segmentar a los clientes según su comportamiento de compra utilizando técnicas de aprendizaje no supervisado, con el fin de identificar patrones diferenciados y oportunidades estratégicas.

Las variables consideradas por cliente fueron:

- Monto total comprado
- Número de órdenes
- Unidades compradas
- Ticket promedio
- Diversidad de categorías adquiridas

El dataset utilizado se encuentra previamente limpio y preparado.

---

## 2 Análisis de Correlación

Antes de aplicar clustering se evaluó la correlación entre variables.

Se observó que:

- **Unidades compradas** presenta alta correlación con:
  - Monto total
  - Número de órdenes

Implicación:

Estas correlaciones podrían sesgar el modelo, otorgando peso excesivo a la magnitud de compra y reduciendo la influencia de otras variables.

Por ello, se decidió aplicar **Reducción de Dimensionalidad mediante PCA** antes de entrenar el modelo de clustering.

---

## 3 Reducción de Dimensionalidad (PCA)

Dado que PCA es sensible a escala:

- Se aplicó escalamiento previo (StandardScaler).
- Se trabajó únicamente con variables continuas.
- Las variables categóricas se reservaron para análisis posterior.

### Varianza Explicada

Se evaluaron distintos números de componentes principales:

- 2 componentes → 89.4%
- 3 componentes → 96.1%
- 4 componentes → 99.3%

Al pasar de:
- 2 → 3 componentes: +6.7%
- 3 → 4 componentes: +3.2%

Siguiendo el **Principio de Parsimonia**, se seleccionaron **3 componentes**, ya que el cuarto aporta información marginal.

Las capturas de las mlflow runs se encuentran en la carpeta `docs/`.

---

## 4 Selección del Algoritmo

Dado que en el EDA se detectaron múltiples outliers, se eligió **DBSCAN**, ya que:

- Maneja valores atípicos como ruido.
- No requiere especificar número de clusters.
- Funciona bien en estructuras de densidad irregular.

Otros modelos basados en centroides podrían verse afectados por los valores extremos.

---

## 5 Selección de Hiperparámetros

Para estimar un valor razonable de `epsilon`, se utilizó la técnica **k-distance**:

- Se calcula la distancia al k-ésimo vecino más cercano.
- Se ordenan las distancias.
- Se identifica el “codo” en la gráfica.

Se identificaron posibles valores candidatos alrededor de:

- 1.2
- 2.0

Posteriormente se realizaron múltiples ejecuciones registradas en **MLflow** para comparar configuraciones.

---

## 6 Modelo Final

El mejor desempeño se obtuvo con:

- `epsilon = 0.5`
- `min_samples = 4`

### Resultados

- Número de clusters: 2
- Datos clasificados como ruido: 25
- Silhouette Score: 0.24

Aunque el silhouette score no es alto, es razonable dado que:

- No existen separaciones claramente definidas.
- La estructura de datos es densa alrededor del origen.
- Existen ramificaciones y clientes extremos.

---

## 7 Interpretación de Clusters

### Cluster 1 (40 clientes)

- Variables por debajo de la media.
- Compras esporádicas.
- Bajo volumen.
- Baja diversidad de productos.

Representa clientes ocasionales o de nicho.

---

### Cluster 0 (9 clientes)

- Valores cercanos a la media.
- Compras regulares.
- Comportamiento estable.

Representa clientes consistentes y recurrentes.

---

### Ruido (25 clientes)

- Altos valores en unidades y monto.
- Comportamiento extremo o altamente valioso.
- Representan una proporción significativa de ingresos.

Estos clientes deben analizarse individualmente, ya que pueden requerir estrategias personalizadas de retención.

---

## 8 Relación Cluster–País

Se aplicó prueba Chi-cuadrado para evaluar dependencia entre:

- Cluster asignado
- País de origen

Resultado:

- p-valor = 0.629

Dado que p > 0.05, no se rechaza la hipótesis nula de independencia.

Conclusión:

No existe relación significativa entre país y tipo de cliente.

Las estrategias de segmentación pueden estandarizarse internacionalmente.

---

## 9 Implementación en Producción (`src/Clustering_clientes.py`)

El pipeline productivo incluye:

1. Monitoreo de drift mediante prueba KS comparando con baseline.
2. Escalado de variables.
3. Transformación PCA (3 componentes).
4. Entrenamiento DBSCAN.
5. Registro de métricas y parámetros en MLflow.
6. Exportación de resultados segmentados.

Se registran:

- Silhouette score
- Número de clusters
- Puntos de ruido
- Varianza explicada del PCA
- Parámetros del modelo

---

## 10 Monitoreo de Data Drift

Se implementó una función que:

- Crea automáticamente un baseline si no existe.
- Compara nuevas observaciones mediante prueba Kolmogorov-Smirnov.
- Registra p-valores por variable en MLflow.
- Genera alerta si p < 0.05.

Esto permite detectar cambios significativos en la distribución de los datos ante nuevos clientes o datos de producción.

---

# Conclusión de la Segmentación

El modelo DBSCAN con reducción de dimensionalidad mediante PCA permitió:

- Identificar dos segmentos principales de clientes.
- Detectar clientes atípicos de alto valor.
- Confirmar independencia entre segmento y país.
- Establecer un pipeline reproducible y monitoreable.

La segmentación abre la puerta a estrategias diferenciadas de retención, personalización y optimización comercial.

---