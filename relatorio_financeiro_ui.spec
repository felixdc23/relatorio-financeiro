# relatorio_financeiro_ui.spec
# ONEDIR REAL em Linux (sem PKG, sem PYZ)
from PyInstaller.utils.hooks import collect_all, copy_metadata
from PyInstaller.building.build_main import Analysis, EXE, COLLECT
from pathlib import Path

PROJECT_ROOT = Path.cwd().resolve()
SRC_DIR = PROJECT_ROOT / "src"

datas = []
binaries = []
hiddenimports = []

# Dependências do pipeline (NÃO embutir streamlit)
for pkg in ["pandas", "numpy", "openpyxl", "pyarrow"]:
    try:
        c = collect_all(pkg)
        binaries += c.binaries
        hiddenimports += c.hiddenimports
        datas += copy_metadata(pkg)
    except Exception:
        pass

# Código da aplicação (cópia recursiva)
datas.append((str(SRC_DIR), "src"))

a = Analysis(
    scripts=[str(PROJECT_ROOT / "run_ui.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    noarchive=True,        # sem PYZ
)

# ✅ CHAVE DA SOLUÇÃO:
# exclude_binaries=True REMOVE O PKG
exe = EXE(
    a.scripts,
    exclude_binaries=True,
    name="RelatorioFinanceiroUI_LINUX",
    console=True,
)

# ONEDIR verdadeiro: tudo entra aqui
app = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="RelatorioFinanceiroUI_LINUX",
)