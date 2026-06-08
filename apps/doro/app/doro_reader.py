class Reader:
    def __init__(self):
        pass

    def get_data_doro(self):
        raise RuntimeError("프로젝트 내부 CSV를 읽지 않습니다. 데이터 업로드를 통해 입력해 주세요.")


    # def head_records(self, n: int = 10) -> list[dict]:
    #    df = self.get_data_doro().head(n)
    #    pandas의 NaN은 JSON 직렬화에서 에러가 나므로 None으로 변환
    #    df = df.astype(object).where(pd.notna(df),None)
    #    return df.to_dict(orient="records")
    

