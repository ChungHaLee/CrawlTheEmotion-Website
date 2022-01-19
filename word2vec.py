import nltk
nltk.download('punkt')
import pandas as pd
import itertools
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, WordPunctTokenizer, TreebankWordTokenizer, RegexpTokenizer, sent_tokenize
from multilabel_pipeline import MultiLabelPipeline
from transformers import ElectraTokenizer
from model import ElectraForMultiLabelClassification
from pprint import pprint
from konlpy.tag import *
okt = Okt()

tokenizer_goemotions = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-goemotions")
model_goemotions = ElectraForMultiLabelClassification.from_pretrained("monologg/koelectra-base-v3-goemotions")

goemotions = MultiLabelPipeline(
    model=model_goemotions,
    tokenizer=tokenizer_goemotions,
    threshold=0.3
)

# 데이터 불러오고 전처리하기
music_by_numbers = pd.read_excel('./music_by_numbers.xlsx', engine='openpyxl')
dance_by_numbers = pd.read_excel('./dance_by_numbers.xlsx', engine='openpyxl')
visual_by_numbers = pd.read_excel('./visual_by_numbers.xlsx', engine='openpyxl')
talking_data_1 = pd.read_excel('/Users/lifeofpy/Desktop/dataset_청각2/감정 분류를 위한 대화 음성 데이터셋_4차년도.xlsx', engine='openpyxl')
talking_data_2 = pd.read_excel('/Users/lifeofpy/Desktop/dataset_청각2/감정 분류를 위한 대화 음성 데이터셋_5차년도_1차.xlsx', engine='openpyxl')
talking_data_3 = pd.read_excel('/Users/lifeofpy/Desktop/dataset_청각2/감정 분류를 위한 대화 음성 데이터셋_5차년도_2차.xlsx', engine='openpyxl')

music_by_numbers = music_by_numbers.drop(['Unnamed: 0'], axis=1)
dance_by_numbers = dance_by_numbers.drop(['Unnamed: 0'], axis=1)
visual_by_numbers = visual_by_numbers.drop(['Unnamed: 0'], axis=1)

# 데이터프레임 리스트로 바꾸기
music_list = music_by_numbers.values.tolist()
dance_list = dance_by_numbers.values.tolist()
visual_list = visual_by_numbers.values.tolist()
talking_data_1_list = talking_data_1[['발화문']].values.tolist()
talking_data_2_list = talking_data_2[['발화문']].values.tolist()
talking_data_3_list = talking_data_3[['발화문']].values.tolist()

# 데이터를 하나의 리스트로 합쳐줌(2차원 리스트 >> 1차원 리스트)
# Word2Vec 모델 학습을 위해 댓글 문장 nltk 를 사용해서 토크나이징
tokens = music_list + dance_list + visual_list + talking_data_1_list + talking_data_2_list + talking_data_3_list
tokens = list(itertools.chain.from_iterable(tokens))

# 진짜 토크나이징한 리스트 real_tokens
real_tokens = []
for i in range(len(tokens)):
    real_tokens.append(word_tokenize(tokens[i]))


# word2vec 모델 불러와서 학습하기
model = Word2Vec(real_tokens, alpha=0.025, window=2, min_count=5, sg=1)
model.train(real_tokens, total_examples=len(real_tokens), epochs=30)


# [응용] 명사 추출한 것 바탕으로 유사어 검색 자동화하기
# 문장에 포함된 명사를 알려주는 함수
def show_nouns(text):
    for i in range(len(text)):
        noun_lst = okt.nouns(text[i])
    return noun_lst


# 문장에 포함된 동사를 알려주는 함수
def show_verbs(text):
    okts = []
    verbs = []
    for i in range(len(text)):
        okts.append(okt.pos(text[i]))
    for j in range(len(okts)):
        for k in range(len(okts[j])):
            if okts[j][k][1] == 'Verb' and len(okts[j][k][0]) > 1:
                verbs.append(okts[j][k][0])
    return verbs


# 문장에 포함된 형용사를 알려주는 함수
def show_adjectives(text):
    okts = []
    adjs = []
    for i in range(len(text)):
        okts.append(okt.pos(text[i]))
    for j in range(len(okts)):
        for k in range(len(okts[j])):
            if okts[j][k][1] == 'Adjective' and len(okts[j][k][0]) > 1:
                adjs.append(okts[j][k][0])
    return adjs


# 단어와 연관된 유사어를 알려주는 함수
def find_similar_words(text):
    similar_words_lst = []
    for i in range(len(text)):
        try:
            similar_words_lst.append({text[i]: model.wv.most_similar(text[i])})
        except:
            pass
    return similar_words_lst


# 문장이 내포하는 감정을 알려주는 함수
def show_emotion(text):
    for i in range(len(text)):
        emotion_lst = goemotions(text[i])
    return emotion_lst


# 문장에 들어있는 명사/동사/형용사 추출 + 감정 분류 함수 실행 코드
def show_emotion_with_text(text):
    print('target text:', text)
    print('emotion label:', show_emotion(text))
    print('\n')
    print('noun words:', show_nouns(text))
    print('similar words w/ noun:', find_similar_words(show_nouns(text)))
    print('\n')
    print('verb words:', show_verbs(text))
    print('similar words w/ verb:', find_similar_words(show_verbs(text)))
    print('\n')
    print('adjective words:', show_adjectives(text))
    print('similar words w/ adj:', find_similar_words(show_adjectives(text)))
    print('\n')
    return


# 예시로 데이터에는 없는 raw text 를 넣어보자
data = ['공주병 말기인 주인공이 머리를 휘날리며 부를 것 같은 음악']
show_emotion_with_text(data)

data = ['드라마 주인공이 복수하러 갈 때 나올 것 같은 노래']
show_emotion_with_text(data)

data = ['부모님이 나에게 주신 사랑을 보답하고 싶어']
show_emotion_with_text(data)

data = ['친구들과 같이 놀러갔는데 마음에 드는 남자를 발견했을 때']
show_emotion_with_text(data)

data = ['자신감 넘치고 당당한 음악']
show_emotion_with_text(data)

data = ['들으면 뭐든지 잘할 수 있을 것 같은 노래']
show_emotion_with_text(data)
