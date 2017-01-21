
# Author: Matteo L. BEDINI
# Date: April 2016

import ModelFactory
import os

###########################################################################
##                   GRID EVALUATION FUNCTION                            ##
###########################################################################

def grid_eval(payoff, settings):
    """ Numerical approximation for payoff pricing.
    """

    x_min = settings["x_min"]
    x_step = settings["x_step"]
    x_max = settings["x_max"]
    
    assert (isinstance(x_min,int) or isinstance(x_min, float)) and x_min>=0, "x_min must be a positive number"
    assert (isinstance(x_step,int) or isinstance(x_step, float)) and x_step>0, "x_step must be a positive number"
    assert (isinstance(x_max,int) or isinstance(x_max, float)) and x_max>=x_min+x_step, "x_max must be greater than x_min+x_step"

    x = list()
    x_i = x_min
    while x_i <= x_max: 
        x.append(x_i)
        x_i += x_step
    
    model_name = payoff.model.name + "PDF"
    model = ModelFactory.ModelFactory(model_name, payoff.model.location, payoff.model.scale)

    #trapezoidal integration rule
    integral = [payoff.payoff_function(x_i) * model.pdf(x_i)*x_step for x_i in x]
    price = sum(integral)-0.5*(integral[0] + integral[-1])
    return price

    
###########################################################################
##                   EXACT EVALUATION FUNCTION                           ##
###########################################################################

def exact_eval(payoff, settings):
    """ Exact computation of payoff price.
    """
    try:

        payoff_name = payoff.name
        model_name = payoff.model.name
        import xlwings as xw
        wb = xw.Workbook()
        
        xw.Range("A1").value=payoff_name
        xw.Range("A1").value=model_name
        
        xw.Range("A2").value="strike"
        xw.Range("A3").value="location"
        xw.Range("A4").value="scale"
        xw.Range("B2").value = payoff.pars.K
        xw.Range("B3").value = payoff.model.location
        xw.Range("B4").value = payoff.model.scale

        xw.Range("A5").value="price"
        # this if-else is ugly but I've no time to make it better for such a simple situation
        # I have used better techniques elsewhere in this project
        if model_name=="Gamma":
            xw.Range("B5").formula="=GAMMA.DIST(B2,B3,B4,TRUE)"
        else:
            xw.Range("B5").formula="=LOGNORM.DIST(B2,B3,B4,TRUE)"
            
        price = xw.Range("B5").value
        #some stuff on automatic recalc should be considered in order to ensure proper execution
        #of calculation operation but I won't check now the scarce documentation of xlwings
        #print(price)

        excel_file_name = payoff_name + "_" + model_name + ".xlsx"
        wkdir = os.getcwd()
        wb.save(wkdir+"\\"+excel_file_name)
        wb.close

        # if it is a digital put we're done, otherwise:
        actual_price = price if payoff.pars.Call_Put_Flag==-1 else 1.0-price

        return actual_price
    
    except ImportError:
        # here it could be a good idea to advise the user if something went wrong
        return grid_eval(payoff, settings)

    
    return 0.0
