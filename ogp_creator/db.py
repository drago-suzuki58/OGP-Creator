from sqlmodel import SQLModel, create_engine, Session
import os

import ogp_creator.env as env


engine = create_engine(env.DATABASE_URL, echo=True)

def init_db():
    if env.DATABASE_URL.startswith("sqlite:///"):
        db_path = env.DATABASE_URL.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
