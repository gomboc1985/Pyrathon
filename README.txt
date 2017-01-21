Title: Python POC: Portfolio Processor

Objective: The goal of the project is NOT to display a particular ability in using Python but, rather, to display how quickly it has been learnt and used.

0. Summary.
This toy-project aims at demonstrating how the author has been able to quickly learn Python: starting from a 0 knowledge, in less than 50 working hours scattered in 10 working days (working after a full-time actual work), the author has read the book "Think Python - How to Think Like a Computer Scientist" by Allen Downey, completed the 95% of its exercise and written this project. The goal of the project is to use Python in a variety of common tasks such as writing a file, reading a JSON and an XML. In this particular case the project deals with the problem of pricing simple derivatives payoff using two different methods.

1. Problem
A system named "LibraryA" provides an XML-file containing a portfolio of derivatives. LibraryA is not able to compute their exact prices, for which The Company uses another system called "LibraryB".
The objective is to write some integration code (in Python) between LibraryA and LibraryB.

2. LibraryA
LibraryA is a Python-written library whose entrance point is the module "PortfolioProcessor". That module contains a function reading the input XML file, browsing nodes of type "Payoff", and reads all the nodes of the XML according to the system settings (saved in a JSON file). This operation uses a PayoffFactory (see homonymous module). Payoffs are imported through a "DealDealer" module which is responsible of choosing the pricing method according to the payoff type.
For some deals the system relies on the approximate pricing method provided by LibraryA, other can be priced more accurately by using LibraryB (see the "PricingMethods" module).

3. Pricing methods
For the sake of simplicity we assume that every payoff is a positive, real-valued random variable. The theoretical price, $y$ of a derivative is computed as the integral on the positive real line of the product function $f(x)p(x)$ with respect to the Lebesgue measure $dx$, where $f$ is the function describing the payoff and $p$ is the probability density function of the underlying.
3.1 Approximate method.
LibraryA approximate the price with a numerical method on grid whose nodes $x_n$ and discretization step $h$ can be configured by the user.
3.2 Exact method.
LibraryB (Microsoft Excel) provides closed-form formula for digital payoff for known probability distributions.

4. Running and testing
At each run, the program creates a log-file and a module, "PayoffTester", contains some Unit Test.
