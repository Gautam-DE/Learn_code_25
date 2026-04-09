from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT        = "DEPOSIT"
    WITHDRAWAL     = "WITHDRAWAL"
    INTEREST       = "INTEREST"
    TRANSFER_IN    = "TRANSFER_IN"
    TRANSFER_OUT   = "TRANSFER_OUT"
    LOAN_REPAYMENT = "LOAN_REPAYMENT"


class LoanStatus(str, Enum):
    ACTIVE    = "ACTIVE"
    REPAID    = "REPAID"
    DEFAULTED = "DEFAULTED"
