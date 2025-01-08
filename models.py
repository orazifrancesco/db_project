from sqlalchemy import Column, Integer, DateTime, Time, String
from database import Base

class Turno(Base):
    __tablename__ = 'hours_manager'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    orario_inizio = Column(Time, nullable=False)
    orario_fine = Column(Time, nullable=False)
    note = Column(String, nullable=True)

    def __repr__(self):
        return f"<Turno(id={self.id}, data={self.data}, orario_inizio={self.orario_inizio}, orario_fine={self.orario_fine}, note={self.note})>"
