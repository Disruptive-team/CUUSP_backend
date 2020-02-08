from flask import Flask
from playhouse.flask_utils import FlaskDB

from config import config
from .utils.jwt_util import FlaskJWT
from .utils.resp_code_util import BuiltInErrorHandler
from .utils.log_util import Logger

db_wrapper = FlaskDB()
jwt_wrapper = FlaskJWT()
built_in_error_handler = BuiltInErrorHandler()
log = Logger()

logger = log.logger
jwt_util = jwt_wrapper


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化插件
    db_wrapper.init_app(app)
    jwt_wrapper.init_app(app)
    built_in_error_handler.init_app(app)
    log.init_app(app)

    logger.debug("插件初始化完毕...")

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app
