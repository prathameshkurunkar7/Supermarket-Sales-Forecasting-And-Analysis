import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Forecasts:
    def __init__(self):
        with open('./model/furniture_forecast.json') as f:
            self.dataFurniture = json.load(f)
        with open('./model/office_forecast.json') as f:
            self.dataOffice = json.load(f)
        with open('./model/tech_forecast.json') as f:
            self.dataTech = json.load(f)
    
    def verify(self):
        va = list(self.dataFurniture.keys())[0]
        print(datetime.strptime(va,'%Y-%m-%d').date())

    def predict(self,category,date):
        date = datetime.strptime(date,'%Y-%m-%d').date()
        date_before_month = date + relativedelta(months=-1)
        date_after_month = date+ relativedelta(months=1)

        date = datetime.strftime(date,'%Y-%m-%d')
        date_before_month = datetime.strftime(date_before_month,'%Y-%m-%d')
        date_after_month = datetime.strftime(date_after_month,'%Y-%m-%d')

        if category == 'Furniture':
            dic = {}
            dic['present'] = {}
            dic['next']= {}
            dic['previous'] = {}
            
            dic['present']['qty'] = round(self.dataFurniture.get(date))
            dic['next']['qty'] = round(self.dataFurniture.get(date_after_month))
            dic['previous']['qty'] = round(self.dataFurniture.get(date_before_month))

            dic['present']['date'] = datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%b-%Y')
            dic['next']['date'] = datetime.strftime(datetime.strptime(date_after_month,'%Y-%m-%d').date(),'%b-%Y')
            dic['previous']['date'] = datetime.strftime(datetime.strptime(date_before_month,'%Y-%m-%d').date(),'%b-%Y')

            return json.dumps(dic)
        
        elif category == 'Office Supplies':
            dic = {}
            dic['present'] = {}
            dic['next']= {}
            dic['previous'] = {}
            
            dic['present']['qty'] = round(self.dataOffice.get(date))
            dic['next']['qty'] = round(self.dataOffice.get(date_after_month))
            dic['previous']['qty'] = round(self.dataOffice.get(date_before_month))

            dic['present']['date'] = datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%b-%Y')
            dic['next']['date'] = datetime.strftime(datetime.strptime(date_after_month,'%Y-%m-%d').date(),'%b-%Y')
            dic['previous']['date'] = datetime.strftime(datetime.strptime(date_before_month,'%Y-%m-%d').date(),'%b-%Y')

            return json.dumps(dic)
        elif category == 'Technology':
            dic = {}
            dic['present'] = {}
            dic['next']= {}
            dic['previous'] = {}
            
            dic['present']['qty'] = round(self.dataTech.get(date))
            dic['next']['qty'] = round(self.dataTech.get(date_after_month))
            dic['previous']['qty'] = round(self.dataTech.get(date_before_month))

            dic['present']['date'] = datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%b-%Y')
            dic['next']['date'] = datetime.strftime(datetime.strptime(date_after_month,'%Y-%m-%d').date(),'%b-%Y')
            dic['previous']['date'] = datetime.strftime(datetime.strptime(date_before_month,'%Y-%m-%d').date(),'%b-%Y')

            return json.dumps(dic)
        else:
            return 'Invalid Input'

    def subCatPredict(self,subcate,date):
        date = datetime.strptime(date,'%Y-%m-%d').date()
        date_before_month = date + relativedelta(months=-1)
        date_after_month = date+ relativedelta(months=1)

        date = datetime.strftime(date,'%Y-%m-%d')
        date_before_month = datetime.strftime(date_before_month,'%Y-%m-%d')
        date_after_month = datetime.strftime(date_after_month,'%Y-%m-%d')
        
        with open('./model/Sub-Categorical-JSON/{}_forecast.json'.format(subcate)) as f:
            self.dataSub = json.load(f)
        dic = {}
        dic['present'] = {}
        dic['next']= {}
        dic['previous'] = {}
        
        dic['present']['qty'] = round(self.dataSub.get(date))
        dic['next']['qty'] = round(self.dataSub.get(date_after_month))
        dic['previous']['qty'] = round(self.dataSub.get(date_before_month))

        dic['present']['date'] = datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%b-%Y')
        dic['next']['date'] = datetime.strftime(datetime.strptime(date_after_month,'%Y-%m-%d').date(),'%b-%Y')
        dic['previous']['date'] = datetime.strftime(datetime.strptime(date_before_month,'%Y-%m-%d').date(),'%b-%Y')

        return json.dumps(dic)