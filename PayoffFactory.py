
# Author: Matteo L. BEDINI
# Date: April 2016

# input: a string and some parameters
# output: a payoff object corresponding to the string with the corresponding parameters

# NOT implemented as a Singleton (I cannot see how to do something meaningful while keeping in mind what I did with a standard factory in C++

import DerivativePayoff

def PayoffFactory(payoff_name, params):
    """ function PayoffFactoryMethod

    input: payoff_name: a string of a payoff name
           params: a list containing the parameters of that payoff
           
    output: a payoff
    """
    assert isinstance(payoff_name, str), "payoff_name must be a string"
    assert isinstance(params, dict), "params must be a dictionary"
    
    this_payoff = None
    payoff_type = getattr(DerivativePayoff,payoff_name) # an AttributeError may be launched if payoff_name is not valid
    this_payoff = payoff_type(**params) #a TypeError may be launched if len(params) doesn't match the number of required parameter
                                       #an AssertionError may be launched if the type/value of the parameters is not correct
    
    return this_payoff
