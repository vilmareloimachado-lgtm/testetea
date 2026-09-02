from ui.utils import (
    exibir_cabecalho,
    data_br_para_iso,
    data_iso_para_br
)
#from ui.utils import exibir_cabecalho
from data.data_manager import carregar_dados, salvar_dados
import core.tarefas as core_tarefas
import core.ia_service as ia_service
import re
#import hashlib  

#def criptografar_senha(senha: str) -> str: 
#    """Gera um hash SHA-256 seguro a partir da senha em texto puro."""  
#    return hashlib.sha256(senha.encode("utf-8")).hexdigest()  

def validar_nome(nome):
    nome = nome.strip()

    # Permite apenas letras e espaços
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome))

def _pedir_prioridade(): 
    print("\nPrioridade da tarefa:") 
    print("1. Baixa") 
    print("2. Média") 
    print("3. Alta") 
    escolha = input("Escolha: ").strip()

    if escolha == "1": 
        return "baixa" 
    if escolha == "3": 
        return "alta" 
    return "media"
def _mostrar_tarefas(tarefas): 
    if not tarefas: 
        print("[Nenhuma tarefa cadastrada.]") 
        return 
    for idx, tarefa in enumerate(tarefas, 1): 
        status = "[X]" if tarefa["concluida"] else "[ ]"
        prioridade = tarefa.get("prioridade", "media").upper() 
        prazo = tarefa.get("prazo", "")
        if prazo:
            prazo = data_iso_para_br(prazo)
        else:
            prazo = "Sem prazo"

        print(f"{idx}. {status} {tarefa['titulo']}") 
        print(f"   Prioridade: {prioridade} | Prazo: {prazo}") 
        
        if tarefa.get("descricao"): 
            print(f"   Descrição: {tarefa['descricao']}")
        
        for i, passo in enumerate(tarefa.get("passos", []), 1): 
            simbolo = "✓" if passo.get("concluido") else " " 
            print(f"   {i}. {simbolo} {passo['texto']}")

def criar_usuario_menu(dados: dict):
    exibir_cabecalho("CRIAR PERFIL DO ESTUDANTE ")
    nome = input("Digite o nome do Estudante: ").strip()

    if not validar_nome(nome):
        print("\nNome inválido! Digite apenas letras e espaços.")
        input("Pressione Enter para continuar...")
        return
    
    if not nome or nome in dados:
        input("\nNome inválido ou já existente. Pressione Enter.")
        return
        
    print("\n--- Preferências de Comunicação ---")
    print("1. Passo a passo curto e direto")
    print("2. Detalhado e explicativo")
    pref = input("Opção: ").strip()
    estilo = "direto" if pref == "1" else "detalhado"
    print("\n--- Nível de Suporte ---")                                      
    print("1. Leve")                                                          
    print("2. Moderado")                                                      
    print("3. Severo")                                                        
    pref_suporte = input("Opção: ").strip()                                   
    if pref_suporte == "2":                                                   
        nivel_suporte = "Moderado"                                            
    elif pref_suporte == "3":                                                 
        nivel_suporte = "Severo"                                              
    else:                                                                     
        nivel_suporte = "Leve"             

    while True:
        data_nascimento = input(
            "\nDigite a data de nascimento (DD/MM/AAAA): "
        ).strip()

        if not data_nascimento:
            data_nascimento = None
            break

        try:
            data_nascimento = data_br_para_iso(data_nascimento)
            break
        except ValueError:
            print("\nData inválida! Exemplo válido: 25/09/" \
            "1984")

        if not data_nascimento:                                                   
            data_nascimento = None

    senha_login = input("Digite a senha de acesso: ").strip()
    #senha_puro_texto = input("Digite a senha de acesso: ").strip()  
    #senha_criptografada = criptografar_senha(senha_puro_texto)  

    dados[nome] = {
        "preferencias": {"estilo_instrucao": estilo},
        "nivel_suporte": nivel_suporte,                                       
        "data_nascimento": data_nascimento,                                   
        "senha_login": senha_login,         
        "tarefas_diarias": [],
        "tarefas_educacionais": []
    }
    salvar_dados(dados)
    input(f"\nPerfil [{nome}] criado! Pressione Enter.")

def gerenciar_tarefas_menu(dados: dict, usuario: str, chave: str, titulo: str):
    while True:
        exibir_cabecalho(titulo)
        tarefas = dados[usuario][chave]
        
        _mostrar_tarefas(tarefas)

        print("\n" + "-"*30)
        print("1. Criar tarefa") 
        print("2. Alternar status da tarefa") 
        print("3. Editar tarefa") 
        print("4. Excluir tarefa") 
        print("5. Marcar passo como concluído") 
        print("6. Desmembrar com IA") 
        print("7. Voltar")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1": 
            titulo_tarefa = input("Título da tarefa: ").strip() 
            if not titulo_tarefa: 
                input("\nO título não pode ficar vazio. Pressione Enter.") 
                continue 
            descricao = input("Descrição curta da tarefa: ").strip() 
            prioridade = _pedir_prioridade() 

            while True:
                prazo = input(
                    "Prazo no formato DD/MM/AAAA (ou deixe vazio): "
                ).strip()

                if not prazo:
                    break

                try:
                    prazo = data_br_para_iso(prazo)
                    break
                except ValueError:
                    print("\nData inválida! Exemplo válido: 15/05/2026")


            core_tarefas.adicionar_tarefa(dados, usuario, chave, titulo_tarefa, descricao, prioridade, prazo) 
            input("\nTarefa criada com sucesso! Pressione Enter.")
        
        elif opcao == "2" and tarefas:
            try:
                idx = int(input("Número da tarefa: ")) - 1
                if not core_tarefas.alternar_status_tarefa(dados, usuario, chave, idx):
                    input("\nNão é possível concluir: existem passos pendentes. Pressione Enter.")
            except ValueError: pass

        elif opcao == "3" and tarefas: 
            try: 
                idx = int(input("Número da tarefa que deseja editar: ")) - 1 
                if 0 <= idx < len(tarefas): 
                    tarefa_atual = tarefas[idx] 
                    print("\nDeixe em branco para manter o valor atual.")
                    novo_titulo = input(f"Novo título [{tarefa_atual['titulo']}]: ").strip() or tarefa_atual["titulo"] 
                    nova_descricao = input(f"Nova descrição [{tarefa_atual.get('descricao', '')}]: ").strip() or tarefa_atual.get("descricao", "") 
                    nova_prioridade = input(f"Nova prioridade baixa/media/alta [{tarefa_atual.get('prioridade', 'media')}]: ").strip() or tarefa_atual.get("prioridade", "media") 
        #           novo_prazo = input(f"Novo prazo AAAA-MM-DD [{tarefa_atual.get('prazo', '')}]: ").strip() or tarefa_atual.get("prazo", "") 
                    prazo_atual = tarefa_atual.get("prazo", "")

                    if prazo_atual:
                        prazo_atual = data_iso_para_br(prazo_atual)

                    novo_prazo = input(
                        f"Novo prazo DD/MM/AAAA [{prazo_atual}]: "
                    ).strip()

                    if novo_prazo:
                        novo_prazo = data_br_para_iso(novo_prazo)
                    else:
                        novo_prazo = tarefa_atual.get("prazo", "")

                    if nova_prioridade not in ["baixa", "media", "alta"]: 
                        nova_prioridade = "media" 
                    core_tarefas.editar_tarefa(dados, usuario, chave, idx, novo_titulo, nova_descricao, nova_prioridade, novo_prazo) 
                    input("\nTarefa editada com sucesso! Pressione Enter.") 
            except ValueError: 
                    input("\nDigite apenas números. Pressione Enter.")
        elif opcao == "4" and tarefas: 
            try: 
                idx = int(input("Número da tarefa que deseja excluir: ")) - 1 
                if 0 <= idx < len(tarefas): 
                    confirmar = input(f"Tem certeza que deseja excluir '{tarefas[idx]['titulo']}'? (s/n): ").lower() 
                    if confirmar == "s": 
                        core_tarefas.excluir_tarefa(dados, usuario, chave, idx) 
                        input("\nTarefa excluída! Pressione Enter.") 
            except ValueError: 
                input("\nDigite apenas números. Pressione Enter.")

        elif opcao == "5" and tarefas: 
            try: 
                idx_tarefa = int(input("Número da tarefa: ")) - 1 
                idx_passo = int(input("Número do passo: ")) - 1 
                core_tarefas.alternar_status_passo(dados, usuario, chave, idx_tarefa, idx_passo) 
                input("\nStatus do passo alterado! Pressione Enter.") 
            except ValueError: 
                input("\nDigite apenas números. Pressione Enter.")
        elif opcao == "6" and tarefas:
            try:                
                idx = int(input("Número da tarefa para desmembrar: ")) - 1                
                if 0 <= idx < len(tarefas):                    
                    passos = ia_service.gerar_passos_tarefa(tarefas[idx]["titulo"])                    
                    print("\nPassos sugeridos:")                    
                    for i, p in enumerate(passos, 1):                        
                        print(f"  {i}. {p}")                    
                    if input("\nAceitar sugestão? (s/n): ").lower() == "s":                        
                        core_tarefas.injetar_passos_ia(dados, usuario, chave, idx, passos)                        
                        input("\nPassos adicionados! Pressione Enter.")            
            except ValueError:                
                input("\nDigite apenas números. Pressione Enter.")        
        elif opcao == "7":            
            break

def painel_ia_menu(dados: dict, usuario: str):
    exibir_cabecalho("ASSISTENTE DE IA PARA TEA")
    print("Peça ajuda para simplificar enunciados, organizar rotinas ou tirar dúvidas.")
    print("Digite 'sair' para retornar.\n")
    estilo = dados[usuario]["preferencias"]["estilo_instrucao"]

    while True:
        pergunta = input("\nVocê: ").strip()
        if pergunta.lower() == 'sair': break
        if not pergunta: continue

        print("\n🤖 Processando sem ambiguidades...")
        respostas = ia_service.obter_resposta_ia(pergunta, estilo)
        print(f"\n[Assistente - Modo {estilo.upper()}]:")
        for linha in respostas:
            print(f"- {linha}")
        print("-" * 30)

def relatorio_menu(dados: dict, usuario: str): 
    resumo = core_tarefas.gerar_resumo_tarefas(dados, usuario) 
    exibir_cabecalho("RELATÓRIO DO ESTUDANTE") 
    print(f"Total de tarefas: {resumo['total']}") 
    print(f"Tarefas concluídas: {resumo['concluidas']}") 
    print(f"Tarefas pendentes: {resumo['pendentes']}") 
    input("\nPressione Enter para voltar.")

def painel_principal_menu(dados: dict, usuario: str):
    while True:
        exibir_cabecalho(f"PAINEL DO USUÁRIO: {usuario}")
        print("1. Rotina diária")
        print("2. Estudos e atividades")
        print("3. Chat com IA")
        print("4. Relatório do Usuário")
        print("5. Voltar")
        opcao = input("\nEscolha: ").strip()
        if opcao == "1": 
            gerenciar_tarefas_menu(dados, usuario, "tarefas_diarias", "ROTINA DIÁRIA") 
        elif opcao == "2": 
            gerenciar_tarefas_menu(dados, usuario, "tarefas_educacionais", "ESTUDOS E ATIVIDADES") 
        elif opcao == "3": 
            painel_ia_menu(dados, usuario) 
        elif opcao == "4": 
            relatorio_menu(dados, usuario) 
        elif opcao == "5": break
