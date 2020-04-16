import pymysql
from pymysql.cursors import DictCursor


class DBHandler(object):
    """
    初始化数据库
    """
    # 也可以继承 Connection 这里没有选择继承
    def __init__(self,
                 host=None,  # 连接名
                 port=3306,  # 端口
                 user=None,  # 用户名
                 password=None,  # 密码
                 charset=None,  # 不能写utf-8 在MySQL里面写utf-8会报错
                 database=None,  # 数据库库名
                 cursorclass=DictCursor,
                 **kwargs):
        self.connect = pymysql.connect(
            host=host,  # 连接名
            port=port,  # 端口
            user=user,  # 用户名
            password=password,  # 密码
            charset=charset,  # 不能写utf-8 在MySQL里面写utf-8会报错
            database=database,  # 数据库库名
            cursorclass=cursorclass,  # 数据转换成字典格式
            **kwargs
        )
        # 创建游标对象  **主要**
        self.cursor = self.connect.cursor()

    def query_one(self, query, args=None):
        """
        查询数据库一条数据
        :param query: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        """
        self.cursor.execute(query, args)
        # 将更改提交到数据库
        self.connect.commit()
        return self.cursor.fetchone()

    def query_all(self, query, args=None):
        """
        查询数据库所有数据
        :param query: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        """
        self.cursor.execute(query, args)
        # 将更改提交到数据库
        self.connect.commit()
        return self.cursor.fetchall()

    def query(self, query, args=None, one=True):
        """
        主体查询数据
        :param query: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        :param one: one是True 时候执行query_one, 否则执行query_all
        """
        if one:
            return self.query_one(query, args)
        return self.query_all(query, args)

    def close(self):
        """
        关闭
        :return:
        """
        # 关闭游标
        self.cursor.close()
        # 断开数据库连接
        self.connect.close()


if __name__ == '__main__':
    db = DBHandler(
        host='127.0.0.1',  # 连接名
        port=3306,  # 端口
        user='root',  # 用户名
        password='root',  # 密码
        charset='utf8',  # 不能写utf-8 在MySQL里面写utf-8会报错
        database='pymysql_test'  # 数据库库名
    )
    # 查询语句
    sql = 'select * from authors'
    sql1 = "select * from authors where authorId = %s;"
    print(db.query(sql, one=False))
    print(db.query(query=sql1, args=[1]))
　　# 关闭连接
　　db.close()