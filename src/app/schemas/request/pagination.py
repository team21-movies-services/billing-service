from pydantic import BaseModel, Field


class PaginationMixin(BaseModel):
    limit: int = Field(3, gt=0)
    page: int = Field(1, gt=0)

    @property
    def offset(self):
        return self.limit * (self.page - 1)


class PaymentsPagination(PaginationMixin):
    ...
