from controllers.usuario_controller import UsuarioController 
from datetime import date
controller = UsuarioController() 
 
while True: 
    print("\n=== EXEMPLO AULA 02 ===") 
    print("1. Listar perfis") 
    print("2. Criar perfil") 
    print("3. Sair") 
 
    opcao = input("Escolha: ").strip() 
 
    if opcao == "1": 
        perfis = controller.listar_perfis() 
 
        print("\nPerfis:") 
        for nome in perfis: 
            print("-", nome) 
 
    elif opcao == "2": 
        nome = input("Nome: ").strip() 
 
        print("1. Direto") 
        print("2. Detalhado") 
        escolha = input("Estilo: ").strip() 
        estilo = ( 
            "detalhado" 
            if escolha == "2" 
            else "direto" 
        ) 
                 
        print("1. Leve") 
        print("2. Moderado")
        print("3. Severo")
                 
        nivel = input("Nivel: ").strip()

        if escolha == "1":
            nivel_suporte = "Leve"
        elif escolha == "2":
            nivel_suporte = "Moderado"
        elif escolha == "3":
            nivel_suporte = "Severo"
        else:
            nivel_suporte = "Não informado"

        data_nascimento = input(
            "\nDigite a data de nascimento (AAAA/MM/DD): "
        ).strip()
        senha_login = input("Digite a senha de acesso: ").strip()
        criado_em = date.today()

        resposta = controller.criar_perfil( 
            nome, 
            estilo,
            nivel_suporte,
            data_nascimento,
            senha_login,
            criado_em
        ) 
 
        print(resposta["mensagem"]) 
 
    elif opcao == "3": 
        break 
 
    else: 
        print("Opção inválida.")