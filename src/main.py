import config
import pandas as pd
from src.generic_dataset import GenericDataset
from src.report import Report
from src.summary import Summary

ref_date = "28-02-2026"

settlements = GenericDataset(config.Settlement)

receivable = GenericDataset(config.Receivable)

open_payments = GenericDataset(config.OpenPayment)

totals = GenericDataset(config.Totals)

summary = Summary(settlements.get_dataset())

report = Report(summary, receivable, open_payments, totals)

with pd.ExcelWriter(f"{config.Paths.PROCESSED}/relatorio-clubedamedalha-{ref_date}.xlsx", engine='openpyxl') as writer:
    settlements.get_dataset().to_excel(writer, sheet_name=config.Excel.SETTLEMENTS_SHEET, index=False)
    for x in settlements.get_dataset().Prf.unique():
        for y  in settlements.get_dataset().Mot.unique():
            settlements.get_dataset()[(settlements.get_dataset().Prf == x) & (settlements.get_dataset().Mot == y)].to_excel(writer, sheet_name=f"{x} {y}", index=False)
    totals.get_dataset().to_excel(writer, sheet_name=config.Excel.TOTALS_SHEET, index=False)
    open_payments.get_dataset().to_excel(writer, sheet_name=config.Excel.OPEN_PAYMENTS_SHEET, index=False)
    summary.get_dataset().to_excel(writer, sheet_name=config.Excel.SUMMARY_SHEET, index=False)
    report.get_report("2026-02-28").to_excel(writer, sheet_name=config.Excel.REPORT_SHEET, index=False)