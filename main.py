import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def ask():
  userName = input("Please Enter Your User Name: ")
  userAccount = db.collection("users").where(u'Name', u'==', userName)
  result = userAccount.get()

#The result is passed in as a list. This will return the first (and Only) user with that username
  if result:
    user = result[0]
    enterPassword(user, userName)
  else:
    newAccount = input("User Name does not exist. Would you like to create a new accout? (y/n)\n")
    if newAccount != 'y':
      print("Goodbye")
    else:
      newUser(userName)

def enterPassword(user, userName):
  password = input("Password: ")
  value = user.to_dict()
  if value["password"] != password:
    print("ACCESS DENIED: Please Try Again Later")
  else:
    print("Access Granted")
    grantedAccess(userName)

def printOptions():
  print("a. Add a Password")
  print("b. Find a Password")
  print("c. Edit a Password")
  print("d. Display List of All Passwords")
  print("e. Show Options")
  print("f. Quit\n")

def addPass(userName):
  print("\nPlease enter the Website and Password to add to your database: \n")
  website = input("Website: ")
  password = input("Password: ")
  value = {"website" : website, "password" : password}
  db.collection("users").document(userName).collection("passwords").document(website).set(value)

def findPass(userName):
  website = input("Website: ")
  result =  db.collection("users").document(userName).collection("passwords")
  document = result.get()
  if document:
    found = result.where("website", "==", website).get()
    if found:
      for elements in found:
        password = elements.to_dict()
        print(f"Password: " + password["password"])
    else:
      print("ERROR: Website Not Found")
  else:
    print("NO PASSWORDS SAVED")

def updatePass(userName):
  website = input("Website: ")
  result =  db.collection("users").document(userName).collection("passwords")
  document = result.get()
  if document:
    password = input("Enter new password: ")
    found = result.document(website).update({"password" : password})
    if found:
      print("Password updated Successfully")
    else:
      print("ERROR: Website Not Found")
  else:
    print("NO PASSWORDS SAVED")

def displayAll(userName):
  snapshot = db.collection("users").document(userName).collection("passwords").get()
  for x in snapshot:
    info = x.to_dict()
    print(f"Website: " + info["website"])
    print(f"Password:" + info["password"])
    print("")

def grantedAccess(userName):
  print("Choose from the Options Below:")
  printOptions()
  choice = ' '
  while choice != 'f':
    choice = input("> ")
    if choice == "a":
      addPass(userName)
    elif choice == "b":
      findPass(userName)
    elif choice == 'c':
      updatePass(userName)
    elif choice == 'd':
      displayAll(userName)
    elif choice == 'e':
      printOptions()
    elif choice == 'f':
      print("Goodbye!")
    else:
      print("Command Not Recognized\n Try Again:")

def newUser(userName):
  password = input("Enter a Password: ")
  values = {"Name" : userName, "password" : password}
  newUser = db.collection("users").document(userName)
  newUser.set(values)

def main():
  print("Password Manager v. 1.0\n")
  ask()



if __name__ == "__main__":
    main()