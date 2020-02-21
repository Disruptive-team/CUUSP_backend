from .ret_util import RespStatus, response


class BuiltInErrorHandler():
    def __init__(self, app=None):
        self._app = app

    def init_app(self, app):
        if self._app is None:
            self._app = app
        self._init_error(self._app)

    def _init_error(self, app):
        @app.errorhandler(400)
        def forbidden(error):
            return response(*RespStatus.BadRequest.describe()), 400

        @app.errorhandler(403)
        def forbidden(error):
            return response(*RespStatus.Forbidden.describe()), 403

        @app.errorhandler(404)
        def page_not_found(error):
            return response(*RespStatus.NotFound.describe()), 404

        @app.errorhandler(405)
        def page_not_found(error):
            return response(*RespStatus.MethodNotAllowed.describe()), 405

        @app.errorhandler(500)
        def general_error(error):
            return response(*RespStatus.ServerError.describe()), 500

        @app.errorhandler(502)
        def gateway_error(error):
            return response(*RespStatus.GateWayError.describe()), 502
