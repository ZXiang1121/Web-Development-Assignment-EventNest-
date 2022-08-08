import shelve

db = shelve.open('storage.db', 'c')
db['Payments'] = {}
db.close()
