from typing import List
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import numpy as np
import tabula
import time
from PyPDF2 import PdfReader
from locale import atof, setlocale, LC_NUMERIC
from plotting import plot

setlocale(LC_NUMERIC, '')

LISTA_ITEMS = {'ativo': '*** Ativo ***', 'ocp': 'Obrigações de Curto Prazo', 'pnc': 'Passivo não Circulante', 'pl': 'Patrimônio Líquido'}

#Diferentes tamanhos de texto
# st.header('Isso é um cabeçalho')
# st.subheader('Isso é um subcabeçalho')
# st.text('Isso é um texto normal')
#formatação
#Utilização para guardar html
# st.markdown('[Isso é um texto com html](https://docs.streamlit.io/en/stable/api.html#display-text)',False)
# st.sidebar.success('To continue select "Run the app".')

placeholder = st.empty()


def main():
    st.markdown('Controle')
    st.sidebar.title("Gráficos")
    app_mode = st.sidebar.selectbox("Escolha os gráficos",
        ["Página inicial", "Mostra Gráficos", "Show the source code"])

    if app_mode == "Página inicial":
        page_inicial()
    elif app_mode == "Show the source code":
        ...
    elif app_mode == "Mostra Gráficos":
        plot_pie()

    # Using "with" notation
    with st.sidebar:
        add_radio = st.radio(
            "Choose",
            ("Standard (5-15 days)", "Express (2-5 days)")
        )


def page_inicial():
    # with placeholder.container():
    #     st.title("Try")
    #     btn = st.button("try")
    st.header('Página Inicial')
    st.text('Isso é um texto normal')
    atualizar = st.button('Atulizar pdf')
    if atualizar:
        handle_pdf()


def handle_pdf():
    print('FIMFIM')
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success('Done!')
        placeholder.empty()


def sheare_in_pdf(info: str, dfs: List):
    for i in range(len(dfs)):
        try:
            resp = atof(dfs[i][dfs[i]['Descrição'] == info].iloc[-1][-1].split(' ')[-0])
            return resp
        except IndexError as e:
            pass



def plot_pie():

    date_today = datetime.now()
    days = pd.date_range(date_today, date_today + timedelta(30), freq="D")

    np.random.seed(seed=1111)
    data = np.random.randint(1, high=100, size=len(days))
    df = pd.DataFrame({"index": days, "col2": data})
    df = df.set_index("index")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    start_time = st.slider(
         "When do you start?",
         value=datetime(2020, 1, 1, 9, 30),
         format="MM/DD/YY")
    st.write("Start time:", start_time)


    dd = df.index.array
    color = st.select_slider(
         'Seleciona um período',
         options=['2022-08-03', '2022-08-04',
                     '2022-08-05', '2022-08-06',
                     '2022-08-07', '2022-08-08',
                     '2022-08-09', '2022-08-10',
                     '2022-08-11', '2022-08-12',
                     '2022-08-13', '2022-08-14',
                     '2022-08-15', '2022-08-16',
                     '2022-08-17', '2022-08-18',
                     '2022-08-19', '2022-08-20',
                     '2022-08-21', '2022-08-22',
                     '2022-08-23', '2022-08-24',
                     '2022-08-25', '2022-08-26',
                     '2022-08-27', '2022-08-28',
                     '2022-08-29', '2022-08-30',
                     '2022-08-31', '2022-09-01',
                     '2022-09-02'],
         value=('2022-08-03', '2022-08-10'))

    st.write('período selecionado', color)


    st.title('Gráficos de pizza')
    dfs = tabula.read_pdf("balanco.pdf", pages='all')
    resp = {item: response for item, value in LISTA_ITEMS.items() if (response:=sheare_in_pdf(value, dfs))}
    dict = {'values': [], 'tipo': []}
    for name, value in resp.items():
        dict['values'].append(value)
        dict['tipo'].append(name)
    df = pd.DataFrame.from_dict(dict)
    st.plotly_chart(plot(df), use_container_width=True)






if __name__ == "__main__":
    main()
