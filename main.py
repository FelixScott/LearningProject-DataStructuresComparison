class Employee:
    # This class holds the sample data for the linked list read in from a csv file.
    # Importantly the data input function which reads the files and creates the lists is in this class and needs to be
    # recreated for any other data.
    def __init__(self, ID, Prefix, FirstKey, MiddleInitial, LastKey, Gender, Email):
        self.ID = ID
        self.Prefix = Prefix
        self.FirstKey = FirstKey
        self.MiddleInitial = MiddleInitial
        self.LastKey = LastKey
        self.Gender = Gender
        self.Email = Email

    def HashDataInput(self, FileKey, EmployeeHashTable, EmployeeUnlinkedList):
        import csv
        with open(FileKey, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for line in csv_reader:
                EmployeeHashTable.Insert(str(line[4]), i)
                EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                i += 1

    def LinkedListDataInput(self, FileKey, EmployeeLinkedList, EmployeeUnlinkedList):
        import csv
        with open(FileKey, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for line in csv_reader:
                EmployeeLinkedList.Insert(str(line[4]), i)
                EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                i += 1

    def BinaryTreeDataInput(self, FileKey, EmployeeBinaryTree, EmployeeUnlinkedList):
        import csv
        with open(FileKey, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for line in csv_reader:
                EmployeeBinaryTree.Insert(str(line[4]), i)
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


class BinaryTreeNode:
    def __init__(self, Value, Key, LowerNode, HigherNode):
        self.Value = Value
        self.Key = Key
        self.HigherNode = HigherNode
        self.LowerNode = LowerNode
        self.PreviousNode = None
        self.Collided = False
        self.CollidedNext = None
        self.CollidedPrevious = None


class BinaryTree:
    def __init__(self):
        self.Head = None

    def NodeSort(self, Target, Subject):
        # Be aware this may throw a fault for data that cant use min() and will need a custom sort method
        # 0: same
        # 1: Subject is higher
        # 2: Target is higher
        if Target == Subject:
            return 0
        elif min(Target, Subject) == Target:
            return 1
        else:
            return 2

    def Insert(self, Value, Key, LowerNode, HigherNode):
        InsertNode = BinaryTreeNode(Value, Key, LowerNode, HigherNode)
        ComparisonNode = None
        IsPlaced = False
        if self.Head is None:
            self.Head = InsertNode
            IsPlaced = True
        else:
            ComparisonNode = self.Head
        while IsPlaced is False:
            if self.NodeSort(InsertNode.Key, ComparisonNode.Key) == 0: # Nodes are equal
                self.TreeCollision(InsertNode, ComparisonNode)
                IsPlaced = True
            elif self.NodeSort(InsertNode.Key, ComparisonNode.Key) == 1: # ComparisonNode is Higher
                if ComparisonNode.LowerNode is None:
                    ComparisonNode.LowerNode = InsertNode
                    InsertNode.PreviousNode = ComparisonNode
                    IsPlaced = True
                else:
                    ComparisonNode = ComparisonNode.LowerNode
            elif self.NodeSort(InsertNode.Key, ComparisonNode.Key) == 2: # InsertNode is Higher
                if ComparisonNode.HigherNode is None:
                    ComparisonNode.HigherNode = InsertNode
                    InsertNode.PreviousNode = ComparisonNode
                    IsPlaced = True
                else:
                    ComparisonNode = ComparisonNode.HigherNode

    def TreeCollision (self, TargetNode, SubjectNode):
        SubjectNode.Collided = True
        TargetNode.Collided = True
        CurrentNode = SubjectNode
        while CurrentNode.CollidedNext is not None:
            CurrentNode = CurrentNode.CollidedNext
        CurrentNode.CollidedNext = TargetNode
        TargetNode.CollidedPrevious = CurrentNode

    def FindEntry(self, Key):
        ComparisonNode = self.Head
        while Key != ComparisonNode.Key:
            if self.NodeSort(Key, ComparisonNode.Key) == 1:
                if ComparisonNode.LowerNode is None:
                    print("Entry not in list")
                    return
                else:
                    ComparisonNode = ComparisonNode.LowerNode
            elif self.NodeSort(Key, ComparisonNode.Key) == 2:
                if ComparisonNode.HigherNode is None:
                    print("Entry not in list")
                    return
                else:
                    ComparisonNode = ComparisonNode.HigherNode
        if ComparisonNode.Collided:
            print("Multiple entries under {} found:".format(Key))
            i = 0
            while ComparisonNode.CollidedNext is not None:
                print("{}: {} ({})".format(i, ComparisonNode.Key, i))
                i += 1
            UserChoice = input("Please choose number from above list: ")
            i = 0
            while i < UserChoice:
                ComparisonNode = ComparisonNode.CollidedNext
            return ComparisonNode.Value
        else:
            return ComparisonNode.Value

    def RemoveEntry(self, Key):
        ComparisonNode = self.Head
        while Key != ComparisonNode.Key:
            if self.NodeSort(Key, ComparisonNode.Key) == 1:
                if ComparisonNode.LowerNode is None:
                    print("Entry not in list")
                    return
                else:
                    ComparisonNode = ComparisonNode.LowerNode
            elif self.NodeSort(Key, ComparisonNode.Key) == 2:
                if ComparisonNode.HigherNode is None:
                    print("Entry not in list")
                    return
                else:
                    ComparisonNode = ComparisonNode.HigherNode
        if ComparisonNode.Collided:
            print("Multiple entries under {} found:".format(Key))
            i = 0
            while ComparisonNode.CollidedNext is not None:
                print("{}: {} ({})".format(i, ComparisonNode.Key, i))
                i += 1
            UserChoice = input("Please choose number from above list: ")
            i = 0
            while i < UserChoice:
                ComparisonNode = ComparisonNode.CollidedNext
            if ComparisonNode.CollidedPrevious is not None:
                ComparisonNode.CollidedPrevious.CollidedNext = ComparisonNode.CollidedNext
            if ComparisonNode.CollidedNext is not None:
                ComparisonNode.CollidedNext.CollidedPrevious = ComparisonNode.CollidedPrevious
        else:
            if ComparisonNode.PreviousNode.LowerNode.Key == Key:
                ComparisonNode.PreviousNode.LowerNode = None
            else:
                ComparisonNode.PreviousNode.HigherNode = None
            self.Insert(ComparisonNode.LowerNode.Value, ComparisonNode.LowerNode.Key, ComparisonNode.LowerNode.LowerNode, ComparisonNode.LowerNode.HigherNode)
            self.Insert(ComparisonNode.HigherNode.Value, ComparisonNode.HigherNode.Key, ComparisonNode.HigherNode.LowerNode, ComparisonNode.HigherNode.HigherNode)




class LinkedListNode:
    def __init__(self, Value, Key):
        self.Value = Value
        self.Key = Key
        self.NextNode = None
        self.PreviousNode = None


class LinkedList:
    # This program uses a linked list for any clashes in ID for the binary tree
    def __init__(self):
        self.Head = None
        self.Tail = None

    def Insert(self, Value, Key):
        Node = LinkedListNode(Value, Key)
        if self.Head is None:
            self.Head = Node
        elif self.Tail is None:
            self.Tail = Node
            self.Tail.PreviousNode = self.Head
            self.Head.NextNode = Node
            Node.PreviousNode = self.Head
        else:
            self.Tail.NextNode = Node
            Node.PreviousNode = self.Tail
            self.Tail = Node

    def PrintLinkedList(self):
        CurrentNode = self.Head
        while CurrentNode != self.Tail:
            print (str(CurrentNode.Key) + " -> ")
            CurrentNode = CurrentNode.NextNode
        print(str(CurrentNode.Key))

    def FindEntryFromKey(self, NodeKey):
        CurrentNode = self.Head
        while CurrentNode.Key != NodeKey and CurrentNode is not self.Tail:
            CurrentNode = CurrentNode.NextNode
        if CurrentNode.Key == NodeKey:
            return CurrentNode.Value
        else:
            return 0

    def FindEntryFromPosition(self, NodePosition):
        CurrentNode = self.Head
        i = 0
        while i < NodePosition:
            CurrentNode = CurrentNode.NextNode
            i += 1
        return CurrentNode.Value

    def PresentEntries(self):
        CurrentNode = self.Head
        i = 1
        while CurrentNode != self.Tail:
            print("{}: {}".format(i, CurrentNode.Key))
            i += 1
            CurrentNode = CurrentNode.NextNode
        print("{}: {}".format(i, CurrentNode.Key))

    def RemoveEntry(self, Key):
        CurrentNode = self.Head
        while CurrentNode.Key != Key and CurrentNode.NextNode is not None:
            CurrentNode = CurrentNode.NextNode
        if CurrentNode.NextNode is None and CurrentNode.Key != Key:
            print("Entry Does not exist, No action taken")
        else:
            if CurrentNode.PreviousNode is not None:
                CurrentNode.PreviousNode.NextNode = CurrentNode.NextNode
            if CurrentNode.NextNode is not None:
                CurrentNode.NextNode.PreviousNode = CurrentNode.PreviousNode




ExampleEmployeeUnlinkedList = []
ExampleEmployeeHashTable = HashTable(1000)
FileKey = "EmployeeRecords.csv"
Employee.HashDataInput("", FileKey, ExampleEmployeeHashTable, ExampleEmployeeUnlinkedList)
ExampleEmployeeHashTable.ListBuckets()













