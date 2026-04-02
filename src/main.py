import config
from base.generic_dataset import GenericDataset
from base import reports
from base.summary import Summary
from streamlit import config as stconfig

stconfig.set_option("global.developmentMode", False)
stconfig.set_option("server.fileWatcherType", "none")
stconfig.set_option("server.headless", True)

def main():
    settlements = GenericDataset(config.Settlement)
    totals = GenericDataset(config.Totals)

    summary = Summary(settlements.get_dataset())
    receivables = GenericDataset(config.Receivable)
    open_payments = GenericDataset(config.OpenPayment)

    report = reports.Report(summary, receivables, open_payments, totals)

    report_compiler = reports.ReportCompiler(
            settlements=settlements,
            receivables=receivables,
            totals=totals,
            open_payments=open_payments,
            summary=summary,
            report=report
        )

    compiled = report_compiler.compile(ref_date="2026-02-28")

    report_writer = reports.ExcelReportWriter(
        output_dir=config.Paths.PROCESSED,
        config=config
    )

    report_writer.write("2026-02-28", compiled)

if __name__ == "__main__":
    main()