from .monad import *

class ListMonad(Monad):
    """
    Monad instance for non-deterministic computation
    using lists.
    """
    
    @staticmethod
    def lift(x):
        """
        Lifts a value into a singleton list.
        
        Arguments:
        x -- the plain value to lift
        """
        
        return [x]
    
    @staticmethod
    def bind(m, f):
        """
        Performs a flat-map operation over a list.
        
        Arguments:
        m -- the list to map over
        f -- a function from list element to list
        """
        
        result = []
        for elem in m:
            result += f(elem)
        return result
        
    @staticmethod
    def empty():
        """
        Constructs an empty list.
        """
        
        return []
        
    @staticmethod
    def concat(x, y):
        """
        Concatenates two lists.
        
        Arguments:
        x -- the list to order first
        y -- the list to order second
        """
        
        return x + y

class NoneMonad(Monad):
    """
    Monad instance for failable computation using None.
    """
    
    @staticmethod
    def lift(x):
        """
        Does nothing.
        
        Since we're not wrapping the non-None case,
        we don't need more than an identity function here.
        
        Arguments:
        x -- the value to return
        """
        
        return x
    
    @staticmethod
    def bind(m, f):
        """
        Performs the operation on the value if it is not None.
        
        Arguments:
        m -- the value to operate on
        f -- a transform that may return None
        """
        
        if m is not None:
            return f(m)
        else:
            return None

    @staticmethod
    def empty():
        """
        Constructs the value None.
        """
        
        return None
    
    @staticmethod
    def concat(x, y):
        """
        Returns the first value that is not None,
        else returns None.
        
        Arguments:
        x -- the first value
        y -- the second value
        """
        return x or y

class ExceptionMonad(Monad):
    """
    Monad instance for failable computation using Exception.
    """
    
    @staticmethod
    def lift(x):
        """
        Does nothing.
        
        Since we're not wrapping the non-Exception case,
        we don't need more than an identity function here.
        
        Arguments:
        x -- the value to return
        """
        
        return x
    
    @staticmethod
    def bind(m, f):
        """
        Performs the operation on the value if it is not an
        Exception.
        
        Arguments:
        m -- the value to operate on
        f -- a transform that may return an Exception
        """
        
        if m is not None:
            return f(m)
        else:
            return None

    @staticmethod
    def empty():
        """
        Constructs an empty Exception.
        """
        
        return Exception()
    
    @staticmethod
    def concat(x, y):
        """
        Returns the first value that is not an Exception,
        else returns the last Exception.
        
        Arguments:
        x -- the first value
        y -- the second value
        """
        if not isinstance(x, Exception):
            return x
        else:
            return y

class FunctionMonad(Monad):
    """
    Monad instance for functions.
    """
    
    @staticmethod
    def lift(x):
        """
        Lifts the value into a constant function that always returns `x`
        regardless of its input.
        
        Arguments:
        x -- the value to always return from the function
        """
        return lambda _: x
    
    @staticmethod
    def bind(m, f):
        """
        Returns a function that feeds its argument into the function that
        results from feeing its argument into the monadic function and
        then feeding that function into the transform function.
        
        Arguments:
        m -- the monadic function
        f -- the transform function
        """
        return lambda x: f(m(x))(x)

class StateMonad(Monad):
    """
    Monad instance that threads state through a computation.
    
    Stateful computations are functions from state to
    result-new state tuples.
    """
    
    @staticmethod
    def lift(x):
        """
        Lifts the value into a state tuple.
        """
        return lambda state: (x, state)
    
    @staticmethod
    def bind(m, f):
        """
        Extracts the result of running the stateful computation
        and passing it into the transform while threading the state
        through.
        
        Arguments:
        m -- the stateful computation
        f -- a function from plain value to stateful computation
        """
        def thread_state(state):
            (x, new_state) = m(state)
            return f(x)(new_state)
        return thread_state

