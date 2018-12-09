class Commit(object):
    def __index__(self, message, parent):
        self.message = message
        self.__parent = parent
