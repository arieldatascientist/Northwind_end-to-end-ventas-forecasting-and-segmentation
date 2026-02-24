# Arquitectura del Proyecto

Este proyecto fue diseñado con una estructura modular y escalable, simulando un flujo de trabajo profesional en ciencia de datos.

## Estructura General

- notebooks/
    Contiene el análisis exploratorio (EDA) y pruebas iniciales de modelos ML y Forecasting.
    
- src/
    Contiene la implementación modular del pipeline:
    - Extracción y limpieza de datos
    - Modelos de clustering
    - Modelo de forecasting
    - Registro automático de experimentos en MLflow
    - Medición de data drift

- dashboard/
    Contiene el archivo Power BI con visualizaciones ejecutivas.

- docs/
    Documentación técnica detallada del proyecto.

- data/
    base de datos Northwind comprimido 

## Flujo del Proyecto

1. Extracción y limpieza de datos.
2. Análisis exploratorio (EDA).
3. Construcción de modelo de forecasting (ARIMA).
4. Segmentación de clientes mediante clustering.
5. Registro de experimentos en MLflow.
6. Evaluación de estabilidad mediante análisis de data drift.
7. Integración de resultados en Power BI.

## Enfoque de Diseño

El proyecto fue desarrollado bajo principios de:

- Modularidad
- Reproducibilidad
- Separación entre experimentación y producción
- Registro automatizado de métricas
- Escalabilidad