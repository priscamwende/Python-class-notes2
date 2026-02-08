## Python-class-notes2
**TITLE : Creating An Automated Accounting System**

**PROBLEM STATEMENT**
Many small businesses and individuals find it difficult to accurately record financial transactions and prepare financial statements because accounting rules can be complex and manual bookkeeping takes a lot of time. Doing records by hand often leads to mistakes, makes it hard to track account balances as transactions occur, and delays the preparation of reliable financial reports. For this reason, there is a need for a simple automated accounting system that can properly record transactions, apply double-entry accounting principles, keep ledger balances up to date, and generate standard financial statements.

**PROJECT DESCRIPTION**
The project will involve developing an automated accounting sysytem using  Python with Object-Oriented Programming (OOP) as the backend and Streamlit as the frontend interface.
  
The system will include:

### Recording Financial Transactions

The user will input financial transactions such as cash receipts, expenses, bill payments, and sales. Each transaction will be recorded in a journal, clearly identifying:

1. The type of transaction
2. The accounts affected
3. The amount involved
4. Whether each account is debited or credited

#### NOTE: Accounting principles to take note of 
1. Assets and Expenses accounts increses with debit and decrease with credit.
2. Liabilities, Equity and Revenues increases with credit and decreases with debit

### Posting Transactions to Ledger Accounts
All journal entries will be posted to their respective ledger accounts. Each ledger account will maintain a running balance, allowing users to view up-to-date account positions at any time.

### Generating Financial Statements
Once transactions are properly recorded and posted, the system will summarize the financial data to generate:

1. Income Statement (Profit and Loss Statement)
2. Balance Sheet (Statement of Financial Position)

### The How

Use OOP as the backend that is create the classes first then define the methods so as to update any transactions

My classes will be :
* class Account showing (name, account type)
* class Journal showing all transactions
* class Ledger that will be updating the accounts based on the journal entries


### The Frontend 
The system will use Streamlit as the user interface, enabling users to:
1. Input and submit transactions
2. View journal entries
3. Display ledger accounts and balances
4. Generate and view financial statements interactively
