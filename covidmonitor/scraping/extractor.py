"""This module extracts specific pieces of data from the free text report downloaded."""

from typing import Optional
import re


def extract_quantity(texto: str) -> str:
    """Get short text and return embedded number."""
    quantity = ''
    for caracter in texto:
        if caracter in '0123456789':
            quantity = quantity + caracter
    return quantity if quantity != '' else 0


def extract_report_covid_numbers(texto: str) -> tuple:
    """Get report text and return counts of recovered, deaths, tested and positive cases."""
    texto = texto.lower()

    recuperados_start = texto.find('se recuper')
    if recuperados_start == -1:
        recuperados_start = texto.find('se report')
    recuperados_end = texto.find('caso', recuperados_start)
    if recuperados_end == -1:
        recuperados_end = texto.find('persona', recuperados_start)
    recuperados = extract_quantity(texto[recuperados_start:recuperados_end])

    fallecidos_start = texto.find('notifi', recuperados_end)
    if fallecidos_start == -1:
        fallecidos_start = texto.find('repor', recuperados_end)
    fallecidos_end = texto.find('persona', fallecidos_start)
    if fallecidos_end == -1:
        fallecidos_end = texto.find('de', fallecidos_start)
    fallecidos = extract_quantity(texto[fallecidos_start:fallecidos_end])

    isopados_start = texto.find('se procesaron un total de', fallecidos_end)
    isopados_end = texto.find('muestra', isopados_start)
    if isopados_end == -1:
        isopados_end = texto.find(')', isopados_start)
    isopados = extract_quantity(texto[isopados_start:isopados_end])

    positivos_start = texto.find('se confirmaron', isopados_end)
    positivos_end = texto.find('caso', positivos_start)
    if positivos_start == -1:
        positivos_start = texto.find('se notific', isopados_end)
        positivos_end = texto.find('caso', positivos_start)
    positivos = extract_quantity(texto[positivos_start:positivos_end])

    return recuperados, fallecidos, isopados, positivos


def extract_weekly_date(text: str) -> str:
    """Get text like 'Del 2 al 5 de marzo de 2022' and extract initial date of week."""
    months = dict(enero=1, febrero=2, marzo=3, abril=4, mayo=5, junio=6, julio=7, 
                    agosto=8, septiembre=9, octubre=10, noviembre=11, diciembre=12)
    general_pattern = r"\D*(\d{1,2})?(\D*)?(\d{1,2})?(\D*)?(\d{2,4})?"
    month_pattern = r"(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)"
    date_components = re.search(general_pattern, text)
    # The first number is for the start day
    day = date_components.groups()[0]
    # Month can appear in 2?? group if the date spans two months...
    month = re.search(month_pattern, date_components.groups()[1])
    if not month:
        # ...or in the 4?? gruou if the date spans only one month
        month = re.search(month_pattern, date_components.groups()[3])
    # Year is in the last group
    month = months[month.groups()[0]]
    year = date_components.groups()[4]

    return f'{day}-{month}-{year}'


def extract_date(text: str) -> Optional[str]:
    """Get text with embbeded date and return it."""
    date_pattern = r"\d{1,2}\s?/\s?\d{1,2}\s?/\s?\d{1,4}"
    date = re.search(date_pattern, text)
    if date:
        return date[0]


def extract_report_date(text: str) -> tuple:
    """Get title report text and return date and report type (S: weekly, D: daily)"""
    semanal = text.lower().find('semanal')
    if semanal != -1:
        this_date = extract_weekly_date(text)
        report_type = 'S'
    else:
        # daily
        this_date = extract_date(text)
        report_type = 'D'
    return this_date, report_type


def extract_report_data(date_text: str, covid_text: str) -> dict:
    """Get report text and return each data count for the dataset."""
    # ['fecha', 'tipo_reporte', 'recuperados', 'fallecidos', 'isopados', 'positivos']
    fecha, tipo_reporte = extract_report_date(date_text)
    recuperados, fallecidos, isopados, positivos = extract_report_covid_numbers(covid_text)
    report_data = dict(fecha=fecha, tipo_reporte=tipo_reporte,
                       recuperados=recuperados, fallecidos=fallecidos,
                       isopados=isopados, positivos=positivos)
    return report_data
