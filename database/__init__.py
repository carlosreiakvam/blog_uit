# https://flask.palletsprojects.com/en/1.1.x/extensiondevy/
from flask import _app_ctx_stack, current_app
from mysql.connector import MySQLConnection, connect, Error
from mysql.connector.cursor import MySQLCursor


class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def connect(self):
        try:
            return connect(
                host=current_app.config['DATABASE_HOST'],
                user=current_app.config['DATABASE_USER'],
                password=current_app.config['DATABASE_PASSWORD'],
                database=current_app.config['DATABASE_NAME']
            )
        except Error as e:
            print(e)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'mysql_db'):
            ctx.mysql_db.close()

    @property
    def connection(self) -> MySQLConnection:
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db'):
                ctx.mysql_db = self.connect()
            return ctx.mysql_db

    @property
    def cursor(self) -> MySQLCursor:
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db_cursor'):
                ctx.mysql_db_cursor = self.connection.cursor(prepared=True)
            return ctx.mysql_db_cursor
