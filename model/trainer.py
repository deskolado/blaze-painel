import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder

def extrair_recursos(df):
    df = df.copy()
    df['cor_cod'] = LabelEncoder().fit_transform(df['cor'])

    df['minuto'] = pd.to_datetime(df['horario'], format='%H:%M').dt.minute
    df['hora'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
    df['momento'] = df['hora'].apply(
        lambda h: 'madrugada' if h < 6 else
        'manha' if h < 12 else
        'tarde' if h < 18 else 'noite'
    )
    df['momento_cod'] = LabelEncoder().fit_transform(df['momento'])

    df['freq_vermelho'] = df['cor'].rolling(20).apply(lambda x: (x == 'vermelho').sum(), raw=False)
    df['freq_preto'] = df['cor'].rolling(20).apply(lambda x: (x == 'preto').sum(), raw=False)
    df['dist_ultimo_branco'] = df['cor'][::-1].eq('branco').cumsum().where(df['cor'] == 'branco').ffill().fillna(0)

    df = df.dropna()
    return df

def treinar_modelo():
    if not os.path.exists("model/dataset.csv") or len(pd.read_csv("model/dataset.csv")) < 10:
        return

    df = pd.read_csv("model/dataset.csv")
    if len(df) < 100:
        return

    df = extrair_recursos(df)

    X = df[['numero', 'minuto', 'hora', 'momento_cod', 'freq_vermelho', 'freq_preto', 'dist_ultimo_branco']]
    y_cor = df['cor_cod']
    y_branco = df['cor'].apply(lambda x: 1 if x == 'branco' else 0)

    X_train, _, y_train_cor, y_train_branco = train_test_split(X, y_cor, test_size=0.2)

    modelo_cor = GradientBoostingClassifier()
    modelo_branco = GradientBoostingClassifier()

    modelo_cor.fit(X_train, y_train_cor)
    modelo_branco.fit(X_train, y_train_branco)

    joblib.dump((modelo_cor, modelo_branco), 'model/modelo.pkl')
