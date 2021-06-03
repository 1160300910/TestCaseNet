from flask_script import Manager,Command
from flask_script.commands import ShowUrls


from flaskr import create_app, DB
from config import config

# 初始化app
app = create_app('dev')

manager = Manager(app)
manager.add_command("showurls", ShowUrls())
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

