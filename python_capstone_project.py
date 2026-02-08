import streamlit as st
## start with creating classes using the OOP concept

# Account class

class Account:
    def __init__ (self, name, account_type, balance=0): # have a defult value of balance as 0 to show the opening balance which can change anytime
        self.name = name
        self.account_type = account_type
        self.balance =  balance

    def debit (self, amount):
        if self.account_type in ["Asset","Expenses"]:
            self.balance += amount # increases the balance or remains same if the amount is 0
        else:
            self. balance -= amount # # decreases the balance

    def credit (self, amount):
        if self.account_type in ["Liabilitie","Equity","Revenue"]:
            self.balance += amount # increases the balance or remains same if the amount is 0
        else:
            self.balance -= amount # # decreases the 
            
            
# Journal class
class Journal:
    def __init__ (self):
        self.entries = [] # create an empty list of entries because journals start empty and transactions are added overtime

    def add_entry(self, date, description, debit_account, credit_account, amount): # define the parameters that youll use to create a d
        self.entries.append({
            "date": date,
            "description": description,
            "debit": debit_account,
            "credit": credit_account,
            "amount": amount
        })

# Ledger class
class Ledger:
    def __init__(self):
        self.accounts = {} # Create an empty dictionary to store all accounts
        self.journal = Journal()# Create a new Journal object to store all transaction records.
       
    def add_account(self, account): # adding an account
        self.accounts[account.name] = account

    def record_transaction(self, date, description, debit_account, credit_account, amount):
        self.journal.add_entry(date, description, debit_account, credit_account, amount)# first record the journals
        self.post_to_ledger(debit_account, credit_account, amount) # update the recorded transactions to show the account balances

    def post_to_ledger(self, debit_account, credit_account, amount):
        self.accounts[debit_account].debit(amount)
        self.accounts[credit_account].credit(amount)
   
    
# Initialize ledger and accounts

if "ledger" not in st.session_state: # an in bult dictionary that keeps values in memory while the app is open.
    ledger = Ledger() # starting as empty but add the initial accounts to the ledger.
    ledger.add_account(Account("Cash", "Asset"))
    ledger.add_account(Account("Capital", "Equity"))
    ledger.add_account(Account("Revenue", "Revenue"))
    ledger.add_account(Account("Rent Expense", "Expense"))
    st.session_state.ledger = ledger

ledger = st.session_state.ledger

st.title("Automated Accounting System")

st.header("Record Transaction")

date = st.date_input("Date") # Let the user select the date of the transaction using a calendar picker
description = st.text_input("Description")
debit_account = st.selectbox("Debit Account", ledger.accounts.keys()) # Let the user choose which account to debit from a drop-down list
credit_account = st.selectbox("Credit Account", ledger.accounts.keys()) # Let the user choose which account to debit from a drop-down list
amount = st.number_input("Amount", min_value=0.0, step=1.0)

if st.button("Record Transaction"):
    if debit_account == credit_account:
        st.error("Debit and Credit accounts cannot be the same.")
    elif amount <= 0:
        st.error("Amount must be greater than zero.")
    else:
        ledger.record_transaction(
            str(date), # Convert date to string for ledger entry
            description,
            debit_account,
            credit_account,
            amount
        )
        st.success("Transaction recorded successfully!")

# get to show the journal

st.header("Journal Entries")
st.table(ledger.journal.entries)

# Show Ledger Balances
st.header("Ledger Balances")
ledger_data = []
for acc in ledger.accounts.values():
    ledger_data.append({
        "Account": acc.name,
        "Type": acc.account_type,
        "Balance": acc.balance
    })
st.table(ledger_data)

# Financial Statements

st.header("Income Statement")
revenue = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Revenue")
expenses = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Expense")
net_income = revenue - expenses

st.write(f"Total Revenue: {revenue}")
st.write(f"Total Expenses: {expenses}")
st.write(f"Net Income: {net_income}")

st.header("Balance Sheet")
assets = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Asset")
liabilities = 0
equity = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Equity") + net_income

st.write(f"Assets: {assets}")
st.write(f"Liabilities: {liabilities}")
st.write(f"Equity: {equity}")
st.write(f"Assets = Liabilities + Equity → {assets == liabilities + equity}")