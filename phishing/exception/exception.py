import os 
import sys
from phishing.logging.custom_logger import logging

class PhishingException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occures script name [{0}] in line no [{1}] error message [{2}]".format(
            self.filename,self.lineno,str(self.error_message)
        )
    
# if __name__ == "__main__":
#     try:
#         logging.info("Exception handling")
#         a = 1/0
#     except Exception as e:
#         raise PhishingException(e,sys)