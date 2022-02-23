from flask import Flask, render_template, redirect, request, url_for, session
import main as python_program  # main.py 에 있는 파이썬 프로그램 모듈로 불러오기
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html") # 초기 페이지를 보여준다
def get_link():
    link = request.args.get("link")
    link = str(link)
    print('melon link:', link)
    return link


@app.route('/wordcloud', methods=['POST', 'GET']) # GET 방식으로 링크를 가져옴

def wordcloud(): # get 방식
    link = str(get_link())
    print('melon link:', link)
    return render_template('wordcloud.html', link=link)

if __name__ == '__main__':
    app.run(debug=True)


# def make_wordcloud():
#     if request.method == 'GET':
#         music_link = request.args.get('music-link', type = str) # GET 방식은 reqeust.args.get 이 맞는데,
#         cloud = python_program.this_is_main(music_link) # 안 고쳐지는 url must be a string 에러... (music_link 가 Nonetype 으로 잘못 잡힌듯)
#     else:
#         cloud = None
#     return cloud