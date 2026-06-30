"""Discord 의존성 조립소 (DIP 팩토리)."""

from comm_agent.app.ports.input.discord_use_case import DiscordUseCase
from comm_agent.app.use_cases.discord_interactor import DiscordInteractor


def get_discord_use_case() -> DiscordUseCase:
    return DiscordInteractor()
