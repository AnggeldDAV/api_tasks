from db.database import Base,engine
from models.user import *
from models.task import *

Base.metadata.create_all(bind=engine())
print(f"Bases creadas correctamente")