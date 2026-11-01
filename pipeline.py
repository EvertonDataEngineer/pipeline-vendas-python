# ========================================== #
# BLOCO 1: Dependências e Configurações
# Responsabilidade: Importar bibliotecas e carregar variáveis globais
# ========================================== #

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
import pandas as pd
import gdown

# Em um projeto real, isso viria de um arquivo .env
EMAIL_REMETENTE = "everton.silva.data@gmail.com"
EMAIL_SENHA = os.getenv("EMAIL_PASS", "SUA_SENHA_AQUI")  # Substitua pela sua senha real ou use variáveis de ambiente
DRIVE_FILE_ID = '1HSFFI4v7ju8qmy4eW12hdl1_BwkEImSw'


# ========================================== #
# BLOCO 2: Ingestão / Extração (Extract)
# Responsabilidade: Conectar com o mundo externo e trazer os dados brutos
# ========================================== #

def extrair_dados_drive(file_id: str, destino: str) -> None:
    print("Extraindo arquivo do Google Drive...")
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, destino, quiet=True)


# ========================================== #
# BLOCO 3: Processamento de Dados (Transform)
# Responsabilidade: Aplicar regras de negócio e matemática (Zero contato com internet)
# ========================================== #

def calcular_metricas_vendas(caminho_arquivo: str) -> tuple:
    print("Calculando métricas com Pandas...")
    tabela = pd.read_excel(caminho_arquivo)
    
    faturamento = tabela['Valor Final'].sum()
    qtde_produtos = tabela['Quantidade'].sum()
    
    return faturamento, qtde_produtos


# ========================================== #
# BLOCO 4: Integração / Alerta (Load / Notify)
# Responsabilidade: Entregar a informação final para o usuário ou sistema
# ========================================== #

def notificar_por_email(faturamento: float, qtde_produtos: int, destinatario: str) -> None:
    print(f"Notificando {destinatario}...")
    
    msg = EmailMessage()
    msg['Subject'] = 'Relatório Diário de Vendas'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario
    
    # 1. Tratamento das variáveis para o padrão Brasileiro
    # Transforma 2,917,311.00 -> 2X917X311.00 -> 2X917X311,00 -> 2.917.311,00
    faturamento_br = f"{faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Transforma 15,227 -> 15.227
    qtde_produtos_br = f"{qtde_produtos:,}".replace(",", ".")
    
    corpo = f"""Prezados,
    
Segue o relatório de vendas de hoje:
- Faturamento: R$ {faturamento_br}
- Produtos Vendidos: {qtde_produtos_br}

Atenciosamente, Everton Silva"""
    
    msg.set_content(corpo)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_REMETENTE, EMAIL_SENHA)
            server.send_message(msg)
            print("Email enviado com sucesso via Gmail!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"ERRO DE LOGIN: O Google recusou a senha. Detalhes: {e}")

# ========================================== #
# BLOCO 5: Orquestrador / Main
# Responsabilidade: Ditar a ordem de execução do pipeline
# ========================================== #

def executar_pipeline():
    print("Iniciando Pipeline de Vendas...")
    
    diretorio_atual = Path(__file__).parent.resolve() if '__file__' in locals() else Path.cwd()
    caminho_arquivo = str(diretorio_atual / "vendas_temp.xlsx")
    
    try:
        # 1. Extrai
        extrair_dados_drive(DRIVE_FILE_ID, caminho_arquivo)
        
        # 2. Transforma
        fat, qtde = calcular_metricas_vendas(caminho_arquivo)
        
        # 3. Carrega/Notifica
        notificar_por_email(fat, qtde, destinatario=EMAIL_REMETENTE)
        
    except Exception as e:
        print(f"Erro Crítico no Pipeline: {e}")
        
    finally:
        # Limpeza do ambiente sempre roda, mesmo se der erro
        if Path(caminho_arquivo).exists():
            os.remove(caminho_arquivo)
            print("Ambiente limpo. Fim da execução.")

# Ponto de entrada do script
if __name__ == "__main__":
    executar_pipeline()