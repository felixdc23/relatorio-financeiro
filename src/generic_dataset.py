from src.base.dataframe_loader import DataFrameLoader
from src.config import Paths


class GenericDataset(DataFrameLoader):

    def __init__(self, config_class):
        full_path = Paths.RAW + config_class.FILENAME

        super().__init__(
            filepath=full_path,
            sheet_name=config_class.SHEET_NAME,
            skiprows=config_class.SKIPROWS,
            header=config_class.HEADER
        )