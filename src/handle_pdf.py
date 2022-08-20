from typing import List
import tabula
from PyPDF2 import PdfReader
from pathlib import Path
from locale import atof, setlocale, LC_NUMERIC
from src.database import Crud

setlocale(LC_NUMERIC, "")


# class Strategy:
#     def run(self, dfs: List):
#         self._strategy_1(dfs)

#     def _strategy_1(self, dfs: List):
#         LISTA_ITEMS = {
#             "ativo": "*** Ativo ***",
#             "ocp": "Obrigações de Curto Prazo",
#             "pnc": "Passivo não Circulante",
#             "pl": "Patrimônio Líquido",
#         }
#         resp = {
#             item: response
#             for item, value in LISTA_ITEMS.items()
#             if (response := sheare_in_pdf(value, dfs))
#         }
#         dict = {"values": [], "tipo": []}
#         for name, value in resp.items():
#             dict["values"].append(value)
#             dict["tipo"].append(name)
#         df = pd.DataFrame.from_dict(dict)


class HandlePdf:
    def __init__(self, db: Crud):
        self._db = db

    def run(self, escritorio: str):
        print('ENTROU NO HANDLEPDF esc: {escritorio}')
        self._esc = escritorio
        self.p = Path(__file__).parent.parent / "pdfs"
        print(f"ESCRITORIO: {escritorio}\npath: {self.p.absolute()}")

        pdfs = [p1 for p1 in self.p.iterdir() if p1.suffix == ".pdf"]

        for path_pdf in pdfs:
            print(f"path_pdf: {path_pdf}")
            self._foo(path_pdf)

    def _foo(self, path_pdf):
        reader = PdfReader(path_pdf)
        page = reader.pages[0]
        text = page.extract_text()
        print("FOOO")
        match text.split(":")[0]:
            case "Demonstração do Resultado do Exercício Pág.":
                self._str_dre(path_pdf)

    def _str_dre(self, path_pdf):
        print(f"ENTROU NO STR_DRE: {path_pdf}")
        df = tabula.read_pdf(path_pdf, pages="all")
        resp = str_dre(df)
        self._db.add_dre(resp, self._esc)
        print(f'resp do str_dre: {resp}')


def str_dre(df):
    abrev = {
                "rbo": "Receita Bruta Operacional",
                "fpms": "Faturamento Prod. Merc. e Serviços",
                "vm": "Venda de Mercadorias",
                "dr": "Deduções da Receita",
                "ifs": "Impostos Faturados",
                "icms": "ICMS",
                "cofins": "COFINS",
                "pis": "PIS",
                "od": "Outras Deduções",
                "vcddi": "Vendas Canc., Devol. e Descontos Inc...",
                "rl": "Receita Líquida",
                "cmspv": "Custo Mercad./Serv./Produtos Vendidos",
                "cmr": "Custo das Mercadorias Revendidas",
                "lb": "Lucro Bruto",
                "do": "Despesas Operacionais",
                "da": "Despesas Administrativas",
                "dt": "Despesas Tributárias",
                "rfo": "Resultado Financeiro",
                "rfs": "Receitas Financeiras",
                "df": "Despesas Financeiras",
                "rapc": "Res. Antes das Participações e Contrib.",
                "raircs": "Res. Antes Imp.Renda e Contrib. Social",
                "cssl": "Contribuição Social Sobre o Lucro",
                "ir": "Imposto de Renda",
                "rle": "Resultado Líquido do Exercicio"
            }

    def line(tipo: str):
        mask = df[[df.columns[1]]].apply(
            lambda x: x.str.contains(
                tipo,
                regex=True
            )
        ).any(axis=1)
        return mask
    resp = {}
    for abr, name in abrev.items():
        try:
            x = df[line(name)].iloc[-1][-1]
            if '(' in x:
                resp[abr] = atof(x[1:-1])
            else:
                resp[abr] = atof(x)             
        except:
            print(abr, name)
    return resp
