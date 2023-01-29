import pymongo

client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb=client['inmuebles_db']
info = mydb.table1
rec = [{
    "name":"jonny"
}]

info.insert_many(rec)
