from __future__ import annotations
import argparse

import config
from base.generic_dataset import GenericDataset
from base.summary import Summary
from base import reports


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera o relatório financeiro"
    )
    parser.add_argument(
        "--ref-date",
        required=True,
        help="Data de referência no formato YYYY-MM-DD",
    )
    args = parser.parse_args()
    ref_date = args.ref_date

    settlements   = GenericDataset(config.Settlement)
    totals        = GenericDataset(config.Totals)
    receivables   = GenericDataset(config.Receivable)
    open_payments = GenericDataset(config.OpenPayment)

    summary = Summary(settlements.get_dataset())

    report = reports.Report(
        summary=summary,
        receivables=receivables,
        open_payments=open_payments,
        totals=totals,
    )

    compiler = reports.ReportCompiler(
        settlements=settlements,
        receivables=receivables,
        totals=totals,
        open_payments=open_payments,
        summary=summary,
        report=report,
    )

    compiled = compiler.compile(ref_date=ref_date)

    writer = reports.ExcelReportWriter(
        output_dir=config.Paths.PROCESSED,
        config=config
    )
    writer.write(ref_date, compiled)

    print(f"OK: Relatório gerado para {ref_date}")


if __name__ == "__main__":
    main()