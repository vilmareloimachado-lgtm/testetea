from services.usuario_service import UsuarioService 
 
 
class UsuarioController: 
    def __init__(self, service=None): 
        self.service = service or UsuarioService() 
 
    def listar_perfis(self): 
        usuarios = self.service.listar_usuarios() 
        return [usuario.nome for usuario in usuarios] 
 
    def criar_perfil(self, nome, estilo_instrucao, nivel_suporte, data_nascimento, senha_login, criado_em): 
        try: 
            usuario = self.service.criar_usuario( 
                nome, 
                estilo_instrucao,
                nivel_suporte,
                data_nascimento,
                senha_login,
                criado_em
             ) 
 
            return { 
                "sucesso": True, 
                "mensagem": f"Perfil {usuario.nome} criado.", 
                "usuario_id": usuario.id 
            } 
 
        except ValueError as erro: 
            return { 
                "sucesso": False, 
                "mensagem": str(erro) 
            } 