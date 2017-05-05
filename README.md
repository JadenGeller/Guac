# Guac

Guac is a package that provides monadic [do-notation](https://en.wikibooks.org/wiki/Haskell/do_notation), 
inspired by Haskell, in Python. [Monads](http://blog.plover.com/prog/burritos.html) provide 
"programmable semicolons" by which the behavior of programs can be changed. A common, useful monad is the
list monad, which represents non-deterministic computations. The list monad makes it very easy to write
backtracking searches.

## Example

Here's an example that computes all the possible ways you can give $0.47 change with pennies, nickels, dimes,
and quarters:

```python
from guac import *

@monadic(ListMonad)
def make_change(amount_still_owed, possible_coins):
    change = []
    
    # Keep adding coins while we owe them money and there are still coins.
    while amount_still_owed > 0 and possible_coins:
    
        # "Nondeterministically" choose whether to give anther coin of this value.
        # Aka, try both branches, and return both results.
        give_min_coin = yield [True, False]
        
        if give_min_coin:
            # Give coin
            min_coin = possible_coins[0]
            change.append(min_coin)
            amount_still_owed -= min_coin
        else:
            # Never give this coin value again (in this branch!)
            del possible_coins[0]
            
    # Did we charge them the right amount?
    yield guard(amount_still_owed == 0)
    
    # Lift the result back into the monad.
    yield lift(change)
    
print(make_change(27, [1, 5, 10, 25]))
```

Running this program will print a list of lists, each list containing a different set of numbers
that add up to 27. You can imagine lots of cool ways this could be used, from unification to parsing!

If you have ever used Python's [asyncio](https://docs.python.org/3/library/asyncio.html) package, this may feel
familiar. That's because asyncio is actually a monad! Of course, they don't formalize it as such, but it could
be implemented as one, and it uses coroutines in the exact same way. Unlike asyncio, which simply continues
computation when a result is available, this library makes it possible to repeat computation from arbitrary
yields in the coroutine.

## Building Your Own Monads

Guac comes with a few simple monads, but it's super easy to implement your own monad. You don't need to worry 
about any of the coroutine logic---Guac handles that for you. You just have to implement two simple
functions, `lift` and `bind`:

```python
class ListMonad(Monad):
    @staticmethod
    def lift(x):
        return [x]
    
    @staticmethod
    def bind(m, f):
        result = []
        for elem in m:
            result += f(elem)
        return result
```

Your definitions should ideally follow the [monad laws](https://wiki.haskell.org/Monad_laws), though the
lack of types can make this a bit janky to reason about.

## Unspecialized Monadic Computations

You might have noticed that you use the `@monadic` decorated to turn a coroutine into a function that runs the
monad. To specialize a compuation to a specific monad instance, you pass that instance as an argument to the
decorator. Otherwise, you create an unspecialized monadic computation that will inherit its instance from
the caller.

Here's the implementation of the `guard` function used above:
```python
@monadic
def guard(condition):
    if condition:
        yield unit()
    else:
        yield empty()
```

Handy helper functions like `unit` and `empty` are defined by Guac. Some functions require a little bit
more than a monad. For example, `empty` must be implemented in addition to `lift` and `bind` on your monad
class to use these functions.

## Usage

### Requirements

Guac requires an implementation of Python 3 that supports `copy.deepcopy` on generator functions. The most
common distribution, CPython, is lacking this feature, but [pypy](http://pypy.org) implements it!

### Installation

If you already have the pypy distribution of Python 3, you can install this package with pip:
```
pypy3 -m pip install guac
```
If you don't yet have pypy, you can download and install it [here](http://pypy.org/download.html). Alternatively,
if you have Homebrew on macOS, you can run this:
```
brew install pypy3
```
