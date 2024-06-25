import sys
from sqlmodel import Session, select
from app.core.database import engine
from app.models import users, posts

User = users.User


# Function to create a new session
def get_db():
    with Session(engine) as session:
        yield session


# Function to start IPython shell
def start_shell():
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(local=locals())


if __name__ == "__main__":
    session = next(get_db())
    # Expose variables to the shell
    variables = globals().copy()
    variables.update(locals())
    start_shell()
