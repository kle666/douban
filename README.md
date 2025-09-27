本项目是一个基于 Python 的豆瓣电影信息展示系统，主要用于学习 Web 开发、网络爬虫与数据库交互等技术。项目通过爬取豆瓣电影网站的公开数据，将“一周口碑榜”、“正在热映”、“热门电影”和“热门电视剧”等模块内容存储至本地 MySQL 数据库，并通过 Flask 框架构建 Web 页面进行展示，同时集成了用户注册/登录功能与基于 WebSocket 的简易聊天室。

主要依赖包
Flask：轻量级 Web 框架，用于构建后端服务与路由。
Flask-SocketIO：实现实时通信，用于电影聊天室功能。
requests：用于向豆瓣网站发起 HTTP 请求，获取页面或接口数据。
BeautifulSoup4 + html5lib：解析豆瓣首页 HTML 内容，提取榜单和热映电影信息。
PyMySQL：连接并操作 MySQL 数据库，实现数据持久化。
json / re / os / threading：标准库模块，分别用于处理 JSON 数据、正则匹配、环境变量及线程锁控制。
项目结构组成
douban.py：封装豆瓣电影数据爬取逻辑，包含获取榜单、热映、热门电影/电视剧等方法，并调用图片下载功能。
db.py：封装数据库操作类 Db，提供对四类电影数据表（s_rank_week、s_hoting、s_hot_movie）及用户表（s_user）的增查接口，并使用线程锁保障并发安全。
main.py：Flask 应用主入口，定义路由（如首页、登录、注册、热门电视剧接口）、处理用户会话，并渲染模板。
templates/：存放前端模板文件（index.html、login.html、register.html），使用 Jinja2 模板语法动态展示数据。
static/pic/douban/：本地存储从豆瓣下载的电影封面图片。
⚠️ 本项目仅用于技术学习与教学演示，请勿用于生产环境或对豆瓣进行高频爬取，以免违反网站使用条款。
