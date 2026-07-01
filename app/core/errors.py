class SugiException(Exception):
    """Clase base para todos los errores de dominio de Sugi."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DuplicatedEmailError(SugiException):
    def __init__(self, email: str):
        super().__init__(f"El correo {email} ya está registrado. Intenta con otro o inicia sesión.")

class UserNotFoundError(SugiException):
    def __init__(self):
        super().__init__("No encontramos a este usuario en la base de datos.")

class InvalidCredentialsError(SugiException):
    def __init__(self):
        super().__init__("Correo o contraseña incorrectos. Revisa tus datos.")

class InactiveUserError(SugiException):
    def __init__(self):
        super().__init__("Esta cuenta está desactivada o suspendida.")