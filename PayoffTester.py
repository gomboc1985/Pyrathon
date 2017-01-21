
# Author: Matteo L. BEDINI
# Date: April 2016

###########################################################################
##                              TEST MODULE                              ##
###########################################################################

import unittest

import DealDealer
import DerivativePayoff

# pricing configuration is the default one (grid_eval)
pricing_config = ({
    "PlainVanilla":
    {
        "strike": "",
        "model":
        {
            "Gamma": "grid_eval", 
            "LogNormal": "grid_eval", 
            "Uniform": "grid_eval"
        }
    },

    "Digital": 
    {
        "strike": "",
        "model":
        {
            "Gamma": "grid_eval", 
            "LogNormal": "grid_eval", 
            "Uniform": "grid_eval"
        }
    },

    "Barrier": 
    {
        "strike": "",
        "barrier": "",
        "model":
        {
            "Gamma": "grid_eval", 
            "LogNormal": "grid_eval", 
            "Uniform": "grid_eval"
        }
    }
})

#grid settings is the default one
settings = {"x_min":1.0, "x_step":0.5, "x_max":100.0}

class KnownPayoffValues(unittest.TestCase):   
    ### TEST FOR CHECKING THE RESULT IS OK ###
    
    def test_to_known_values_pv_call(self):
        """DealDealer should price correctly a Plain Vanilla Call"""  
        pv_call_1 = DerivativePayoff.PlainVanilla(10.0,1,"Uniform",10.0,3)

        known_price = 0.875

        pric_meth = pricing_config["PlainVanilla"]["model"][pv_call_1.model.name]
        DealDealer.deal_pricer(pv_call_1, pric_meth, settings)

        self.assertAlmostEqual(pv_call_1.price, known_price,4)
            
            
    def test_to_known_values_pv_put(self):
        """DealDealer should price correctly a Plain Vanilla Put"""     
        pv_put_1 = DerivativePayoff.PlainVanilla(15.0,-1,"Gamma",9.0,3.0)

        known_price =  0.16159367585336953
        
        pric_meth = pricing_config["PlainVanilla"]["model"][pv_put_1.model.name]
        DealDealer.deal_pricer(pv_put_1, pric_meth, settings)
            
        self.assertAlmostEqual(pv_put_1.price, known_price,4)


    def test_to_known_values_digital(self):
        """DealDealer should price correctly a Digital Call"""     
        digi_call_1 = DerivativePayoff.Digital(7.0,1,"LogNormal",10.0,3.0)

        known_price =  0.03256
        
        pric_meth = pricing_config["Digital"]["model"][digi_call_1.model.name]
        DealDealer.deal_pricer(digi_call_1, pric_meth, settings)
            
        self.assertAlmostEqual(digi_call_1.price, known_price,4)

            
    def test_to_known_values_barrier(self):
        """DealDealer should price correctly a Barrier Call""" 
        barrier_call_1 = DerivativePayoff.Barrier(15.0,20.0,1,"LogNormal",15.0,3.0)

        known_price = 2.4134880177084893e-05

        pric_meth = pricing_config["Barrier"]["model"][barrier_call_1.model.name]
        DealDealer.deal_pricer(barrier_call_1, pric_meth, settings)

        self.assertAlmostEqual(barrier_call_1.price, known_price,2)


    
class BadPVCallInput(unittest.TestCase):
    ### TEST FOR BAD INPUT CHECKING ###
    
    def test_bad_input_pv_call_strike(self):
        """DerivativePayoff should check proper input parameters"""  
        self.assertRaises(AssertionError, DerivativePayoff.PlainVanilla, *(-5,1,"Uniform",10.0,3))

    def test_bad_input_pv_call_CPflag(self):
        """DerivativePayoff should check proper input parameters"""  
        self.assertRaises(AssertionError, DerivativePayoff.PlainVanilla, *(10.0,3,"Uniform",10.0,3))

    def test_bad_input_pv_call_model(self):
        """DerivativePayoff should check proper input parameters"""  
        self.assertRaises(AssertionError, DerivativePayoff.PlainVanilla, *(-5,1,[1,2,4],10.0,3))

    def test_bad_input_pv_call_nof_arg(self):
        """DerivativePayoff should check proper input parameters"""  
        self.assertRaises(TypeError, DerivativePayoff.PlainVanilla, *(10.0,3,"Uniform"))



########## HERE I COULD CONTINUE FOR TOO MUCH: THIS IS JUST A TINY POC! SO I'LL STOP TESTING HERE
   
if __name__=="__main__":
    unittest.main()
