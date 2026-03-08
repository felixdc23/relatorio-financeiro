import pandas as pd
from pathlib import Path

class ExcelReportWriter:
    def __init__(self, output_dir: str, config):
        self.output_dir = Path(output_dir)
        self.config = config

    def write(self, ref_date: str, compiled):
        output_path = self.output_dir / f"relatorio-clubedamedalha-{ref_date}.xlsx"

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

            # Aba principal
            compiled["settlements"].to_excel(
                writer,
                sheet_name=self.config.Settlement.SHEET_NAME,
                index=False
            )

            # Abas por PRT/MOT
            for sheet_name, df in compiled["settlement_tabs"].items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Totais
            compiled["totals"].to_excel(
                writer,
                sheet_name=self.config.Excel.TOTALS_SHEET,
                index=False
            )

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