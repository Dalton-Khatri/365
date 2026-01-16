class BankAccount:
    def __init__(self,name, number,balance):
        self.name=name
        self.number=number
        self.balance=balance

    def deposit(self,amount):
        try: 
            if amount<0:
                raise ValueError("Money cant be in negative")
            else:
                self.balance+=amount
                print(f"Your new balance is {self.balance}\n")
        except ValueError as e:
            print(e)

    def withdraw(self,amount):
        try:
            if(self.balance<amount):
                raise ValueError("Not Enough Balance")
            elif(amount<0):
                raise ValueError("Money cant be in negative")
            else:
                self.balance-=amount
                print(f"Withdrawed {amount}, now your balance is {self.balance}")
        except ValueError as e:
            print(e)

    def check_balance(self):
        print(f"Balance of Account Number:{self.number} is {self.balance}\n")

    def info(self):
        print(f"Account Number:{self.number}\nAccount Holder:{self.name}\nBalance:{self.balance}")
    
# Create accounts
account1 = BankAccount("John Doe", "ACC001", 1000)
account2 = BankAccount("Jane Smith", "ACC002", 500)

# Test deposit
account1.deposit(500)  # Should work
account1.deposit(-100)  # Should reject

# Test withdraw
account1.withdraw(200)  # Should work
account1.withdraw(5000)  # Should reject (insufficient)

# Test balance
account1.check_balance()
account2.check_balance()

# Verify independence
# Changes to account1 don't affect account2


