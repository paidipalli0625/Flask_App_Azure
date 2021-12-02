db=[]
di = {'username':'admin',
      'password':'password',
      'firstname':'admin',
      'lastname':'admin',
      'email':'admin@gmail.com'}
db.append(di)


def addRec(di):
	db.append(di)

def validate(username,password):
   print(db)
   for di in db:
   	if (di['username'] == username and di['password']== password):
     		return di
   return False

