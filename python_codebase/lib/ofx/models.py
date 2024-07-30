# ofx_classes.py

import pandas as pd

class OFXFile:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'OFXFile(statements={self.statements})'


class Statement:
    def __init__(self, account, transactions):
        self.account = account
        self.transactions = transactions

    def __repr__(self):
        return f'Statement(account={self.account}, transactions={self.transactions})'

    def to_dataframes(self):
        banking_transactions = [txn for txn in self.transactions if not isinstance(txn, InvestmentTransaction)]
        investment_transactions = [txn for txn in self.transactions if isinstance(txn, InvestmentTransaction)]

        banking_df = pd.DataFrame([txn.__dict__ for txn in banking_transactions])
        investment_df = pd.DataFrame([txn.__dict__ for txn in investment_transactions])

        return banking_df, investment_df


class Account:
    def __init__(self, account_id, bank_id, account_type):
        self.account_id = account_id
        self.bank_id = bank_id
        self.account_type = account_type

    def __repr__(self):
        return f'Account(account_id={self.account_id}, bank_id={self.bank_id}, account_type={self.account_type})'


class Transaction:
    def __init__(self, date_posted, transaction_amount, fit_id, name, memo, transaction_type):
        self.date_posted = date_posted
        self.transaction_amount = transaction_amount
        self.fit_id = fit_id
        self.name = name
        self.memo = memo
        self.transaction_type = transaction_type

    def __repr__(self):
        return (f'Transaction(date_posted={self.date_posted}, transaction_amount={self.transaction_amount}, '
                f'fit_id={self.fit_id}, name={self.name}, memo={self.memo}, transaction_type={self.transaction_type})')


class InvestmentTransaction(Transaction):
    def __init__(self, date_posted, transaction_amount, fit_id, name, memo, transaction_type, security_id, units, unit_price, commission):
        super().__init__(date_posted, transaction_amount, fit_id, name, memo, transaction_type)
        self.security_id = security_id
        self.units = units
        self.unit_price = unit_price
        self.commission = commission

    def __repr__(self):
        return (f'InvestmentTransaction(date_posted={self.date_posted}, transaction_amount={self.transaction_amount}, '
                f'fit_id={self.fit_id}, name={self.name}, memo={self.memo}, transaction_type={self.transaction_type}, '
                f'security_id={self.security_id}, units={self.units}, unit_price={self.unit_price}, commission={self.commission})')


# Example of creating an OFX file object

if __name__ == '__main__':
    # Create some sample banking transactions
    banking_transaction1 = Transaction('2023-01-01', 100.00, '12345', 'Sample Banking Transaction 1', 'Sample memo 1', 'DEBIT')
    banking_transaction2 = Transaction('2023-01-02', -50.00, '12346', 'Sample Banking Transaction 2', 'Sample memo 2', 'CREDIT')
    banking_transaction3 = Transaction('2023-01-03', 75.00, '12347', 'Sample Banking Transaction 3', 'Sample memo 3', 'CHECK')

    # Create some sample investment transactions
    investment_transaction1 = InvestmentTransaction('2023-01-04', 5000.00, '12348', 'Sample Investment Transaction 1', 'Sample memo 4
