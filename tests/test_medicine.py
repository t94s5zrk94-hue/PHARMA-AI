from modules.database import PharmaDatabase
from modules.medicine import Medicine

db = PharmaDatabase()

product = db.get_product()

medicine = Medicine(product.iloc[0])

print(medicine.card())