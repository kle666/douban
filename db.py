import datetime
import pymysql
from threading import Lock
import os

host = "127.0.0.1"
user = "root"
password = os.getenv("DB_PASSWORD")
database = "douban"

class Db:
    def __init__(self) -> None:
        # 连接数据库
        conn = pymysql.connect(host=host, user=user, password=password, db=database)
        self.conn = conn
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)
        self.lock = Lock()
        pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def test(self):
        sql = "show tables"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        print(res)

    # 一周榜单
    def saveRankWeek(self, args):
        self.lock.acquire()
        sql = f"INSERT INTO `s_rank_week` (`movie_name`) VALUES ('{args}')"
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.conn.commit()
        self.lock.release()

    def getRankWeek(self):
        self.lock.acquire()
        sql = 'SELECT * FROM s_rank_week limit 10'
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.lock.release()
        return result

    # 正在热映电影
    def saveHoting(self, args):
        self.lock.acquire()
        sql = f"INSERT INTO `s_hoting`(`id`,`title`,`rate`,`img`,`link`) values ('{args['id']}','{args['title']}','{args['rate']}','{args['img']}','{args['link']}')"
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.conn.commit()
        self.lock.release()

    def getHoting(self):
        self.lock.acquire()  # 修正拼写错误
        sql = 'SELECT * FROM s_hoting'
        self.conn.ping(reconnect=True)  # 修正拼写错误
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.lock.release()
        return results

    # 最近热门的电影
    def saveHotMovie(self, args):
        self.lock.acquire()
        # 添加status字段
        sql = f"INSERT INTO `s_hot_movie`(`id`,`title`,`rate`,`url`,`img`,`status`) values ('{args['id']}','{args['title']}','{args['rate']}','{args['url']}','{args['img']}',1)"
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.conn.commit()
        self.lock.release()

    def getHotMovie(self):
        self.lock.acquire()
        sql = 'SELECT * FROM s_hot_movie WHERE status=1'  # 添加空格
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()  # 修正变量名
        self.lock.release()
        return result  # 返回正确的变量

    # 最近热门电视剧
    def saveHotTV(self, args):
        self.lock.acquire()
        # 添加status字段
        sql = f"INSERT INTO `s_hot_movie`(`id`,`title`,`rate`,`url`,`img`,`status`) values ('{args['id']}','{args['title']}','{args['rate']}','{args['url']}','{args['img']}',2)"
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        self.conn.commit()
        self.lock.release()

    def getHotTV(self):
        self.lock.acquire()
        sql = 'SELECT * FROM s_hot_movie WHERE status=2'
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.lock.release()
        return results

#获取用户
    def createUser(self,username,password):
        self.lock.acquire()
        sql = f"SELECT * FROM `s_user` where username='{username}'"
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        fetchUser = self.cursor.fetchone()
        if not fetchUser:
            sql = f"insert into `s_user` (`username`, `password`) values ('{username}','{password}')"

            print(sql)

            self.cursor.execute(sql)
            self.conn.commit()
            self.lock.release()
            return "注册成功！"
        else:
            self.lock.release()
            return "注册失败，用户已经存在！"

    def getUser(self,user):
        self.lock.acquire()
        sql = f"SELECT * FROM `s_user` where username='{user}'"
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.lock.release()
        return result

doubanDB = Db()

# 本项目仅用于技术学习，  请勿用于生产环境或高频爬取
# > 使用前请配置数据库并设置环境变量：

# doubanDB.createUser("admin","123456")
#
# print(doubanDB.getUser("admin"))

# # 测试代码1
# doubanDB.saveHotMovie({
#     "id": "1",
#     "title": '仲夏夜的金梦-电影版',
#     "rate": '9.8',
#     "img": 'img/........',
#     "url": 'img...'
# })
#
# print(doubanDB.getHotMovie())
#
# doubanDB.saveHotTV({
#     "id": "2",
#     "title": '仲夏夜的金梦-电视剧版',
#     "rate": '9.8',
#     "img": 'img/........',
#     "url": 'img...'
# })

# print(doubanDB.getHotTV())
