from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
import db

app = Flask(__name__)
app.debug = True

app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

app.secret_key = "123456"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        curUser = db.doubanDB.getUser(user)
        if curUser:
            if curUser['password'] == password:
                session['username'] = user
                return redirect("/")
            else:
                return '账号密码错误！'
        else:
            return '没有该用户'
    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form.get("password")
        # 这里假设createUser 方法返回一个可以被 Flask 直接返回的响应
        # 如果它只是执行操作而不返回内容，你可能需要添加一个重定向或返回一个页面
        result = db.doubanDB.createUser(user, password)
        # 示例：如果 createUser 成功后应跳转到登录页
        # return redirect("/login")
        # 或者显示一个成功消息
        return result # 或者 return "注册成功" 之类的
    else:
        return render_template("register.html")


@app.route("/hottv")
def hottv():
    # 假设 getHoTV 返回的是可以直接渲染的 HTML 或 JSON
    # 如果是数据，需要处理成模板或 JSON 响应
    return db.doubanDB.getHoTV()


@app.route("/")
def index():
    # 获取一周口碑榜数据
    rank_week_data = db.doubanDB.getRankWeek()  # 返回的是字典列表，如 [{'id': 1, 'movie_name': '阿凡达'}]

    # 组织正在热映的电影数据（每组5个）
    renderHoting = []
    for movie in db.doubanDB.getHoting():
        renderHotingLen = len(renderHoting)
        curList = []

        if renderHotingLen == 0 or len(renderHoting[renderHotingLen - 1]) >= 5:
            pass
        else:
            curList = renderHoting[renderHotingLen - 1]

        curList.append(movie)

        if len(curList) == 1:
            renderHoting.append(curList)
        else:
            renderHoting[renderHotingLen - 1] = curList

    # 组织热门电影数据（每组7个）
    renderHotMovie = []
    for movie in db.doubanDB.getHotMovie():
        renderHotMovielen = len(renderHotMovie)
        curList = []

        if renderHotMovielen == 0 or len(renderHotMovie[renderHotMovielen - 1]) >= 7:
            pass
        else:
            curList = renderHotMovie[renderHotMovielen - 1]

        curList.append(movie)

        if len(curList) == 1:
            renderHotMovie.append(curList)
        else:
            renderHotMovie[renderHotMovielen - 1] = curList

    # 组织热门电视剧数据（每组7个）
    renderHotTv = []
    for movie in db.doubanDB.getHotTV():
        renderHotTvlen = len(renderHotTv)
        curList = []

        if renderHotTvlen == 0 or len(renderHotTv[renderHotTvlen - 1]) >= 7:
            pass
        else:
            curList = renderHotTv[renderHotTvlen - 1]

        curList.append(movie)

        if len(curList) == 1:
            renderHotTv.append(curList)
        else:
            renderHotTv[renderHotTvlen - 1] = curList

    username = session.get("username")

    return render_template("index.html",
                           hoting=renderHoting,
                           hotmovie=renderHotMovie,
                           hottv=renderHotTv,
                           rank_week=rank_week_data,
                           username=username)


@socketio.on('msg')
def handle_message(data):
    # 广播消息给所有连接的客户端
    emit("msg", data, broadcast=True)


@socketio.on('connect')
def test_connect(auth):
    print("新用户链接事件：", auth)


if __name__ == "__main__":
    # 传递 allow_unsafe_werkzeug=True 以允许在开发模式下使用 Werkzeug
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

    # 豆瓣电影展示系统（学习项目）


    # 本项目仅用于技术学习，  请勿用于生产环境或高频爬取
    # > 使用前请配置数据库并设置环境变量：




