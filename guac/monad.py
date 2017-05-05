import abc, copy, inspect

class Monad(metaclass=abc.ABCMeta):  
    """An abstract class whose subclasses represent monad instances."""
    
    @staticmethod    
    @abc.abstractmethod
    def lift(x):
        """
        Lifts a plain value into the monadic context.
        
        Arguments:
        x - the plain value to lift
        """
        return NotImplemented
        
    @staticmethod
    @abc.abstractmethod
    def bind(m, f):
        """
        Unwraps the plain value from the monadic context and
        feeds it into the function, yielding a monadic value.

        Arguments:
        m -- the monadic value
        f -- the function from plain value to monadic value
        """
        return NotImplemented
        
    class _Builtin:
        def __init__(self, impl):
            self.evaluate_in_monad = impl
                
    @classmethod    
    def _run(self, computation):
        def step(monadic_value, continuation):
            if isinstance(monadic_value, Monad._Builtin):
                monadic_value = monadic_value.evaluate_in_monad(self)
            def proceed(x):
                invocation = copy.deepcopy(continuation) # Requires Pypy!
                try:
                    return step(invocation.send(x), invocation)
                except StopIteration as e:
                    if e.value:
                        raise ValueError("unexpected return value in monadic function")
                    return self.lift(x)
            return self.bind(monadic_value, proceed)
        try:
            return step(next(computation), computation)
        except StopIteration as e:
            raise ValueError("monadic function must yield at least once")

# + Decorator for executing a monad
#   - an argument may be specified to specialize for a specific monad
#     - otherwise, the monad may be specialized by named arg at callsite
#   - yield correpsonds to the bind operator in that it "unpacks" a value
#     - execution of the monadic effects end at last yield before return 
def monadic(instance):
    """
    Decorates a monadic function so that invocation runs the monad.
    
    If no instance argument is supplied, the function may only be
    invoked from other monadic functions. In these cases, the instance
    argument will be inherited from the caller.
    
    Arguments:
    instance -- an optional argument specializing the monad instance
    
    Usage:
    Within the decorated function, use `yield` to perform a bind operation
    on a monadic value. The value to be yielded is that monadic value to
    bind. The result of the yield will be the unwrapped mondic value.
    The function must end with a yield of the resulting value after the
    desired transforms have been applied.
    
    Example:
    @monadic(ListMonad)
    def make_change(amount_still_owed, possible_coins):
        change = []
        while amount_still_owed > 0 and possible_coins:
            give_min_coin = yield [True, False] # nondeterministic choice
            if give_min_coin:
                min_coin = possible_coins[0]
                change.append(min_coin)
                amount_still_owed -= min_coin
            else:
                del possible_coins[0]
        yield guard(amount_still_owed == 0)
        yield lift(change)
    print(make_change(27, [1, 5, 10, 25]))
    """
    def wrap(f, monad=None):
        def monadic_context(*args, monad=monad, **kwargs):
            if monad is None: #infer from context
                for (frame, _, _, name, _, _) in inspect.stack()[1:]:
                    if name == 'monadic_context':
                        monad = inspect.getargvalues(frame).locals['monad']
                        break
                    del frame
                else:
                    raise RuntimeError('unspecified monadic context')
            return monad._run(f(*args, **kwargs))
        return monadic_context
            
    if issubclass(instance, Monad):
        return lambda f: wrap(f, monad=instance)
    elif not callable(instance):
        raise TypeError('expected instance of Monad')
    
    # We weren't given an instance; return an unspecialized wrapper.
    f = instance
    del instance
        
    if inspect.isgeneratorfunction(f):
        return wrap(f)
    else:
        raise ValueError('monadic function must be a generator')        
