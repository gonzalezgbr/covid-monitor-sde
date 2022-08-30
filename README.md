# COVID Monitor SDE
> App no oficial que recolecta datos oficiales de la pandemia COVID-19 en la provincia de Santiago del Estero y 
> genera visualizaciones de seguimiento.

![license](https://img.shields.io/badge/license-Apache-orange)
![made_with](https://img.shields.io/badge/Made%20with-Python-blue)


`COVID Monitor SDE` es una web app (no oficial) de procesamiento de datos que recolecta datos de los reportes 
diarios/semanales de la pandemia COVID-19 emitidos por el Ministerio de Salud de Santiago del Estero en su 
web oficial y los procesa para mostrar la evolución de testeos, contagios, recuperaciones y fallecimientos 
por semana, los totales acumulados y los máximos y mínimos por período.

## Instalación

`COVID Monitor SDE` está deployada en `streamlit cloud`. Para acceder [click aquí]().

## Uso

La app muestra las métricas y gráficos en base al dataset generado y para el año seleccionado. 

![Covid Monitor GUI](docs/covid_monitor_main.png)

Se puede cambiar el año del que se desea ver el reporte en la barra de la izquierda y los datos mostrados 
se actualizarán de forma dinámica. También hay una opción para ver "todos los años".

![Covid Monitor año](docs/covid_monitor_elegir_anio.png)

> ℹ️El reporte diario comenzó a publicarse en la web mencionada en abril del 2021, por lo tanto
en el análisis no se cuenta con datos previos a esa fecha. Por esta misma razón, los totales acumulados de todos
los años no coincidirán con las fuentes oficiales ya que no incluyen los datos del año 2020 ni de los primeros 
meses de 2021.


### Fuentes de datos

Los datos utilizados en el análisis fueron descargados de [Ministerio de Salud de Santiago del Estero](https://msaludsgo.gov.ar/web/seccion/covid-19/reporte-diario/).

## Tech stack

* `requests` para descargar la información
* `beatifulsoup4` y `re` para extraer los datos 
* `pandas` para procesar el dataset y generar las stats
* `streamlit` y `millify` para mostrar los datos

## Release History

* 0.1.0 | First release


## Meta

By GG - [@GargaraG](https://twitter.com/GargaraG) 

Distribuido bajo licencia Apache. Ver ``LICENSE`` para más información.

[https://github.com/gonzalezgbr/](https://github.com/gonzalezgbr/)
