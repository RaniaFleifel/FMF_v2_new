# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 04:54:32 2023

@author: rania
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 11:41:24 2023

@author: rania
"""

from flask import Flask,render_template,request
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate
import re
from pretty_html_table import build_table

a=[]
b=[]
std_loan_noapprox=[]
flexible_loan_noapprox=[]   
entries=[]
app=Flask(__name__,template_folder='templates')
options_month = ['jan', 'feb', 'mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
interest_rate=18/100

@app.route("/")
def home():
    return render_template('ideal_html.html')

@app.route('/calculations',methods=['POST'])
def calculations():
    #a=[]

    data=request.form#.values()

    amount=int(data["amount"])
    std_loan_noapprox=[]
    flexible_loan_noapprox=[] 

    while amount>15000: 
        tmp="The cap of the loan is 15000!.. Please re-enter the loan amount"
        return render_template('ideal_html.html',loan_size_txt_no=tmp)#.append('The size of the loan is {} egp\n'.format(loan_size[0])))
    else:
        a.append(amount)

        tmp=f"Loan amount: {amount} EGP"
        return render_template('ideal_html.html',loan_size_txt_yes=tmp)#.append('The size of the loan is {} egp\n'.format(loan_size[0])))
    print("############### IN CALCULATIONS",a)
    
@app.route('/payment_schedule',methods=['POST'])
def payment_schedule():
    #print("############### IN PAYMENT SCHEDULE",a[0])

    loan_size=a[len(a)-1]#in case of multiple entries 
    print("############### IN PAYMENT SCHEDULE",loan_size,'LEN(A)',len(a))

    data=request.form
    b.append(data)
    print(data)
    frequency=data["frequency"]
    holiday_yn=data["holiday"]
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>b after append",b,'LEN(B)',len(b))

    if data["grace"]=="no":
        grace_yn=data["grace"]
        grace_dur=0
        grace_txt="Grace period not applied"
    else:
        grace_yn=re.split(r'(\d+)', data["grace"])[0]
        grace_dur = int(re.split(r'(\d+)', data["grace"])[1])
        grace_txt=f"Grace period applied for {str(grace_dur)} months \n"
    
    if holiday_yn=="no":
        holiday_txt="Repayment holiday not applied"
        holiday_dur=0
        holiday_months=""
    else:
        
        if data["month1"]==' ':
            holiday_months=data["month2"].capitalize()
            holiday_dur=1
        elif data["month2"]==' ':
            holiday_months=data["month1"].capitalize()
            holiday_dur=1
        else:
            holiday_months=[data["month1"].capitalize(),data["month2"].capitalize()]
            holiday_dur=2

        holiday_txt=f"Repayment holiday applied for {holiday_dur} months: {holiday_months} \n"

    # #ideal v1 assumes dispersment starts tomorrow
    # tom_date = datetime.now()+timedelta(1)
    # tom_month=tom_date.strftime("%b")
    # start_month=tom_month.lower()
    # #ideal v2 wants to start next month
    this_month=datetime.now().strftime("%b").lower()
    start_month=options_month[options_month.index(this_month)+1]
    
    loan_amount_txt=f"Loan amount is {loan_size} EGP"
    start_month_txt=f"Dispersment starts in {str(start_month)}\n"
    frequency_txt=f"{frequency.capitalize()} payment"
#    print(str(start_month_txt),frequency_txt,grace_txt,holiday_txt)

    df = pd.DataFrame(columns=['Month','Standard loan','Flexible loan'])
    monthly_share=(loan_size+(interest_rate*loan_size))/12    
    print("monthly_share",monthly_share,start_month)

    num_months=12+holiday_dur+grace_dur
    loc_start_month=options_month.index(start_month)
    
    updated_loan_size=loan_size*num_months/12
    updated_monthly_intrest=updated_loan_size*interest_rate/num_months
    flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
     
    x=0
    
#    if holiday_yn=='yes':
#        if data["month1"]==' ' and data["month2"]==' ':
#            holiday_txt+="but didn't pick a month! Please enter at least one month"

            
            
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',grace_yn,holiday_yn,)
    std_loan_noapprox=[]
    flexible_loan_noapprox=[]    
    if grace_yn=='no' and holiday_yn=='no':
        num_months=12
        loc_start_month=options_month.index(start_month)
        std_loan_noapprox.append(monthly_share)
        flexible_loan_noapprox.append(monthly_share)
        
        if frequency=="monthly":
            for i in range(num_months):
                this_month=options_month[(loc_start_month+i)%12].capitalize()
                new_line=[this_month,round(monthly_share,2),round(monthly_share,2)]
    
                df.loc[i]=new_line
                
            print("^^^^^^^^^^^^^^^^^^^^^how much is i now?",i)
            df.loc[i+1]=["------------------","------------------","------------------"]

            df.loc[i+2]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]

        elif frequency=="biweekly":
            for i in range(0,num_months*2,2):
                
                this_month=options_month[(loc_start_month+int(i/2))%12].capitalize()
                new_line=[this_month+", week2",0,round(monthly_share/2,2)]
                df.loc[i]=new_line
                
                new_line=[this_month+", week4",round(monthly_share,2),round(monthly_share/2,2)]
                df.loc[i+1]=new_line
                
            print("^^^^^^^^^^^^^^^^^^^^^how much is i now?",i)
            df.loc[i+2]=["------------------","------------------","------------------"]

            df.loc[i+3]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
        else:
            for i in range(0,num_months*4,4):
                
                this_month=options_month[(loc_start_month+int(i/4))%12].capitalize()
                new_line=[this_month+", week1",0,round(monthly_share/4,2)]
                df.loc[i]=new_line
                new_line=[this_month+", week2",0,round(monthly_share/4,2)]
                df.loc[i+1]=new_line
                new_line=[this_month+", week3",0,round(monthly_share/4,2)]
                df.loc[i+2]=new_line
                new_line=[this_month+", week4",round(monthly_share,2),round(monthly_share/4,2)]
                df.loc[i+3]=new_line
                
                
            print("^^^^^^^^^^^^^^^^^^^^^how much is i now?",i)
            df.loc[i+4]=["------------------","------------------","------------------"]

            df.loc[i+5]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
            #print(df)
    elif grace_yn=='yes' and holiday_yn=='no':
        num_months=12+grace_dur
        loc_start_month=options_month.index(start_month)
                
        updated_loan_size=loan_size*num_months/12
        updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
        #print(this_month,monthly_share,round(flexible_monthly_share,1))

        if frequency=="monthly":

            for i in range(num_months):
                this_month=options_month[(loc_start_month+i)%12].capitalize()
                        
                if i in range(grace_dur):
                    new_line=[this_month,round(monthly_share,2),round(updated_monthly_intrest,2)]    
                    df.loc[i]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                elif i>=12:
                    new_line=[this_month,0,round(flexible_monthly_share,2)]  
                    df.loc[i]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month,round(monthly_share,2),round(flexible_monthly_share,2)]    
                    df.loc[i]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
            df.loc[i+1]=["------------------","------------------","------------------"]
       
            df.loc[i+2]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
            # print(df)
        elif frequency=="biweekly":
            for i in range(0,num_months*2,2):
                
                this_month=options_month[(loc_start_month+int(i/2))%12].capitalize()
                
                if i in range(grace_dur*2):
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/2,2)]    
                    df.loc[i+1]=new_line

                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                elif i>=12*2:
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/2,2)]  
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",0,round(flexible_monthly_share/2,2)]  
                    df.loc[i+1]=new_line
                    
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(flexible_monthly_share/2,2)]    
                    df.loc[i+1]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
                
            print("^^^^^^^^^^^^^^^^^^^^^how much is i now?",i)
            df.loc[i+2]=["------------------","------------------","------------------"]

            df.loc[i+3]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
        
        else:#if frequency=="biweekly":
            for i in range(0,num_months*4,4):
                
                this_month=options_month[(loc_start_month+int(i/4))%12].capitalize()
                
                if i in range(grace_dur*4):
                    new_line=[this_month+", week1",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/4,2)]    
                    df.loc[i+3]=new_line

                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                elif i>=12*4:
                    new_line=[this_month+", week1",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+3]=new_line
                    
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month+", week1",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(flexible_monthly_share/4,2)]    
                    df.loc[i+3]=new_line
                    
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
                
            print("^^^^^^^^^^^^^^^^^^^^^how much is i now?",i)
            df.loc[i+4]=["------------------","------------------","------------------"]

            df.loc[i+5]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
    
        
    elif grace_yn=='no' and holiday_yn=='yes':
        num_months=12+holiday_dur
        loc_start_month=options_month.index(start_month)
                
        updated_loan_size=loan_size*num_months/12
        updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
        
        
        x=0
        if frequency=="monthly":

            for i in range(num_months):
                this_month=options_month[(loc_start_month+i)%12].capitalize()
                print(i,this_month)
    
                if this_month.capitalize() in holiday_months and x<holiday_dur:
                    #covered=1
                    new_line=[this_month,round(monthly_share,2),round(updated_monthly_intrest,2)]    
                    df.loc[i]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                    x+=1
                
                elif i>=12:
                    new_line=[this_month,0,round(flexible_monthly_share,2)]  
                    df.loc[i]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month,round(monthly_share,2),round(flexible_monthly_share,2)]    
                    df.loc[i]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
            df.loc[i+1]=["------------------","------------------","------------------"]
            df.loc[i+2]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
            #print(df)
        elif frequency=="biweekly":
            for i in range(0,num_months*2,2):
                this_month=options_month[(loc_start_month+int(i/2))%12].capitalize()

                if this_month.capitalize() in holiday_months and x<holiday_dur:
                    #covered=1
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/2,2)]    
                    df.loc[i+1]=new_line
                    
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                    x+=1
                
                elif i>=12*2:
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/2,2)]  
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",0,round(flexible_monthly_share/2,2)]  
                    df.loc[i+1]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(flexible_monthly_share/2,2)]    
                    df.loc[i+1]=new_line
    
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
            df.loc[i+2]=["------------------","------------------","------------------"]

            df.loc[i+3]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]

        else:
            for i in range(0,num_months*4,4):
                this_month=options_month[(loc_start_month+int(i/4))%12].capitalize()

                if this_month.capitalize() in holiday_months and x<holiday_dur:
                    #covered=1
                    new_line=[this_month+", week1",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/4,2)]    
                    df.loc[i+3]=new_line
    
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                    x+=1
                
                elif i>=12*4:
                    new_line=[this_month+", week1",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+3]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month+", week1",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(flexible_monthly_share/4,2)]    
                    df.loc[i+3]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
            df.loc[i+4]=["------------------","------------------","------------------"]
            df.loc[i+5]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]

    elif grace_yn=='yes' and holiday_yn=='yes':
        num_months=12+holiday_dur+grace_dur
        loc_start_month=options_month.index(start_month)
        
        updated_loan_size=loan_size*num_months/12
        updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
         
        x=0
        if frequency=="monthly":

            for i in range(num_months):
                this_month=options_month[(loc_start_month+i)%12].capitalize()
                #print(i,this_month)
    
                if this_month.capitalize() in holiday_months and x<holiday_dur and i not in range(grace_dur):
                    #print(this_month)
                    new_line=[this_month,round(monthly_share,2),round(updated_monthly_intrest,2)]    
                    df.loc[i]=new_line
                    
    
                    x+=1
                    if i>=12:#num_months-holiday_dur-grace_dur:
                        new_line=[this_month,0,round(updated_monthly_intrest,2)]  
                        df.loc[i]=new_line
                        std_loan_noapprox.append(0)
                        flexible_loan_noapprox.append(updated_monthly_intrest)
                    else:
                        new_line=[this_month,round(monthly_share,2),round(updated_monthly_intrest,2)]  
                        df.loc[i]=new_line
                        std_loan_noapprox.append(monthly_share)
                        flexible_loan_noapprox.append(updated_monthly_intrest)
                        
                elif i in range(grace_dur):
                    new_line=[this_month,round(monthly_share,2),round(updated_monthly_intrest,2)]    
                    df.loc[i]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                  
                elif i>=num_months-holiday_dur-grace_dur:
                    new_line=[this_month,0,round(flexible_monthly_share,2)]  
                    df.loc[i]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month,round(monthly_share,2),round(flexible_monthly_share,2)]    
                    df.loc[i]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
            df.loc[i+1]=["------------------","------------------","------------------"]
            df.loc[i+2]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]
        elif frequency=="biweekly":
            for i in range(0,num_months*2,2):
                this_month=options_month[(loc_start_month+int(i/2))%12].capitalize()
    
                if this_month.capitalize() in holiday_months and x<holiday_dur and i not in range(grace_dur*2):
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/2,2)]    
                    df.loc[i+1]=new_line
                    print('caseA')
                    x+=1
                    if i>=12*2:#(num_months-holiday_dur-grace_dur):
                        new_line=[this_month+", week2",0,round(updated_monthly_intrest/2,2)]  
                        df.loc[i]=new_line
                        new_line=[this_month+", week4",0,round(updated_monthly_intrest/2,2)]  
                        df.loc[i+1]=new_line
                        std_loan_noapprox.append(0)
                        flexible_loan_noapprox.append(updated_monthly_intrest)
                        print('caseAA')
                    else:
                        new_line=[this_month+", week2",0,round(updated_monthly_intrest/2,2)]  
                        df.loc[i]=new_line
                        new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/2,2)]  
                        df.loc[i+1]=new_line
                        std_loan_noapprox.append(monthly_share)
                        flexible_loan_noapprox.append(updated_monthly_intrest)
                        print('caseAA')
                        print('?????')
                        
                elif i in range(grace_dur*2):
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/2,2)]    
                    df.loc[i+1]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
                    print('caseC')
    
                  
                elif i>=12*2:#(num_months-holiday_dur-grace_dur)*2:
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/2,2)]  
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",0,round(flexible_monthly_share/2,2)]  
                    df.loc[i+1]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
                    print('caseD')
    
                else:
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/2,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(flexible_monthly_share/2,2)]    
                    df.loc[i+1]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
                    print('caseE')
            df.loc[i+2]=["------------------","------------------","------------------"]
            df.loc[i+3]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]

        else:
            for i in range(0,num_months*4,4):
                this_month=options_month[(loc_start_month+int(i/4))%12].capitalize()
    
                if this_month.capitalize() in holiday_months and x<holiday_dur and i not in range(grace_dur*4):
                    new_line=[this_month+", week1",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/4,2)]    
                    df.loc[i+3]=new_line
                    
                    x+=1
                    if i>=12*4:#num_months-holiday_dur-grace_dur:
                        new_line=[this_month+", week1",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i]=new_line
                        new_line=[this_month+", week2",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i+1]=new_line
                        new_line=[this_month+", week3",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i+2]=new_line
                        new_line=[this_month+", week4",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i+3]=new_line
                        std_loan_noapprox.append(0)
                        flexible_loan_noapprox.append(updated_monthly_intrest)
                    
                    else:
                        
                        
                        new_line=[this_month+", week1",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i]=new_line
                        new_line=[this_month+", week2",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i+1]=new_line
                        new_line=[this_month+", week3",0,round(updated_monthly_intrest/4,2)]  
                        df.loc[i+2]=new_line
                        new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/4,2)]  
                        df.loc[i+3]=new_line
                        
                        std_loan_noapprox.append(monthly_share)
                        flexible_loan_noapprox.append(updated_monthly_intrest)
                        print('caseAA')
                        print('?????')
                elif i in range(grace_dur*4):
                    new_line=[this_month+", week1",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(updated_monthly_intrest/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(updated_monthly_intrest/4,2)]    
                    df.loc[i+3]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(updated_monthly_intrest)
    
                  
                elif i>=12*4:#num_months-holiday_dur-grace_dur:
                    new_line=[this_month+", week1",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",0,round(flexible_monthly_share/4,2)]  
                    df.loc[i+3]=new_line
                    std_loan_noapprox.append(0)
                    flexible_loan_noapprox.append(flexible_monthly_share)
    
                else:
                    new_line=[this_month+", week1",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i]=new_line
                    new_line=[this_month+", week2",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+1]=new_line
                    new_line=[this_month+", week3",0,round(flexible_monthly_share/4,2)]    
                    df.loc[i+2]=new_line
                    new_line=[this_month+", week4",round(monthly_share,2),round(flexible_monthly_share/4,2)]    
                    df.loc[i+3]=new_line
                    std_loan_noapprox.append(monthly_share)
                    flexible_loan_noapprox.append(flexible_monthly_share)
            df.loc[i+4]=["------------------","------------------","------------------"]
            df.loc[i+5]=["Total",round(sum(std_loan_noapprox),2),round(sum(flexible_loan_noapprox),2)]



    # def df_style(val):
    #     return "font-weight: bold"

    # # get a handle on the row that starts with `"Total"`, i.e., the last row here
    # last_row = pd.IndexSlice[df.index[-1], :]
    # # and apply styling to it via the `subset` arg; first arg is styler function above
    # dfStyled = df.style.applymap(df_style, subset=last_row)
    # #display(summaryStyled)

    html_table_blue_light = build_table(df, 'blue_dark',padding="10px 10px 10px 10px" )
    # Save to html file
    with open('html_table_blue.html', 'w') as f:
        f.write(html_table_blue_light)

    return render_template('ideal_html.html',loan_amount_txt=loan_amount_txt,start_month_txt=start_month_txt,frequency_txt=frequency_txt,grace_txt=grace_txt,holiday_txt=holiday_txt, table_final=html_table_blue_light)
    


if __name__=="__main__":
    app.run(debug=True)
