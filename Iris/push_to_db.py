#!/usr/bin/python

import sqlite3

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self): 
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def get(self):
        return self.items

class Db:
    _name = None  # type: object

    def __init__(self, _name):
        self._name = _name

    def create(self):
        conn = sqlite3.connect(self._name)
        #print "Opened database %s"%(self._name)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE Iris_master
                    (Room INT PRIMARY KEY NOT NULL,
                    Name TEXT NOT NULL,
                    Occupany INT NOT NULL,
                    Occupied INT)''')

    def update(self, room, new_occupied):
        conn = sqlite3.connect(self._name)
        #print "Opened database %s" % self._name
        conn.execute('''UPDATE Iris_master SET Occupied = ? WHERE Room = ?''', (new_occupied, room))
        conn.commit()

    def select(self):
        conn = sqlite3.connect(self._name)
        #print "Opened database %s" % (self._name)
        cur = conn.cursor()
        cur.execute('''SELECT Room, Name, Occupancy, 
                    Occupied from Iris_master''')
        print cur.fetchall()
#def main():
#    queue = Queue()
#
##    db = Db.create('test.db')
#
#if __name__ == "__main__":
#    main()
