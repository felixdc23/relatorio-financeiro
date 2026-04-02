# run_ui.py
from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

# Ambiente estável para app empacotado
os.environ["STREAMLIT_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_WATCH_DIRS"] = ""
os.environ["WATCHFILES_FORCE_POLLING"] = "false"

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# Deixe o Streamlit abrir o navegador
os.environ["STREAMLIT_SERVER_HEADLESS"] = "false"

# Higieniza variáveis que induziam dev server/porta alternativa
os.environ.pop("STREAMLIT_DEVELOP_MODE", None)
os.environ.pop("STREAMLIT_DEV_SERVER", None)
os.environ.pop("STREAMLIT_DEV_SERVER_PORT", None)
os.environ.pop("STREAMLIT_BROWSER_SERVER_PORT", None)
os.environ.pop("STREAMLIT_BROWSER_SERVER_ADDRESS", None)

def main() -> None:
    base_dir = Path(__file__).resolve().parent
    ui_script = base_dir / "src" / "ui_streamlit.py"

    if not ui_script.exists():
        print(f"[ERRO] UI não encontrada: {ui_script}")
        sys.exit(1)

    print("[UI] Iniciando Streamlit...")

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{base_dir / 'src'}:{env.get('PYTHONPATH', '')}"

    subprocess.Popen(
        [
            sys.executable,
            "-m", "streamlit", "run", str(ui_script),
            "--server.address=127.0.0.1",
            "--server.port=8501",
        ],
        env=env,
        cwd=str(base_dir),
    )

if __name__ == "__main__":
    main()