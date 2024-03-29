from django.db import models
from accounts.models import UserBankAccount
from django_bank.constants import TRANSACTION_TYPE

# Create your models here.


class Transaction(models.Model):
    # one user can have many transactions. so i use ForeignKey. related_name is used to access transactions from user model. on_delete=models.CASCADE means if a user is deleted, all transactions of that user will also be deleted.
    account = models.ForeignKey(
        UserBankAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(
        max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approved = models.BooleanField(default=False)
    loan_repayment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.account_no} - {self.transaction_type} - {self.amount}"

    @property
    def css_classes(self):
        css_classes = {
            'Deposit': 'text-green-700 bg-green-100',
            'Receive': 'text-green-700 bg-green-100',
            'Withdraw': 'text-red-700 bg-red-100',
            'Transfer': 'text-red-700 bg-red-100',
            'Loan': 'text-green-700 bg-green-100' if self.loan_approved else 'text-yellow-700 bg-yellow-100',
            'Repayment': 'text-red-700 bg-red-100'
        }
        return css_classes.get(self.transaction_type, '')

    class Meta:
        ordering = ['-timestamp']
