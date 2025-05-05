from database import engine
from models import Base
from parser import parse_swift

Base.metadata.create_all(bind=engine)

parse_swift("Interns_2025_SWIFT_CODES.csv")
