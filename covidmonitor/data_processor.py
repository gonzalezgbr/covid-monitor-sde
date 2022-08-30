# data_processor.py

"""Carga dataset de casos de covid y calcula los datos necesarios para cada estadística a mostrar."""

from datetime import date, datetime, timedelta
import locale

import pandas as pd


def preprocess_data():
    """Preprocesa el dataset original corrigiendo fechas y convirtiendo todas las filas en semanales."""

    df = pd.read_csv('covidmonitor/data/covid_dataset.csv', encoding='utf8')

    # Separo en dos df, según el tipo de reporte de la linea: semanal o diario
    df_weekly = df.loc[df['tipo_reporte'] == 'S'].copy()
    df_daily = df.loc[df['tipo_reporte'] == 'D'].copy()

    # Preproceso DAILY para agrupar por semana. Primero convierto fecha a tipo datetime
    # Luego genero columna con el nro de día de la semana
    df_daily['fecha'] = pd.to_datetime(df_daily['fecha'], format="%d/%m/%Y")
    df_daily['day_nbr'] = df_daily.apply(lambda row: row['fecha'].weekday()+1 if row['fecha'].weekday() <= 5
                                        else 0, axis=1)
    # Ahora modifico las fechas, dejando a las de una misma semana con la fecha de ese domingo
    # Luego agrupo por fecha, sumando las demás columnas
    df_daily['fecha'] = df_daily.apply(lambda row: row['fecha'] - timedelta(days=row['day_nbr']), axis=1)
    df_daily = df_daily.groupby(df_daily['fecha']).sum()
    df_daily.reset_index(inplace=True)
    df_daily.drop(['day_nbr'], inplace=True, axis=1)

    # Preproceso WEEKLY antes de unirlos y terminar.
    df_weekly['fecha'] = pd.to_datetime(df_weekly['fecha'], format="%d-%m-%Y")
    df_weekly.drop(['tipo_reporte'], inplace=True, axis=1)

    # Uno daily y weekly y lo guardo en file.
    final_df = pd.concat([df_weekly, df_daily])
    final_df.reset_index(inplace=True)
    final_df.to_csv('covidmonitor/data/covid_dataset_weekly.csv', encoding='utf8')

    return final_df


def load_data(years):
    """Carga el dataset original, preprocesa y filtra el dataset weekly por año elegido en la app."""

    # Preproceso el df
    df = preprocess_data()

    # Calculo años a excluir para eliminar esas filas del DF
    all_years = range(2021, date.today().year + 1)
    years = [int(year) for year in years]
    excluded_years = set(all_years) - set(years)

    for year in excluded_years:
        df.drop(df.index[df.fecha.dt.year == year], inplace=True)

    return df


def total_acumulado(column):
    """Recibe una columna del df y devuelve la suma de sus valores."""
    return column.sum()


def semana_legible(week_date: datetime) -> str:
    """Recibe una fecha en formato ISO 8601 y la devuelve en modo '05 de marzo de 2022'."""
    locale.setlocale(locale.LC_TIME, '')
    return week_date.strftime("%d de %B de %Y")


def contar_ceros(column: pd.Series) -> int:
    """Recibe una columna del df y devuelve la cantidad de veces que es igual a 0."""
    counts = column.value_counts()
    return counts.loc[0]


def get_minimos(df):
    """Recibe un df y devuelve un dict con valores mínimos para cada métrica. Si el minimo == 0 devuelve cant.
    semanas en 0"""
    minimos = {}
    columns = ['isopados', 'positivos', 'recuperados', 'fallecidos']
    for column in columns:
        week = semana_legible(df.loc[df[column].idxmin(), "fecha"])
        if df[column].min() != 0:
            minimos[column] = (week, df[column].min())
        else:
            minimos[column] = (contar_ceros(df[column]), df[column].min())
    return minimos


def get_maximos(df):
    """Recibe un df y devuelve un dict con los valores máximos para cada métrica."""
    maximos = {}
    columns = ['isopados', 'positivos', 'recuperados', 'fallecidos']
    for column in columns:
        week = semana_legible(df.loc[df[column].idxmax(), "fecha"])
        maximos[column] = (week, df[column].max())
    return maximos







