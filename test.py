import inspect

class Class(object):
    def helo(self, a,b:int,c):
        pass

sig=inspect.signature(Class.helo)

print(sig.parameters)