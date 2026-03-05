import pandas as pd

class Summary(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        df = pd.DataFrame(
            columns=['PRT', 'MOT', 'Valor Original', 'Jur/Multa', 'Correcao', 'Descontos', 'Abatimentos', 'Impostos',
                     'Valor Acessorio', 'Total Baixado'])


    def create_dataframe(self):
        rows = []
        for (prt, mot), group in self.get().groupby(["Prf", "Mot"]):
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
        return rows

    def get_dataframe(self):
        return pd.concat(self.df, self.create_dataframe())