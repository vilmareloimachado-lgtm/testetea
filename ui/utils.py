import os
from datetime import datetime

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo: str):
    limpar_tela()
    print("=" * 60)
    print(f"{titulo.center(60)}")
    print("=" * 60 + "\n")

    from datetime import datetime

def data_br_para_iso(data_str):
    if not data_str:
        return ""
    try:
        return datetime.strptime(
            data_str,
            "%d/%m/%Y"
        ).strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Data inválida. Utilize DD/MM/AAAA."
        )    

def data_iso_para_br(data_str):
    if not data_str:
        return ""
    return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")