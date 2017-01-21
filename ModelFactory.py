
# Author: Matteo L. BEDINI
# Date: April 2016

import KnownModels

def ModelFactory(model_name, location, scale):
    """ function ModelFactory

    input: model_name: a string of a model name
           location: the location parameter of the distribution
           scale: the scale parameter of the distribution
           
    output: a known model
    """

    assert isinstance(model_name, str), "model_name must be a string"
    assert (isinstance(location,int) or isinstance(location, float)) and location>0, "location must be a positive number"
    assert (isinstance(scale,int) or isinstance(scale, float)) and scale>0, "scale must be a positive number"  
    
    this_model = None
    model_type = getattr(KnownModels,model_name) # an AttributeError may be launched if model_name is not valid
    this_model = model_type(location, scale) #an AssertionError may be launched if the type/value of the parameters is not correct
    
    return this_model
