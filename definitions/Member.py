from definitions import SharkErrors, Item
import json

class Member():
    
    def __init__(self, member_data):
        
        self.id = member_data["id"]
        self.balance = member_data["balance"]
        self.inventory = member_data["inventory"]
        self.collection = member_data["collection"]
        self.linked_account = member_data["email"]

    def write_data(self):
        member_data = {}
        member_data["id"] = self.id
        member_data["balance"] = self.balance
        member_data["inventory"] = self.inventory
        member_data["collection"] = self.collection
        member_data["email"] = self.linked_account

        update_json_file(self.id, member_data)

    def add_to_inventory(self, item):
        if item.id not in self.collection:
            self.add_to_collection(item)
        self.inventory.append(item.id)
        self.write_data()

    def add_to_collection(self, item):
        if item.id not in self.collection:
            self.collection.append(item.id)
        self.write_data()

    def remove_from_inventory(self, item):
        if item.id not in self.inventory:
            raise SharkErrors.ItemNotInInventoryError
        self.inventory.remove(item.id)
        self.write_data()

    def get_balance(self):
        return self.balance

    def add_balance(self, amount):
        self.balance += amount
        self.write_data()

    def set_balance(self, amount):
        self.balance = amount
        self.write_data()

    def link_account(self, account):
        account = account.lower()
        if self.linked_account != None:
            raise SharkErrors.AccountAlreadyLinkedError
        
        usedAccounts = get_used_accounts()
        if account in usedAccounts:
            raise SharkErrors.AccountAlreadyInUseError

        usedAccounts.append(account)
        write_used_accounts(usedAccounts)
        
        self.linked_account = account
        self.write_data()

    def unlink_account(self):
        if self.linked_account == None:
            raise SharkErrors.AccountNotLinkedError
        
        usedAccounts = get_used_accounts()
        usedAccounts.remove(self.linked_account)
        write_used_accounts(usedAccounts)

        self.linked_account = None
        self.write_data()

    def __del__(self):
        pass
        ##self.write_data()




class BlankMember(Member):
    
    def __init__(self, member_id):
        self.id = int(member_id)
        self.balance = defaultvalues["balance"]
        self.inventory = defaultvalues["inventory"]
        self.collection = defaultvalues["collection"]
        self.linked_account = defaultvalues["email"]

class JsonMemberConverter(Member):
    
    def __init__(self, filename):
        try:
            r = open(f"data/members/{filename}", "r")
            rawFileData = r.read()
            fileData = rawFileData.split("\n")
            r.close()
        except FileNotFoundError:
            raise SharkErrors.MemberFileNotFoundError

        self.id = int(fileData[0])
        self.balance = int(fileData[1])
        self.inventory = fileData[2].split(",")
        self.collection = fileData[3].split(",")
        if fileData[4] == "No Account Linked":
            self.linked_account = None
        else:
            self.linked_account = fileData[4]

        if self.inventory == [""]:
            self.inventory = []
        if self.collection == [""]:
            self.collection = []

def get(member_id):
    with open("data/memberdata.json", "r") as infile:
        data = json.load(infile)

    if str(member_id) in data:
        member = Member(update_data(data[str(member_id)]))
    else:
        member = BlankMember(member_id)
        member.write_data()
    return member

def update_json_file(member_id, member_data):
    with open("data/memberdata.json", "r") as infile:
        json_data = json.load(infile)
    json_data[str(member_id)] = member_data
    with open("data/memberdata.json", "w") as outfile:
        json.dump(json_data, outfile, indent=4)

def get_used_accounts():
    r = open(f"data/usedaccounts.txt", "r")
    rawFileData = r.read()
    if rawFileData == "":
        fileData = []
    else:
        fileData = rawFileData.split("\n")
    r.close()
    return fileData

def write_used_accounts(accountList):
    w = open(f"data/usedaccounts.txt", "w")
    w.write("\n".join(accountList))
    w.close()

defaultvalues = {
    "id" : 1234,
    "balance" : 0,
    "inventory" : [],
    "collection" : [],
    "email" : None
    }

def update_data(data):
    for value in defaultvalues:
        if value not in data:
            data[value] = defaultvalues[value]
    return data
