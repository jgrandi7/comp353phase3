
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



engine = create_engine("postgresql+psycopg2://postgres:password@localhost/postgres")

class Base(DeclarativeBase):
    pass

##create institution class

class institution(Base):
    __tablename__ = "institution"
    
    institutionid: Mapped[int] = mapped_column(Integer, primary_key=True)
    institutionname: Mapped[str] = mapped_column(String(100))
    institutionaddress: Mapped[str] = mapped_column(String(200))

    customers: Mapped[List["schoolCustomer"]] = relationship(back_populates="institution", cascade="all, delete-orphan")
    employees: Mapped[List["schoolEmployee"]] = relationship(back_populates="institution", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"institution(institutionid={self.institutionid!r}, institutionname={self.institutionname!r}, institutionaddress={self.institutionaddress!r})"

##create schoolCustomer class

class schoolCustomer(Base):
    __tablename__ = "schoolCustomer"
    
    customerid: Mapped[int] = mapped_column(Integer, primary_key=True)
    customerlast: Mapped[str] = mapped_column(String(100))
    customerfirst: Mapped[str] = mapped_column(String(100))
    institutionid: Mapped[int] = mapped_column(Integer, ForeignKey("institution.institutionid"))

    institution: Mapped["institution"] = relationship(back_populates="customers")
    
    def __repr__(self) -> str:
        return f"schoolCustomer(customerid={self.customerid!r}, customerlast={self.customerlast!r}, customerfirst={self.customerfirst!r}, institutionid={self.institutionid!r})"

##create schoolEmployee class

class schoolEmployee(Base):
	__tablename__ = "schoolEmployee"

	employeeid: Mapped[int] = mapped_column(Integer, primary_key=True)
	employeelast: Mapped[str] = mapped_column(String(100))
	employeefirst: Mapped[str] = mapped_column(String(100))
	employeetitle: Mapped[str] = mapped_column(String(100))
	employeesalary: Mapped[int] = mapped_column(Integer, primary_key=True)
	institutionid: Mapped[int] = mapped_column(Integer, ForeignKey("institution.institutionid"))

	institution: Mapped["institution"] = relationship(back_populates="employees")

def __repr__(self) -> str:
    return f"schoolEmployee(employeeid={self.employeeid!r}, employeelast={self.employeelast!r}, employeefirst={self.employeefirst!r}, employeetitle={self.employeetitle!r},employeesalary={self.employeesalary!r},institutionid={self.institutionid!r})"


Base.metadata.create_all(engine)


##add data to institution class

session = Session(engine)

loyola = institution(
    institutionid=1870,
    institutionname="Loyola University Chicago",
    institutionaddress="1032 W Sheridan Rd, Chicago, IL 60660",
)
northwestern = institution(
    institutionid=1851,
    institutionname="Northwestern University",
    institutionaddress="633 Clark Street, Evanston, IL 60208",
)
uchicago = institution(
    institutionid=1890,
    institutionname="The University of Chicago",
    institutionaddress="5801 S Ellis Ave, Chicago, IL 60637",
)
uic = institution(
    institutionid=1982,
    institutionname="University of Illinois Chicago",
    institutionaddress="1200 W Harrison St, Chicago, IL 60607",
)

session.add_all([loyola, northwestern, uchicago, uic])
session.commit()

session.close()

##add data to schoolcustomer class

session = Session(engine)

jane = schoolCustomer(
    customerid = 12346,
    customerlast = "March",
    customerfirst = "Jane",
    institutionid = 1870,
)
patrick = schoolCustomer(
    customerid = 11450,
    customerlast = "Holcolmbe",
    customerfirst = "Patrick",
    institutionid = 1982,
)
richard = schoolCustomer(
    customerid = 11999,
    customerlast = "Williams",
    customerfirst = "Richard",
    institutionid = 1870,
)
cori = schoolCustomer(
    customerid = 11678,
    customerlast = "Masters",
    customerfirst = "Cori",
    institutionid = 1851,
)
megan = schoolCustomer(
    customerid = 10998,
    customerlast = "Gupta",
    customerfirst = "Megan",
    institutionid = 1890,
)
lola = schoolCustomer(
    customerid = 15673,
    customerlast = "Patrick",
    customerfirst = "Lola",
    institutionid = 1982,
)
carrie = schoolCustomer(
    customerid = 19333,
    customerlast = "Corall",
    customerfirst = "Carrie",
    institutionid = 1870,
)
matt = schoolCustomer(
    customerid = 12678,
    customerlast = "Tripp",
    customerfirst = "Matt",
    institutionid = 1870,
)

session.add_all([jane, patrick, richard, cori, megan, lola, carrie, matt])
session.commit()

session.close()

##add data to schoolEmployee class

session = Session(engine)

john = schoolEmployee(
    employeeid = 210,
    employeelast = "Wilson",
    employeefirst = "John",
    employeetitle = "Student Employee",
    employeesalary = 10000,
	institutionid = 1870
)

anna = schoolEmployee(
    employeeid = 243,
    employeelast = "George",
    employeefirst = "Anna",
    employeetitle = "Student Employee",
	employeesalary = 9000,
	institutionid = 1851
)

steve = schoolEmployee(
    employeeid = 145,
    employeelast = "Green",
    employeefirst = "Steve",
    employeetitle = "Student Employee",
	employeesalary = 9000,
	institutionid = 1890
)

dean = schoolEmployee(
    employeeid = 149,
    employeelast = "Preston",
    employeefirst = "Dean",
    employeetitle = "Student Employee",
	employeesalary = 9500,
	institutionid = 1851
)

mark = schoolEmployee(
    employeeid = 150,
    employeelast = "Rober",
    employeefirst = "Mark",
    employeetitle = "Student Employee",
	employeesalary = 9750,
	institutionid = 1982
)

neil = schoolEmployee(
    employeeid = 151,
    employeelast = "Tyson",
    employeefirst = "Neil",
    employeetitle = "Student Employee",
	employeesalary = 3000,
	institutionid = 1890
)

mattpage = schoolEmployee(
    employeeid = 142,
    employeelast = "Page",
    employeefirst = "Matt",
    employeetitle = "Student Employee",
	employeesalary = 2000,
	institutionid = 1982
)

angie = schoolEmployee(
    employeeid = 153,
    employeelast = "Blue",
    employeefirst = "Angie",
    employeetitle = "Student Employee",
	employeesalary = 15000,
	institutionid = 1870
)

session.add_all([john, anna, steve, dean, mark, neil, mattpage, angie])
session.commit()

session.close()


#allInstitutionNames query (Ella)

session = Session(engine)

all_institutions = session.query(institution.institutionname)

print("### Print All Institution Names ###")
for institution_name in all_institutions:
  print(f"Institution Name: {institution_name}")

session.close()


##loyolaCustomers query (Ella)

session = Session(engine)
loyola_customers = session.query(schoolCustomer).join(institution).where(institution.institutionname == "Loyola University Chicago")

print("\n### Print Only Loyola University Chicago Customers ###")
for customer in loyola_customers:
    print(f"Customer Name: {customer.customerfirst} {customer.customerlast}")

session.close()

##northwesternEmployeeSalary query (Jacob)


session = Session(engine)
northwestern_employees = session.query(schoolEmployee).join(institution).where(institution.institutionname == "Northwestern University")

print("\n### Print Salaries of Northwestern University Employees ###")
for employee in northwestern_employees:
    print(f"Employee Name: {employee.employeefirst} {employee.employeelast} (employee id: {employee.employeeid}) makes ${employee.employeeSalary}.")


