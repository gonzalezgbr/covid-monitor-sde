"""This module scrapes the MH SDE web to extract data for the generation of the dataset."""

import csv
from pathlib import Path
import requests

from bs4 import BeautifulSoup

from covidmonitor.scraping.extractor import extract_report_data


class COVIDScraper:
    """Scrapes the COVID reports from the MH SDE website in order to generate the dataset."""

    def __init__(self):
        self.start_url = 'https://msaludsgo.gov.ar/web/seccion/covid-19/reporte-diario/'
        self.end_url = ''
        self.dataset_path = Path('../data/covid_dataset.csv')
        self.dataset_fields = ['fecha', 'tipo_reporte', 'recuperados', 'fallecidos', 'isopados', 'positivos']

    def collect_data(self):
        """Public interface. Check wich date to start from and trigger download of data."""
        print('>>> INICIANDO DESCARGA DE DATOS...')
        # check if there's data in the dataset, if not the end url will be the first report
        self.end_url = 'https://msaludsgo.gov.ar/web/reporte-diario-29-04-2021/'
        # if I already have data downloaded, extract last date and change end url
        # self.end_url = is the last one dowloaded
        self.navigate_to(self.start_url)
        print('>>> DESCARGA DE DATOS COMPLETADA!')

    def navigate_to(self, url: str):
        """Browse the report pages using the next page link."""
        try:
            r = requests.get(url)
        except Exception as e:
            print(f'>>> ERROR Falla en navegación: {e}')
            return

        soup = BeautifulSoup(r.content, features='html.parser')
        report_pages = soup.find_all('div', class_='thumb-post')
        for page in report_pages:
            report_url = page.find('a', href=True)['href']
            self.scrape_page(report_url)

        next_url = soup.find('a', href=True, class_='next page-link')
        if next_url:
            self.navigate_to(next_url['href'])
            # ['href'] == self.end_url:
        else:
            return

    def scrape_page(self, url: str):
        """Downloads the specific fields needed for reporting."""
        try:
            r = requests.get(url)
        except Exception as e:
            print(f'>>> ERROR Falla en scraping: {e}')
            return

        print(f'>>> Scrapeando {url}')
        soup = BeautifulSoup(r.content, features='html.parser')
        date_text = soup.find('h1', class_='p-0 azul')
        covid_text = soup.find('div', class_='card-body')
        report_data = extract_report_data(date_text.string, covid_text.get_text())
        print(f'>>> Scraping exitoso: {report_data}')
        self.save_to_file(report_data)

    def save_to_file(self, covid_data: dict):
        """Save the report data in the file that will be processed as dataset."""
        new = True
        if self.dataset_path.exists():
            new = False
        with open(self.dataset_path, 'a', encoding='utf8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.dataset_fields)
            if new:
                writer.writeheader()
            writer.writerow(covid_data)
        print('>>> Dataset actualizado')


if __name__ == '__main__':
    COVIDScraper().collect_data()
