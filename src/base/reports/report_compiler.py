class ReportCompiler:
    # def __init__(self, settlements, totals, receivable, open_payments, summary, report):
    def __init__(self, settlements, totals, open_payments, summary, report):
        self.settlements = settlements
        self.totals = totals
        # self.receivable = receivable
        self.open_payments = open_payments
        self.summary = summary
        self.report = report

    def compile(self, ref_date: str):
        """Retorna um dicionário com todos os DataFrames prontos para gravação."""
        df_settlements = self.settlements.get_dataset()
        df_totals = self.totals.get_dataset()
        # df_receivable = self.receivable.get_dataset()
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
            "totals": df_totals,
            # "receivable": df_receivable,
            "open_payments": df_open_payments,
            "summary": df_summary,
            "report": df_report,
        }