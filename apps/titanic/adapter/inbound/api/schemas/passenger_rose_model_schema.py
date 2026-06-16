from pydantic import BaseModel, Field

class RoseModelSchema(BaseModel):
    id: int = Field(0, description="Passenger ID")
    name: str = Field("로즈 드윗 부카터", description="Passenger's name")

    model_config = {
        "json_schema_extra": {
            "example": {"id": 11, "name": "Rose DeWitt Bukater"}
        }
    }

class RosePredictSchema(BaseModel):
    pclass: int = Field(3, description="객실 등급 (1/2/3)")
    sex: str = Field("female", description="성별 (male/female)")
    age: float = Field(17.0, description="나이")
    sib_sp: int = Field(1, description="형제자매/배우자 수")
    parch: int = Field(2, description="부모/자녀 수")
    fare: float = Field(7.25, description="요금")
    embarked: str = Field("S", description="승선지 (C/Q/S)")
    algorithm: str = Field(
        "random_forest",
        description="xgboost | random_forest | lightgbm | catboost | logistic_regression | decision_tree | svm | knn | naive_bayes | kmeans_pca",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "pclass": 1, "sex": "female", "age": 17.0,
                "sib_sp": 1, "parch": 2, "fare": 71.2833,
                "embarked": "C", "algorithm": "xgboost",
            }
        }
    }