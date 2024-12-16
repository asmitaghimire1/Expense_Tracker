class Expense:
    
    def __init__(self,id,date,name,category,amount) -> None:
        self.id = id
        self.date = date
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):       
        return f"<Expense: {self.id}, {self.date}, {self.name}, {self.category}, {self.amount}>"
        