import os, csv

import talib

import yfinance as yf
import pandas as pd
import tech

from flask import Flask, escape, request, render_template, jsonify ,url_for,redirect


app = Flask(__name__)
global newdata
global stock,start,end 
global stocks
global dicsubmit
stock=""
start=""
end=""
stocks={}
dicsubmit={}
global newdata
newdata=pd.DataFrame()

@app.route('/')

def index():

    return render_template('index.html')


@app.route('/test', methods=['POST', 'GET'])

def input():
    if request.method == 'POST':
        global stocks
        data={}
        data=request.get_json()
        # print (data)
        # print(type(data))
        for d in data:
            stocks.update(d)
        
        global newdata
        global stock,start,end 
        global dicsubmit
        print('/testroute',stocks)
        dicsubmit = {1: 'apple', 2: 'ball'}
        print('dicc',dicsubmit)

        
    results = {'processed': 'true'}
    return jsonify(results)
        

@app.route('/test1', methods=['POST','GET'])

def input1():
    if request.method == 'POST':
        data1={}
        data1=request.get_json()
        # print (data1)
        # print(type(data1))
        global indout
        global stock,end,start,dicsubmit
        global newdata
        ind=[]
        para=[]
        mcd=[]
        indout=[]
        rss=int()
       
       
        for e in range(1,len(data1)):
            ind.append(data1[e]['code'])
            para.append(data1[e]['parameter'])
            
        print(ind)
        print(para)
        
        for i in range(0,len(ind)):
            if ind[i]=="MACD":
                value=para[i]
                print(value)
                mcd=value.split(",",3)
                print(mcd)
                print(type((mcd)))
                test_list = list(map(int, mcd))
                print(type(test_list))
                print((test_list)) 
                print(type(test_list[0]))   
                print('/testroute2',stocks)
                global stock,end,start,dicsubmit
                stock = stocks.get('choice')
                start = stocks.get('from')        
                end = stocks.get('to')
                dicsubmit = {1: 'apple', 2: 'ball'}
                print('dicc',dicsubmit)
                tech.calculatestock(stock, start, end)
                tech.macdfram()
                indout=tech.macdd(test_list)
                newdata=tech.outframemacd()
                print(newdata)
                print("yes its is printed")
            elif ind[i]=="RSI":
                value=para[i]
                print(value)
                rss=int(value)
                print(rss)
                print(type((rss)))

                print('/testroute2',stocks)
                stock = stocks.get('choice')
                start = stocks.get('from')        
                end = stocks.get('to')
                dicsubmit = {1: 'apple', 2: 'ball'}
                print('dicc',dicsubmit)
                tech.calculatestock(stock, start, end)
                tech.rsiframe()
                indout=tech.rsifun(rss)
                newdata=tech.outframersi()
                print(newdata)
                print("yes its is printed")
            elif ind[i]=="Arron":
                value=para[i]
                print(value)
                rss=int(value)
                print(rss)
                print(type((rss)))
                print('/testroute2',stocks)
                stock = stocks.get('choice')
                start = stocks.get('from')        
                end = stocks.get('to')
                dicsubmit = {1: 'apple', 2: 'ball'}
                print('dicc',dicsubmit)
                tech.calculatestock(stock, start, end)
                tech.arronframe()
                indout=tech.arronfun(rss)
                newdata=tech.outframearron()
                print(newdata)
                print("yes its is printed")
            elif ind[i]=="Engulfing_pattern":
                # value=para[i]
                # print(value)
                # mcd=value
                # print(mcd)
                # print(type((mcd)))
                # test_list = list(map(int, mcd))
                # print(type(test_list))
                # print((test_list)) 
                # print(type(test_list[0]))   

                print('/testroute2',stocks)
                stock = stocks.get('choice')
                start = stocks.get('from')        
                end = stocks.get('to')
                dicsubmit = {1: 'apple', 2: 'ball'}
                print('dicc',dicsubmit)
                tech.calculatestock(stock, start, end)
                tech.engpatternfram()
                indout=tech.engpfun()
                # global newdata
                newdata=tech.outframeengf()
                print(newdata)
                print("yes its is printed")
            elif ind[i]=="ADX":
                value=para[i]
                print(value)
                rss=int(value)
                print(rss)
                print(type((rss)))
                print('/testroute2',stocks)
                stock = stocks.get('choice')
                start = stocks.get('from')        
                end = stocks.get('to')
                dicsubmit = {1: 'apple', 2: 'ball'}
                print('dicc',dicsubmit)
                tech.calculatestock(stock, start, end)
                tech.adxframe()
                indout=tech.adxfun(rss)
                newdata=tech.outframeadx()
                print(newdata)
                print("yes its is printed")
            else:
                pass
                         
    resultss = {'processed': 'true'}
    return jsonify(resultss)
    
@app.route('/output')

def output():
    return render_template('result.html',result="pass")

@app.route('/submit', methods=["POST","GET"])
def submitb():
    if request.method == "GET" :
        working="yes"
        global dicsubmit
        global newdata
        global stock,start,end
        global stocks
        global indout
        outvalue=[]
        outvalue=indout.copy()
        heading= outvalue[10]+ ' Data-Frame of ' + stock
        mxprofitt=0.0
        mxprofitt=outvalue[6]-100
        print(outvalue)
        print(working)
        print('submutfirst',stocks)
        print('submutsecond',stock,start,end)
        print('diccsecond',dicsubmit)
        print(newdata)

    return render_template('output.html',Company=stock,From=start,To=end,Indicator=outvalue[10],intialfun=outvalue[0],endprofit=outvalue[3],Buysignal=outvalue[1],Sellsignal=outvalue[2],maxprofit=mxprofitt,maxloss=outvalue[8],buyt=outvalue[4],sellt=outvalue[5],tables=[newdata.to_html()], titles = ['na',heading],patternn=outvalue[9],stockk=stock)
            

# @app.route('/base.html')

# def output(newframe):
#     return render_template('base.html',tables=[newframe.to_html()],titles=['na','first table'])


if __name__=='__main__':
    app.run(debug=True)