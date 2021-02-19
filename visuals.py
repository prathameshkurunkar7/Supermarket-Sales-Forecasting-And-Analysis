import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np

import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SuperMarketSalesAnalysis:

    def __init__(self):
        self.df = pd.read_excel('./sales.xls')
        self.df['Order_Date'] = pd.to_datetime(self.df['Order_Date'],format='%d/%m/%Y')
        self.df['Year'] = self.df['Order_Date'].map(lambda x: x.strftime('%Y'))
        self.df['Month'] = self.df['Order_Date'].map(lambda x: x.strftime('%m'))
        self.df.sort_values(by=['Month'])

        with open('./model/furniture_forecast.json') as f:
            self.dataFurniture = json.load(f)
        with open('./model/office_forecast.json') as f:
            self.dataOffice = json.load(f)
        with open('./model/tech_forecast.json') as f:
            self.dataTech = json.load(f)

    def regionWiseSales(self):
        cd = self.df[['Region','Sales']]
        byRegion = cd.groupby('Region')
        byRegionCount = byRegion.count()
        order_df = [
            go.Scatter(
                x= byRegionCount.index,
                y= byRegionCount.Sales,
                mode = 'lines+markers+text'
            )
        ]

        data=go.Figure(data = order_df,layout = go.Layout(title = 'Region vs Sales',template = 'plotly_dark',xaxis_title="Region",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))


        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def regionVsQuantity(self):
        
        rq=self.df[['Region','Quantity']]
        region_quantityGroup=rq.groupby('Region')
        region_quantity=region_quantityGroup.sum()
        trace = [
            go.Scatter(
                x = region_quantity.index,
                y = region_quantity.Quantity,
                mode = 'lines+markers+text'
            )
        ]

        data=go.Figure(data = trace,layout = go.Layout(title = 'Region vs Quantitative Sales',template = 'plotly_dark',xaxis_title="Region",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))

        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return chartAsJSON

    def discountVsSalesAndProfit(self):
        DiscountAndSales = self.df[['Discount','Sales','Profit']]
        df1 = DiscountAndSales.groupby('Discount').mean()
        # This can be done with count() as well for Sales only.

        trace1 = go.Scatter(
            x = df1.index,
            y = df1.Sales,
            name = 'Sales',
            mode = 'lines+markers'
        )
        trace2 = go.Scatter(
            x = df1.index,
            y = df1.Profit,
            name = 'Profit',
            mode = 'lines+markers'
        )

        resDf = [trace1,trace2]
        data=go.Figure(data = resDf,layout = go.Layout(title = 'Discount vs Sales and Profit',template = 'plotly_dark',xaxis_title="Year",
                yaxis_title="Sales/Profit",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))

        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    def regionVsQuantityYearly(self):
        #region vs total quantity
        year_2014=self.df[self.df['Year']=='2014']
        year_2015=self.df[self.df['Year']=='2015']
        year_2016=self.df[self.df['Year']=='2016']
        year_2017=self.df[self.df['Year']=='2017']

        trace1 = go.Bar(
            x = year_2014['Region'].to_list(),
            y = year_2014['Quantity'].to_list(),
            name = '2014'
        )
        trace2 = go.Bar(
            x = year_2015['Region'].to_list(),
            y = year_2015['Quantity'].to_list(),
            name = '2015'
        )
        trace3 = go.Bar(
            x = year_2016['Region'].to_list(),
            y = year_2016['Quantity'].to_list(),
            name = '2016'
        )
        trace4 = go.Bar(
            x = year_2017['Region'].to_list(),
            y = year_2017['Quantity'].to_list(),
            name = '2017'
        )

        data = [trace1,trace2,trace3,trace4]

        data=go.Figure(data = data,layout = go.Layout(title = 'Region vs Yearly Sales',template = 'plotly_dark',xaxis_title="Region",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON

    def yearlyProfit(self):
        # Year wise overall profit  
        profit_quantity=self.df[['Year','Profit']]
        profit_quantity=profit_quantity.groupby('Year')
        profit_quantity=profit_quantity.sum()

        trace = go.Scatter(
            x = profit_quantity.index,
            y = profit_quantity.Profit,
            mode = 'lines+markers+text'
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Yearly Profit',template = 'plotly_dark', xaxis_title="Year",
                yaxis_title="Profit",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"))
            )
        # data = [trace]
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def yearlySales(self):
        quantity=self.df[['Year','Quantity']]
        quantity=quantity.groupby('Year')
        quantity=quantity.sum()
        trace = go.Scatter(
            x = quantity.index,
            y = quantity.Quantity,
            mode = 'lines+markers+text',
        )

        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Yearly Sales',template = 'plotly_dark',xaxis_title="Year",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        # data = [trace]
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def categoricalSales(self):
        #Analysis: Sells per category
        categoricalQuantity=self.df[['Category','Quantity']]
        categoricalQuantity=categoricalQuantity.groupby('Category')
        categoricalQuantity=categoricalQuantity.sum()
        trace = go.Bar(
            x = categoricalQuantity.index,
            y = categoricalQuantity.Quantity,
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Categorical Sales',template = 'plotly_dark',xaxis_title="Categories",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def profitSalesPerYear(self,year):
        yeardf=self.df[self.df['Year']==year]
        profit_quantity=yeardf[['Quantity','Profit']]
        profit_quantity=profit_quantity.groupby('Quantity')
        profit_quantity=profit_quantity.sum()


        trace = go.Scatter(
            x = profit_quantity.index,
            y = profit_quantity.Profit,
            mode = 'lines+markers+text'
        )
        data=go.Figure(data = trace,layout = go.Layout(title='Analysis of Year wise overall profit',template = 'plotly_dark',xaxis_title="Sales for {}".format(year),
                yaxis_title="Profit for {}".format(year),
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON




    def subcategoricalSales(self):
        # Analysis: Sells per sub-category 
        subcategoricalQuantity=self.df[['Sub_Category','Quantity']]
        subcategoricalQuantity=subcategoricalQuantity.groupby('Sub_Category')
        subcategoricalQuantity=subcategoricalQuantity.sum()
        
        trace = go.Bar(
            x = subcategoricalQuantity.index,
            y = subcategoricalQuantity.Quantity,
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Sub-Categorical Sales',template = 'plotly_dark',xaxis_title="Sub-Categories",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON

    def temperatureSales(self):
        # Analysis Temperature wise sales
        temperatureQuantity=self.df[['Temperature','Quantity']]
        temperatureQuantity=temperatureQuantity.groupby('Temperature')
        temperatureQuantity=temperatureQuantity.sum()

        trace = go.Scatter(
            x = temperatureQuantity.index,
            y = temperatureQuantity.Quantity,
            mode = 'lines+text'
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Temperature vs Sales',template = 'plotly_dark',xaxis_title="Temperature(F)",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def fuelPriceVsSales(self):
        fuelPriceQuantity=self.df[['Fuel_Price','Quantity']]
        fuelPriceQuantity=fuelPriceQuantity.groupby('Fuel_Price')
        fuelPriceQuantity=fuelPriceQuantity.sum()

        trace = go.Scatter(
            x = fuelPriceQuantity.index,
            y = fuelPriceQuantity.Quantity,
            mode = 'lines+text'
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Fuel Price vs Sales',template = 'plotly_dark',xaxis_title="Fuel Price($USD)",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White")
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def holidaySales(self):
        holidayQuantity=self.df[['Is_Holiday','Quantity']]
        holidayQuantity=holidayQuantity.groupby('Is_Holiday')
        holidayQuantity=holidayQuantity.sum()

        trace = go.Bar(
            x = holidayQuantity.index,
            y = holidayQuantity.Quantity,
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Holiday vs Sales',template = 'plotly_dark',xaxis_title="Holiday",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"),
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON

    def discountVsSales(self):
        discountQuantity=self.df[['Discount','Quantity']]
        discountQuantity=discountQuantity.groupby('Discount')
        discountQuantity=discountQuantity.sum()

        trace = go.Scatter(
            x = discountQuantity.index,
            y = discountQuantity.Quantity,
            mode = 'lines+markers+text'
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Discount vs Sales',template = 'plotly_dark',xaxis_title="Discount",
                yaxis_title="Quantitative Sales ",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"),
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def discountVsProfit(self):
        discountQuantity=self.df[['Discount','Profit']]
        discountQuantity=discountQuantity.groupby('Discount')
        discountQuantity=discountQuantity.sum()

        trace = go.Scatter(
            x = discountQuantity.index,
            y = discountQuantity.Profit,
            mode = 'lines+markers+text'
        )
        data=go.Figure(data = trace,layout = go.Layout(title = 'Analysis of Discount vs Profit',template = 'plotly_dark',xaxis_title="Discount",
                yaxis_title="Profit",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"),
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def yearlySalesPerCategory(self,cat):
        dfCategory=self.df[self.df['Category']==cat]
        dfCategory=dfCategory[['Year','Category','Quantity']]
        dfCategory=dfCategory.groupby('Year')
        dfCategory=dfCategory.sum()

        trace = go.Scatter(
            x = dfCategory.index,
            y = dfCategory.Quantity,
            mode = 'lines+markers+text'
        )
    
        data=go.Figure(data = trace,layout = go.Layout(title ='Sales per {}'.format(cat),template = 'plotly_dark',xaxis_title="Year",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"),
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def yearlySalesPerSubCategory(self,subCat):
        subCategory=self.df[self.df['Sub_Category']==subCat]
        subCategory=subCategory[['Year','Sub_Category','Quantity']]
        subCategory=subCategory.groupby('Year')
        subCategory=subCategory.sum()

        trace = go.Scatter(
            x = subCategory.index,
            y = subCategory.Quantity,
            mode = 'lines+markers+text'
        )
    
        data=go.Figure(data = trace,layout = go.Layout(title ='Sales per {}'.format(subCat),template = 'plotly_dark',xaxis_title="Year",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"),
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON

    def monthlySalesPerSubCategory(self,subCat):
        subCategory=self.df[self.df['Sub_Category']==subCat]
        subCategory=subCategory[['Month','Sub_Category','Quantity']]
        subCategory=subCategory.groupby('Month')
        subCategory=subCategory.sum()

        trace = go.Scatter(
            x = subCategory.index,
            y = subCategory.Quantity,
            mode = 'lines+markers+text'
        )
    
        data=go.Figure(data = trace,layout = go.Layout(title ='Sales per {}'.format(subCat),template = 'plotly_dark',xaxis_title="Month",
                yaxis_title="Sales",
                # legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=14,
                color="White"),
            ))
        chartAsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return chartAsJSON
    
    def monthlyCategorical(self,date,category):
        date = datetime.strptime(date,'%Y-%m-%d').date()
        date_before_month = date + relativedelta(months=-1)
        date_after_month = date+ relativedelta(months=1)

        date = datetime.strftime(date,'%Y-%m-%d')
        date_before_month = datetime.strftime(date_before_month,'%Y-%m-%d')
        date_after_month = datetime.strftime(date_after_month,'%Y-%m-%d')
