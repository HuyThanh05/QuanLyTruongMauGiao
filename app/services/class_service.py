from typing import List
from app.models.Models import Classroom

def get_all_class() -> List[Classroom]:
    return Classroom.query.all()

