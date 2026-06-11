import ollama
from kiwipiepy import Kiwi

# 1. 한국어 형태소 분석기 Kiwi 초기화
kiwi = Kiwi()

def run_korean_ai(user_text):
    print("\n--- [1단계] 입력 문장 전처리 중... ---")
    
    # kiwipiepy를 활용한 가벼운 전처리 예시 (띄어쓰기 오차 보정)
    cleaned_text = user_text
    print(f"입력 문장: {user_text}")
    
    # 형태소 분석 결과 예시 출력 (명사만 추출해보기)
    tokens = kiwi.tokenize(cleaned_text)
    nouns = [t.form for t in tokens if t.tag.startswith('NN')]
    print(f"추출된 핵심 명사: {nouns}")
    
    print("\n--- [2단계] 야놀자 EEVE-Korean 모델 추론 중... ---")
    
    # 2. Ollama에 설치된 야놀자 EEVE 모델에 질문 던지기
    response = ollama.chat(
        model='anpigon/eeve-korean-10.8b',
        messages=[
            {
                'role': 'user', 
                'content': cleaned_text
            }
        ]
    )
    
    # 3. 결과 반환
    return response['message']['content']

# 실제 실행 테스트
if __name__ == "__main__":
    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."
    answer = run_korean_ai(question)
    
    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)
 # python test.py   