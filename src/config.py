class Paths:
    DATA_DIR = "../data/"
    RAW = DATA_DIR + "raw/"
    PROCESSED = DATA_DIR + "processed/"

class Excel:
    EXTENSION = ".xlsx"

class Settlement:
    FILENAME = "finr190.xlsx"
    SHEET_NAME = "Baixas"
    SKIPROWS = 1
    HEADER = 0

class Payable:
    FILENAME = "finr130.xlsx"
    SHEET_NAME = "Titulos a receber"
    SKIPROWS = 1
    HEADER = 0
class OpenPayment:
    FILENAME = "fina740.xlsx"
    SHEET_NAME = "Listagem do Browse"
    SKIPROWS = 1
    HEADER = 0

# Extensões aceitas
EXTENSIONS = ".xlsx"