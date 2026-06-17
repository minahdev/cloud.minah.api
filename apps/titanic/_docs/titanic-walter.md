지속적인 시스템 아키텍처 관리를 위해 개인 지식 베이스(Obsidian 등)에 바로 누적하여 기록하실 수 있는 형태로 제공합니다.

⚓ [Titanic App] Walter Nichols (Crew Roaster) 개발 및 검증 보고서

1. 아키텍처 명세 및 변경 요약

Walter Nichols(일등 항해사, 승객 명단 관리 담당)의 요구사항에 맞춰 데이터셋 조회 엔드포인트 구현 및 기존 의존성 주입(DI) 버그를 전면 수정했습니다.

[Inbound Adapter]                   [Core / Input Port]              [Outbound Adapter]
  Router: /walter/train (def)  ──>    WalterRoasterUseCase   ──>    WalterRoasterRepository
  Router: /walter/test  (def)          (pd.DataFrame 반환)            (Pandas + Sync Engine)

🧱 포트 및 인터페이스 변경 사항
동기(Sync) 처리 원칙 적용: 데이터베이스를 동기로 읽는 Pandas CPU/I/O 작업이므로, async def로 이벤트 루프를 블로킹하지 않도록 일반 def 함수로 선언하여 FastAPI가 내부 스레드풀에서 안전하게 처리하도록 구조화했습니다.
반환 타입 정립: DTO(WalterRoasterResponse)의 규격 제한을 탈피하고 분석 목적에 맞게 pd.DataFrame을 직접 반환하도록 포트 인터페이스를 통일했습니다.
2. 레이어별 코드 구현 현황

📥 Input / Output Ports

apps/titanic/app/ports/input/crew_walter_roaster_use_case.py

Python
from abc import ABC, abstractmethod
import pandas as pd

class WalterRoasterUseCase(ABC):
    
@abstractmethod

    def get_train_set(self) -> pd.DataFrame:
        """월터가 DB에서 train set 만 가져오는 메소드"""
        pass

    
@abstractmethod

    def get_test_set(self) -> pd.DataFrame:
        """월터가 DB에서 test set 만 가져오는 메소드"""
        pass

⚙️ Use Cases (Interactor)

apps/titanic/app/use_cases/crew_walter_roaster_interactor.py

Python

import pandas as pd
from http://titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort

class WalterRoasterInteractor(WalterRoasterUseCase):
    def __init__(self, repository: WalterRoasterPort) -> None:
        self.repository = repository

    def get_train_set(self) -> pd.DataFrame:
        return self.repository.get_train_set()

    def get_test_set(self) -> pd.DataFrame:
        return self.repository.get_test_set()

📤 Outbound Repositories
apps/titanic/adapter/outbound/repositories/crew_walter_roaster_repository.py
Python

from sqlalchemy import create_engine
import pandas as pd
import core.matrix.grid_oracle_database_manager as _db_manager

class WalterRoasterRepository(WalterRoasterPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def get_train_set(self) -> pd.DataFrame:
        """Survived 컬럼이 있는 데이터 전체를 데이터프레임으로 반환"""
        sync_url = _to_sync_url(_db_manager.engine.url.render_as_string(hide_password=False))
        sync_engine = create_engine(sync_url)
        return http://pd.read_sql("SELECT * FROM passengers WHERE survived IS NOT NULL", sync_engine)

    def get_test_set(self) -> pd.DataFrame:
        """Survived 컬럼이 없는 데이터 전체를 데이터프레임으로 반환"""
        sync_url = _to_sync_url(_db_manager.engine.url.render_as_string(hide_password=False))
        sync_engine = create_engine(sync_url)
        return http://pd.read_sql("SELECT * FROM passengers WHERE survived IS NULL", sync_engine)
3. 디버깅 및 트러블슈팅 내역 (Bug Fixes)
서버 기동 및 격리 검증 단계에서 발견된 코드 전반의 구조적 결함과 기존 버그들을 일괄 해결했습니다.
발생 지점 / 유발 요인현상 및 원인 분석조치 사항 (Refactoring)SQLAlchemy Engine URLstr(engine.url) 사용 시 DB 패스워드가 ***로 마스킹되어 동기 엔진 생성 시 인증 실패(Authentication Failed) 발생url.render_as_string(hide_password=False)로 명시하여 정상적인 원본 스토리지 자격증명 주입모듈 단위 결합도 결함from module import engine 실행 시, init_engine() 호출 전의 None 객체를 변수가 조기 스냅숏 캡처하는 문제모듈 객체 전체를 가져온 후(import module as _m), 런타임 시점에 컨텍스트 체이닝(.engine)으로 안전하게 접근하도록 수정
타이타닉 앱 Providers

(Pre-existing Bug)
http://adapter.outbound.pg.* 경로 오 지정 및 get_jack_train_use_case 등 팩토리 메소드 식별자 오타로 인해 전면 실행 불가 상태타이타닉 소속 전역 프로바이더/라우터 의존성 수입 경로 및 식별자 네이밍 전수 교정 완료
4. 최종 통합 검증 결과 (Verification & Verdict)
검증 방식: Walter 라우터 스코프를 격리 적용한 단독 미니 FastAPI 테스트 하네스를 빌드하여 실제 런타임 파이프라인 검증 수행.