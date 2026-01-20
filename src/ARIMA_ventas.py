import mlflow
import mlflow.statsmodels
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error

class NorthwindForecaster:
    def __init__(self, experiment_name="Ventas_Northwind"):
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
                                         , artifact_path="data/processed")
            
            #Reentrenamiento 100% datos

            final_model = ARIMA(processed_series, order=order)
            final_model = final_model.fit()
            
            return final_model

    def forecast(self, final_model, steps): #Pronosticos
      
        forecast_log = final_model.forecast(steps)
        forecast_real = np.exp(forecast_log)
        
        return forecast_real
    