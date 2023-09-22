from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, mapped_column

Column = mapped_column

metadata = MetaData()

BaseModel = declarative_base(metadata=metadata)


class RestrictForeignKey(ForeignKey):
    def __init__(self, column, **dialect_kw):
        super().__init__(column, ondelete='RESTRICT', onupdate='RESTRICT', **dialect_kw)
