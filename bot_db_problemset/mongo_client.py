from unittest import result
import pymongo


class ExpenseMongoClient:
    def __init__(
        self,
        host: str,
        port: int,
        db_name: str = "telegram_bot",
        collection_name: str = "expenses",
    ):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def add_expense(self, user_id: int, amount: int, category: str, description: str):
        user = {
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "description": description,
        }
        self.collection.insert_one(user)

    def get_expenses(self, user_id: int) -> list:
        result = self.collection.find({"user_id": user_id})
        res = []
        for doc in result:
            res.append(
                {
                    "amount": doc["amount"],
                    "category": doc["category"],
                    "description": doc["description"],
                }
            )
        return res

    def get_categories(self, user_id: int) -> list:
        result = self.collection.distinct("category", {"user_id": user_id})
        return result

    def get_expenses_by_category(self, user_id: int, category: str) -> list:
        result = self.collection.find({"user_id": user_id, "category": category})
        res = []
        for doc in result:
            res.append(
                {
                    "amount": doc["amount"],
                    "category": doc["category"],
                    "description": doc["description"],
                }
            )
        return res

    def get_total_expense(self, user_id: int):
        result = self.collection.aggregate(
            [
                {"$match": {"user_id": user_id}},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
            ]
        )
        total = next(result, {}).get("total", 0)
        return total

    def get_total_expense_by_category(self, user_id: int):
        result = self.collection.aggregate(
            [
                {"$match": {"user_id": user_id}},
                {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
            ]
        )
        category_totals = {doc["_id"]: doc["total"] for doc in result}
        return category_totals


if __name__ == "__main__":
    expense_mongo_client = ExpenseMongoClient("localhost", 27017)
    expense_mongo_client.add_expense(123, 100, "غذا", "ناهار")
    expense_mongo_client.add_expense(123, 200, "غذا", "شام")
    expense_mongo_client.add_expense(123, 300, "سفر", "پرواز")
    expense_mongo_client.add_expense(321, 400, "غذا", "ناهار")
    expense_mongo_client.add_expense(321, 500, "سفر", "پرواز")

    print("Expenses of 123")
    print(expense_mongo_client.get_expenses(123))

    print("Categories of 123")
    print(expense_mongo_client.get_categories(123))

    print("Total expense of 321")
    print(expense_mongo_client.get_total_expense(321))

    print("Total expense by category of 321")
    print(expense_mongo_client.get_total_expense_by_category(321))

    print("Expenses by category of 123")
    print(expense_mongo_client.get_expenses_by_category(123, "غذا"))
