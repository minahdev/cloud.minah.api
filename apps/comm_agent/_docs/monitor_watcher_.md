# [Specification] Multi-Agent System Test Harness Specification

## 1. System Overview & Architecture Context

본 시스템은 허브 앤 스포크(Hub-and-Spoke) 및 온톨로지 기반의 거대 비즈니스 ERP 멀티 에이전트 아키텍처이다.

- **최고 사령탑 (Hub / Brain)**: `core/lol/t1_mid_faker_orchestrator.py`
  초거대 AI 모델(EXAONE)이 상주하는 최고 권한의 오케스트레이터 에이전트.
- **온톨로지 버스 (Ontology Hub)**: `star_craft/`
  전사 데이터 흐름, 엔티티 관계(Ontology) 및 전사 컨텍스트를 총괄하는 데이터 허브 버스.
- **커뮤니케이션 스포크 (Communication Spoke)**: `comm_agent/`
  외부 채널(Email, Mail, Telegram, Discord 등)과의 소통 및 인바운드 이벤트를 전담하는 스포크.
- **기타 스포크 (Spokes)**: `titanic/`, `silicon_valley/` 등 (ERP의 개별 도메인 파트)

## 2. Agent Core Logic & Routing Criteria

외부 커뮤니케이션 채널을 통해 인입되는 이벤트는 비즈니스 중요도 및 의도(Intent)에 따라 다음과 같이 라우팅된다.

- **Case A (일반 업무)**: 중요 거래처가 아니거나 단순 문의인 경우
  ➔ `comm_agent` 내부의 홈즈(Holmes) 에이전트가 자체적으로 컨텍스트를 소화하여 처리 및 종결.
- **Case B (중요/에스컬레이션 업무)**: 중요 거래처이거나 자동 보고서 생성을 요청하는 경우
  ➔ 상위 온톨로지 버스인 `star_craft`를 경유하여 최고 에이전트인 **페이커(Faker / EXAONE)**에게 격상(Escalation). 페이커가 전사 ERP 데이터를 취합하여 최종 보고서를 생성하고 하향 전달.

## 3. Moniter (Watcher Hub / Entry Point) 역할 정의

`comm_agent/adapter/inbound/` 레이어에 위치한 **모니터(monitor_watcher)**은 본 테스트 하네스의 핵심 검증 대상이자 인바운드 게이트웨이이다. 왓슨은 단순한 라우터가 아닌 **'Triage Nurse(초진 및 분류 관문)'** 역할을 수행한다.

### 왓슨의 핵심 메커니즘

1. **감시 및 후킹 (Watch & Hook)**: 경찰/조력자 레이어(`telegram_router`, `discord_router` 등)로부터 유저 메시지 및 이벤트를 낚아챔.
2. **1차 분류 및 조율 (Validation & Triage)**: 인입된 메시지의 발신자(중요 거래처 여부)와 본문(보고서 요청 등의 의도)을 가볍고 빠르게 분석.
3. **컨텍스트 스위칭 및 라우팅 (Routing Decision)**:
   - 일반 메일 ➔ `comm_agent/app/use_cases` (홈즈) 호출.
   - 중요/보고서 메일 ➔ `star_craft` 온톨로지 버스로 이벤트 발행(Publish).

## 4. Test Harness Implementation Instructions (for Claude)

이 마크다운을 컨텍스트로 받는 LLM(클로드)은 위 설계를 검증하기 위한 테스트 하네스(Test Harness) 환경 코드를 다음 지시사항에 따라 생성하시오.

### [지시사항 1] 가상 이벤트 생성기 (Mock Event Generator) 구현

- `telegram_router`, `discord_router` 등 인바운드 라우터들이 외부에서 메일/메시지를 수신하는 상황을 모사하는 Mock 데이터 생성기를 작성할 것.
- 테스트 케이스 시나리오는 최소 2가지 이상을 포함해야 함:
  - **Scenario 1**: 일반 거래처의 단순 인사/일반 문의 메일 인입.
  - **Scenario 2**: VIP 거래처(`important_client: true`)의 "분기 실적 자동 보고서 발행 요망" 메시지 인입.

### [지시사항 2] Moniter의 라우팅 인터셉터 구현

- 가상 이벤트 생성기에서 발생한 raw 데이터를 모니터 인터페이스(`monitor_watcher_hub.py`)가 가로채어 검증하는 라우팅 로직을 구현할 것.
- **홈즈 호출 트리거**: Scenario 1 감지 시, `comm_agent/app/use_cases/` 내의 가상 홈즈 모듈 함수를 호출하고 로그를 남길 것.
- **페이커 에스컬레이션 트리거**: Scenario 2 감지 시, 상위 허브인 `star_craft` 프로토콜 메커니즘을 거쳐 `core/lol/t1_mid_faker_orchestrator.py`가 최종 활성화(Wake-up)되는 이벤트 버스 파이프라인(가상 MCP Notification 등)을 구현할 것.

### [지시사항 3] 하네스 대시보드 및 검증 로그 출력

- 이벤트 인입부터 최종 처리 완료(`monitor_watcher_hub` ➔ `star_craft` ➔ `t1_mid_faker_orchestrator`)까지의
  전체 멀티 에이전트 저니(Journey)를 콘솔에 **추적 서사 로그(Narrative Log)** 형태로 일목요연하게 출력하는 모니터링 기능을 포함할 것.
- 저니 스텝을 순서대로 출력하는 **추적기(JourneyTracer)** 헬퍼를 두고, 모니터 인터셉터가 각 단계에서 이를 호출한다.
- 하나의 이벤트에 대해 다음 스텝이 순서대로 콘솔에 남아야 한다:
  1. **인입**: 채널(telegram/discord), 발신자, VIP 여부(`important_client`), 본문 요약
  2. **Triage**: `monitor_watcher_hub`의 판정 결과(일반 / VIP·보고서요청)와 판정 근거
  3. **라우팅**: 일반건은 로컬 종결, VIP·보고서건은 `star_craft`로 이벤트 발행(Publish)
  4. **에스컬레이션**: `star_craft` 프로토콜 통과 → `t1_mid_faker_orchestrator`(Faker) Wake-up (가상 MCP Notification)
  5. **완료**: 최종 처리자와 결과, 소요 스텝 수
- 출력 예시:

  ```text
  ════════════════════════════════════════
  📨 [1] 인입        | 채널=discord | 발신자=VIP거래처 | VIP=True | 본문="분기 실적 보고서 발행 요망"
  🚑 [2] Triage      | monitor_watcher_hub → VIP=True, 보고서요청=True → 판정: ESCALATE 🚨
  ⬆️ [3] 라우팅       | monitor_watcher_hub → star_craft 이벤트 발행(Publish)
  🛰️ [4] 에스컬레이션 | star_craft 프로토콜 통과 → (가상 MCP Notification)
  🧠 [5] Faker       | t1_mid_faker_orchestrator Wake-up → 전사 ERP 취합 → 보고서 생성
  ✅ [6] 완료         | 처리자=Faker | 소요 5스텝
  ════════════════════════════════════════
  ```