"""
This file contains functions to process user input.
"""
# return integer user input
class Input:
    """
    This class provides methods to process user input
    """
    def get_int(self, message='Enter your number: ', default=0, warning=''):
        """
        Accepts only integers 
        """
        hasInputNumbers = False 
        while hasInputNumbers==False: 
            try: # try to convert user input into a integer  number 
                userInput = input(message)
                if userInput is '':
                    if default == 0:
                        message = message+'\r'
                        continue
                    else:
                        return default
                userInput = int(userInput)
                hasInputNumbers=True
                return userInput
            except ValueError: # if it gives a ValueError, return to line 2!
                print("[!] invalid input try again")

    # return floating point user input
    def get_float(self, message='Enter your number: ', default=0,warning=''):
        """
        Accepts integer and floating point numbers
        """
        hasInputNumbers = False 
        while hasInputNumbers==False: 
            try: # try to convert user input into a floating number 
                userInput = input(message)
                if userInput is '':
                    if default == 0:
                        continue
                    else:
                        return default
                userInput = float(userInput)
                hasInputNumbers=True
                return userInput
            except KeyboardInterrupt :
                raise
            except ValueError: # if it gives a ValueError, return to line 2!
                print("[!] invalid input try again")
    
    def get_coin(self, message='Enter Coin symbol : ', default='', warning=''):
        """
        Accepts Coin Symbol
        """
        return input(message)
        #TODO: Logic need to be implimented