"""Load the covid dataset and calculates each stat to be shown."""

from datetime import date, datetime, timedelta
import locale

import pandas as pd


def preprocess_data():
    """Preprocess original dataset correcting dates and making all rows weekly observations."""

    df = pd.read_csv('covidmonitor/data/covid_dataset.csv', encoding='utf8')

    # Split on 2 df, according to the type of report: weekly or daily
    df_weekly = df.loc[df['tipo_reporte'] == 'S'].copy()
    df_daily = df.loc[df['tipo_reporte'] == 'D'].copy()

    # Preprocess DAILY to group by week. First convert date column to datetime
    # Then make column with weekday nbr
    df_daily['fecha'] = pd.to_datetime(df_daily['fecha'], format="%d/%m/%Y")
    df_daily['day_nbr'] = df_daily.apply(lambda row: row['fecha'].weekday()+1 
                                            if row['fecha'].weekday() <= 5
                                            else 0, axis=1)
    # Now change dates, all rows from same week will have that week's sunday date
    # And then group by date, adding the rest of the columns
    df_daily['fecha'] = df_daily.apply(lambda row: row['fecha'] - timedelta(days=row['day_nbr']), axis=1)
    df_daily = df_daily.groupby(df_daily['fecha']).sum()
    df_daily.reset_index(inplace=True)
    df_daily.drop(['day_nbr'], inplace=True, axis=1)

    # Preprocess WEEKLY before merging with the DAILY df.
    df_weekly['fecha'] = pd.to_datetime(df_weekly['fecha'], format="%d-%m-%Y")
    df_weekly.drop(['tipo_reporte'], inplace=True, axis=1)

    # Concat DAILY and WEEKLY and save to file.
    final_df = pd.concat([df_weekly, df_daily])
    final_df.reset_index(inplace=True)
    final_df.to_csv('covidmonitor/data/covid_dataset_weekly.csv', encoding='utf8')

    return final_df


def load_data(years):
    """Load original dataset, preprocess and filter weekly dataset by year chosen in app."""

    # Preprocess df
    df = preprocess_data()

    # Calculate years to exclude, to remove those rows from df
    all_years = range(2021, date.today().year + 1)
    years = [int(year) for year in years]
    excluded_years = set(all_years) - set(years)

    for year in excluded_years:
        df.drop(df.index[df.fecha.dt.year == year], inplace=True)

    return df


def total_acumulado(column):
    """Get df column and return sum of values."""
    return column.sum()


def semana_legible(week_date: datetime) -> str:
    """Get a date in ISO 8601 format and return as '05 de marzo de 2022'."""
    locale.setlocale(locale.LC_TIME, '')
    return week_date.strftime("%d de %B de %Y")


def contar_ceros(column: pd.Series) -> int:
    """Get df column and return count of rows = 0."""
    counts = column.value_counts()
    return counts.loc[0]


def get_minimos(df):
    """Get df and return dict with minimum values for each metric. If min == 0 then return
    how many weeks with 0 count."""
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
    """Get df and return dict with max values for each metric."""
    maximos = {}
    columns = ['isopados', 'positivos', 'recuperados', 'fallecidos']
    for column in columns:
        week = semana_legible(df.loc[df[column].idxmax(), "fecha"])
        maximos[column] = (week, df[column].max())
    return maximos







