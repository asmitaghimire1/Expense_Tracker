from expense import Expense
from datetime import datetime
from datetime import date
import calendar
import os


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    while True:
        # Get user to input their expense
        expense = get_user_expense(expense_file_path)
        
        # Write their expense to a file
        save_expense_to_file(expense, expense_file_path)
        u_input = input("Do you want to enter another expense(Y/N)? ")
        if u_input.lower() == "y":
            pass
        elif u_input.lower() == "n":
            break
        else:
            print("Invalid option. Enter Again!")

    # Read file and summarize expenses
    summarize_expenses(expense_file_path,budget)

    # Delete expense according to the user entered expense id
    delete_expense(expense_file_path)

    # Get summary of a specific month
    monthly_summary()

def get_user_expense(expense_file_path,length=2):

    if not os.path.exists(expense_file_path):  # File does not exist
        expense_id = 1
    elif os.path.getsize(expense_file_path) == 0:  # File exists but is empty
        expense_id = 1
    else:  # File exists and is not empty
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                expensee_id, expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")
                expense_id = int(expensee_id) + 1   

    expense_date = date.today()
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍔 Food" , 
        "🏘️ Home" , 
        "🏢 Work" , 
        "🎉 Fun" , 
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)} ]"
        
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category=expense_categories[selected_index]
            new_expense = Expense(id=expense_id, date=expense_date,name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid Category. Please try again!")
        
def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path,"a",encoding="utf-8") as f:
        f.write(f"{expense.id},{expense.date},{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_id, expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                id = expense_id , date = expense_date , name = expense_name , amount = float(expense_amount) , category = expense_category                
            )
            print(line_expense)
            expenses.append(line_expense)

    amount_by_category = {}   
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("📃 Expenses by Category:")
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💸 Total Spent: ${total_spent:.2f} this month!")

    remaining_budget = budget - total_spent
    if remaining_budget > 0:
        print(f"✅ Budget Remaining: ${remaining_budget:.2f} this month!")
        today = datetime.today()
        _, days_in_month = calendar.monthrange(today.year, today.month)
        remaining_days = days_in_month - today.day
        print("Remaining days in the current month:", remaining_days)    

        daily_budget = remaining_budget / remaining_days
        print(f"👉 Budget Per Day: ${daily_budget:.2f}")

    else:
        print(f"✅ Budget Remaining: $0 this month!")  

def delete_expense(expense_file_path):
    count1 = 0
    count2 = 0
    while True:
        user_input = input("Delete any expense (Y/N)?")
        if user_input.lower() == "y":
            while True:
                id_to_be_deleted = input("Enter Expense id to be deleted: ")
                expenses = []
                with open(expense_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        count1 += 1
                        expense_id, expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")
                        if expense_id != id_to_be_deleted:
                            expenses.append(line)
                            count2 += 1
                if count1 != count2:
                    # opening in writing mode
                    with open('expenses.csv', 'w' , encoding="utf-8") as fw:
                        fw.writelines(expenses)
                                        
                    print("Deleted Successfully.")
                    break
                else:
                    print("Invalid Id. Please Try Again!")    
                      
        elif user_input.lower() == "n":
            exit
            break

        else:
            print("Invalid option. Enter again!")
                   
def monthly_summary():
    data=[]
    while True:
        user_input = input("Do you want a monthly summary of your expenses(Y/N)?") 
        if user_input.lower() == "y":
            req_month = input("Select a month[1-12]: ")
            try:
                if 1 <= int(req_month) <= 12:
                    with open("expenses.csv","r",encoding = "utf - 8") as f:
                        lines = f.readlines()
                        for line in lines:
                            expense_id, expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")
                            year,month,day = expense_date.strip().split("-")
                            if req_month == month:
                                data.append(line)
                    if not data :            
                        print("There are no expenses in that particular month.")
                        break
                    else:
                        for value in data:            
                            print(value)            
                        break   
            except:
                print("Invalid option. Please enter the month within the range[1-12]!")
                break    
                    

                
        elif user_input.lower() == "n":
            break
        else:
            print("Invalid option. Enter Again!") 

if __name__=="__main__":
    main()