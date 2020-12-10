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

    def FindEntry(self, Key, Tracked):
        Index = self.Hash(Key)
        Node = self.Buckets[Index]
        if Tracked:
            Tracker = 0
            while Node is not None and Node.Key != Key:
                Tracker += 1
                Node = Node.NextNode
            if Node is None:
                return None
            else:
                print("Entry found in {} steps".format(Tracker))
                return Node.Value
        else:
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
    def __init__(self, Value, Key):
        self.Value = Value
        self.Key = Key
        self.HigherNode = None
        self.LowerNode = None
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

    def Insert(self, Value, Key):
        InsertNode = BinaryTreeNode(Value, Key)
        ComparisonNode = None
        IsPlaced = False
        if self.Head is None:
            self.Head = InsertNode
            return
        else:
            ComparisonNode = self.Head
        while IsPlaced is False:
            if self.NodeSort(InsertNode.Key, ComparisonNode.Key) == 0:  # Nodes are equal
                self.TreeCollision(InsertNode, ComparisonNode)
                IsPlaced = True
            elif self.NodeSort(InsertNode.Key, ComparisonNode.Key) == 1:  # ComparisonNode is Higher
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

    def FindEntry(self, Key, Tracked):
        ComparisonNode = self.Head
        if Tracked:
            Tracker = 0
            while Key != ComparisonNode.Key:
                if self.NodeSort(Key, ComparisonNode.Key) == 1:
                    if ComparisonNode.LowerNode is None:
                        Tracker += 1
                        print("Entry not found in {} steps".format(Tracker))
                        print("Entry not in list")
                        return
                    else:
                        Tracker += 1
                        ComparisonNode = ComparisonNode.LowerNode
                elif self.NodeSort(Key, ComparisonNode.Key) == 2:
                    if ComparisonNode.HigherNode is None:
                        Tracker += 1
                        print("Entry not found in {} steps".format(Tracker))
                        print("Entry not in list")
                        return
                    else:
                        Tracker += 1
                        ComparisonNode = ComparisonNode.HigherNode
            if ComparisonNode.Collided:
                print("Entry found collided in {} steps".format(Tracker))
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
                print("Entry found uncollided in {} steps".format(Tracker))
                return ComparisonNode.Value
        else:
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
    def __init__(self, Key, Value):
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

    def FindEntry(self, NodeKey, Tracked):
        CurrentNode = self.Head
        if Tracked:
            Tracker = 0
            while (CurrentNode.Key != NodeKey) and (CurrentNode is not self.Tail):
                CurrentNode = CurrentNode.NextNode
                Tracker += 1
            if CurrentNode.Key == NodeKey:
                print("Found in {} iterations".format(Tracker))
                return CurrentNode.Value
            else:
                print("Could not find in {} iterations".format(Tracker))
                return 0
        else:
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


class Menu:
    def __init__(self, PassedMenuName):
        self.ReturnMenu = None
        self.MenuOptions = []
        self.MenuName = str(PassedMenuName)

    def InsertMenuOption(self, PassedName, PassedMenuReturn,  PassedFunction):
        TempName = str(PassedName)
        MenuReturn = PassedMenuReturn
        TempFunction = PassedFunction
        self.MenuOptions.append(TempName)
        self.MenuOptions.append(MenuReturn)
        self.MenuOptions.append(TempFunction)

    def Display(self):
        print("\n----------{}----------".format(self.MenuName))
        i = 0
        j = 1
        while i < len(self.MenuOptions):
            print("{}: {}".format(j, self.MenuOptions[i]))
            i += 3
            j += 1
        if self.ReturnMenu is None:
            print("{}: Exit Program".format(j))
        else:
            print("{}: Back".format(j))
        print("----------{}----------".format("-"*len(self.MenuName)))
        print()
        Selection = input("Please Choose from above options: ")
        Selection = int(Selection)
        if Selection == j:
            if self.ReturnMenu is None:
                print("Exiting Program...")
                quit()
            else:
                self.ReturnMenu.Display()
        else:
            Selection = (Selection * 3 - 1)
            print()
            if (self.MenuOptions[Selection-1]) is True:
                self.MenuOptions[Selection]()
                self.Display()
            else:
                self.MenuOptions[Selection]()


def HashDataInput(FileKey, EmployeeHashTable, EmployeeUnlinkedList):
    import csv
    with open(FileKey, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        i = 11
        for line in csv_reader:
            EmployeeHashTable.Insert(str(line[4]), i)
            EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
            i += 1


def LinkedListDataInput(FileKey, EmployeeLinkedList, EmployeeUnlinkedList):
    import csv
    with open(FileKey, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        i = 1
        for line in csv_reader:
            EmployeeLinkedList.Insert(str(line[4]), i)
            EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
            i += 1


def BinaryTreeDataInput(FileKey, EmployeeBinaryTree, EmployeeUnlinkedList):
    import csv
    with open(FileKey, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        i = 1
        for line in csv_reader:
            EmployeeBinaryTree.Insert(i, str(line[4]))
            EmployeeUnlinkedList.append(Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
            i += 1


def TakeFetchRequest():
    RequestedData = 0
    LastName = input("\nPlease enter the last name of the employee you wish to find: ")
    print("1: ID")
    print("2: FirstName")
    print("3: Middle Initial")
    print("4: Last Name")
    print("5: Gender")
    print("6: Email")
    RequestedData = int(input("\nPlease enter the number corresponding to the data you wish to find: "))
    while not 0 < RequestedData < 7:
        RequestedData = int(input("Error - Value not in list please try again"))
    return LastName, RequestedData


def PrintRequestedData(UnlinkedList, RequestedData, DataIndex):
    switcher = {
        1: UnlinkedList[DataIndex].ID,
        2: UnlinkedList[DataIndex].FirstKey,
        3: UnlinkedList[DataIndex].MiddleInitial,
        4: UnlinkedList[DataIndex].LastKey,
        5: UnlinkedList[DataIndex].Gender,
        6: UnlinkedList[DataIndex].Email
    }
    print("\n   ",switcher[RequestedData],"\n")


def LinkedListFindRecord(UnlinkedList, fLinkedList, Tracked):
    Key, RequestedData = TakeFetchRequest()
    Index = fLinkedList.FindEntry(Key, Tracked)
    if Index == 0:
        print ("Item not in list please try again")
    else:
        PrintRequestedData(UnlinkedList, RequestedData, Index)


def BinaryTreeFindRecord(UnlinkedList, fBinaryTree, Tracked):
    Key, RequestedData = TakeFetchRequest()
    Index = fBinaryTree.FindEntry(Key, Tracked)
    if Index == 0:
        print ("Item not in list please try again")
    else:
        PrintRequestedData(UnlinkedList, RequestedData, Index)


def HashTableFindRecord(UnlinkedList, fHashTable, Tracked):
    Key, RequestedData = TakeFetchRequest()
    Index = fHashTable.FindEntry(Key, Tracked)
    if Index == 0:
        print ("Item not in list please try again")
    else:
        PrintRequestedData(UnlinkedList, RequestedData, Index)


# Menu Functions
def MenuLinkedListImport():
    print("---Importing linked list---")
    LinkedListDataInput(FileName, DataLinkedList, DataUnlinkedList)
    print("---Imported linked list---")


def MenuLinkedListDisplay():
    print("---Displaying linked list---")
    DataLinkedList.PrintLinkedList()
    print("---Displayed linked list---")


def MenuLinkedListFindEntryTracked():
    print("---Find entry tracked---")
    LinkedListFindRecord(DataUnlinkedList, DataLinkedList, True)
    print("---Found entry tracked---")


def MenuLinkedListFindEntryUntracked():
    print("---Find entry untracked---")
    LinkedListFindRecord(DataUnlinkedList, DataLinkedList, False)
    print("---Found entry untracked---")


def MenuBinaryTreeImport():
    print("---Import binary tree---")
    BinaryTreeDataInput(FileName, DataBinaryTree, DataUnlinkedList)
    print("---Imported binary tree---")


def MenuBinaryTreeFindEntryTracked():
    print("---Find entry tracked---")
    BinaryTreeFindRecord(DataUnlinkedList, DataBinaryTree, True)
    print("---Found entry tracked---")


def MenuBinaryTreeFindEntryUntracked():
    print("---Find entry untracked---")
    BinaryTreeFindRecord(DataUnlinkedList, DataBinaryTree, False)
    print("---Found entry untracked---")


def MenuHashTableImport():
    print("---Import hash table---")
    HashDataInput(FileName, DataHashTable, DataUnlinkedList)
    print("---Imported hash table---")


def MenuHashTableFindEntryTracked():
    print("---Find entry tracked---")
    HashTableFindRecord(DataUnlinkedList, DataHashTable, True)
    print("--- Found entry Tracked---")


def MenuHashTableFindEntryUntracked():
    print("---Find entry untracked---")
    HashTableFindRecord(DataUnlinkedList, DataHashTable, False)
    print("---Found entry untracked")


# Menu declarations
MainMenu = Menu("MAIN MENU")
LinkedListOptions = Menu("Linked list options")
LinkedListOptions.ReturnMenu = MainMenu
BinaryTreeOptions = Menu("Binary tree options")
BinaryTreeOptions.ReturnMenu = MainMenu
HashTableOptions = Menu("Hash table options")
HashTableOptions.ReturnMenu = MainMenu

# Menu option declarations
MainMenu.InsertMenuOption("Linked list options", False, LinkedListOptions.Display)
MainMenu.InsertMenuOption("Binary tree options", False, BinaryTreeOptions.Display)
MainMenu.InsertMenuOption("Hash table options", False, HashTableOptions.Display)

LinkedListOptions.InsertMenuOption("Import data to linked list", True, MenuLinkedListImport)
LinkedListOptions.InsertMenuOption("Display linked list", True, MenuLinkedListDisplay)
LinkedListOptions.InsertMenuOption("Find entry tracked", True, MenuLinkedListFindEntryTracked)
LinkedListOptions.InsertMenuOption("Find entry untracked", True, MenuLinkedListFindEntryUntracked)

BinaryTreeOptions.InsertMenuOption("Import data to binary tree", True, MenuBinaryTreeImport)
BinaryTreeOptions.InsertMenuOption("Find entry tracked", True, MenuBinaryTreeFindEntryTracked)
BinaryTreeOptions.InsertMenuOption("Find entry untracked", True, MenuBinaryTreeFindEntryUntracked)

HashTableOptions.InsertMenuOption("Import data to hash table", True, MenuHashTableImport)
HashTableOptions.InsertMenuOption("Find entry tracked", True, MenuHashTableFindEntryTracked)
HashTableOptions.InsertMenuOption("Find entry untracked", True, MenuHashTableFindEntryUntracked)



# Global variable declaration
DataUnlinkedList = []
FileName = "EmployeeRecords.csv"
HashTableCapacity = 1000
DataLinkedList = LinkedList()
DataBinaryTree = BinaryTree()
DataHashTable = HashTable(HashTableCapacity)

# Startup
MenuLinkedListImport()
MenuBinaryTreeImport()
MenuHashTableImport()
MainMenu.Display()















