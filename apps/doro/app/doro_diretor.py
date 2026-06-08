from fastapi import FastAPI

from doro.app.doro_reader import Reader

app = FastAPI(title="Doro(Diretor)")


class Diretor:
    def __init__(self):
        pass
    
    def get_data_doro(self):
        r = Reader()
        return r.get_data_doro()
