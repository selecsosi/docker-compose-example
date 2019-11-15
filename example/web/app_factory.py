from flask import Flask


def create_app(logger_override=None):
    app = Flask("web")

    if logger_override:
        app.logger.handlers = logger_override.handlers
        app.logger.setLevel(logger_override.level)

    return app
