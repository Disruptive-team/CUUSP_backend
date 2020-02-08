import os

from dotenv import load_dotenv

# 加载环境文件
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('FLASK_COVERAGE') == "True":
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click
from app import create_app
from app.models import Student, WechatBind, MicroService

app = create_app(os.getenv("FLASK_ENV") or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(Student=Student, WechatBind=WechatBind, MicroService=MicroService)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """运行单元测试."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = 'True'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests', pattern="test*.py")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@app.cli.command()
def fake():
    """
    产生数据库虚拟数据
    """
    from fake import student, wechat_bind, micro_service

    # 清除以前的数据
    Student.delete().execute()
    WechatBind.delete().execute()
    MicroService.delete().execute()

    WechatBind.insert_many(wechat_bind).execute()
    Student.insert_many(student).execute()
    MicroService.insert_many(micro_service).execute()


