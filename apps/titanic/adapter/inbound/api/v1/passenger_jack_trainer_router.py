from fastapi import APIRouter
from titanic.app.use_cases.passenger_cal_tester_interactor import CaledonValidation

'''
잭 도슨 (Jack Dawson)
자유로운 영혼, 예술가, 그리고 로즈를 구원하는 인물인 만큼
'그림'이나 '포커 도박'과 관련된 키워드가 잘 어울립니다.
생존 예측 모델의 핵심 인터페이스를 담당합니다.
'''

jack_train_router = APIRouter(prefix="/titanic/jack", tags=["jack"])


@jack_train_router.get("/myself")
async def introduce_myself():
    return {"character": "Jack Dawson", "role": "train", "memo": "자유로운 예술가. ML 생존 예측 모델 학습·추론 담당"}