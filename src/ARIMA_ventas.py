import mlflow
import mlflow.statsmodels
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
from pathlib import Path

class NorthwindForecaster:
    def __init__(self, experiment_name="Ventas_Northwind"):
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        self.experiment_name = experiment_name
        mlflow.set_experiment(self.experiment_name)

    def preprocess_data(self, series): #Preprocesamiento de la serie
        
        #Logaritmo
        series_log = np.log(series)
        
        #Winsorización
        limite_sup = np.percentile(series_log, 95)
        series_processed = series_log.clip(upper=limite_sup)
        
        return pd.Series(series_processed, index=series.index)

    def train_and_log(self, raw_series, order): #Entrenamiento y tracking mlflow
        #Empezamos experimento
        with mlflow.start_run(run_name=f"ARIMA_{order}"):
            
            mlflow.log_param("Parametro_p", order[0])
            mlflow.log_param("Parametro_d", order[1])
            mlflow.log_param("Parametro_q", order[2])
            mlflow.log_param("Winzorización_con_percentil", 95)
            mlflow.log_param("Función", "Logarítmica")
            
            processed_series = self.preprocess_data(raw_series)

            train_size = int(len(processed_series) * 0.9)
            train, test = processed_series.iloc[0:train_size], processed_series.iloc[train_size:len(processed_series)]

            model = ARIMA(train, order=order)
            model_fit = model.fit()

            pronostico = model_fit.forecast(len(test))
            pronostico_real = np.exp(pronostico)
            test_real = np.exp(test)
            
            rmse = np.sqrt(mean_squared_error(pronostico_real, test_real))
            mae = mean_absolute_error(pronostico_real, test_real)

        
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            

            # Guardamos el modelo para uso futuro
            mlflow.statsmodels.log_model(model_fit, registered_model_name="ARIMA NorthWind ventas"
                                         , artifact_path="model")
            
            #Reentrenamiento 100% datos

            final_model = ARIMA(processed_series, order=order)
            final_model = final_model.fit()
            
            return final_model

    def forecaster(self, final_model, steps): #Pronosticos
      
        forecast_log = final_model.forecast(steps)
        forecast_real = np.exp(forecast_log)
        
        return forecast_real
    


BASE_DIR = Path(__file__).resolve().parents[1]
ruta_csv = BASE_DIR / "data" / "processed" / "Ventas_dia.csv"
Data_final = BASE_DIR / "data" / "processed"

ventas = pd.read_csv(ruta_csv)
ventas["Fecha"]= pd.to_datetime(ventas["Fecha"])
ventas = ventas.set_index("Fecha")

serie_ventas = ventas["Monto"]

ventas_arima = NorthwindForecaster(experiment_name="Northwind_forecasting")

orden_arima = (1, 0, 1)

ventas_modelo = ventas_arima.train_and_log(serie_ventas, order=orden_arima)

pronostico = ventas_arima.forecaster(ventas_modelo, steps=10)

fechas_futuras = pd.date_range(start=ventas.index[-1], periods=10 + 1, freq='B')[1:]
serie_prediccion = pd.Series(pronostico.values, index=fechas_futuras)

print(serie_prediccion)



serie_prediccion.to_csv(Data_final / "Pronostico_10_días_ventas.csv", index=True)

