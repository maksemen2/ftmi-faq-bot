from infrastructure.database.models.base import Base, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column

class QuestionModel(Base, TimestampMixin):
    __tablename__ = "questions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)