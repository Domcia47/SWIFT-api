from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class SwiftCode(Base):
    __tablename__ = "swift_codes"

    swiftCode = Column(String, primary_key=True, index=True)
    address = Column(String)
    bankName = Column(String)
    countryISO2 = Column(String)
    countryName = Column(String)


    headquarter_bic = Column(String, ForeignKey("swift_codes.swiftCode"), nullable=True)

    headquarter = relationship("SwiftCode", remote_side=[swiftCode], back_populates="branches")

    branches = relationship("SwiftCode", back_populates="headquarter")


    @property
    def isHeadquarter(self):
        return self.headquarter_bic is None
