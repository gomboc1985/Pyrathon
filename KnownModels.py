
# Author: Matteo L. BEDINI
# Date: April 2016

import math

###########################################################################
##                          GENERIC RECOGNIZED PDF                       ##
###########################################################################

class RecognizedPDF:
    
    def __init__(self, location, scale):
        assert (isinstance(location,int) or isinstance(location, float)) and location>0, "location must be a positive number"
        assert (isinstance(scale,int) or isinstance(scale, float)) and scale>0, "scale must be a positive number"
        self.location = location
        self.scale = scale

    def pdf(self, x):
        pass


###########################################################################
##                                GAMMA PDF                              ##
###########################################################################

class GammaPDF(RecognizedPDF):    

    def pdf(self, x):
        """ Gamma probability density function evaluated at x.
            (see, e.g., https://en.wikipedia.org/wiki/Gamma_distribution)

            Input arguments:
            + x: a positive number.
            + location: a positive number representing the location parameter of the gamma pdf.
            + scale: a positive number representing the scale parameter of the gamma pdf

            Output:
            + The Gamma PDF evaluated at x.
        """
        assert 0<=x, "x must be positive"
        return pow(x,self.location-1)*math.exp(-x/self.scale)/(math.gamma(self.location)*pow(self.scale, self.location))


###########################################################################
##                            LOGNORMAL PDF                              ##
###########################################################################

class LogNormalPDF(RecognizedPDF):

    x_min = 1.e-5
    x_tol = 1.e-5

    def pdf(self, x):
        """ Lognormal probability density function evaluated at x.
            (see, e.g., https://en.wikipedia.org/wiki/Log-normal_distribution)

            Input arguments:
            + x: a positive number.
            + location: a positive number representing the location parameter of the lognormal pdf.
            + scale: a positive number representing the scale parameter of the lognormal pdf

            Output:
            + The Lognormal PDF evaluated at x.
        """
        assert 0<=x, "x must be positive"
        y = x_min if abs(x-LogNormalPDF.x_min)<=LogNormalPDF.x_tol else x # if we are too close to 0 round to x_min
        return math.exp(-pow(math.log(y)-self.location,2)/(2*self.scale**2)) / (y*self.scale*math.sqrt(2*math.pi))


###########################################################################
##                            UNIFORM PDF                                ##
###########################################################################

class UniformPDF(RecognizedPDF):    

    def pdf(self, x):
        """ Uniform probability density function evaluated at x.
            (see, e.g., https://en.wikipedia.org/wiki/Uniform_distribution_(continuous))

            Input arguments:
            + x: a positive number.
            + location: a positive number representing the location parameter of the gamma pdf.
            + scale: a positive number representing the scale parameter of the gamma pdf

            Output:
            + The Uniform PDF evaluated at x.
        """
        assert 0<=x, "Invalid input value for x"
        a = self.location-math.sqrt(3*self.scale)
        b = self.location+math.sqrt(3*self.scale)
        return 1 / (b -a) if a<= x <=b else 0.0
    

    
