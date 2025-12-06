import dataclasses
import enum
from datetime import datetime, date
from typing import List, Optional

# Enums
class GenderEnum(enum.Enum):
    Nam = "Nam"
    Nu = "Nữ"

class PaymentStatusEnum(enum.Enum):
    Paid = "Paid"
    Unpaid = "Unpaid"

@dataclasses.dataclass
class UserDTO:
    id:int
    name:str
    phone: str
    email: str
    roles: List[str]

@dataclasses.dataclass
class UserCreateDTO:
    name:str
    phone:str
    email:str
    password:str

@dataclasses.dataclass
class StudentDTO:
    id:int
    name:str
    age:int
    formatted_dob:str
    gender: GenderEnum
    address:str
    entry_date: date

@dataclasses.dataclass
class StudentCreateDTO:
    name:str
    age:int
    gender: GenderEnum
    address:str
    parent_id:int

@dataclasses.dataclass
class TuitionDTO:
    id: int
    month: int
    year: int
    fee_base: float
    meal_fee: float
    extra_fee: float
    total: float
    payment_date: Optional[datetime]
    status: PaymentStatusEnum
    invoice_id: Optional[int]
    student_id: int

@dataclasses.dataclass
class InvoiceResponseDTO:
    id: int
    date_created: datetime
    amount: float
    content: str
    accountant_id: int
