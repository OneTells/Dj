class LoggerInfo:
    PATH = '/root/logs'
    FORMAT = "<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <y>{level}</> | <w>{extra[user_id]}</> | <c>{message}</>"


class DatabaseInfo:
    USER = 'gen_user'
    PASSWORD = "m!Q*eh0Jq!zD^Z"
    HOST = "82.97.254.168"
    NAME = 'default_db'
    PORT = 5432

    DSN = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
