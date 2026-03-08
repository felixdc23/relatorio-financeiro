import config
from base.generic_dataset import GenericDataset
from base.reports import Report
from base.summary import Summary
from base.reports import ReportCompiler
from base.reports import ExcelReportWriter

def main():
    settlements = GenericDataset(config.Settlement)
    totals = GenericDataset(config.Totals)

    summary = Summary(settlements.get_dataset())
    receivable = GenericDataset(config.Receivable)
    open_payments = GenericDataset(config.OpenPayment)

    report = Report(summary, receivable, open_payments, totals)

    report_compiler = ReportCompiler(
            settlements=settlements,
            totals=totals,
            open_payments=open_payments,
            summary=summary,
            report=report
        )

    compiled = report_compiler.compile(ref_date="2026-02-28")

    report_writer = ExcelReportWriter(
        output_dir=config.Paths.PROCESSED,
        config=config
    )

    report_writer.write("2026-02-28", compiled)

if __name__ == "__main__":
    main()