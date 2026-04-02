# Relatório Financeiro

Gerador de **Relatório Financeiro** a partir de arquivos de controle (baixas, títulos a receber e títulos em aberto), com:

*   ✅ **Pipeline em Python (CLI)**
*   ✅ **Interface Web com Streamlit**
*   ✅ Saída final em **Excel consolidado**
*   ✅ Estrutura organizada e desacoplada (CLI → UI)

***

## 📂 Estrutura do Projeto

```text
relatorio-financeiro/
├── src/
│   ├── cli.py                    # CLI para geração do relatório
│   ├── ui_streamlit.py           # Interface Streamlit
│   ├── config.py                 # Configurações e metadados
│   ├── base/
│   │   ├── generic_dataset.py
│   │   ├── summary.py
│   │   ├── reports.py
│   │   └── __init__.py
│   ├── utils/
│   └── __init__.py
├── data/
│   ├── raw/                      # Arquivos de entrada (xlsx)
│   └── processed/                # Relatórios gerados
├── environment.yml               # Ambiente Conda
└── README.md
```

***

## 📥 Arquivos de Entrada

O projeto trabalha com **3 arquivos obrigatórios**, cujos nomes **são definidos no `config.py`**:

| Domínio         | Descrição         |
| --------------- | ----------------- |
| `settlements`   | Baixas de títulos |
| `receivables`   | Títulos a receber |
| `open_payments` | Títulos em aberto |

> ⚠️ **Importante**  
> Os nomes físicos dos arquivos (`.xlsx`) **não são fixados no código da UI nem do CLI**,  
> eles são **sempre lidos a partir do `config.py`**.

Os arquivos devem estar em:

```text
data/raw/
```

***

## 🧠 Arquitetura

### ✅ Pipeline (núcleo)

Toda a lógica de negócio está no pipeline Python (`base/*`) e é acionada por:

*   **CLI (`cli.py`)**
*   **UI (`ui_streamlit.py`)**

A UI **não reimplementa lógica** — apenas coleta inputs e chama o mesmo fluxo do CLI.

***

## 🖥️ Uso via CLI (modo recomendado para automação)

### 1️⃣ Ativar o ambiente

```bash
conda activate relatorio-de-baixas
```

### 2️⃣ Gerar relatório

```bash
python src/cli.py --ref-date 2026-02-28
```

### ✅ Resultado

*   Relatório Excel gerado em:

```text
data/processed/
```

*   Mensagem de sucesso no terminal:

```text
OK: Relatório gerado para 2026-02-28
```

***

## 🌐 Uso via Interface Web (Streamlit)

### 1️⃣ Ativar o ambiente

```bash
conda activate relatorio-de-baixas
```

### 2️⃣ Subir o Streamlit

```bash
streamlit run src/ui_streamlit.py
```

### 3️⃣ Acessar no navegador

```text
http://localhost:8501
```

### ✅ Funcionalidades da UI

*   Upload dos 3 arquivos obrigatórios
*   Seleção da data de referência
*   Geração do relatório
*   Download direto do Excel final

***

## 🧪 Ambiente

O ambiente é gerenciado via **Conda**.

### Criar o ambiente

```bash
conda env create -f environment.yml
```

### Atualizar o ambiente

```bash
conda env update -f environment.yml --prune
```

### Dependências principais

*   Python 3.11
*   pandas
*   numpy
*   openpyxl
*   pyarrow
*   streamlit

***

## ✅ Estado Atual do Projeto

✔️ Pipeline validado e funcional  
✔️ CLI estável e idempotente  
✔️ Streamlit testado localmente (`streamlit run`)  
✔️ Sem empacotamento ou autoexec  
✔️ Base pronta para:

*   automação (cron / CI)
*   empacotamento futuro (ex: `conda-pack`, `.exe` no Windows)

***

## 📌 Observações Importantes

*   Durante desenvolvimento, **execute sempre**:
    ```bash
    streamlit run src/ui_streamlit.py
    ```
*   Evite wrappers, subprocess ou autoexec para o Streamlit
*   O CLI é a fonte da verdade para a lógica do relatório