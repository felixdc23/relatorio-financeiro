from __future__ import annotations
import streamlit as st
from pathlib import Path
from datetime import date, timedelta

import config
from base.generic_dataset import GenericDataset
from base.summary import Summary
from base import reports

# ---------------------------------------------------------------------
# Diretórios conforme config.py
# ---------------------------------------------------------------------
RAW_DIR = Path(config.Paths.RAW)
PROCESSED_DIR = Path(config.Paths.PROCESSED)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Auxiliar: último dia do mês anterior
# ---------------------------------------------------------------------
def default_ref_date() -> date:
    first = date.today().replace(day=1)
    return first - timedelta(days=1)

# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------
st.set_page_config(page_title="Relatório Financeiro", page_icon="📊", layout="centered")

st.title("📊 Gerador de Relatório Financeiro")
st.write(
    "Faça upload dos **3 arquivos obrigatórios** que serão salvos em `data/raw/` "
    "com os nomes definidos no `config.py`."
)

with st.expander("Nomes de arquivos esperados (vindos de config.py)", expanded=False):
    st.markdown(
        f"""
- **settlements** (Baixas de títulos) → `{config.Settlement.FILENAME}`
- **receivables** (Títulos a receber) → `{config.Receivable.FILENAME}`
- **open_payments** (Títulos em aberto) → `{config.OpenPayment.FILENAME}`
        """.strip()
    )

# Uploads (domínio)
col1, col2 = st.columns(2)
with col1:
    settlements = st.file_uploader(
        f"settlements — (Baixas) — esperado: `{config.Settlement.FILENAME}`",
        type=["xlsx"],
        key="settlements",
    )
    receivables = st.file_uploader(
        f"receivables — (Títulos a Receber) — esperado: `{config.Receivable.FILENAME}`",
        type=["xlsx"],
        key="receivables",
    )
with col2:
    open_payments = st.file_uploader(
        f"open_payments — (Títulos em Aberto) — esperado: `{config.OpenPayment.FILENAME}`",
        type=["xlsx"],
        key="open_payments",
    )

# Data de referência
ref_date = st.date_input("Data de referência", default_ref_date())
ref_str = ref_date.isoformat()

# Guardião (evita duplo clique / rerun simultâneo)
if "running" not in st.session_state:
    st.session_state["running"] = False

# Ação
clicked = st.button(
    "Gerar Relatório",
    type="primary",
    disabled=st.session_state.get("running", False),
)

if clicked and not st.session_state["running"]:
    # Validação
    missing = []
    if settlements is None:
        missing.append("settlements")
    if receivables is None:
        missing.append("receivables")
    if open_payments is None:
        missing.append("open_payments")

    if missing:
        st.error("Uploads faltando: " + ", ".join(missing))
        st.stop()

    st.session_state["running"] = True
    try:
        with st.spinner("Gerando relatório..."):
            RAW_DIR.mkdir(parents=True, exist_ok=True)

            # Salva com nomes do config.py
            (RAW_DIR / config.Settlement.FILENAME).write_bytes(settlements.read())
            (RAW_DIR / config.Receivable.FILENAME).write_bytes(receivables.read())
            (RAW_DIR / config.OpenPayment.FILENAME).write_bytes(open_payments.read())

            # ------------------ PIPELINE (como no main.py) -------------------
            settlements_ds   = GenericDataset(config.Settlement)
            totals_ds        = GenericDataset(config.Totals)
            receivables_ds   = GenericDataset(config.Receivable)
            open_payments_ds = GenericDataset(config.OpenPayment)

            summary = Summary(settlements_ds.get_dataset())

            report = reports.Report(
                summary=summary,
                receivable=receivables_ds,
                open_payments=open_payments_ds,
                totals=totals_ds,
            )

            compiler = reports.ReportCompiler(
                settlements=settlements_ds,
                totals=totals_ds,
                open_payments=open_payments_ds,
                summary=summary,
                report=report,
            )

            compiled = compiler.compile(ref_date=ref_str)

            writer = reports.ExcelReportWriter(
                output_dir=config.Paths.PROCESSED,
                config=config,
            )
            writer.write(ref_str, compiled)
            # ----------------------------------------------------------------

        # Saída final
        out_file = PROCESSED_DIR / f"{config.Compiled.FILENAME}{ref_str}{config.Excel.EXTENSION}"

        if out_file.exists():
            st.success(f"Relatório gerado com sucesso: `{out_file.name}`")
            st.toast("✅ Relatório pronto para download.", icon="✅")
            with open(out_file, "rb") as f:
                st.download_button(
                    label="⬇️ Baixar Relatório",
                    data=f.read(),
                    file_name=out_file.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="secondary",
                )
        else:
            st.error(
                "O relatório deveria ter sido gerado, mas não foi encontrado em "
                f"`{PROCESSED_DIR.as_posix()}`."
            )

    except Exception as e:
        st.exception(e)
        st.error("Falha ao gerar o relatório. Verifique os arquivos enviados e tente novamente.")
    finally:
        st.session_state["running"] = False