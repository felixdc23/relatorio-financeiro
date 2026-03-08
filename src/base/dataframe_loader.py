from src.utils.data_loader import excel


class DataFrameLoader:

    def __init__(self, filepath, sheet_name=None, skiprows=None, header=0):
        self._df = excel.load_excel(
            filepath=filepath,
            sheet_name=sheet_name,
            skiprows=skiprows,
            header=header
        )

    def get_dataset(self):
        return self._df

    def head(self):
        return self._df.head()