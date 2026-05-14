from fastapi import Depends, FastAPI, Query
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.db_health_adapter import DatabaseHealthAdapter
from deps import get_db
from titanic.app.james_controller import JamesController
from doro.app.doro_diretor import Diretor

app = FastAPI(title="Minahdev Cloud Main Page")


@app.get("/")
def read_root():
    return {"message": "FastAPI 메인페이지", "docs": "/docs"}

#타이타닉 데이터
@app.get("/titanic/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data_titanic()
    return df.to_dict(orient="records")


#타이타닉 전체 승객 수
@app.get("/titanic/count")
def read_titanic_count():
    james = JamesController()
    total_passengers = james.titanic_count()
    return {"total_passengers": total_passengers}


#타이타닉 생존자 수
@app.get("/titanic/count/survived")
def read_titanic_survived():
    james = JamesController()
    survived_passengers = james.titanic_survived()
    return {"survived_passengers": survived_passengers}


#타이타닉 사망자 수
@app.get("/titanic/count/dead")
def read_titanic_dead():
    james = JamesController()
    dead_passengers = james.titanic_dead()
    return {"dead_passengers": dead_passengers}



#타이타닉 결정트리 모델명, 정확도 표시
@app.get("/titanic/model")
def read_titanic_tree():
    james = JamesController()
    model_name = james.current_model_name()
    accuracy = james.current_model_accuracy()
    return {"model_name": model_name, "accuracy": accuracy}




@app.get("/doro/data")
def read_doro_data():
    diretor = Diretor()
    df = diretor.get_data_doro()
    return df.to_dict(orient="records")


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DatabaseHealthAdapter.server_time_payload(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)