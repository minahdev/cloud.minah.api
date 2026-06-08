from secom.app.ports.output.signup_repository import SignupRepository

class SignupPgRepository(SignupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    pass
    