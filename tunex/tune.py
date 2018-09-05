from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['dbUsersData']
collection = db['usersData']

cursor = collection.find({"userInfo.username" : "Walki"})
for row in cursor:
    print row["userInfo"]["username"]
