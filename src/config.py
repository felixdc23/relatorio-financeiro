class Paths:
    DATA_DIR = "../data/"
    RAW = DATA_DIR + "raw/"
    PROCESSED = DATA_DIR + "processed/"

class Excel:
    EXTENSION = ".xlsx"
    SUMMARY_SHEET = "Resumo"
    REPORT_SHEET = "Relatorio"
    OPEN_PAYMENT_SHEET = "Saldo RA"
    TOTALS_SHEET = "Saldo a receber"

#RELATÓRIO DE TÍTULOS BAIXADOS NO MÊS
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

#RELATÓRIO DE TÍTULOS A RECEBER
class Totals:
    FILENAME = "finr130.xlsx"
    SHEET_NAME = "Totais"
    SKIPROWS = 1
    HEADER = 0

#RELATÓRIO DE SALDO RA
class OpenPayment:
    FILENAME = "fina740.xlsx"
    SHEET_NAME = "Listagem do Browse"
    SKIPROWS = 1
    HEADER = 0

# Extensões aceitas
EXTENSIONS = ".xlsx"

class Compiled:
    FILENAME = "relatorio-clubedamedalha-"