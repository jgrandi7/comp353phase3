import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, DateTime, Column, func
from sqlalchemy.orm import relationship, declarative_base, Session
from sqlalchemy import create_engine

# password must be replaced with your own
engine = create_engine("postgresql+psycopg2://postgres:##password##@localhost/postgres")

Base = declarative_base()



class Institution(Base):
    __tablename__ = "institution"
    
    institutionid = Column(Integer, primary_key=True)
    institutionname = Column(String(100))
    institutionaddress = Column(String(200))

    customers = relationship("SchoolCustomer", back_populates="institution", cascade="all, delete-orphan")
    employees = relationship("SchoolEmployee", back_populates="institution", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Institution(institutionid={self.institutionid!r}, institutionname={self.institutionname!r}, institutionaddress={self.institutionaddress!r})"

class SchoolCustomer(Base):
    __tablename__ = "schoolcustomer"
    customerid = Column(Integer, primary_key=True)
    customerlast = Column(String(100))
    customerfirst = Column(String(100))
    
    institutionid = Column(Integer, ForeignKey("institution.institutionid"))
    institution = relationship("Institution", back_populates="customers")
    
    equipmentloans = relationship("EquipmentLoan", back_populates="schoolcustomer", cascade="all,delete-orphan")

    def __repr__(self) -> str:
        return f"SchoolCustomer(customerid={self.customerid!r}, customerlast={self.customerlast!r}, customerfirst={self.customerfirst!r}, institutionid={self.institutionid!r})"

class SchoolEmployee(Base):
    __tablename__ = "schoolemployee"

    employeeid = Column(Integer, primary_key=True)
    employeelast = Column(String(100))
    employeefirst = Column(String(100))
    employeetitle = Column(String(100))
    employeesalary = Column(Integer)
    
    institutionid = Column(Integer, ForeignKey("institution.institutionid"))
    institution = relationship("Institution", back_populates="employees")
	
    equipmentloans = relationship("EquipmentLoan", back_populates="schoolemployee", cascade="all,delete-orphan")
    
    def __repr__(self) -> str:
        return f"SchoolEmployee(employeeid={self.employeeid!r}, employeelast={self.employeelast!r}, employeefirst={self.employeefirst!r}, employeetitle={self.employeetitle!r}, employeesalary={self.employeesalary!r}, institutionid={self.institutionid!r})"

class EquipmentLoan(Base):
    __tablename__ = "equipmentloan"

    loanid = Column(Integer, primary_key=True)
    loantype = Column(String(100))
    loancheckouttime = Column(DateTime(timezone=True), server_default=func.now())
    loanreturntime = Column(DateTime(timezone=True), server_default=func.now())
    loannumber = Column(Integer)
	
    customerid = Column(Integer, ForeignKey("schoolcustomer.customerid"))
    schoolcustomer = relationship("SchoolCustomer", back_populates="equipmentloans")
    
    employeeid = Column(Integer, ForeignKey("schoolemployee.employeeid"))
    schoolemployee = relationship("SchoolEmployee", back_populates="equipmentloans")
    
    fines = relationship("Fine", back_populates="loan")
    
    def __repr__(self) -> str:
        return f"EquipmentLoan(loanid={self.loanid!r}, loantype={self.loantype!r}, loancheckouttime={self.loancheckouttime!r}, loanreturntime={self.loanreturntime!r}, loannumber={self.loannumber!r}, customerid={self.customerid!r}, employeeid={self.employeeid!r})"

class Fine(Base):
    __tablename__ = "fine"

    fineid = Column(Integer, primary_key=True)
    fineamount = Column(Integer)
    finepaymenttype = Column(String(100))
    loanid = Column(Integer, ForeignKey("equipmentloan.loanid"))
    
    loan = relationship("EquipmentLoan", back_populates="fines")
    
    def __repr__(self) -> str:
        return f"Fine(fineid={self.fineid!r}, fineamount={self.fineamount!r}, finepaymenttype={self.finepaymenttype!r}, loanid={self.loanid!r})"
    
    
    
    
Base.metadata.create_all(engine)

#allInstitutionNames query (Ella)

session = Session(engine)

all_institutions = session.query(Institution.institutionname)

print("### Print All Institution Names ###")
for institution_name in all_institutions:
  print(f"Institution Name: {institution_name}")

session.close()
    
##loyolaCustomers query (Ella)

session = Session(engine)
loyola_customers = session.query(SchoolCustomer).join(Institution).where(Institution.institutionid == "1870")

print("\n### Print Only Loyola University Chicago Customers ###")
for customer in loyola_customers:
    print(f"Customer Name: {customer.customerfirst} {customer.customerlast}")
    
##northwesternEmployeeSalary query (Jacob)

session = Session(engine)
northwestern_employees = session.query(SchoolEmployee).join(Institution).where(Institution.institutionid == "1851")

print("\n### Print Salaries of Northwestern University Employees ###")
for employee in northwestern_employees:
    print(f"Employee Name: {employee.employeefirst} {employee.employeelast} (employee id: {employee.employeeid}) makes ${employee.employeesalary}.")
    
##activeLoans query (Erin)

session = Session(engine)

activeLoans = session.query(EquipmentLoan).filter(EquipmentLoan.loanreturntime == None).all()

print("\n### Print All Active Loans ###")
for loan in activeLoans:
    print(f"Customer #{loan.customerid} checked out a {loan.loantype} on {loan.loancheckouttime} and has yet to return it.")

session.close()

    
# creditFinesAbove0 (Matthew)

session = Session(engine)
fines = session.query(Fine).where(Fine.finepaymenttype == "Credit Card").where(Fine.fineamount > 0)
print("\n### Print credit card fines above $0 ###")
for fine in fines:
    print(f"Fine id: {fine.fineid}, fine amount: {fine.fineamount}")

session.close()
