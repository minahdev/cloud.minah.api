from dataclasses import dataclass

@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class RuthValidationQuery:
    
    id: int   # 직관적인 타입 변경
    name: str


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class RuthValidationResponse:
    
    id: int   # 직관적인 타입 변경
    name: str