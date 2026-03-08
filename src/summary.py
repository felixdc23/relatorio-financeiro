from pandas import DataFrame

class Summary:
    def __init__(self, df: DataFrame):
        self._df = df  # mantém o DataFrame original

    def create_dataframe(self):
        rows = []
        for (prt, mot), group in self._df.groupby(["Prf", "Mot"]):
            rows.append({
                "PRT": prt,
                "MOT": mot,
                "Valor Original": group["Valor Original"].sum(),
                "Jur/Multa": group["Jur/Multa"].sum(),
                "Correcao": group["Correcao"].sum(),
                "Descontos": group["Descontos"].sum(),
                "Abatimentos": group["Abatim."].sum(),
                "Impostos": group["Impostos"].sum(),
                "Valor Acessorio": group["Valor Acessorio"].sum(),
                "Total Baixado": group["Total Baixado"].sum(),
            })
        return DataFrame(rows)

    def get_dataset(self):
        return self.create_dataframe()
