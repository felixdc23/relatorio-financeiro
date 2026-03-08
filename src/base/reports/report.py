
from pandas import DataFrame

from base.generic_dataset import GenericDataset
from base.summary import Summary


class Report():
    def __init__(self,
                 summary: Summary,
                 receivables: GenericDataset,
                 open_payments: GenericDataset,
                 totals : GenericDataset):
        self._summary = summary.get_dataset()
        self._receivables = receivables.get_dataset()
        self._open_payments = open_payments.get_dataset()
        self._totals = totals.get_dataset()

    def get_report(self, ref_date):
        print(self._open_payments.head())
        print(self._open_payments.columns.tolist())

        d = {
            'Recebimento de Títulos': float(self._summary[(self._summary["PRT"] == '4') & (
                    self._summary.MOT == 'CMP')]['Total Baixado'].iloc[0]),
            'Retenção de Tributos': float(self._summary[(self._summary.PRT == '4') & (
                    self._summary.MOT == 'CMP')]['Impostos'].iloc[0]),
            'Compensações de Títulos': float(self._summary[(self._summary.PRT == '4') & (
                    self._summary.MOT == 'NOR')]['Total Baixado'].iloc[0]),
            f"Saldo a receber em {ref_date}": float(
                self._totals.drop(self._totals.index[-1])['(Vencidos+Vencer)'].sum()),
            f"Saldo RA em {ref_date}": float(self._open_payments["Saldo"].sum().round(2))
        }
        return DataFrame.from_dict([d])
