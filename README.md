# 🚀 Automação de Pipeline ETL: Relatório de Vendas Diário

Este projeto consiste em um pipeline de dados automatizado e *headless* (sem interface gráfica) desenvolvido em Python. A arquitetura segue o padrão ETL (Extract, Transform, Load/Notify) para buscar dados na nuvem, processar métricas de negócios e alertar os *stakeholders* via e-mail.

## 🏗️ Arquitetura do Projeto

1. **Extract (Extração):** Conecta à API pública do Google Drive via `gdown` e faz o download do arquivo de vendas (`.xlsx`) de forma silenciosa para o ambiente de execução.
2. **Transform (Transformação):** Utiliza a biblioteca `pandas` para ler o arquivo Excel, calcular o faturamento total e a quantidade de produtos vendidos, aplicando regras de formatação numérica para o padrão brasileiro (R$ X.XXX,XX).
3. **Load / Notify (Carga / Notificação):** Constrói e envia um e-mail formatado de forma nativa utilizando o protocolo SMTP do Gmail (`smtplib` e `email.message`).
4. **Cleanup (Limpeza):** Rotina de encerramento que remove arquivos temporários do disco, garantindo a resiliência do ambiente para a próxima execução.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Pandas** (Processamento de dados)
- **Gdown** (Integração com Google Drive)
- **Smtplib / EmailMessage** (Protocolos de rede e SMTP)
- **Pathlib** (Manipulação dinâmica de caminhos de arquivos)

## ⚙️ Como Configurar e Executar

### 1. Clonar o repositório
```bash
git clone [https://github.com/EvertonDataEngineer/pipeline-vendas-python.git](https://github.com/EvertonDataEngineer/pipeline-vendas-python.git)
cd pipeline-vendas-python
