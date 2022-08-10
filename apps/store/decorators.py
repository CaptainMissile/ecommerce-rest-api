# def my_decorator(fnc):
#     def wrapper():
#         print('Something is happening before fnc')
#         fnc()
#         print('After fnc')

#     return wrapper

# @my_decorator
# def say_whee():
#     print('whee!')

# # say_whee = my_decorator(say_whee)

# say_whee()

# from datetime import datetime

# def say_whee():
#     print('WHEE!')


# def not_during_the_night(fnc):
#     def wrapper():
#         if 7 <= datetime.now().hour < 22:
#             fnc()
#         else:
#             print('hush!')
    
#     return wrapper


# def not_during_the_night_simplified(fnc):
#     if 7 <= datetime.now().hour < 22:
#         fnc()
#     else:
#         print('hush!')


# not_during_the_night_simplified(say_whee)

# print('-----------------------')

# say_whee = not_during_the_night(say_whee)
# say_whee()

# def do_twice(fnc):
#     def wrapper_do_twice(arg):
#         fnc(arg)
#         fnc(arg)
    
#     return wrapper_do_twice

# @do_twice
# def say_whee():
#     print('Whee!')

# @do_twice
# def greet(name):
#     print('Hello! ', name)

# greet = do_twice(greet)
# greet = do_twice(greet)

# greet('Sazin')

# import functools

# def do_twice(fnc):
#     @functools.wraps(fnc)
#     def wrapper_do_twice(*args, **kwargs):
#         return fnc(*args, *kwargs)

#     return wrapper_do_twice


# def return_greeting(name):
#     print('creating greeting')
#     return f'HI {name}'

# print(return_greeting)

# return_greeting = do_twice(return_greeting)

# print(return_greeting)

# a = return_greeting('Sazin')
# print(a)

# import functools

# def decorator(fnc):
#     @functools.wraps(fnc)
#     def wrapper_decorator(*args, **kwargs):
#         # DO SOMETHING BEFORE
#         val = fnc(*args, **kwargs)
#         # DO SOMETHING AFTER
#         return val

import functools
import time

def timer(fnc):
    '''PRINT THE RUNTIME OF A FUNCTION'''
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        val = fnc(*args, **kwargs)
        print('total time taken: ', time.perf_counter() - start_time)
        
        return val

    return wrapper_timer

@timer
def say_something(after_no_of_times):
    for _ in range(after_no_of_times):
        pass

    print('Something Said!')


say_something(100)
say_something(10000)
say_something(1000000)
say_something(100000000)
say_something(10000000000)

    
