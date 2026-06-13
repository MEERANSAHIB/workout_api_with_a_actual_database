from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL="sqlite:///./Databases.db"
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
Base=declarative_base()
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
