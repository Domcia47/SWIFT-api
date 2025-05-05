from app.database import engine
from app.models import Base
from app.parser import parse_swift

Base.metadata.create_all(bind=engine)

parse_swift("Interns_2025_SWIFT_CODES.csv")
