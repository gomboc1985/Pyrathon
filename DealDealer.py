
# Author: Matteo L. BEDINI
# Date: April 2016

import PricingMethods


def deal_pricer(payoff, pricing_method, settings):
    """deal_pricer
    input: a payoff, a pricing method, pricing settings
    this functions compute the price of a payoff and add the result to
    the payoff's instance attributes
    """
    #print(payoff)
    pricing_fun = getattr(PricingMethods,pricing_method)
    
    price = pricing_fun(payoff, settings)
    #print(price)
    payoff.price = price
