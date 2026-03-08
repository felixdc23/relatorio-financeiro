class Paths:
    DATA_DIR = "../data/"
    RAW = DATA_DIR + "raw/"
    PROCESSED = DATA_DIR + "processed/"

class Excel:
    EXTENSION = ".xlsx"
    SETTLEMENTS_SHEET = "Baixas"
    PAYABLES_SHEET = "Saldo a receber"
    OPEN_PAYMENTS_SHEET = "Saldo RA"
    SUMMARY_SHEET = "Resumo"
    REPORT_SHEET = "Relatorio"
    TOTALS_SHEET = "Saldo a receber"

class Settlement:
    FILENAME = "finr190.xlsx"
    SHEET_NAME = "Baixas"
    SKIPROWS = 1
    HEADER = 0

class Receivable:
    FILENAME = "finr130.xlsx"
    SHEET_NAME = "Titulos a receber"
    SKIPROWS = 1
    HEADER = 0

class Totals:
    FILENAME = "finr130.xlsx"
    SHEET_NAME = "Totais"
    SKIPROWS = 1
    HEADER = 0

class OpenPayment:
    FILENAME = "fina740.xlsx"
    SHEET_NAME = "Listagem do Browse"
    SKIPROWS = 1
    HEADER = 0

# Extensões aceitas
EXTENSIONS = ".xlsx"