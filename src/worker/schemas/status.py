from enum import StrEnum


class StatusEnum(StrEnum):
    created = "created"
    pending = "pending"
    succeeded = "succeeded"
    canceled = "canceled"
    failed = "failed"
