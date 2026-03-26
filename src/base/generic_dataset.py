from utils.data_loader.dataframe_loader import DataFrameLoader
from config import Paths

class GenericDataset(DataFrameLoader):

    def __init__(self, config_class):
        full_path = Paths.RAW + config_class.FILENAME

        super().__init__(
            filepath=full_path,
            sheet_name=config_class.SHEET_NAME,
            skiprows=config_class.SKIPROWS,
            header=config_class.HEADER
        )

        self.col_fix()

    def col_fix(self):
        self.get_dataset().columns = [col.replace('_x000D_\n', ' ') for col in self.get_dataset().columns]
