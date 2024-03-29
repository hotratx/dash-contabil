from typing import List
from datetime import datetime
import tabula
from PyPDF2 import PdfReader
import os
from pathlib import Path
import re
from locale import atof, setlocale, LC_NUMERIC
from src.database import Crud
from src.database.schemas import IDadosdre

setlocale(LC_NUMERIC, "pt_BR.UTF-8")


regex_cnpj = re.compile(r".*CNPJ:(\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}).*")
regex_name = re.compile(r"Empresa: (.*) -")


class HandlePdf:
    def __init__(self, db: Crud):
        self.crud = db

    def run(self, escritorio: str) -> list[str]:
        self.escritorio = escritorio
        self.p = Path(__file__).parent.parent / "pdfs"

        pdfs = [p1 for p1 in self.p.iterdir() if p1.suffix == ".pdf"]
        files = []

        for path_pdf in pdfs:
            try:
                self.handle_pdf(path_pdf)
                files.append(path_pdf.name)
            except Exception as e:
                print(f"erro no handle do pdf: {path_pdf} -- {e}")
            os.remove(path_pdf)
        return files

    def handle_pdf(self, path_pdf):
        reader = PdfReader(path_pdf)
        page = reader.pages[0]
        text = page.extract_text()
        name, cnpj = self._get_info(text)

        if resp := self.pdf_is_valid(text, path_pdf):
            self.save(resp, cnpj, name)
        else:
            print("PDF não valido")

    def pdf_is_valid(self, text, path_pdf):
        if text.split(":")[0] == "Demonstração do Resultado do Exercício Pág.":
            return self.extract_pdf(path_pdf)
        return None

    def _get_info(self, text: str):
        texto = text[:120]
        text_cnpj = texto.replace(" ", "")
        cnpj = regex_cnpj.search(text_cnpj).groups()[0]
        name = regex_name.search(texto).groups()[0]
        return name, cnpj

    def extract_pdf(self, path_pdf):
        df = tabula.read_pdf(path_pdf, pages="all")
        return self.extract_data_from_pdf(df[0])

    def extract_data_from_pdf(self, df):
        tri_1 = datetime.strptime(df.loc[1][5], "%d/%m/%Y")
        tri_2 = datetime.strptime(df.loc[1][4], "%d/%m/%Y")
        tri_3 = datetime.strptime(df.loc[1][3], "%d/%m/%Y")
        tri_4 = datetime.strptime(df.loc[1][2], "%d/%m/%Y")
        abrev = {
            "lucro_bruto": "Lucro Bruto",
            "rec_bruta_ope": "Receita Bruta Operacional",
            "result_liquido_exer": "Resultado Líquido do Exercicio",
            "receita_liquida": "Receita Líquida",
            "receitas_financeiras": "Receitas Financeiras",
            "dedu_receita": "Deduções da Receita",
            "resultado_financeiro": "Resultado Financeiro",
            "fatu_pro_merc_serv": "Faturamento Prod. Merc. e Serviços",
            "vendas_mercadorias": "Venda de Mercadorias",
            "vendas_can_dev": "Vendas Canc., Devol. e Descontos Inc...",
            "custo_mercad_ser_pro_vendidos": "Custo Mercad./Serv./Produtos Vendidos",
            "custo_mercadorias_revendidas": "Custo das Mercadorias Revendidas",
            "desp_operacional": "Despesas Operacionais",
            "desp_admin": "Despesas Administrativas",
            "desp_trib": "Despesas Tributárias",
            "desp_financeiras": "Despesas Financeiras",
            "imposto_renda": "Imposto de Renda",
            "impostos_faturados": "Impostos Faturados",
            "icms": "ICMS",
            "cofins": "COFINS",
            "pis": "PIS",
            "outras_deducoes": "Outras Deduções",
            "res_antes_das_part": "Res. Antes das Participações e Contrib.",
            "res_antes_imp_renda": "Res. Antes Imp.Renda e Contrib. Social",
            "contri_social_sobre_lucro": "Contribuição Social Sobre o Lucro",
        }
        tri1 = {"tri": tri_1}
        tri2 = {"tri": tri_2}
        tri3 = {"tri": tri_3}
        tri4 = {"tri": tri_4}

        for abr, name in abrev.items():
            try:
                response = self.extract_1(df, name)
                tri1[abr] = response[0]
                tri2[abr] = response[1]
                tri3[abr] = response[2]
                tri4[abr] = response[3]
            except Exception as e:
                print(f"ERRRROR: {abr}, {name} ----- errro: {e}")
        return [tri4, tri3, tri2, tri1]

    def extract_1(self, df, name):
        resp = []
        mask = self.line(df, name)
        for i in range(1, 5):
            x = df[mask].iloc[-1][-i]
            if "(" in x:
                resp.append(atof(x[1:-1]))
            else:
                resp.append(atof(x))
        return resp

    def line(self, df, name):
        mask = df[[df.columns[1]]].apply(lambda x: x.str.contains(name, regex=True)).any(axis=1)
        return mask

    def save(self, dados, cnpj, name):
        if emp := self.crud.get_empresa(cnpj):
            self.verify_data_already_exist(dados, cnpj, emp)
        else:
            emp = self.crud.create_empresa(name, cnpj, self.escritorio)
            for dado in dados:
                idata = IDadosdre(**dado)
                new_dado = self.crud.create_dre(idata, emp)

        empresa = self.crud.get_empresa(cnpj)

    def verify_data_already_exist(self, dados, cnpj, emp):
        data_save = self.crud.get_datas_from_empresa(cnpj)
        for dado in dados:
            idata = IDadosdre(**dado)
            self.verify_1(idata, data_save, emp)

    def verify_1(self, idata: IDadosdre, data_save, emp):
        for d in data_save:
            if idata.tri == d.tri:
                return None
        new_dado = self.crud.create_dre(idata, emp)
