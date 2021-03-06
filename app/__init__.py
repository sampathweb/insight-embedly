#! ../env/bin/python
from flask import Flask, render_template, request, send_from_directory, g
from sqlalchemy import create_engine


def create_app(object_name, env, dbcon):
    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env
    app.config['SQLALCHEMY_DATABASE_URI'] = dbcon

    @app.errorhandler(500)
    def error_handler_500(e):
        if app.config['APP_SERVER'] != 'DEV':
            return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_handler_404(e):
        if app.config['APP_SERVER'] != 'DEV':
            return render_template('404.html'), 404

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    @app.before_request
    def before_request():
        g.app_server = app.config['APP_SERVER']
        if 'db_engine' not in 'g':
            g.db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # register our blueprints
    from app.blueprints import main
    app.register_blueprint(main)

    return app
