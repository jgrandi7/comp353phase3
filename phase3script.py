from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select



engine = create_engine("postgresql+psycopg2://postgres:power2postgres@localhost/postgres")

class Base(DeclarativeBase):
    pass

##create institution class

class institution(Base):
    __tablename__ = "institution"
    
    institutionid: Mapped[int] = mapped_column(Integer, primary_key=True)
    institutionname: Mapped[str] = mapped_column(String(100))
    institutionaddress: Mapped[str] = mapped_column(String(200))

    customers: Mapped[List["schoolcustomer"]] = relationship(back_populates="institution", cascade="all, delete-orphan")
    employees: Mapped[List["schoolemployee"]] = relationship(back_populates="institution", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"institution(institutionid={self.institutionid!r}, institutionname={self.institutionname!r}, institutionaddress={self.institutionaddress!r})"

##create schoolcustomer class

class schoolcustomer(Base):
    __tablename__ = "schoolcustomer"
    
    customerid: Mapped[int] = mapped_column(Integer, primary_key=True)
    customerlast: Mapped[str] = mapped_column(String(100))
    customerfirst: Mapped[str] = mapped_column(String(100))
    institutionid: Mapped[int] = mapped_column(Integer, ForeignKey("institution.institutionid"))

    institution: Mapped["institution"] = relationship(back_populates="customers")
    
    def __repr__(self) -> str:
        return f"schoolcustomer(customerid={self.customerid!r}, customerlast={self.customerlast!r}, customerfirst={self.customerfirst!r}, institutionid={self.institutionid!r})"

##create schoolEmployee class

class schoolemployee(Base):
	__tablename__ = "schoolemployee"

	employeeid: Mapped[int] = mapped_column(Integer, primary_key=True)
	employeelast: Mapped[str] = mapped_column(String(100))
	employeefirst: Mapped[str] = mapped_column(String(100))
	employeetitle: Mapped[str] = mapped_column(String(100))
	employeesalary: Mapped[int] = mapped_column(Integer, primary_key=True)
	institutionid: Mapped[int] = mapped_column(Integer, ForeignKey("institution.institutionid"))

	institution: Mapped["institution"] = relationship(back_populates="employees")

def __repr__(self) -> str:
    return f"schoolemployee(employeeid={self.employeeid!r}, employeelast={self.employeelast!r}, employeefirst={self.employeefirst!r}, employeetitle={self.employeetitle!r},employeesalary={self.employeesalary!r},institutionid={self.institutionid!r})"


Base.metadata.create_all(engine)


