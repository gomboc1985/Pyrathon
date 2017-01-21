
# Author: Matteo L. BEDINI
# Date: April 2016

from collections import namedtuple

###########################################################################
##                          ABSTRACT PAYOFF TYPE                         ##
###########################################################################

class SimplePayoff:
    """A generic Payoff Class.
    
    A payoff is characterised by:

    - a list of name-value parameters (a namedtuple)
    - a function from R_+ to R
    - a model for its pricing (a namedtuple)

    SimplePayoff is meant to be "abstract"
    """

    # Parameters = None # a generic payoff cannot have parameters
    Model = namedtuple("PayoffModel",['name', 'location', 'scale'])
    
    def __init__(self):
        self.name = "Abstract Simple Payoff doing nothing"
        self.pars = None
        sel.model = None

    def __str__(self):
        payoff_info = self.name + "\n  + Payoff Parameters: " + str(self.pars) + "\n  + Model Parameters: " + str(self.model)
        if hasattr(self,"price"):
            payoff_info = payoff_info + "\nPrice = " +str(self.price)
        return payoff_info

    def _model_pars_check_in(model_name, location, scale):
        assert isinstance(model_name,str), "model_name must be a string"
        assert (isinstance(location,int) or isinstance(location, float)) and location>=0, "location must be a positive number"
        assert (isinstance(scale,int) or isinstance(scale, float)) and scale>=0, "scale must be a positive number"
        return (model_name, location, scale)

    def payoff_function(self, underlying):
        pass


###########################################################################
##                     PLAIN VANILLA PAYOFF TYPE                         ##
###########################################################################

class PlainVanilla(SimplePayoff):
    """A Plain Vanilla Payoff Class.
	(see, e.g., https://en.wikipedia.org/wiki/Call_option and/or https://en.wikipedia.org/wiki/Put_option)

    Attributes:
    - A name 
    - A named-valued parameter (named-tuple): 'K' representing the strike
                                              'Call_Put_Flag' representing the flavor of the payoff
                                                        (*) Call_Put_Flag = 1 --> Call Payoff
                                                        (*) Call_Put_Flag =-1 --> Put Payoff
    - A named-valued parameter (named-tuple): 'name' representing the model name
                                              'location' representing the location parameter
                                              'scale' representing the scale parameter
    - A payoff-function f(x) = max{Call_Put_Flag*(x-K),0}
    """

    Parameters = namedtuple("PlainVanillaParameters",['K', 'Call_Put_Flag'])

    def __init__(self, strike, call_put_flag, model_name, model_location, model_scale):
        """ Plain Vanilla Option. Compulsory input arguments:
        Payoff Parameters:
            + strike = a positive number representing the strike of the vanilla option
            + call_put_flag = 1 or -1 for representing the payoff type (put or call)
        Model Parameters:
            + model_name = a string identifying the model
            + model_location = a positive number representing the location parameter
            + model_scale = a positive number representing the scale parameter
        """
        assert (isinstance(strike,int) or isinstance(strike, float)) and strike>=0, "strike must be a positive number"
        assert abs(int(call_put_flag))==1, "CallPutFlag can be either 1 or -1"
        self.name = "Call Payoff" if int(call_put_flag)==1 else "Put Payoff" 
        self.pars = PlainVanilla.Parameters(strike, int(call_put_flag))

        model = PlainVanilla._model_pars_check_in(model_name, model_location, model_scale)
        self.model = PlainVanilla.Model(*model)

    def payoff_function(self, underlying):
        """ Payoff Function:
        Input: underlying (a positive number)
        Output: max{Call_Put_Flag*(underlying-K),0}
        """
        assert (isinstance(underlying,int) or isinstance(underlying, float)) and underlying>=0, "underlying must be a positive number"
        return max(self.pars.Call_Put_Flag * (underlying - self.pars.K), 0.0)



###########################################################################
##                          DIGITAL PAYOFF TYPE                          ##
###########################################################################


class Digital(SimplePayoff):
    """A Digital Payoff Class.
	(see, e.g., https://en.wikipedia.org/wiki/Binary_option)

    Attributes:
    - A name
    - A named-valued parameter (named-tuple) 'K' representing the strike
                                             'Call_Put_Flag' representing the flavor of the payoff
                                                        (*) Call_Put_Flag = 1 --> Call Payoff
                                                        (*) Call_Put_Flag =-1 --> Put Payoff
    - A named-valued parameter (named-tuple): 'name' representing the model name
                                              'location' representing the location parameter
                                              'scale' representing the scale parameter
    
    - A payoff-function f(x) = 1 if Call_Put_Flag*(x-K)>=0 else 0
    """

    Parameters = namedtuple("DigitalParameters",['K', 'Call_Put_Flag'])

    def __init__(self, strike, call_put_flag, model_name, model_location, model_scale):
        """ Digital Option. Compulsory input arguments:
        Payoff Parameters:
            + strike = a positive number representing the strike of the vanilla option
            + call_put_flag = 1 or -1 for representing the payoff type (put or call)
        Model Parameters:
            + model_name = a string identifying the model
            + model_location = a positive number representing the location parameter
            + model_scale = a positive number representing the scale parameter
        """
        assert (isinstance(strike,int) or isinstance(strike, float)) and strike>=0, "strike must be a positive number"
        assert abs(int(call_put_flag))==1, "CallPutFlag can be either 1 or -1"
        self.name = "Digital Call Payoff" if int(call_put_flag)==1 else "Digital Put Payoff" 
        self.pars = Digital.Parameters(strike, int(call_put_flag))

        model = Digital._model_pars_check_in(model_name, model_location, model_scale)
        self.model = Digital.Model(*model)

    def payoff_function(self, underlying):
        """ Payoff Function:
        Input: underlying (a positive number)
        Output: 1 if {Call_Put_Flag*(underlying-K)>=0 else 0
        """
        assert (isinstance(underlying,int) or isinstance(underlying, float)) and underlying>=0, "underlying must be a positive number"
        return 1 if self.pars.Call_Put_Flag*(underlying- self.pars.K) >= 0.0 else 0



###########################################################################
##                          BARRIER PAYOFF TYPE                          ##
###########################################################################


class Barrier(SimplePayoff):
    """A Barrier Payoff Class.
	(see, e.g., https://en.wikipedia.org/wiki/Barrier_option)

    Attributes:
    - A name
    - A named-valued parameter (named-tuple): 'K' representing the strike
                                              'B' representing the barrier
                                              'Call_Put_Flag' representing the flavor of the payoff
                                                        (*) Call_Put_Flag = 1 --> Call Payoff
                                                        (*) Call_Put_Flag =-1 --> Put Payoff
    - A named-valued parameter (named-tuple): 'name' representing the model name
                                              'location' representing the location parameter
                                              'scale' representing the scale parameter
    - A payoff-function f(x) = max{Call_Put_Flag*(x-K),0} if Call_Put_Flag*(x-B)<0 else 0
    """

    Parameters = namedtuple("BarrierParameters",['K', 'B', 'Call_Put_Flag'])

    def __init__(self, strike, barrier, call_put_flag, model_name, model_location, model_scale):
        """ Barrier Option. Compulsory input arguments:
        Payoff Parameters:
            + strike = a positive number representing the strike of the option
            + barrier = a positive number representing the barrier value
            + call_put_flag = 1 or -1 for representing the payoff type (put or call)
        Model Parameters:
            + model_name = a string identifying the model
            + model_location = a positive number representing the location parameter
            + model_scale = a positive number representing the scale parameter
        """
        assert abs(int(call_put_flag))==1, "CallPutFlag can be either 1 or -1"
        self.name = "Barrier Call Payoff" if int(call_put_flag)==1 else "Barrier Put Payoff"
        assert (isinstance(strike,int) or isinstance(strike, float)) and strike>=0, "strike must be a positive number"
        assert (isinstance(barrier,int) or isinstance(barrier, float)) and call_put_flag*(barrier-strike)>=0.0, "(barrier-strike)*Call_Put_Flag must be a positive number"
        self.pars = Barrier.Parameters(strike, barrier, call_put_flag)

        model = Barrier._model_pars_check_in(model_name, model_location, model_scale)
        self.model = Barrier.Model(*model)

    def payoff_function(self, underlying):
        """ Payoff Function:
        Input: underlying (a positive number)
        Output: max{Call_Put_Flag*(x-K),0} if Call_Put_Flag*(x-B)<0 else 0
        """
        assert (isinstance(underlying,int) or isinstance(underlying, float)) and underlying>=0, "underlying must be a positive number"
        return max((underlying - self.pars.K)*self.pars.Call_Put_Flag, 0.0) if (underlying-self.pars.B)*self.pars.Call_Put_Flag < 0.0 else 0.0

