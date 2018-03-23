from abc import ABCMeta, abstractmethod
##################################
#This class helps implement some of the observer class features. Code is
#modified from example by Ira Woodring
#@author Brendan Dent
#@version 3/23/18
#################################
#class for abstract method outlining the update for observers
class Observer(object):
        __metaclass__ = ABCMeta

        @abstractmethod
        def observer_update(self, sender):
        	pass
#class to help implement observable classes
class Observable(object):

        def __init__(self):    
                self.observers = []

        def add_observer(self, observer):
                if not observer in self.observers:
                        self.observers.append(observer)

        def remove_observe(self, observer):
                if observer in self.observers:
                        self.observers.remove(observer)

        def remove_all_observers(self):
                self.observers = []

        def update(self, sender):
                for observer in self.observers:
                        observer.observer_update(self, sender)
