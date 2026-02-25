from fpdf import FPDF
import streamlit as st
# start with creating classes using the OOP cncept
# Account Class
class Account:
    def __init__(self, name, account_type,balance=0):# have a defult value of balance as 0 to show the opening balance which can change anytime
         self.name = name 
         self.account_type = account_type
         self.balance = balance


    def debit (self, amount):
        if self.account_type in ["Asset","Expense"]:
            self.balance += amount # increases the balance or remains same if the amount is 0
        else:
            self. balance -= amount # # decreases the balance

    def credit (self, amount):
        if self.account_type in ["Liability","Equity","Revenue"]:
            self.balance += amount # increases the balance or remains same if the amount is 0
        else:
            self.balance -= amount # # decreases the balance or remains same if the amount is 0
              
    
            
            
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


# Accounts for Assets
    ledger.add_account(Account("Cash", "Asset"))
    ledger.add_account(Account("Accounts Receivable", "Asset"))
    ledger.add_account(Account("Inventory", "Asset"))
    ledger.add_account(Account("Office Equipment", "Asset"))
    # Accounts for Liabilities
    ledger.add_account(Account("Accounts Payable", "Liability"))
    ledger.add_account(Account("Loan Payable", "Liability"))
    ledger.add_account(Account("Accrued Expenses", "Liability"))
 # Accounts for Equity
    ledger.add_account(Account("Capital", "Equity"))
    # Accounts for Revenue
    ledger.add_account(Account("Sales Revenue", "Revenue"))
    # Accounts for Expenses
    ledger.add_account(Account("Rent Expense", "Expense"))
    ledger.add_account(Account("Salaries Expense", "Expense"))

    
    
    st.session_state.ledger = ledger  # acts as memory for the app while it is running

ledger = st.session_state.ledger

st.title("M LTD Automated Accounting System")

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

st.header("Income Statement") # Display main title in Streamlit
# Collect all Revenue accounts from the ledger and loop through all revenues
revenue_accounts = [
    account for account in ledger.accounts.values()
    if account.account_type == "Revenue"
]

# Collect all Expense accounts from the ledger and loop through all expenses
expense_accounts = [
    account for account in ledger.accounts.values()
    if account.account_type == "Expense"
]


st.subheader("Revenue") # create a subheader for revenue in the income statement

# We create a variable to accumulate (add up) total revenue
total_revenue = 0

# Loop through each revenue account
for account in revenue_accounts:
    
    # Display the account name and its balance
    st.write(f"{account.name}: {account.balance}")
    
    # Add that account's balance to total revenue
    total_revenue += account.balance

# After looping through all revenue accounts,
# display the total revenue
st.write(f"Total Revenue: {total_revenue}")


st.subheader("Expenses")

# Create a variable to accumulate total expenses
total_expenses = 0

# Loop through each expense account
for account in expense_accounts:
    
    # Display account name and balance
    st.write(f"{account.name}: {account.balance}")
    
    # Add the balance to total expenses
    total_expenses += account.balance

# After looping, display total expenses
st.write(f"Total Expenses: {total_expenses}")


# Net Income formula:
# Net Income = Revenue - Expenses
net_income = total_revenue - total_expenses

# Display Net Income clearly
st.subheader(f"Net Income: {net_income}")



# BALANCE SHEET

# Display the main title in Streamlit
st.header("Balance Sheet")

assets = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Asset")
liabilities = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Liability")
equity = sum(a.balance for a in ledger.accounts.values() if a.account_type == "Equity") + net_income

st.write(f"Assets: {assets}")
st.write(f"Liabilities: {liabilities}")
st.write(f"Equity: {equity}")
st.write(f"Assets = Liabilities + Equity → {assets == liabilities + equity}")

# ASSETS SECTION

st.subheader("Assets")  # Subheading for assets

# Collect all Asset accounts from the ledger
# We loop through all accounts and select only those with account_type "Asset"
asset_accounts = [a for a in ledger.accounts.values() if a.account_type == "Asset"]
# Initialize a variable to hold total assets
total_assets = 0
# Loop through each Asset account
for account in asset_accounts:
    # Display account name and its current balance
    st.write(f"{account.name}: {account.balance}")
    # Add this account's balance to total_assets
    total_assets += account.balance
# After looping, display total assets
st.write(f"Total Assets: {total_assets}")

# LIABILITIES

st.subheader("Liabilities")  # Subheading for liabilities

#Collect all Liability accounts
liability_accounts = [a for a in ledger.accounts.values() if a.account_type == "Liability"]

# Initialize a variable to hold total liabilities
total_liabilities = 0

# Loop through each Liability account
for account in liability_accounts:
    # Display account name and its current balance
    st.write(f"{account.name}: {account.balance}")
    # Add this account's balance to total_liabilities
    total_liabilities += account.balance
# After looping, display total liabilities
st.write(f"Total Liabilities: {total_liabilities}")
         
# EQUITY 
st.subheader("Equity")  # Subheading for equity

# Collect all Equity accounts
equity_accounts = [a for a in ledger.accounts.values() if a.account_type == "Equity"]
# Initialize total equity
total_equity = 0
# Loop through each Equity account
for account in equity_accounts:
    # Display account name and its balance
    st.write(f"{account.name}: {account.balance}")
    # Add this account's balance to total_equity
    total_equity += account.balance
# Add Net Income from Income Statement to Equity
# Net income increases owner's equity
total_equity += net_income

# Display total equity including net income
st.write(f"Total Equity (Including Net Income): {total_equity}")


# ACCOUNTING EQUATION 

st.subheader("Accounting Equation Check")

# Assets = Liabilities + Equity
st.write(f"Assets = Liabilities + Equity")

# Display the calculated totals
st.write(f"{total_assets} = {total_liabilities + total_equity}")

# Check if the equation balances (True/False)
st.write(f"Balanced: {total_assets == (total_liabilities + total_equity)}")

st.write(f"Assets: {total_assets}")
st.write(f"Liabilities: {total_liabilities}")
st.write(f"Equity: {total_equity}")
st.write(f"Assets = Liabilities + Equity - > {total_assets == total_liabilities + total_equity}")


# Function to generate PDF

def generate_pdf():

    pdf = FPDF()
    pdf.add_page()
    # Set font for main title: Arial, Bold, size 16
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "M LTD Financial Statements", ln=True, align="C")

     
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Income Statement", ln=True)

    pdf.set_font("Arial", "", 12)

    # Add Revenue, Expenses, and Net Income as text
    pdf.cell(0, 8, f"Total Revenue: {total_revenue}", ln=True)
    pdf.cell(0, 8, f"Total Expenses: {total_expenses}", ln=True)
    pdf.cell(0, 8, f"Net Income: {net_income}", ln=True)

    pdf.ln(5) # adding space

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Balance Sheet", ln=True)

    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 8, f"Total Assets: {total_assets}", ln=True)
    pdf.cell(0, 8, f"Total Liabilities: {total_liabilities}", ln=True)
    pdf.cell(0, 8, f"Total Equity: {total_equity}", ln=True)


    # Convert the PDF to bytes 
    # dest="S" → return the PDF as a string of bytes
    return bytes(pdf.output(dest="S")) 


# Download Button
pdf_data = generate_pdf()

st.download_button(
    label="Download Financial Statements as PDF",
    data=pdf_data,
    file_name="financial_statements.pdf",
    mime="application/pdf"
)
 
