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
BASELINE_FILE = BASE_DIR / "baseline_northwind.csv"

def medir_drift_o_crear_baseline(df_nuevo, features, ruta_baseline):
    
    features = ['Monto', 'Frecuencia', 'UnidadesCompradas', 'TicketPromedio', 'DiversidadCategorias']
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
    
    return hay_drift_global, 
