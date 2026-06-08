from secom.app.ports.input.signup_use_case import SignupUseCase
from secom.app.ports.output.signup_repository import SignupRepository




class SignupInteractor(SignupUseCase):
    def __init__(self, repository: SignupRepository) -> None:
        self._repository = repository
    pass