from .monad import *

@monadic
def bind(m, f):
    """
    Unwraps the plain value from the monadic context and
    feeds it into the function, yielding a monadic value.
    
    Arguments:
    m -- the monadic value
    f -- the function from plain value to monadic value
    """
    
    yield f(m)

@monadic
def lift(value):
    """
    Lifts a plain value into the monadic context.
    
    Arguments:
    x - the plain value to lift
    """
    
    yield Monad._Builtin(lambda m: m.lift(value))

@monadic
def empty():
    """
    Creates an empty monadic context.
    
    Note that this function is not required to be implemented
    by all monads.
    """
    
    yield Monad._Builtin(lambda m: m.empty())
    
@monadic
def concat(x, y):
    """
    Concatenates two monadic context.
    
    Note that this function is not required to be implemented
    by all monads.
    """
    
    yield Monad._Builtin(lambda m: m.concat(x, y))

@monadic
def unit():
    """
    Lifts a unit value into the monadic context.
    """
    
    yield lift(())

@monadic
def guard(condition):
    """
    Guards against a condition within a monadic context, trimming
    branches where this condition does not hold.
    
    Requires the monad to support `empty`.
    
    Argument:
    condition -- the condition that must hold
    """
    
    if condition:
        yield unit()
    else:
        yield empty()

@monadic
def map(f, m):
    """
    Maps the transform over the plain value within the monadic context.
    
    Argument:
    f -- function that maps from plain value to plain value
    m -- the monadic value to be mapped over
    """
    
    x = yield m
    yield lift(f(x))
    
@monadic
def join(m):
    """
    Flattens a layer of nesting of monadic context.
    
    Argument:
    m -- a monadic value nested in a monadic value
    """
    
    x = yield m
    yield x

@monadic
def filter(predicate, m):
    """
    Filters out values where the condition does not hold.
    
    Requires the monad to support `empty`.
    
    Argument:
    predicate -- a bool-returning function over plain values
    m -- the monadic value to filter
    """
    
    x = yield m
    guard(pred(x))
    yield x
