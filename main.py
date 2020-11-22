class Employee:
    # This class holds the sample data for the linked list read in from a csv file.
    # Importantly the data input function which reads the files and creates the lists is in this class and needs to be
    # recreated for any other data.
    def __init__(self, ID, Prefix, FirstName, MiddleInitial, LastName, Gender, Email):
        self.ID = ID
        self.Prefix = Prefix
        self.FirstName = FirstName
        self.MiddleInitial = MiddleInitial
        self.LastName = LastName
        self.Gender = Gender
        self.Email = Email

    def HashDataInput(self, FileName, EmployeeHashTable, EmployeeUnlinkedList):
        import csv
        with open(FileName, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for line in csv_reader:
                EmployeeHashTable.Insert(str(line[4]), i)
                EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                i += 1


class HashTableNode:
    def __init__(self, Key, Value):
        self.Key = Key
        self.Value = Value
        self.NextNode = None

class HashTable:
    def __init__(self, Capacity):
        self.Capacity = Capacity  # Number of buckets
        self.Size = 0  # Number of elements
        self.Buckets = [None] * self.Capacity  #Internal flat array

    def Hash(self, Key):
        HashSum = 0
        for idx, Char in enumerate(Key):
            HashSum += ((idx + len(Key)) ** ord(Char))
            HashSum = HashSum % self.Capacity
        return HashSum

    def Insert(self, Key, Value):
        self.Size += 1
        Index = self.Hash(Key)
        Node = self.Buckets[Index]
        if Node is None:
            self.Buckets[Index] = HashTableNode(Key, Value)
            return
        PreviousNode = Node
        while Node is not None:
            PreviousNode = Node
            Node = Node.NextNode
        PreviousNode.NextNode = HashTableNode(Key, Value)

    def FindEntry(self, Key):
        Index = self.Hash(Key)
        Node = self.Buckets[Index]
        while Node is not None and Node.Key != Key:
            Node = Node.NextNode
            if Node is None:
                return None
            else:
                return Node.Value

    def RemoveEntry(self, Key):
        Index = self.Hash(Key)
        Node = self.Buckets[Index]
        while Node is not None and Node.Key != Key:
            PreviousNode = Node
            Node = Node.NextNode
            if Node is None:
                print("Entry Does not exist, No action taken")
                return
            else:
                if PreviousNode is None:
                    Node = None
                else:
                    PreviousNode.NextNode = PreviousNode.NextNode.NextNode
                    Node = None

    def ListBuckets(self):
        i = 0
        while i < self.Capacity:
            Node = self.Buckets[i]
            if Node is None:
                print("Index {} is empty".format(i))
            else:
                Counter = 1
                while Node.NextNode is not None:
                    Counter += 1
                    Node = Node.NextNode
                print("Index {} has {} entries".format(i, Counter))
            i += 1



ExampleEmployeeUnlinkedList = []
ExampleEmployeeHashTable = HashTable(1000)
FileName = "EmployeeRecords.csv"
Employee.HashDataInput("", FileName, ExampleEmployeeHashTable, ExampleEmployeeUnlinkedList)
ExampleEmployeeHashTable.ListBuckets()













