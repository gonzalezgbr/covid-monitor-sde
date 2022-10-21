"""This module is the interface of COVID Monitor SDE. It generates the streamlit app from
 the dataset."""

from datetime import date

from millify import millify
import streamlit as st

from covidmonitor.data_processor import get_minimos, get_maximos, load_data, total_acumulado


def sidebar():
    """Generate the streamlit app sidebar."""
    with st.sidebar:
        st.title('COVID Monitor SDE')
        year = st.selectbox("Elegir año del reporte", ['2021', '2022', 'Todos los años'])

        # Footer
        st.markdown("""---""")
        st.markdown('COVID Monitor es una app no oficial. Los datos mostrados se descargan'
                    ' y procesan de forma automática por lo que pueden contener errores.')
        st.markdown("[Fuentes de datos](#fuentes-de-datos)", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("By **GG** | [github.com@gonzalezgbr](https://github.com/gonzalezgbr)")

    return year


def main():
    """Genera la app streamlit."""
    st.set_page_config(
        page_title="COVID Monitor SDE",
        page_icon="📉", )

    # The report year is chosen in the combo box from the sidebar
    year = sidebar()

    # Title
    st.image('covidmonitor/img/banner.png')
    st.info('COVID Monitor SDE es una app no oficial que recuenta datos de la pandemia'
            ' COVID-19 tomados de la web del Ministerio de Salud de la pcia. de Santiago'
            ' del Estero, Argentina.')

    # Generates a list with the years to inlcude in the report
    if year == 'Todos los años':
        years = range(2021, date.today().year + 1)
        title_year = f'2021-{str(date.today().year)}'
    else:
        title_year = year
        years = [year]

    st.title(f'Reporte {title_year}')
    df = load_data(years)

    # Cumulative totals
    st.header('Totales acumulados')
    col1, col2, col3, col4 = st.columns(4)
    isopados_ac = millify(total_acumulado(df['isopados']), precision=2)
    positivos_ac = millify(total_acumulado(df['positivos']), precision=2)
    recuperados_ac = millify(total_acumulado(df['recuperados']), precision=2)
    fallecidos_ac = millify(total_acumulado(df['fallecidos']), precision=2)

    with col1:
        st.metric(label="Isopados", value=isopados_ac)
    with col2:
        st.metric(label="Positivos", value=positivos_ac)
    with col3:
        st.metric(label="Recuperados", value=recuperados_ac)
    with col4:
        st.metric(label="Fallecidos", value=fallecidos_ac)

    # Trends
    st.header('Tendencias')
    st.subheader('Isopados y positivos')
    chart_data_iso_pos = df[['fecha', 'isopados', 'positivos']]
    st.line_chart(chart_data_iso_pos, x='fecha', y=['isopados', 'positivos'])

    st.subheader('Recuperados')
    chart_data_recu_fall = df[['fecha', 'recuperados']]
    st.line_chart(chart_data_recu_fall, x='fecha', y=['recuperados'])

    st.subheader('Fallecidos')
    chart_data_recu_fall = df[['fecha', 'fallecidos']]
    st.line_chart(chart_data_recu_fall, x='fecha', y=['fallecidos'])

    # Minimum and maximum
    st.header('Mínimos y Máximos')
    tab1, tab2, tab3 = st.tabs(["Contagios".upper(), "Altas".upper(), "Fallecimientos".upper()])
    minimos = get_minimos(df)
    maximos = get_maximos(df)

    with tab1:
        st.error(f'La semana con más contagios fue la del {maximos["positivos"][0]} con {maximos["positivos"][1]} '
                 f'isopados positivos.', icon='☣')
        if minimos["positivos"][1] != 0:
            st.success(f'La semana con menos contagios fue la del {minimos["positivos"][0]} con '
                       f'{minimos["positivos"][1]} isopados positivos.', icon='🕊')
        else:
            st.success(f'Hubo {minimos["positivos"][0]} semanas sin isopados positivos durante este período.', icon='🕊')

    with tab2:
        if minimos["recuperados"][1] != 0:
            st.error(f'La semana con menos recuperados fue la del {minimos["recuperados"][0]} con '
                     f'{minimos["recuperados"][1]} altas.', icon='☣')
        else:
            st.error(f'Hubo {minimos["recuperados"][0]} semanas sin recuperados durante este período.', icon='☣')
        st.success(f'La semana con más recuperados fue la del {maximos["recuperados"][0]} con '
                   f'{maximos["recuperados"][1]} altas.', icon='🕊')

    with tab3:
        st.error(
            f'La semana con más fallecimientos fue la del {maximos["fallecidos"][0]} con {maximos["fallecidos"][1]}'
            f' personas fallecidas.', icon='☣')
        if minimos["fallecidos"][1] != 0:
            st.success(f'La semana con menos fallecidos fue la del {minimos["fallecidos"][0]} con '
                     f'{minimos["fallecidos"][1]} personas fallecidas.', icon='🕊')
        else:
            st.success(f'Hubo {minimos["fallecidos"][0]} semanas sin fallecimientos durante este período.', icon='🕊')

    # Data sources
    st.markdown("---")
    st.header('Fuentes de datos')
    st.markdown('Los datos utilizados en el análisis fueron descargados de:')
    st.markdown("[Ministerio de Salud de Santiago del Estero]"
                "(https://msaludsgo.gov.ar/web/seccion/covid-19/reporte-diario/)")
    st.caption('ACLARACIÓN: El reporte diario comenzó a publicarse en la web mencionada en abril del 2021, '
               'por lo tanto en el análisis no se cuenta con datos previos a esa fecha. Por esta misma razón, los '
               'totales acumulados de todos los años no coincidirán con las fuentes oficiales ya que no incluyen los '
               'datos del año 2020 ni de los primeros meses de 2021.')


if __name__ == '__main__':
    main()
