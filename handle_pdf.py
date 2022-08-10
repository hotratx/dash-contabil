from typing import List
import tabula
from PyPDF2 import PdfReader
from pathlib import Path
from locale import atof, setlocale, LC_NUMERIC

setlocale(LC_NUMERIC, '')


class Strategy:
    def run(self, dfs: List):
        self._strategy_1(dfs)

    def _strategy_1(self, dfs: List):
        LISTA_ITEMS = {'ativo': '*** Ativo ***', 'ocp': 'Obrigações de Curto Prazo', 'pnc': 'Passivo não Circulante', 'pl': 'Patrimônio Líquido'}
        resp = {item: response for item, value in LISTA_ITEMS.items() if (response:=sheare_in_pdf(value, dfs))}
        dict = {'values': [], 'tipo': []}
        for name, value in resp.items():
            dict['values'].append(value)
            dict['tipo'].append(name)
        df = pd.DataFrame.from_dict(dict)


class ReadPdf:
    def __init__(self) -> None:
        self.str = Strategy()
        self.folder_path = '/home/hotratx/ttttest'

    def search_pdf(self);
        p1 = Path(self.folder_path)
        pdfs = self._search_files_pdf(p1)

    def _handle_pdf(self, pdfs: List[Path]):
        for pdf in pdfs:
            dfs = tabula.read_pdf(pdf, pages='all')
            self.str.run(dfs)




    def _search_files_pdf(self, path: Path) -> List[Path]:
        """Filtra os arquivos da pasta path, retornarndo apenas arquivos .pdf 
            e que possuem o padrão do pattern regex.

        Args:
            path: Path da pasta com arquivos para ser analisado.

        Return:
            pdfs: List[Path] com os Path de cada pdf
        """
        pdfs = [p for p in path.iterdir() if p.suffix == '.pdf']
        return pdfs


