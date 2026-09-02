from controllers.usuario_controller import UsuarioController 
 
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
        nivel = input("Nivel Suporte: ").strip() 
         
        print("1. Leve") 
        print("2. Moderado")
        print("3. Severo")
                 
        escolha = input("Nivel: ").strip() 
        estilo = ( 
            "Moderado" 
            if escolha == "2" 
            else "Leve"
                if escolha =="3" 
        ) 








        resposta = controller.criar_perfil( 
            nome, 
            estilo
         
        ) 
 
        print(resposta["mensagem"]) 
 
    elif opcao == "3": 
        break 
 
    else: 
        print("Opção inválida.")