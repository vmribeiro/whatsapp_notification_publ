# Get path from files
import inspect
import sys
import os
runtimePath = inspect.stack()[1].filename
runtimePath = os.path.abspath(runtimePath).split('<')[0]
sys.path.append(runtimePath)

# Import packages
from pynubank import Nubank, MockHttpClient
from datetime import datetime
import pandas as pd
import json

# Import customized codes
from util.Util import Util


class NubankAPI:
    """
    Class with objective of connecting and managing 
    API calls to Nubank using private account
    """



    def authenticate():
        """
        Authenticates with Nubank and returns
        an authenticated object
        """

        try:
            Util.writeLog("[Nubank API] Executing Nubank authentication")

            credentialsFile = open(r'add here the location with your json credentials!')
            credentials     = json.load(credentialsFile)
            cpf             = str(credentials['cpf'])
            password        = str(credentials['password'])

            nu = Nubank()
            nu.authenticate_with_cert(cpf, password, r'add here the location of where to find the certificate')

            Util.writeLog("[Nubank API] Authenticated successfully")

            return nu
        
        except Exception as ex:
            Util.writeLog("[Nubank API] Error during Nubank authentication. Error: " + str(ex))
            return False




    def treatSource(row):
        source_str = str(row['description'])
        
        if Util.containsAnyString(source_str, ['DROGA', 'DRUG', 'FARMA', 'PANVEL', 'RAIA']):
            return 'Farmácia'
        elif Util.containsAnyString(source_str, ['VANESSA', 'STUDIO', 'TIM', 'FMU']):
            return 'Vanessa - Adhoc'
        elif Util.containsAnyString(source_str, ['ALIEXPRESS', 'AMAZON.COM.BR', 'MERCADOLIVRE', 'MP *', 'PAYPAL', 'SHOPEE', 'MERCADO LIVRE']):
            return 'Ecommerce'
        elif Util.containsAnyString(source_str, [ 'ADIDAS', 'CEA', 'FASHION', 'SHEIN', 'ZARA', 'AMARO', 'GRECO'
                                            , 'BOTICARIO', 'DIOR', 'IKESAKI', 'RENNER', 'CABELEIREIRO'
                                            , 'NATURA', 'LIVESTORE', 'LUPO', 'AUTHENTIC', 'PROMEX'
                                            , 'RIACHUELO', 'BARBEARIA', 'COSMETIC', 'PRIVALIA']):
            return 'Roupas, Cosmeticos & Estética'
        elif Util.containsAnyString(source_str, [  'MAXXI', 'ASSAI', 'ASSB', 'ATACADAO', 'CARREFOUR'
                                            , 'CENTER CARNES', 'CEREHALLI', 'HORTUS', 'HORTIFRUTI', 'QUITANDA'
                                            , 'MERCAD', 'SENDAS', 'ROD RAF', 'SERGIO MARTIN', 'PET' ]):
            return 'Mercado'
        elif Util.containsAnyString(source_str, [  'AUTO POSTO', 'BERLINF', 'CENTRO AUTOMOTIVO', 'POSTO', 'BALIZA PARK'
                                            , 'CBC SHOPPING', 'ECOVIA', 'ESTAC', 'ESTAPAR', 'GARAGE', 'GLOBE PARK'
                                            , 'OPERADORA DE SHOPPING', 'ALIANSCE', 'AUTOPOSTO']):
            return 'Gasolina, Pedágio e Estacionamento'
        elif Util.containsAnyString(source_str, [    'ACAI HYPE', 'ADISER COMERCIO DE ALI', 'BACIO', 'BK DRIVE', 'BUBLEKILL', 'BOA PRACA'
                                                , 'BURGUER KING', 'BURGER KING', 'BURGMAN ', 'CACAU SHOW', 'CAFE', 'CHALEZINHO', 'CHINA DA SERRA'
                                                , 'DELIVERY', 'EMPORIO', 'DRIVE SAO PAULO', 'BURGER', 'CHICKEN', 'FRUTTA E CREMA', 'GIRAFFAS'
                                                , 'ITAIM FOODS', 'KOP', 'LA GUAPA', 'LADOLCE VITA', 'LINDT', 'MC DONALDS', 'MOOI MOOI'
                                                , 'PRETZEL', 'OUTBACK', 'SPOLETO', 'KFC', 'JUAREZ', 'GASTRONOMIA', 'DOCE', 'MINTCHICROISSANT'
                                                , 'OAKBERRY', 'BUFFET', 'PIADINA', 'PASTEIS', 'RCIDADE'
                                                , 'REI DO MATE', 'IFOOD', 'RAPPI', 'IFD', 'DULADU', 'VIOLETA', 'STARBUCKS', 'VILLAGRANO'
                                                , 'TEMAKI']):
            return 'Restaurantes & Delivery'
        elif Util.containsAnyString(source_str, ['PORTO VILLARES', 'LAVILLE', 'PORTO VILARE', 'PADARIA', 'JOHNPAESLTDA']):
            return 'Padaria'
        elif Util.containsAnyString(source_str, [  'ARCO IRIS ROSEIRA', 'CEREJEIRA', 'DECOLAR', 'DL FRANQUIAS', 'DON MACEDO', 'GEYSA NOVELLO'
                                            , 'LAVANDARIO', 'MAIYE RESTAURANTE', 'NETUNO TOURS', 'PARATY', 'PUB VAN GOGH', 'POMONA'
                                            , 'RECANTO' ]):
            return 'Viagem'
        elif Util.containsAnyString(source_str, ['UBER']):
            return 'Uber'
        elif Util.containsAnyString(source_str, [  'AMAZON KINDLE UNLTD', 'AMAZON PRIME', 'AMAZONPRIMEBR', 'APPLE.COM'
                                            , 'MICROSOFT', 'SPOTIFY', 'GOOGLE', 'EC*NIVEL6', 'NETFLIX'   ]):
            return 'Assinaturas'
        elif Util.containsAnyString(source_str, ['CINEMARK', 'UCI', 'INGRESSO.COM', 'CINE']):
            return 'Cinema'
        elif Util.containsAnyString(source_str, ['IPLACE', 'SCHUTZ', 'INGRESSOS']):
            return 'Compras Grandes'
        elif Util.containsAnyString(source_str, [  'ADS PHONE', 'BIKEGO', 'CASA DA MAMAE', 'DAISO', 'RELOJOARIA', 'FOTOPTICA'
                                            , 'LIV CTBA', 'LIVRARIA', 'AMERICANAS', 'MEGA BYT', 'MEI SIM', 'MERCPAGO'
                                            , 'MULTICOISAS', 'MULTIPLAN', 'OTICA', 'JULIANA MASCARENHAS'
                                            , 'PICPAY *', 'BMART', 'ANDREAROMINAFABRI', 'JOSECLEMENTE', 'LEILAOMELCZUK'
                                            , 'CULTURA', 'PATRICIAOLIVEIRA', 'PAULOHENRIQUE', 'PB ADMINISTRA', 'PHOENIX'
                                            , 'PRESENTE', 'RAFIENAJEMABDALLA', 'REIDASCAPAS', 'RENATO PLATERO SIMOES'
                                            , 'OTICA', 'OPTICA', 'PHONE'
                                            ]):
            return 'Outros'
        else:
            if Util.containsAnyString(str(row['title']), ['Transporte']):
                return 'Gasolina, Pedágio e Estacionamento'
            elif Util.containsAnyString(str(row['title']), ['Vestuário']):
                return 'Roupas, Cosmeticos & Estética'
            elif Util.containsAnyString(str(row['title']), ['Supermercado']):
                return 'Mercado'
            elif Util.containsAnyString(str(row['title']), ['Casa', 'Serviços', 'Saúde', 'Lazer']):
                return 'Outros'
            elif Util.containsAnyString(str(row['title']), ['Restaurante']):
                return 'Restaurantes & Delivery'
            elif Util.containsAnyString(str(row['title']), ['Viagem']):
                return 'Viagem'
            return source_str #'Outros'




    def downloadCardStatements(nuSession, filePath = "path to save your card statements"):
        """
        Download card statements from Nubank and save in an excel file
        """
        
        try:
            Util.writeLog("[Nubank API] Downloading card statements")
            
            cardStatements = nuSession.get_card_statements()
    
            # transforming as json to handle first treatment
            cardStatements = json.loads(str(cardStatements).replace("'", '"').replace('False', 'false').replace('True', 'true'))
            
            # transform results into a dataframe
            dfTemp = None
            dfCardStatements = pd.DataFrame({
                'description': ['dummy'],                               
                'category': ['dummy'],     
                'amount': ['dummy'],     
                'time': ['dummy'],     
                'source': ['dummy'],     
                'title': ['dummy'],     
                'amount_without_iof': ['dummy'],     
                'account': ['dummy'],     
                'status': ['dummy'],     
                'num_installments': ['dummy'],     
                'total_installments_amount': ['dummy'],     
                'id': ['dummy'],     
                '_links': ['dummy'],     
                'tokenized': ['dummy'],     
                'href': ['dummy']
            })

            for i in range(0,len(cardStatements)):
                try:
                    num_installments = str(cardStatements[i].get('details')['charges']['count']).replace("'",'').replace('[','').replace(']','')       
                    total_installments_amount = str(cardStatements[i].get('details')['charges']['amount']).replace("'",'').replace('[','').replace(']','')    
                except:
                    num_installments= 0
                    total_installments_amount = 0
                    pass 
                try: 
                    status = str(cardStatements[i].get('details')['status']).replace("'",'').replace('[','').replace(']','')
                except:
                    status = 'not defined'
                    pass
                
                dfTemp = pd.DataFrame(data = {  'description': [str(cardStatements[i].get('description')).replace("'",'').replace('[','').replace(']','')],                               
                                                'category': [str(cardStatements[i].get('category')).replace("'",'').replace('[','').replace(']','')],
                                                'amount': [str(cardStatements[i].get('amount')).replace("'",'').replace('[','').replace(']','')],
                                                'time': [str(cardStatements[i].get('time')).replace("'",'').replace('[','').replace(']','')],
                                                'source': [str(cardStatements[i].get('source')).replace("'",'').replace('[','').replace(']','')],
                                                'title': [str(cardStatements[i].get('title')).replace("'",'').replace('[','').replace(']','')],
                                                'amount_without_iof': [str(cardStatements[i].get('amount_without_iof')).replace("'",'').replace('[','').replace(']','')],
                                                'account': [str(cardStatements[i].get('account')).replace("'",'').replace('[','').replace(']','')],
                                                'status': [status],                                       
                                                'num_installments': [num_installments],
                                                'total_installments_amount': [total_installments_amount],
                                                'id': [str(cardStatements[i].get('id')).replace("'",'').replace('[','').replace(']','')],
                                                '_links': [str(cardStatements[i].get('_links')).replace("'",'').replace('[','').replace(']','')],
                                                'tokenized': [str(cardStatements[i].get('tokenized')).replace("'",'').replace('[','').replace(']','')],
                                                'href': [str(cardStatements[i].get('href')).replace("'",'').replace('[','').replace(']','')]
                                                })
                
                dfCardStatements = pd.concat([dfCardStatements, dfTemp])
            
                dfCardStatements = dfCardStatements[dfCardStatements['description'] != 'dummy']

            # temporary save
            dfCardStatements.to_excel(filePath, index = False)
            Util.writeLog("[Nubank API] Card statements temporary saved at: " + filePath)
            
            dfCardStatements = pd.read_excel(filePath)

            # Applying treatments to dataframe
            Util.writeLog("[Nubank API] Applying treatments to card statements data")

            dfCardStatements                = dfCardStatements.fillna('nan')
            dfCardStatements['description'] = dfCardStatements['description'].astype(str)
            dfCardStatements['category']    = dfCardStatements['category'].astype(str)
            dfCardStatements['source']      = dfCardStatements['source'].astype(str)
            dfCardStatements['title']       = dfCardStatements['title'].astype(str)
            dfCardStatements['title']       = dfCardStatements.apply(lambda row: str(row['title']).capitalize(), axis = 1)
            dfCardStatements['status']      = dfCardStatements['status'].astype(str)
            dfCardStatements['id']          = dfCardStatements['id'].astype(str)
            dfCardStatements['_links']      = dfCardStatements['_links'].astype(str)
            dfCardStatements['tokenized']   = dfCardStatements['tokenized'].astype(str)
            dfCardStatements['href']        = dfCardStatements['href'].astype(str)

            dfCardStatements['time']                      = dfCardStatements.apply(lambda row: '1900-01-01T00:00:00Z' if str(row['time']) == 'nan' else str(row['time']), axis = 1)
            dfCardStatements['transaction_date']          = dfCardStatements.apply(lambda row: Util.formatDate(row), axis = 1)    
            dfCardStatements['amount']                    = dfCardStatements.apply(lambda row: Util.formatFloat(row, 'amount'), axis = 1)   
            dfCardStatements['amount_without_iof']        = dfCardStatements.apply(lambda row: Util.formatFloat(row, 'amount_without_iof'), axis = 1)    
            dfCardStatements['num_installments']          = dfCardStatements.apply(lambda row: Util.formatFloat(row, 'num_installments')*100, axis = 1)    
            dfCardStatements['total_installments_amount'] = dfCardStatements.apply(lambda row: Util.formatFloat(row, 'total_installments_amount'), axis = 1)    

            dfCardStatements['description']    = dfCardStatements.apply(lambda row: str(row['description']).upper().replace('PAG*', ''), axis = 1)
            dfCardStatements['treated_source'] = dfCardStatements.apply(lambda row: NubankAPI.treatSource(row), axis = 1)
            

            columns_to_filter = [
                  'transaction_date'
                , 'time'
                , 'treated_source'
                , 'title'
                , 'description'
                
                , 'amount'
                , 'amount_without_iof'
                , 'category'
                , 'num_installments'
                , 'total_installments_amount'
                , 'status'
                
                , 'id'
                , 'href'
            ]

            dict_columns = {
                'transaction_date'            : 'transaction_date'                                                             
                , 'time'                      : 'transaction_time'                              
                , 'treated_source'            : 'treated_source'                              
                , 'title'                     : 'nubank_suggested_source'                              
                , 'description'               : 'transaction_title'                  
                , 'amount'                    : 'amount'                              
                , 'amount_without_iof'        : 'amount_without_iof'                              
                , 'category'                  : 'transaction_type'                              
                , 'num_installments'          : 'num_installments'                              
                , 'total_installments_amount' : 'total_installments_amount'                                
                , 'status'                    : 'status'                        
                , 'id'                        : 'id'                              
                , 'href'                      : 'href'                              
            }
            
            dfCardStatements = dfCardStatements.filter(items = columns_to_filter)
            dfCardStatements = dfCardStatements.rename(columns = dict_columns)
            dfCardStatements['treated_amount'] = dfCardStatements.apply(lambda row: float(row['amount']) if float(row['num_installments']) == float(0.0) else float(row['total_installments_amount']), axis = 1)
            dfCardStatements['snapshot'] = datetime.now()

            Util.writeLog("[Nubank API] Card statements successfully transformed into a DataFrame")

            dfCardStatements.to_excel(filePath, index = False)
            Util.writeLog("[Nubank API] Card statements saved at: " + filePath)

            return True

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error during card statements download. Error: " + str(ex))
            return False
        



    def downloadBills(nuSession, filePath = "path to save your bills file"):

        try:
            Util.writeLog("[Nubank API] Downloading bills (faturas)")
            
            # downloading bills (faturas) from nubank
            bills = nuSession.get_bills()
            
            # transforming as json to handle first treatment
            bills = json.loads(str(bills).replace("'", '"').replace('False', 'false').replace('True', 'true'))

            # Initialize an empty list to store results
            results = []

            # Iterate over each item in the JSON data to get current, previous and next month bills
            for item in bills:
                state = item['state']
                close_date = item['summary']['close_date']
                total_balance = float(item['summary']['total_balance']) / 100  # Convert to float and divide by 100
                remaining_balance = 0
                try: 
                    remaining_balance = float(item['summary']['remaining_balance'])
                except Exception:
                    pass

                # Check if the bill is open
                if state == 'open' and Util.getMonthYear(close_date) == datetime.now().strftime('%Y-%m'):
                    results.append({'closed_month': Util.getMonthYear(close_date), 'total_balance': total_balance, 'status': state})
                elif state == 'future' and Util.getMonthYear(close_date) == Util.getNextMonth(datetime.now().strftime('%Y-%m')):
                    results.append({'closed_month': Util.getMonthYear(close_date), 'total_balance': total_balance, 'status': state})
                elif state == 'overdue' and Util.getMonthYear(close_date) == Util.getPreviousMonth(datetime.now().strftime('%Y-%m')):
                    results.append({'closed_month': Util.getMonthYear(close_date), 'total_balance': total_balance, 'status': state if remaining_balance > 0 else 'paid'})


            # Create a DataFrame from the results
            dfBills = pd.DataFrame(results)
            dfBills.to_excel(filePath, index = False)

            Util.writeLog("[Nubank API] Bills successfully downloaded and saved at: '" + filePath + "'")

            return True

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error during bills download. Error: " + str(ex))
            return False



    
    def getAmountSpentCurrentCycle(dfCardStatements):
        """
        Based on the card statements file, returns the total amount spent in the current cycle.

        * Cycle: 25th from previous month until 25th of the current month.
        """

        total_amount = float(0.0)

        try:
            # Convert the 'transaction_date' column to datetime
            dfCardStatements['transaction_date'] = pd.to_datetime(dfCardStatements['transaction_date'])

            # Get the current date
            current_date = pd.to_datetime('now')

            # Get the 25th day of the previous month
            start_date = current_date - pd.offsets.MonthBegin(2) + pd.DateOffset(days=23)

            # Get the 25th day of the current month
            end_date = current_date - pd.offsets.MonthBegin(1) + pd.DateOffset(days=23)
            
            # Filtering the transactions for this cycle
            filtered_transactions = dfCardStatements[
                (dfCardStatements['transaction_date'] >= start_date) & (dfCardStatements['transaction_date'] <= end_date)
            ]

            # Calculate the sum of the 'amount' column
            total_amount = float(filtered_transactions['treated_amount'].sum())

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error when calculating spent of the current cycle. Error: " + str(ex))
        
        return total_amount
    



    def getCurrentMonthBill(dfBill):

        currentMonthBill = float(0.0)

        try:
            currentMonthBill = float(dfBill[dfBill['closed_month'] == Util.getMonthYear(str(datetime.now().strftime('%Y-%m-%d')))]['total_balance'])

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error when getting current month's bill. Error: " + str(ex))
        
        return currentMonthBill




    def getPreviousMonthBill(dfBill):
    
        previousMonthBill = float(0.0)

        try:
            previousMonthBill = float(dfBill[dfBill['closed_month'] == Util.getPreviousMonth(str(datetime.now().strftime('%Y-%m')))]['total_balance'])

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error when getting previous month's bill. Error: " + str(ex))
        
        return previousMonthBill




    def getNextMonthBill(dfBill):
        
        nextMonthBill = float(0.0)

        try:
            nextMonthBill = float(dfBill[dfBill['closed_month'] == Util.getNextMonth(str(datetime.now().strftime('%Y-%m')))]['total_balance'])

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error when getting next month's bill. Error: " + str(ex))
        
        return nextMonthBill




    def getPreviousTxnsString(dfCardStatements):
        import pytz

        print(dfCardStatements.columns.tolist())
        dfCardStatements = dfCardStatements.sort_values(by = 'transaction_time', ascending = False)
        
        # adjusting timezone to BRT
        dfCardStatements['transaction_time'] = pd.to_datetime(dfCardStatements['transaction_time'])
        dfCardStatements['transaction_time'] = dfCardStatements['transaction_time'].dt.tz_convert('America/Sao_Paulo')
        dfCardStatements['transaction_time'] = dfCardStatements['transaction_time'].dt.strftime('%d/%m/%Y às %Hh')

        try: 
            strPreviousTxns = "*Últimas transações:* " + "\n"

            maxRows = 6
            rowCount = 0
            for index, row in dfCardStatements.iterrows():
                strPreviousTxns = strPreviousTxns + "[R$ " + str(float(row['amount'])) + str( " - em " + str(int(round(float(row['num_installments']), 0))) + "x]" if int(row['num_installments']) > 0 else "] " ) + str(row['transaction_title']) + " - [" + str(row['transaction_time']) + "]" + "\n"
                if rowCount == maxRows:
                    break
                rowCount = rowCount + 1 

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error when preparing string with previous transactions. Error: " + str(ex))


        return strPreviousTxns




    def getNubankAlertMessage(amountSpentCurrentCycle, currentMonthBill, previousMonthBill, nextMonthBill, strPreviousTxns, monthLimit = 4500):
        
        nubankMessage = ""

        try:
            # Get the current date
            current_date = pd.to_datetime('now')

            # Get the next 25th day of the current cycle
            end_date = current_date - pd.offsets.MonthBegin(1) + pd.DateOffset(days=23)

            # Get the difference between today and the last day of this cycle
            difference = end_date - current_date

            # Get the number of days
            num_days_until_end_of_cycle = difference.days  

            nubankMessage = nubankMessage + "Olá! 🤖  \n\n"
            nubankMessage = nubankMessage + "Seu resumo diário do Nubank está pronto\n"
            nubankMessage = nubankMessage + " \n"
            nubankMessage = nubankMessage + "Para se manter no limite de R$ " + str(int(round(monthLimit,0))).replace('.', ',') + " você pode gastar *por dia: R$ " + str(int(round(float((monthLimit - currentMonthBill) / num_days_until_end_of_cycle), 0))).replace('.', ',') + "*\n"
            nubankMessage = nubankMessage + "No total, você ainda pode gastar: *R$ " + str(int(round(float((monthLimit - currentMonthBill)), 0))).replace('.', ',') + "*\n"
            nubankMessage = nubankMessage + "Esse mês você já gastou (exc. parcelas): R$ " + str(round(amountSpentCurrentCycle, 2)).replace('.', ',') + "\n"
            nubankMessage = nubankMessage + " \n"
            nubankMessage = nubankMessage + "*Detalhes das faturas:* \n"
            nubankMessage = nubankMessage + "- *Fatura atual:* R$ " + str(round(currentMonthBill, 2)).replace('.', ',') + "\n"
            nubankMessage = nubankMessage + "- *Fatura do mês anterior:* R$ " + str(round(previousMonthBill, 2)).replace('.', ',') + "\n"
            nubankMessage = nubankMessage + "- *Fatura do próximo mês já vai iniciar em:* R$ " + str(round(nextMonthBill, 2)).replace('.', ',') + "\n"
            nubankMessage = nubankMessage + " " + "\n"
            nubankMessage = nubankMessage + strPreviousTxns + "\n"
            nubankMessage = nubankMessage + " " + "\n"

        except Exception as ex:
            Util.writeLog("[Nubank API][ERROR] Error when preparing message string to be sent in WhatsApp. Error: " + str(ex))
        
        return nubankMessage