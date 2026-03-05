import os
import pandas as pd


def load_excel(
    filepath: str,
    sheet_name=None,
    skiprows=None,
    header=0,
    **kwargs
) -> pd.DataFrame:
    # Verifica se o arquivo existe
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    # Verifica extensão
    if not filepath.lower().endswith(".xlsx"):
        raise ValueError("O arquivo deve ser um .xlsx")

    # Carrega o arquivo
    return pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        skiprows=skiprows,
        header=header,
        **kwargs
    )