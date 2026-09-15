class AuthException(Exception):
    """Exceção base para erros de autenticação."""
    pass

class InvalidCredentialsException(AuthException):
    """Lançada quando e-mail ou senha estão incorretos."""
    pass

class UserNotVerifiedException(AuthException):
    """Lançada quando o e-mail do usuário ainda não foi confirmado."""
    pass

class UserRegistrationException(AuthException):
    """Usado no Registro (HTTP 400/409)."""
    pass


class UserEditException(Exception):
    """Usado na edição do perfil do usuário"""
    pass


