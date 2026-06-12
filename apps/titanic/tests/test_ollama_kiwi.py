import pytest
import ollama
from kiwipiepy import Kiwi

kiwi = Kiwi()


def run_korean_ai(user_text: str) -> str:
    print("\n--- [1단계] 입력 문장 전처리 중... ---")
    print(f"입력 문장: {user_text}")

    tokens = kiwi.tokenize(user_text)
    nouns = [t.form for t in tokens if t.tag.startswith('NN')]
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] 야놀자 EEVE-Korean 모델 추론 중... ---")
    response = ollama.chat(
        model='anpigon/eeve-korean-10.8b',
        messages=[{'role': 'user', 'content': user_text}]
    )
    return response['message']['content']


@pytest.mark.ollama
def test_korean_ai():
    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."
    answer = run_korean_ai(question)

    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)

    assert isinstance(answer, str)
    assert len(answer) > 0


if __name__ == "__main__":
    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."
    answer = run_korean_ai(question)
    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)

