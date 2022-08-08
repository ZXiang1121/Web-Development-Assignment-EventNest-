import shelve


db = shelve.open('storage.db', 'c')
db['Questions'] = {}
db.close()