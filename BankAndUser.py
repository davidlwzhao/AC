# Banks are holders of user accounts, transactions, balance due to other banks

import random
from datetime import datetime
import mysql.connector


class Db:

    def __init__(self, host, user, passwd, database=None):
        kwargs = {
            "host": host,
            "user": user,
            "passwd": passwd
        }

        if database is not None:
            kwargs['database'] = database
            self.name = database
        else:
            self.name = 'All'

        self.handle = mysql.connector.connect(**kwargs)
        self.con = self.handle.cursor()

    def show(self):
        self.con.execute("SHOW TABLES")
        for table in self.con:
            print(table)

    def create(self, name, *args):
        # add additional validation (needs to be at least one column)
        flatargs = flatten(args)
        self.con.execute(f"CREATE TABLE {name} {flatargs}")

    def drop(self, name):
        query = f"DROP TABLE {name}"
        try:
            self.con.execute(query)
        except mysql.connector.errors.ProgrammingError:
            print(f"Table does not exist in {self.name}")


Database = Db('localhost', 'root', '', database='Python')
Database.show()
Database.drop('tom')


class Bank:

    num_inst = 0

    def __init__(self, name=None, accounts=None):
        # assignment
        self.name = name
        if accounts is not None:
            self.accounts = accounts
        else:
            self.accounts = []

        # increase the counter of bank instances
        self.iter_counter()  # self.__class__.num_inst += 1

    def __repr__(self):
        return f"Bank({self.name}, {self.accounts})"

    def __str__(self):
        return f"{self.name}: {len(self.accounts)} accounts"

    def __getattr__(self, item):  # called when there isn't an explicit attribute
        raise AttributeError(f"{item} is not an attribute of the Bank Class")

    # def __setattr__(self, key, value):  # this is called every time an attribute is set!!
    #     print('called', key)
    #     if key == "n_accs":
    #         raise AttributeError(f"n_accs cannot be set")

    @property
    def n_accs(self):
        return len(self.accounts)

    def add_accs(self, *args):
        for arg in args:
            self.accounts.append(arg)

    @classmethod
    def iter_counter(cls):
        cls.num_inst += 1


class Account:

    def __init__(self, name, address, birthday, bank,
                 joindate=None, trans=None):
        self.balance = 0
        self.name = name
        self.address = address
        self.birthday = birthday
        self.bank = bank
        self.joindate = joindate
        if trans is not None:
            self.trans = trans
        else:
            self.trans = []
        self.updateBalance()

    def __str__(self):
        return f"{self.name}'s Account: ${self.balance}"

    def __repr__(self):
        return f"Account({self.name},{self.address},{self.birthday}," \
               f"{self.bank}.{self.joindate},{self.balance}, {self.trans})"

    def add_trans(self, *args):
        for arg in args:
            self.trans.append(arg)
        self.updateBalance()

    def updateBalance(self):
        self.balance += sum(self.trans)  # needs to account for debits


class Trans:

    def __init__(self, debitBank, creditBank, amount):
        self.id = self.generateID(debitBank, creditBank)
        self.amount = amount
        self.debitBank = debitBank
        self.creditBank = creditBank

    def __str__(self):
        return f"From {self.debitBank} to {self.creditBank}: {self.amount}"

    def __add__(self, other):
        try:
            return self.amount + other.amount
        except AttributeError:
            if isinstance(other, (int, float)):
                return self.amount + other

    def __iadd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    @staticmethod
    def generateID(debitBank, creditBank):
        return 110001010


class FactoryTrans:

    @staticmethod
    def create(bank, n, limit=1000000):
        trans = []
        for i in range(n):
            if random.randint(0, 1):
                debitBank = bank
                creditBank = 'other bank'
            else:
                creditBank = bank
                debitBank = 'other bank'
            trans.append(Trans(debitBank, creditBank, random.randint(0, limit)))
        return trans

    @staticmethod
    def append_to_user(user, n, limit=1000000):
        pass

    def generate(self, bank, n):
        pass


alltrans = FactoryTrans.create('HSBC', 20)
for trans in alltrans:
    pass
    #print(trans)
#print(sum(alltrans))

bank1 = Bank('HSBC')
bank2 = Bank('JP Morgan')

list1 = [100, 2100, 20002, 30303]
bank1.add_accs(*list1)

print(repr(bank1))
print(bank1)
print(bank1.n_accs)


t1 = Trans('HSBC', 'JP Morgan', 10000)
t2 = Trans('JP Morgan', 'HSBC', 10000)

acc1 = Account('TestAcc1', 'address', 'birthday', 'HSBC', joindate=datetime.today(), trans=[t1, t2])
print(acc1.trans)
acc1.add_trans(*alltrans)
print(acc1.balance)

# this should really work by passing users rather than just passing raw data