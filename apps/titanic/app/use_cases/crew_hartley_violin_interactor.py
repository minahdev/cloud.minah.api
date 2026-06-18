from __future__ import annotations

import io

import matplotlib
matplotlib.use("Agg")  # 서버 환경에서 GUI 백엔드 비활성화
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort

import logging

logger = logging.getLogger(__name__)


class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        return await self._repository.introduce_myself(HartleyViolinQuery(
            id=schema.id,
            name=schema.name,
        ))

    def get_heatmap(self, df: pd.DataFrame) -> bytes:
        """상관관계 히트맵 PNG를 메모리 버퍼에서 바이트로 반환한다.

        파일 저장 없이 StreamingResponse로 직접 전송할 수 있다.
        """
        numeric_df = df.select_dtypes(include="number")

        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Titanic Correlation Heatmap")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        plt.close()

        return buf.read()

    def get_plotly_html(self, df: pd.DataFrame) -> str:
        """상관관계 히트맵을 인터랙티브 HTML 문자열로 반환한다.

        HTMLResponse에 담아 브라우저로 바로 전송할 수 있다.
        """
        numeric_df = df.select_dtypes(include="number")
        corr = numeric_df.corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Titanic Correlation Heatmap",
        )

        plot_html = fig.to_html(full_html=False)

        return f"""
        <html>
            <head><title>타이타닉 상관관계</title></head>
            <body>
                <h2>타이타닉 상관관계 Heatmap</h2>
                {plot_html}
            </body>
        </html>
        """
