from typing import List
import tabula
from PyPDF2 import PdfReader
from pathlib import Path
from locale import atof, setlocale, LC_NUMERIC

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
    def __init__(self, db):
        self._db = db

    def run(self, escritorio: str):
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
        print("tudo certo")
