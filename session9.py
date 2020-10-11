from datetime import datetime , timezone
from functools import wraps
from functools import singledispatch
import html
from html import escape
from decimal import Decimal
from numbers import Integral

## Allows a function to run only on odd seconds - 100pts

def function_odd_sec(fn):
    """
    This allows a function to run only on odd seconds
    """
    @wraps(fn)
    def inner(*args,**kwargs):
        result = fn(*args,**kwargs)
        if datetime.now().time().second % 2 == 0 :
            return(result)
        print("The function executes only in odd second")
    return(inner)

## Logging Function

def logging_function(fn):
    """
    This function maintains the log, so that the time can be clocked at which the
    function was called
    """
    @wraps(fn)
    def inner(*args,**kwargs):
        run_dt = datetime.now()
        result = fn(*args,**kwargs)
        
        args_ = [str(a) for a in args]
        kwargs_ = ['{0} = {1} '.format(k,v) for k , v in kwargs.items() ]

        all_args = args_ + kwargs_
        args_str = ",".join(all_args)

        print(f"The function {fn.__name__}({all_args}) was called at : {run_dt}")
        
        return(result)
    return(inner)

## Authentication function

def set_password():
    """
    This function allows a person the set password
    """
    password = ""
    def inner():
      nonlocal password
      if password == "":
        password = input()
      return password
    return inner

current_password = set_password()
print("Set Password!!")
current_password()

def authentication(current_password):
    def authenticate_function(fn):
        """
        This function authenticates a function before providing access
        """
        count = 0
        attempts_left = 4
        print("Enter your password :")
        user_password = input()
        
        while attempts_left > 1 :
            if current_password() == user_password:
                def inner(*args, **kwargs):
                    nonlocal count
                    count += 1
                    print(f'{fn.__name__}() was called {count} times')
                    return(fn(*args, **kwargs))
                return inner
            else :
                attempts_left -= 1
                print(f"Invalid Password , You have {attempts_left} number of attempts remaining")
                print("Please Try again.")
                print("Enter your password :")
                user_password = input()

        print("Sorry You have Exhausted the number of attempts, Your account is temporary locked")
    return authenticate_function


"""
@authentication(current_password)
def add(x,y):
    return(x + y)
add(1,2)
"""
## Timed (n times) function to find the average execution time of any function

def timed(reps):
    def timed_decorator(fn):
        from time import perf_counter
        def inner(*args,**kwargs):
            total_elapsed = 0
            for i in range(reps):
                start = perf_counter()
                result = fn(*args,**kwargs)
                stop = perf_counter()
                total_elapsed += (stop - start)
            avg_run_time = total_elapsed / reps
            print('Avg Run time: {0:.6f}s ({1} reps)'.format(avg_run_time, reps))
            return result
        return inner
    return timed_decorator
                
def calc_recursive_fib(n):
  if n<=2 :
    return(1)
  else:
    return (calc_recursive_fib(n-1) + calc_recursive_fib(n-2))

@timed(reps = 20)
def fib_recursive(n):
  return (calc_recursive_fib(n))

fib_recursive(10)   

## Privilege Access

        


## Write our htmlize code using inbuild singledispatch
## Adding Features to our decorators from outside

@singledispatch
def htmlize(a : str) -> str :
    """
    To htmlize the input string
    input: string .
    return: htmlized string
    """
    return escape(str(a))

@htmlize.register(Integral)
def htmlize_int(a : int) -> int :
    """
    To htmlize the input integer
    input : Integer
    output : htmlize integer
    """
    return f"{a}(<i>{str(hex(a))}</i>)"

@htmlize.register(Decimal)
@htmlize.register(float)
def html_real(a: float) -> float:
    """
    Converts the real number to rounded real number rounded to second decimal value.
    """
    return f"(<i>{round(a, 2)}</i>)"

def html_escape(arg):
    return escape(str(arg))

@htmlize.register(tuple)
@htmlize.register(list)
def html_sequence(l):
    """
    To htmlize the output returned from a list or tuple
    """
    items = (f'<li>{html_escape(item)}</li>' for item in l)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'


@htmlize.register(dict)
def html_dict(d):
    """
    To htmlize the list returned from a dictionary
    """
    items = (f'<li>{k}={v}</li>' for k, v in d.items())
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'
