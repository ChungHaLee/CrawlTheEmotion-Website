from flask import Flask, render_template, redirect, request, url_for, session
import main as python_program # 파이썬 프로그램 모듈로 불러오기
app = Flask(__name__)
# bp = Blueprint('main', __name__, url_prefix='/')

@app.route('/', methods=['GET'])
# app.route() 아래에 적어주는 뷰 함수에서 return 하는 응답은 일반적으로는 웹페이지의 HTML 이다.
# def index():
#     if session.get('LINK_IN'): # session의 ID 가 LINK_IN 이면 
#         return render_template("show_wordcloud.html") # 워드클라우드를 보여준다
#     else: # 아니면
#         return render_template("index.html") # 초기 페이지를 보여준다

def index():
    return render_template("index.html") # 초기 페이지를 보여준다


@app.route('/make_wordcloud') # 새로운 페이지로 이동까지는 됨 (라우팅 부분을 HTML 에 연결해줘야함)
def make_wordcloud():
    if request.method == 'GET':
        music_link = request.args.get('link', type = str) # GET 방식은 reqeust.args.get 이 맞는데,
        cloud = python_program.this_is_main(music_link) # 안 고쳐지는 url must be a string 에러... (music_link 가 Nonetype 으로 잘못 잡힌듯)
    else:
        cloud = None
    return cloud
    

if __name__ == '__main__':
    app.run(debug=True)