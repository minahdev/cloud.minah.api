from secom.app.ports.input.login_use_case import LoginUseCase
from secom.app.ports.output.login_repository import LoginRepository




class LoginInteractor(LoginUseCase):
    def __init__(self, repository: LoginRepository) -> None:
        self._repository = repository
    pass