
import streamlit as st
from datetime import date

# -----------------------------------
# PERSONAL EXPENSE TRACKER
# -----------------------------------

st.title("Personal Expense Tracker")

# Categories
categories = ["Food", "Travel", "Shopping", "Bills", "Other"]

# Session state to store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# -----------------------------------
# FUNCTIONS
# -----------------------------------

def add_expense(name, amount, category, expense_date):
    expense = {
        "id": st.session_state.next_id,
        "name": name,
        "amount": amount,
        "category": category,
        "date": expense_date
    }

    st.session_state.expenses.append(expense)
    st.session_state.next_id += 1


def delete_expense(expense_id):
    for expense in st.session_state.expenses:
        if expense["id"] == expense_id:
            st.session_state.expenses.remove(expense)
            return True
    return False


def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total


def get_highest_expense(expenses):
    if len(expenses) == 0:
        return None

    highest = expenses[0]

    for expense in expenses:
        if expense["amount"] > highest["amount"]:
            highest = expense

    return highest


def category_totals(expenses):
    totals = {}

    for category in categories:
        totals[category] = 0

    for expense in expenses:
        totals[expense["category"]] += expense["amount"]

    return totals


def filter_expenses(expenses, search, category, amount_range):
    filtered = []

    for expense in expenses:
        name_match = search.lower() in expense["name"].lower()

        category_match = (
            category == "All" or expense["category"] == category
        )

        amount_match = (
            amount_range[0] <= expense["amount"] <= amount_range[1]
        )

        if name_match and category_match and amount_match:
            filtered.append(expense)

    return filtered


# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("Search & Filters")

search_text = st.sidebar.text_input(
    "Search Expense by Name"
)

selected_category = st.sidebar.selectbox(
    "Filter by Category",
    ["All"] + categories
)

# Calculate maximum amount for slider
max_amount = 1000.0

for expense in st.session_state.expenses:
    if expense["amount"] > max_amount:
        max_amount = expense["amount"]

max_amount = float(int(max_amount) + 1)

amount_range = st.sidebar.slider(
    "Filter by Amount",
    min_value=0.0,
    max_value=max_amount,
    value=(0.0, max_amount)
)


# -----------------------------------
# TASK 1: ADD EXPENSE
# -----------------------------------

st.header("Add New Expense")

with st.form("expense_form"):

    expense_name = st.text_input("Expense Name")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0
    )

    category = st.selectbox(
        "Category",
        categories
    )

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:

        if expense_name.strip() == "":
            st.error("Please enter an expense name.")

        elif amount <= 0:
            st.error("Amount must be greater than zero.")

        else:
            add_expense(
                expense_name.strip(),
                amount,
                category,
                expense_date
            )

            st.success("Expense added successfully!")


# -----------------------------------
# TASK 2: DASHBOARD SUMMARY
# -----------------------------------

st.header("Dashboard Summary")

all_expenses = st.session_state.expenses

total_spending = calculate_total(all_expenses)
total_transactions = len(all_expenses)
highest_expense = get_highest_expense(all_expenses)

if highest_expense is None:
    highest_amount = 0
else:
    highest_amount = highest_expense["amount"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Expenses",
        f"Rs. {total_spending:,.2f}"
    )

with col2:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col3:
    st.metric(
        "Highest Expense",
        f"Rs. {highest_amount:,.2f}"
    )


# -----------------------------------
# TASK 3 & 4: RECORDS AND FILTERS
# -----------------------------------

st.header("Expense Records")

filtered_expenses = filter_expenses(
    all_expenses,
    search_text,
    selected_category,
    amount_range
)

if len(all_expenses) == 0:
    st.warning("No expenses available. Add your first expense.")

elif len(filtered_expenses) == 0:
    st.warning("No expenses match your search or filters.")

else:
    table_data = []

    for expense in filtered_expenses:
        table_data.append({
            "Expense Name": expense["name"],
            "Amount": expense["amount"],
            "Category": expense["category"],
            "Date": str(expense["date"])
        })

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------
# TASK 5: DELETE EXPENSE
# -----------------------------------

st.header("Delete Expense")

if len(filtered_expenses) == 0:
    st.warning("No expenses available to delete.")

else:
    for expense in filtered_expenses:

        st.subheader(
            f"{expense['name']} - Rs. {expense['amount']:,.2f}"
        )

        st.write(
            f"Category: {expense['category']} | "
            f"Date: {expense['date']}"
        )

        if st.button(
            "Delete",
            key=f"delete_{expense['id']}"
        ):
            if delete_expense(expense["id"]):
                st.success("Expense deleted successfully!")
                st.rerun()
            else:
                st.error("Unable to delete expense.")


# -----------------------------------
# TASK 6: ADDITIONAL FEATURES
# -----------------------------------

st.header("Additional Features")

st.subheader("Highest Expense Details")

if highest_expense is None:
    st.warning("No highest expense available.")

else:
    st.write(
        f"Expense Name: {highest_expense['name']}"
    )

    st.write(
        f"Amount: Rs. {highest_expense['amount']:,.2f}"
    )

    st.write(
        f"Category: {highest_expense['category']}"
    )

    st.write(
        f"Date: {highest_expense['date']}"
    )


# Category-wise summary
st.subheader("Category-wise Total Expenses")

totals = category_totals(all_expenses)

if len(all_expenses) == 0:
    st.warning("No category expenses available.")

else:
    summary_data = []

    for category in categories:
        summary_data.append({
            "Category": category,
            "Total Amount": totals[category]
        })

    st.dataframe(
        summary_data,
        use_container_width=True,
        hide_index=True
    )


# Total transactions
st.subheader("Transaction Count")

st.metric(
    "Total Number of Transactions",
    len(all_expenses)
)
