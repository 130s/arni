from python_qt_binding.QtGui import QSortFilterProxyModel
from python_qt_binding.QtCore import QObject, QModelIndex

import sys

if sys.version_info[0] is 2 or (sys.version_info[0] is 3 and sys.version_info[1] < 2):
    from lru_cache import lru_cache
else:
    from functools import lru_cache

class ItemFilterProxy(QSortFilterProxyModel):
    """
    The ItemFilterProxy which is a QSortFilterProxyModel helps to filter the data going to the view so the user only sees what he wants to see (which he can modified by telling the view).
     """

    # todo: will call to setFilterRegEx be redirected to the parent automatically?

    def __init__(self, parent=None):
        """
        Initializes the ItemFilterProxy

        :param parent: the parent-object
        :type parent: QObject
        """
        super(ItemFilterProxy, self).__init__(parent)
        #todo: how will these be set correctly at the initialization of the program?
        self.__show_hosts = True
        self.__show_nodes = True
        self.__show_connections = True
        self.__show_topics = True

        self.__filter_string = ""

    def invalidateFilter(self):
        """
        Invalidates the filter
        """
        QSortFilterProxyModel.invalidateFilter(self)
        #invalidate cache
        print(self.filterAcceptsRow.cache_info())
        print("now deleting cache")
        self.filterAcceptsRow.cache_clear()

    #creating cache with infinite size
    @lru_cache(None)
    def filterAcceptsRow(self, source_row, source_parent):
        """
        Tells by analysing the given row if it should be shown or not. This behaviour can be modified via
        setFilterRegExp method so that e.g. only the entries of a specific host can be shown.

        :param source_row: the source of the parent
        :type source_row: int
        :param source_parent: the source of the parent
        :type source_parent: QModelIndex

        :returns: True if the row should be shown
        :rtype: bool
        """
        entries = []
        
        for item in range(0, 4):
            entries.append(self.sourceModel().index(source_row, item, source_parent))

        correct_type = False

        if entries[0] is None:
            raise UserWarning("None values in filterAcceptsRow")

        data = self.sourceModel().data(entries[0])
        for i in range(0, 1):
            if self.__show_hosts is True:
                if data == "host":
                    correct_type = True
                    break
            if self.__show_nodes is True:
                if data == "node":
                    correct_type = True
                    break
            if self.__show_connections is True:
                if data == "connection":
                    correct_type = True
                    break
            if self.__show_topics is True:
                if data == "topic":
                    correct_type = True
                    break

        if correct_type is False:
            return False

        #todo: speed this implementation a lot up by not using the model!!!
        if self.__filter_string is not "":
            #print("now filter")
            #print(self.__filter_string)
            #for i in range(0, len(entries)):
            #    print(self.sourceModel().data(entries[i]))

            tests = [self.__filter_string in self.sourceModel().data(entries[i]) for i in range(0, len(entries))]

            if True in tests:
                return QSortFilterProxyModel.filterAcceptsRow(self, source_row, source_parent)
            else:
                return False

        return QSortFilterProxyModel.filterAcceptsRow(self, source_row, source_parent)


    def setFilterRegExp(self, string):
        self.invalidateFilter()
        QSortFilterProxyModel.setFilterRegExp(self, string)

    def lessThan(self, left, right):
        """
        Defines the sorting of behaviour when comparing two entries of model item by telling how to compare these.

        :param left: the left-hand side
        :type left: QModellIndex
        :param right: the right-hand side
        :type right: QModellIndex

        :returns: bool
        """
        return left < right


    def show_hosts(self, show_hosts):
        """
        Set true if hosts should be shown

        :param show_hosts: true if hosts should be shown
        :type show_hosts: bool
        """
        self.__show_hosts = show_hosts
        self.invalidateFilter()
        

    def show_nodes(self, show_nodes):
        """
        Set true if nodes should be shown

        :param show_nodes: true if nodes should be shown
        :type show_nodes: bool
        """
        self.__show_nodes = show_nodes
        self.invalidateFilter()
        

    def show_connections(self, show_connections):
        """
        Set true if connections should be shown

        :param show_connections: true if connections should be shown
        :type show_connections: bool
        """
        self.__show_connections = show_connections
        self.invalidateFilter()


    def show_topics(self, show_topics):
        """
        Set true if topics should be shown

        :param show_topics: true if topics should be shown
        :type show_topics: bool
        """
        self.__show_topics = show_topics
        self.invalidateFilter()

    def set_filter_string(self, filter_string):
        self.__filter_string = filter_string
        self.invalidateFilter()