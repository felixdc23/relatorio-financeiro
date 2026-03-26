from pandas import DataFrame, ExcelWriter
from base.generic_dataset import GenericDataset
from base.summary import Summary
from pathlib import Path


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

class ReportCompiler:
    def __init__(self, settlements, receivables, totals, open_payments, summary, report):
        self.settlements = settlements
        self.receivables = receivables
        self.totals = totals
        self.open_payments = open_payments
        self.summary = summary
        self.report = report

    def compile(self, ref_date: str):
        """Retorna um dicionário com todos os DataFrames prontos para gravação."""
        df_settlements = self.settlements.get_dataset()
        df_receivables = self.receivables.get_dataset()
        df_totals = self.totals.get_dataset()
        df_open_payments = self.open_payments.get_dataset()
        df_summary = self.summary.get_dataset()
        df_report = self.report.get_report(ref_date)

        # Abas separadas por PRT e MOT
        settlement_tabs = {}
        for prt in df_settlements.Prf.unique():
            for mot in df_settlements.Mot.unique():
                df_filtered = df_settlements[
                    (df_settlements.Prf == prt) &
                    (df_settlements.Mot == mot)
                ]
                settlement_tabs[f"{prt} {mot}"] = df_filtered

        return {
            "settlements": df_settlements,
            "settlement_tabs": settlement_tabs,
            "receivables": df_receivables,
            "totals": df_totals,
            "open_payments": df_open_payments,
            "summary": df_summary,
            "report": df_report,
        }

class ExcelReportWriter:
    def __init__(self, output_dir: str, config):
        self.output_dir = Path(output_dir)
        self.config = config

    def write(self, ref_date: str, compiled):
        output_path = self.output_dir / f"relatorio-clubedamedalha-{ref_date}.xlsx"

        with ExcelWriter(output_path, engine="openpyxl") as writer:

            # Aba principal
            compiled["settlements"].to_excel(
                writer,
                sheet_name=self.config.Settlement.SHEET_NAME,
                index=False
            )

            # Abas por PRT/MOT
            for sheet_name, df in compiled["settlement_tabs"].items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Saldo a Receber
            compiled["receivables"].to_excel(
                writer,
                sheet_name=self.config.Excel.RECEIVABLES_SHEET,
                index=False
            )

            # # Totais
            # compiled["totals"].to_excel(
            #     writer,
            #     sheet_name=self.config.Excel.TOTALS_SHEET,
            #     index=False
            # )
            #
            # RA
            compiled["open_payments"].to_excel(
                writer,
                sheet_name=self.config.Excel.OPEN_PAYMENT_SHEET,
                index=False
            )

            # Resumo
            compiled["summary"].to_excel(
                writer,
                sheet_name=self.config.Excel.SUMMARY_SHEET,
                index=False
            )

            # Relatório final
            compiled["report"].to_excel(
                writer,
                sheet_name=self.config.Excel.REPORT_SHEET,
                index=False
            )

        print(f"Relatório gerado em: {output_path}")