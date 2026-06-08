from secom.app.ports.output.login_repository import LoginRepository

class SignupPgRepository(LoginRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    pass