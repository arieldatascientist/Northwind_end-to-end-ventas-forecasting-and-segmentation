import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from scipy.stats import ks_2samp
import mlflow
import mlflow.sklearn 


BASE_DIR = Path(__file__).resolve().parents[1]
ruta_csv = BASE_DIR / "data" / "processed" / "Features_clusters.csv"
Data_final = BASE_DIR / "data" / "processed"
BASELINE_FILE = BASE_DIR / "data" / "processed" / "baseline_northwind.csv"

def medir_drift_o_crear_baseline(df_nuevo, ruta_baseline):
    
    features = ['Monto', 'NumeroDeOrdenes', 'UnidadesCompradas', 'TicketPromedio', 'DiversidadCategorias']
    path_obj = Path(ruta_baseline)

    if not path_obj.exists():
        print(f"No se encontró baseline en '{path_obj.name}'. Creando uno nuevo...")
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        df_nuevo[features].to_csv(path_obj, index=False)
        return False, {"info": "Baseline inicial creado exitosamente"}
    
    print("Baseline encontrado. Verificando consistencia de datos...")
    df_baseline = pd.read_csv(path_obj)
    reporte_drift = {}
    hay_drift_global = False

    for col in features:
        stat, p_val = ks_2samp(df_baseline[col], df_nuevo[col])
        reporte_drift[col] = p_val
        mlflow.log_metric(f"drift_p_val_{col}", p_val)

        if p_val < 0.05:
            hay_drift_global = True
            print(f" DRIFT DETECTADO en variable: {col} (p={p_val:.4f})")
    
    return hay_drift_global, reporte_drift

def preprocesar_datos(df):
  
    print(" Iniciando Preprocesamiento (Scaler + PCA)...")
    
    features = ['Monto', 'NumeroDeOrdenes', 'UnidadesCompradas', 'TicketPromedio', 'DiversidadCategorias']
    # 1. Escalado
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])
    
    # 2. PCA
    pca = PCA(n_components=3)
    pca_data = pca.fit_transform(scaled_data)

    varianza_total = pca.explained_variance_ratio_.sum()

    mlflow.log_metric("Varianza explicada total PCA", varianza_total)
    
    return pca_data, scaler, pca

def main(df):
    
    
    # Iniciamos el experimento en MLflow
    mlflow.set_experiment("Northwind_Clustering_Segmentation")
    
    with mlflow.start_run(run_name="DBSCAN_Produccion"):
        
        # 1. MONITOREO DE DRIFT
        # Pasamos la ruta definida con pathlib
        drift_alert, reporte = medir_drift_o_crear_baseline(df, BASELINE_FILE)
        mlflow.log_param("drift_detected", drift_alert)
        
        if drift_alert:
            print(" ALERTA: La distribución de los datos ha cambiado significativamente.")
        
        # 2. PREPROCESAMIENTO
        pca_data, scaler, pca = preprocesar_datos(df)
        
        # 3. MODELADO (DBSCAN)
        print(" Entrenando DBSCAN con eps=0.5 y min_samples=4")
        dbscan = DBSCAN(eps=0.5, min_samples=4)
        clusters = dbscan.fit_predict(pca_data)
        
        # 4. MÉTRICAS Y LOGS
        n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
        n_noise = list(clusters).count(-1)
        
        if n_clusters > 1:
            sil_score = silhouette_score(pca_data, clusters)
            mlflow.log_metric("silhouette_score", sil_score)
            print(f" Silhouette Score: {sil_score:.4f}")
        
        mlflow.log_param("epsilon ", 0.5)
        mlflow.log_param("Min_samples ", 4)
        mlflow.log_metric("n_clusters", n_clusters)
        mlflow.log_metric("noise_points", n_noise)
        
        # 5. GUARDADO DE RESULTADOS
        df['Cluster'] = clusters
        output_file = Data_final / "Northwind_Clustered.csv"
        df.to_csv(output_file, index=False)
        
        mlflow.sklearn.log_model(dbscan, "model_dbscan")

if __name__ == "__main__":
    df = pd.read_csv(ruta_csv)
    main(df)


