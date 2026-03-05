import config
import pandas as pd
from src.generic_dataset import GenericDataset
from src.summary import Summary

ref_date = "2026-02-28"

settlements = GenericDataset(config.Settlement)
print(settlements.head())

payables = GenericDataset(config.Payable)
print(payables.head())

df_ra = GenericDataset(config.OpenPayment)
print(df_ra.head())

print(settlements.get()[['Prf', 'Mot']])



# df_resumo = pd.DataFrame(columns= ['PRT','MOT','Valor Original','Jur/Multa','Correcao','Descontos','Abatimentos','Impostos','Valor Acessorio','Total Baixado'])
# resumo_rows = []
#
# for (prt, mot), grupo in settlements.get().groupby(["Prf", "Mot"]):
#     resumo_rows.append({
#         "PRT": prt,
#         "MOT": mot,
#         "Valor Original": grupo["Valor Original"].sum(),
#         "Jur/Multa": grupo["Jur/Multa"].sum(),
#         "Correcao": grupo["Correcao"].sum(),
#         "Descontos": grupo["Descontos"].sum(),
#         "Abatimentos": grupo["Abatim."].sum(),
#         "Impostos": grupo["Impostos"].sum(),
#         "Valor Acessorio": grupo["Valor Acessorio"].sum(),
#         "Total Baixado": grupo["Total Baixado"].sum(),
#     })
#
#
# df_resumo = pd.DataFrame(resumo_rows)

df_resumo = Summary(settlements.get())

d = {
    'Recebimento de Títulos':float(df_resumo[(df_resumo["PRT"] == '4') & (df_resumo.MOT == 'CMP')]['Total Baixado'].iloc[0].round(2)),
    'Retenção de Tributos':float(df_resumo[(df_resumo.PRT == '4') & (df_resumo.MOT == 'CMP')]['Impostos'].iloc[0].round(2)),
    'Compensações de Títulos':float(df_resumo[(df_resumo.PRT == '4') & (df_resumo.MOT == 'NOR')]['Total Baixado'].iloc[0].round(2)),
    f"Saldo a receber em {ref_date}":float(payables.get().drop(payables.get().index[-1])['(Vencidos+Vencer)'].sum().round(2)),
    f"Saldo RA em {ref_date}":float(df_ra.get().Saldo.sum().round(2))
}

df_relatorio = pd.DataFrame([d])

with pd.ExcelWriter(f"relatorio-clubedamedalha-{ref_date}.xlsx", engine='openpyxl') as writer:
    settlements.get().to_excel(writer, sheet_name='Baixas', index=False)
    for x in settlements.get().Prf.unique():
        for y  in settlements.get().Mot.unique():
            settlements.get()[(settlements.get().Prf == x) & (settlements.get().Mot == y)].to_excel(writer, sheet_name=f"{x} {y}", index=False)
    payables.get().to_excel(writer, sheet_name='Saldo a receber', index=False)
    df_ra.get().to_excel(writer, sheet_name='Saldo RA', index=False)
    df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
    df_relatorio.to_excel(writer, sheet_name='Relatorio', index=False)