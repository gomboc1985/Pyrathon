
# Author: Matteo L. BEDINI
# Date: April 2016

###########################################################################
##                              MAIN MODULE                              ##
###########################################################################

import xml.etree.ElementTree as etree
import datetime
import json
import os

import PayoffFactory
import DealDealer

def PortfolioProcessor(filename):
    """ Function PortfolioProcessor.
    Input Argument: filename (string). Name of the XML file containing the portfolio
    Output: Nothing. A log file (log.txt) is produced alongside with an output XML
    containing the priced portfolio.
    """

    #STEP 0: PRELIMINARIES    
    assert isinstance(filename, str), "filename must be a string"
    log_name = "log.txt"
    
    log_header = "PortfolioProcessor LOG: " + filename + " - " + datetime.datetime.now().isoformat() + "\n"
    with open(log_name, mode="w", encoding="utf-8") as f:
        f.write(log_header.upper())    

    # Default settings #TODO BETTER
    settings = {"x_min":0.01, "x_step":0.5, "x_max":100.01}
    log_settings = "\nDefault Settings: " + str(settings) + "\n"
    with open(log_name, mode="a", encoding="utf-8") as f:
        f.write(log_settings)

    # Default pricing configuration
    pricing_configuration = get_default_pricing_configuration()

    # Getting pricing configuration
    config_file_name = "pricing_configuration.json"
    log_pricing_configuration = "\n\nLoading Pricing Configuration file: " +  config_file_name +"\n"
    with open(log_name, mode="a", encoding="utf-8") as f:
        f.write(log_pricing_configuration)
        try:
            with open(config_file_name, "r", encoding="utf-8") as json_pr_config:
                pricing_configuration = json.load(json_pr_config)
                f.write("Pricing Configuration loaded successfully: \n")
                f.write(str(pricing_configuration) + "\n")
        except ValueError as verr:
            f.write("A ValueError occurred while reading Pricing Configuration file: " +  str(verr.args)+"\n")
            f.write("Applying default settings\n")
        except:
            f.write("A problem occurred while reading Pricing Configuration file: " +  config_file_name +"\n")
            f.write("Applying default settings\n")
        f.write("\n")
    

    # XML Parsing
    with open(log_name, mode="a", encoding="utf-8") as f:
        try:
            input_portfolio = etree.parse(filename)
        except FileNotFoundError as ferr:
            f.write("A FileNotFoundError occurred while parsing file: " +  filename +"\n")
            f.write("Details: " +  str(ferr.args)+"\n Exiting Portfolio Processor\n")
            return
        except xml.etree.ParseError as xerr: #If the XML is not well-formed an "xml.etree.ParseError" is launched
            f.write("A xml.etree.ParseError occurred while parsing file: " +  filename +"\n")
            f.write("Details: " +  str(xerr.args)+"\n Exiting Portfolio Processor\n")
            return
        except:
            f.write("A Problem occurred while parsing file: " +  filename +"\n")
            f.write("Details not available \n Exiting Portfolio Processor\n")
            return

    root = input_portfolio.getroot()

    #portfolio as a list of deals (see below)
    portfolio = list()

    #STEP 1: BEGINNING OF LOADING OPERATION
    with open(log_name, mode="a", encoding="utf-8") as f:
        f.write("Loading deals in portfolio: \n")
        deal_counter = 0
        
        for child in root:
            f.write("Scanning element: " + str(child) + "\n")
            
            # CASE 1: We get a payoff
            if child.tag == "Payoff":
                try:
                    payoff_raw_info = child.attrib["type"]
                    if payoff_raw_info.endswith("Call"):######
                        payoff_type = payoff_raw_info[:-4]   #
                        put_call_flag = 1                    #
                    elif payoff_raw_info.endswith("Put"):    # Not very nice: space for improvement but I've no time for it
                        payoff_type = payoff_raw_info[:-3]   # 
                        put_call_flag = -1                   #
                    else:                                    #
                        raise ValueError######################

                    assert payoff_type in pricing_configuration, payoff_type + " cannot be priced.\n"

                    params_label = [k for k in pricing_configuration[payoff_type] if k!="model"]
                    payoff_params = list() #list of tuple (param name, param val)
                    for par in params_label:
                        payoff_params.append((par, float(child.find(par).text)))

                    deal_ID = child.find("dealID").text

                    model_name = child.find("model").get("distribution")
                    model_scale = float(child.find("model").find("scale").text)
                    model_location = float(child.find("model").find("location").text)
                    
                    f.write("-------------------------------------------------------------------\n")
                    f.write("Payoff "+ payoff_raw_info + " loaded successfully. Import summary: \n")
                    f.write("  Payoff type: " + payoff_type + "\n")
                    f.write("  Call Put Flag: " + str(put_call_flag) + "\n") 
                    f.write("  Payoff parameters: " + str(payoff_params) + "\n")
                    f.write("  Payoff model name: " + model_name + "\n")
                    f.write("     Model location: %g" % model_location + "\n")
                    f.write("     Model scale: %g" % model_scale + "\n")
                    f.write("-------------------------------------------------------------------\n")

                    params = dict(payoff_params)
                    params["call_put_flag"]=put_call_flag
                    params["model_name"]=model_name
                    params["model_scale"]=model_scale
                    params["model_location"]=model_location
                    deal = PayoffFactory.PayoffFactory(payoff_type, params)

                    #following two attributes added on-the-fly
                    deal.type = payoff_type
                    deal.ID = deal_ID

                    portfolio.append(deal)

                    deal_counter +=1

                # Following could be done better    
                except AssertionError as aerr:
                     f.write("An AssertionError occurred while reading payoff:" + str(child.attrib) +"\n")
                     f.write("Assertion: " + str(aerr.args) + ".\n")
                except ValueError as verr:
                     f.write("A ValueError occurred while reading payoff:" + str(child.attrib) +"\n")
                     f.write("Value " + str(verr.args) + " not valid.\n")
                except KeyError as kerr:
                     f.write("A KeyError occurred while reading payoff:" + str(child.attrib) +"\n")
                     f.write("Key " + str(kerr.args) + " not found.\n")
                except TypeError as terr:
                     f.write("A TypeError occurred while reading payoff:" + str(child.attrib) +"\n")
                     f.write("Type " + str(terr.args) + " not valid.\n")
                except:
                    f.write("A problem occurred while reading payoff:" + str(child.attrib) +"\n")
                    
            # CASE 2: We get some custom pricing settings
            elif child.tag == "PricingSettings":
                try:
                    # Reading default settings
                    x0    = child.find("x0").text
                    xStep = child.find("xStep").text
                    xMAX  = child.find("xMAX").text
                    x_min  = float(x0)
                    x_step = float(xStep)
                    x_max  = float(xMAX)
                    ## Logging settings info
                    f.write("Overwriting default settings: \n x_min: %s \n x_step: %s \n x_max: %s" %(x0,xStep,xMAX))
                    f.write("\n")
                    ## Overwriting default settings
                    settings["x_min"]  = x_min
                    settings["x_step"] = x_step
                    settings["x_max"]  = x_max
                except:
                    f.write("A problem occurred while parsing custom pricing settings found in " + child.tag +"\n")
                    f.write("Applying default settings\n")
                    
            # CASE 3: We get some spam
            else:
                f.write("  ... unrecognized child element found ... \n")

        #END OF LOADING OPERATION
        f.write("\nLoading operation completed...\n")
        f.write("   ...%d deals loaded are ready to be priced.\n" %deal_counter)


    #STEP 2: BEGINNING OF PRICING OPERATION
    with open(log_name, mode="a", encoding="utf-8") as f:
        f.write("\nBeginning pricing operations: \n")
        
        for deal in portfolio:
            try:
                f.write("\nDeal: " + str(deal) + "\n")
                pricing_method = pricing_configuration[deal.type]["model"][deal.model.name]
                f.write("Pricing Method: " + pricing_method + " \n")
                DealDealer.deal_pricer(deal, pricing_method, settings)
                f.write("\nDeal priced successfully. Price = %f \n" % deal.price)
            except: ## Exception operation should be done better (not enough info for debugging: but I'm too much in a hurry
                f.write("A problem occurred while pricing deal " + str(deal) +"\n")
            print(deal)


    print("\n \n ***** DONE ***** \n \n ")



def get_default_pricing_configuration():
    d = ({
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
                "Gamma": "exact_eval", 
                "LogNormal": "exact_eval", 
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
    return d

filename = "DerivativeCatalog.xml"
PortfolioProcessor(filename)
