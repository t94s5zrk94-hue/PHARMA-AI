from modules.database import PharmaDatabase

db = PharmaDatabase()

medicine = db.get_complete_medicine("Dolo 650")

print(medicine)