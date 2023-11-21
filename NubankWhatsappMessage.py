
#######################
### Package imports ###
#######################

# Import packages
from datetime import datetime
import pandas as pd
import time
pd.set_option('display.max_columns', None)

# Import customized codes
from util.Util import Util
from api.NubankAPI import NubankAPI






############################
### Script configuration ###
############################


# Phone numbers
PHONE_TO_SEND = "XXXX"

# Monthly limits
expectedMonthlyLimit = 4500


# Date definition
dateString     = str(datetime.now().strftime('%Y-%m-%d'))
dateTimeString = str(datetime.now().strftime('%Y-%m-%d HH:MM'))


# File path definitions
billsPath = "path to save your bills file"
cardStatementsPath = "path to save your card statements"







##############
### Start! ###
##############


Util.writeLog("[Nubank Main] Staring script execution")


### Phase 1: Downloading files

try: 
    Util.writeLog("[Nubank Main] Authenticating with Nubank")
    nuSession = NubankAPI.authenticate()

    Util.writeLog("[Nubank Main] Downloading card statements")
    cardStatementsDownload = NubankAPI.downloadCardStatements(nuSession, cardStatementsPath)

    if(cardStatementsDownload == False):
        Util.writeLog("[Nubank Main][ERROR] Error when downloading card statements")
        exit()

    time.sleep(5)

    Util.writeLog("[Nubank Main] Downloading bills")
    billsDownload = NubankAPI.downloadBills(nuSession, billsPath)
    
    if(billsDownload == False):
        Util.writeLog("[Nubank Main][ERROR] Error when downloading bills")
        exit()

except Exception as ex:
    Util.writeLog("[Nubank Main][ERROR] Error when executing main script. Error: " + str(ex))
    exit()





### Phase 2: Preparing infos

Util.writeLog("[Nubank Main] Preparing infos to be shared")

alertMessage = ""
try:
    dfCardStatements = pd.read_excel(cardStatementsPath)
    dfBills = pd.read_excel(billsPath)

    currentMonthBill        = NubankAPI.getCurrentMonthBill(dfBills)
    previousMonthBill       = NubankAPI.getPreviousMonthBill(dfBills)
    nextMonthBill           = NubankAPI.getNextMonthBill(dfBills)
    amountSpentCurrentCycle = NubankAPI.getAmountSpentCurrentCycle(dfCardStatements)
    strPreviousTxns         = NubankAPI.getPreviousTxnsString(dfCardStatements)
    
    alertMessage = NubankAPI.getNubankAlertMessage(amountSpentCurrentCycle, currentMonthBill, previousMonthBill, nextMonthBill, strPreviousTxns, monthLimit = expectedMonthlyLimit)
    Util.writeLog("[Nubank Main] Preparing infos to be shared")

    print()
    print(alertMessage)
    print()

except Exception as ex:
    Util.writeLog("[Nubank Main][ERROR] Error when executing main script. Error: " + str(ex))
    exit()





### Phase 3: Send WA message

try: 
    # message to be sent
    Util.writeLog("[Nubank Main] Sending WhatsApp message")
    Util.sendWhatsMessageInstantly(PHONE_TO_SEND, alertMessage)

    Util.writeLog("[Nubank Main] Script executed successfully")

except Exception as ex:
    Util.writeLog("[Nubank Main][ERROR] Error when executing main script. Error: " + str(ex))
    exit()