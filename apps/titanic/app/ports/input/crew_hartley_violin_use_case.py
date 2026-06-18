from abc import ABC, abstractmethod

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse


class HartleyViolinUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        pass

    @abstractmethod
    def get_heatmap(self, df: pd.DataFrame) -> bytes:
        """상관관계 히트맵을 PNG 바이트로 반환한다 (Seaborn/Matplotlib)."""
        pass

    @abstractmethod
    def get_plotly_html(self, df: pd.DataFrame) -> str:
        """상관관계 히트맵을 인터랙티브 HTML 문자열로 반환한다 (Plotly)."""
        pass
