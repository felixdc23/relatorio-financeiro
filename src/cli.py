# src/cli.py
from __future__ import annotations
from pathlib import Path
import argparse
import config
from base.generic_dataset import GenericDataset
from base import reports
from base.summary import Summary

def main() -> int:
    parser = argparse.ArgumentParser(description="Gera o Relatório Financeiro consolidado.")
    parser.add_argument("--ref-date", required=True, help="Data de referência (YYYY-MM-DD).")
    args = parser.parse_args()
    ref_date = args.ref_date

    settlements = GenericDataset(config.Settlement)
    totals = GenericDataset(config.Totals)
    receivables = GenericDataset(config.Receivable)
    open_payments = GenericDataset(config.OpenPayment)
    summary = Summary(settlements.get_dataset())

    report = reports.Report(summary, receivables, open_payments, totals)
    report_compiler = reports.ReportCompiler(
        settlements=settlements,
        receivables=receivables,
        totals=totals,
        open_payments=open_payments,
        summary=summary,
        report=report
    )
    compiled = report_compiler.compile(ref_date=ref_date)

    report_writer = reports.ExcelReportWriter(output_dir=config.Paths.PROCESSED, config=config)
    report_writer.write(ref_date, compiled)

    out = Path(config.Paths.PROCESSED) / f"{config.Compiled.FILENAME}{ref_date}{config.Excel.EXTENSION}"
    print(f"✅ Relatório gerado: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
