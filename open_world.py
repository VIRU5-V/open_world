from app.app import create_app, db
from app.models import User, Post, Like, KeyWord

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post, Like=Like, KeyWord=KeyWord)


@app.cli.command('init')
def init():
    print('Initializing database')
    db.drop_all()
    db.create_all()
    u = User(name='virus', password='123')
    db.session.add(u)
    db.session.commit()
    print('Database created')