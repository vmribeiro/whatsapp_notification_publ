
# Get path from files
import inspect
import sys
import os
runtimePath = inspect.stack()[1].filename
runtimePath = os.path.abspath(runtimePath).split('<')[0]
sys.path.append(runtimePath)


# Import packages
from datetime import datetime, timedelta



# Class definition
class Util:
    """
    Class used to centralize methods that are
    frequently used throughout the project
    """
    


    def writeLog(text, fileName = "#"):
        """
        Writes a log in a txt file and prints in console

        * Default file: util/logs/log_YYYY-MM-DD.txt
        """
        
        dateString = str(datetime.now().strftime('%Y-%m-%d'))
        dateTimeString = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        try:
            if fileName == "#":
                fileName = str(runtimePath) + "util/logs/log_" + dateString + ".txt"

            with open(fileName, 'a') as file:
                file.write("[" + dateTimeString + "]" + text + '\n')
            
            file.close()

            print("[" + dateTimeString + "]" + text)

        except Exception as ex:
            print("[" + dateTimeString + "]" + "[Util][ERROR] Error when writing log. Error: " + str(ex))
            return False
        
        return True
    



    def sendWhatsMessageInstantly(phone, message):

        """
        Sends a whatsapp message using pywhatkit (need to open browser)
        """
        import pywhatkit # Documentation: https://github.com/Ankit404butfound/PyWhatKit/wiki/Sending-WhatsApp-Messages

        try:
            # sendwhatmsg_instantly(phone_no: str, message: str, wait_time: int = 15, tab_close: bool = False, close_time: int = 3) -> None
            pywhatkit.sendwhatmsg_instantly(phone, message, 15, True, 4)
            Util.writeLog("[Util] WhatsApp message sent")

        except Exception as ex:
            Util.writeLog("[Util][ERROR] Error when sending WhatsApp message. Error: " + str(ex))
            return False
        
        return True
    



    def getMonthYear(date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m')




    def getNextMonth(month_str):
        date_obj = datetime.strptime(month_str, '%Y-%m')
        next_month = date_obj + timedelta(days=31)  # Adding a number of days more than a month
        return next_month.strftime('%Y-%m')




    def getPreviousMonth(month_str):
        date_obj = datetime.strptime(month_str, '%Y-%m')
        next_month = date_obj - timedelta(days=31)  # Adding a number of days more than a month
        return next_month.strftime('%Y-%m')




    def formatDate(row):
        return datetime.strptime(str(row['time']).split('T')[0], '%Y-%m-%d')




    def formatFloat(row, column_name):
        if str(row[column_name]).replace(' ', '').replace('None', 'nan') == 'nan':
            return float(0)
        else:
            return float(str(row[column_name]).replace(' ', ''))/100    



    
    def containsAnyString(s, string_list):
        return any(string in s for string in string_list)





