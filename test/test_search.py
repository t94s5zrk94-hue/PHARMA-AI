from modules.search import search_medicine

query = input("Search Medicine : ")

result, result_type = search_medicine(query)

if result is None:

    print("\n❌ No Record Found")

else:

    print("\n=============================")
    print("Search Type :", result_type)
    print("=============================\n")

    print(result)