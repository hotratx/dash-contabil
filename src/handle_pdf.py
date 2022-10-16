from typing import List
import tabula
from PyPDF2 import PdfReader
import os
from pathlib import Path
import re
from locale import atof, setlocale, LC_NUMERIC
from src.database import Crud

setlocale(LC_NUMERIC, "")


regex_cnpj = re.compile(r'.*CNPJ:(\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}).*')
regex_name = re.compile(r'Empresa: (.*) -')


class HandlePdf:
    def __init__(self, db: Crud):
        self.crud = db

    def run(self, escritorio: str) -> list[str]:
        print(f'ENTROU NO HANDLEPDF esc: {escritorio}')
        self.escritorio = escritorio
        self.p = Path(__file__).parent.parent / "pdfs"
        # print(f"ESCRITORIO: {escritorio}\npath: {self.p.absolute()}")

        pdfs = [p1 for p1 in self.p.iterdir() if p1.suffix == ".pdf"]
        files = []

        for path_pdf in pdfs:
            try:
                self.handle_pdf(path_pdf)
                files.append(path_pdf.name)
            except Exception as e:
                print(f'erro no handle do pdf: {path_pdf} -- {e}')
            os.remove(path_pdf)
        return files

    def handle_pdf(self, path_pdf):
        reader = PdfReader(path_pdf)
        page = reader.pages[0]
        text = page.extract_text()
        name, cnpj = self._get_info(text)

        # print(f'get nome da empresa: {name}, cnpj: {cnpj}')
        if resp := self.pdf_is_valid(text, path_pdf):
            self.save(resp, cnpj)
        else:
            print('PDF não valido')

    def pdf_is_valid(self, text, path_pdf):
        if text.split(":")[0] == "Demonstração do Resultado do Exercício Pág.":
            return self.extract_pdf(path_pdf)
        return None

    def _get_info(self, text: str):
        texto = text[:120]
        text_cnpj = texto.replace(' ', '')
        cnpj = regex_cnpj.search(text_cnpj).groups()[0]
        name = regex_name.search(texto).groups()[0]
        return name, cnpj

    def extract_pdf(self, path_pdf):
        df = tabula.read_pdf(path_pdf, pages="all")
        return self.extract_data_from_pdf(df[0])

    def extract_data_from_pdf(self, df):
        tri_1 = df.loc[1][2]
        tri_2 = df.loc[1][3]
        tri_3 = df.loc[1][4]
        tri_4 = df.loc[1][5]
        abrev = {
                    "rec_bruta_ope": "Receita Bruta Operacional",
                    "fatu_pro_merc_serv": "Faturamento Prod. Merc. e Serviços",
                    "vendas_mercadorias": "Venda de Mercadorias",
                    "dedu_receita": "Deduções da Receita",
                    "impostos_faturados": "Impostos Faturados",
                    "icms": "ICMS",
                    "cofins": "COFINS",
                    "pis": "PIS",
                    "outras_deducoes": "Outras Deduções",
                    "vendas_can_dev": "Vendas Canc., Devol. e Descontos Inc...",
                    "receita_liquida": "Receita Líquida",
                    "custo_mercad_ser_pro_vendidos": "Custo Mercad./Serv./Produtos Vendidos",
                    "custo_mercadorias_revendidas": "Custo das Mercadorias Revendidas",
                    "lucro_bruto": "Lucro Bruto",
                    "desp_operacionnal": "Despesas Operacionais",
                    "desp_admin": "Despesas Administrativas",
                    "desp_trib": "Despesas Tributárias",
                    "resultado_financeiro": "Resultado Financeiro",
                    "receitas_financeiras": "Receitas Financeiras",
                    "desp_financeiras": "Despesas Financeiras",
                    "res_antes_das_part": "Res. Antes das Participações e Contrib.",
                    "res_antes_imp_renda": "Res. Antes Imp.Renda e Contrib. Social",
                    "contri_social_sobre_lucro": "Contribuição Social Sobre o Lucro",
                    "importo_renda": "Imposto de Renda",
                    "result_liquido_exer": "Resultado Líquido do Exercicio"
        }
        tri1 = {'tri': tri_1}
        tri2 = {'tri': tri_2}
        tri3 = {'tri': tri_3}
        tri4 = {'tri': tri_4}

        for abr, name in abrev.items():
            try:
                response = self.extract_1(df, name)
                tri1[abr] = response[0]
                tri2[abr] = response[1]
                tri3[abr] = response[2]
                tri4[abr] = response[3]
            except Exception:
                print(abr, name)
        return [tri1, tri2, tri3, tri4]

    def extract_1(self, df, name):
        resp = []
        mask = self.line(df, name)
        for i in range(1, 5):
            x = df[mask].iloc[-1][-i]
            if '(' in x:
                resp.append(atof(x[1:-1]))
            else:
                resp.append(atof(x))
        return resp

    def line(self, df, name):
        mask = df[[df.columns[1]]].apply(
            lambda x: x.str.contains(
                name,
                regex=True
            )
        ).any(axis=1)
        return mask

    def save(self, datas, cnpj):
        emp = self.crud.get_empresa(cnpj)
        escritorio = self.crud.get_escritorio(self.escritorio)
        
        # if not emp:
        #     new_emp = self.crud.create_empresa(name, cnpj)
        #     self.salve_all(datas, escritorio)
        # else:
        #     for new in datas:
        #         self.verify_datas(new, datas_saved)

    # def save_all(self, datas, escritorio)

    # def verify_datas(self, new, datas_saved):
    #     for d in datas_saved:
    #         if new == d:
    #             return None
        





# def str_dre(df):
#     print(f'DATAFRAME: {df}')
#     abrev = {
#                 "rbo": "Receita Bruta Operacional",
#                 "fpms": "Faturamento Prod. Merc. e Serviços",
#                 "vm": "Venda de Mercadorias",
#                 "dr": "Deduções da Receita",
#                 "ifs": "Impostos Faturados",
#                 "icms": "ICMS",
#                 "cofins": "COFINS",
#                 "pis": "PIS",
#                 "od": "Outras Deduções",
#                 "vcddi": "Vendas Canc., Devol. e Descontos Inc...",
#                 "rl": "Receita Líquida",
#                 "cmspv": "Custo Mercad./Serv./Produtos Vendidos",
#                 "cmr": "Custo das Mercadorias Revendidas",
#                 "lb": "Lucro Bruto",
#                 "do": "Despesas Operacionais",
#                 "da": "Despesas Administrativas",
#                 "dt": "Despesas Tributárias",
#                 "rfo": "Resultado Financeiro",
#                 "rfs": "Receitas Financeiras",
#                 "df": "Despesas Financeiras",
#                 "rapc": "Res. Antes das Participações e Contrib.",
#                 "raircs": "Res. Antes Imp.Renda e Contrib. Social",
#                 "cssl": "Contribuição Social Sobre o Lucro",
#                 "ir": "Imposto de Renda",
#                 "rle": "Resultado Líquido do Exercicio"
#             }

#     def line(tipo: str):
#         mask = df[[df.columns[1]]].apply(
#             lambda x: x.str.contains(
#                 tipo,
#                 regex=True
#             )
#         ).any(axis=1)
#         return mask
#     resp = {}
#     for abr, name in abrev.items():
#         try:
#             x = df[line(name)].iloc[-1][-1]
#             if '(' in x:
#                 resp[abr] = atof(x[1:-1])
#             else:
#                 resp[abr] = atof(x)
#         except:
#             print(abr, name)
#     # print(f'resultado dados extraidos do pdf: {resp}')
#     return resp
