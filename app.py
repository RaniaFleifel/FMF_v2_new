from flask import Flask,render_template,request
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)
a=[]
entries=[]
options_month = ['jan', 'feb', 'mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
interest_rate=18/100

@app.route('/')
#def hello_world():
#    return 'Hello, World!'
def home():
    return render_template('index_new_v2.html')

@app.route('/amount',methods=['POST'])

def amount():
    #a=[]
    loan_size=[int(x) for x in request.form.values()]#int(request.form.values())
    while loan_size[0]>15000:        
        tmp="The cap of the loan is 15000.. Please re-enter the loan amount"
        # loan_size=[int(x) for x in request.form.values() if isinstance(x,int)]#int(request.form.values())
        for x in request.form.values():
            if isinstance(x,int):
                loan_size=int(x)
            else:
                continue
        output=loan_size#np.round_(prediction[0],2)
        
        return render_template('index_new_v2.html',loan_size_txt=tmp)#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

    else:
        print(request.form.values())
        tmp=f"You selected: {loan_size[0]} egp"
        output=loan_size
        #print(output,output[0])
        print("new entry###############################################")
        
        a.append(loan_size[0])
        print(a)

        return render_template('index_new_v2.html',loan_size_txt=tmp)
    
@app.route('/freq',methods=['POST'])
def freq():     
        print("freq ###############################################")
        print(len(a)-2)

        if len(a)<=4:
            loan_size_txt="Loan amount= {} egp".format(a[0])
        else:
            loan_size_txt="Loan amount= {} egp".format(a[len(a)-1])
        # Get the user-selected value from the dropdown
        selected_option = request.form['option']
        a.append(selected_option)
        
        # Process the selected option (You can add your own logic here)
        result = f"You selected: {selected_option} payements"
        tom_date = datetime.now()+timedelta(1)
        tom_month=tom_date.strftime("%b")
        
        print(tom_month)
       
        if selected_option=='monthly':
            result+="..... Dispersment starts tomorrow (aka month {})".format(tom_month)
            a.append(tom_month)
        else:
            result+="..This option is not applied in the website yet"  
            
        print(a)
        return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=result)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

@app.route('/grace_period',methods=['POST'])
def grace_period():     
        print("grace_period? ###############################################")

        if len(a)<=4:
            loan_size_txt="Loan amount= {} egp".format(a[0])
            loan_size=a[0]
            frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[2])
            start_month=a[2]

        else:
            loan_size_txt="Loan amount= {} egp".format(a[len(a)-3])
            loan_size=a[len(a)-3]
            frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[len(a)-1])
            start_month=a[len(a)-1]

            
        #loan_size_txt="Loan amount= {} egp".format(a[len(a)-3])
        #frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[len(a)-2])
        
        # Get the user-selected value from the dropdown
        selected_option = request.form['option']
        a.append(selected_option)
        
        # Process the selected option (You can add your own logic here)
        options_txt = f"Grace period? {selected_option} "

        df = pd.DataFrame(columns=['month','std_loan','flexible_loan'])
        monthly_share=round((loan_size+(interest_rate*loan_size))/12,1)

        if selected_option.lower()=='non':
            options_txt+="--> std loan schedule"
            num_months=12
            print("###############################################")
            print("monthly_share",monthly_share)
            print(start_month,options_month.index(start_month.lower()))
            loc_start_month=options_month.index(start_month.lower())
           
            for i in range(num_months):
                this_month=options_month[(loc_start_month+i)%12]
                new_line=[this_month,monthly_share,monthly_share]
                
                df.loc[i]=new_line
            
            df.loc[i+1]=["Total (egp)",round(df['std_loan'].sum(),1),round(df['flexible_loan'].sum(),1)]
            print(a)
            table=tabulate(df, headers='keys', tablefmt='psql')
            print(table)

            table = df.to_html(index=False)
        
            entries.append(a)
            return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt,options_txt=options_txt)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

        else:# selected_option.lower()=='yes':
            print("###############",a)
            #@app.route('/grace_period_months',methods=['POST'])
            return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt,options_txt=options_txt)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))
@app.route('/grace_period_months',methods=['POST'])
def grace_period_months():
    print("grace_period months ###############################################")

    if len(a)<=4:
        loan_size_txt="Loan amount= {} egp".format(a[0])
        loan_size=a[0]
        frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[2])
        start_month=a[2]
        grace_yn=a[3]

    else:
        loan_size_txt="Loan amount= {} egp".format(a[len(a)-4])
        loan_size=a[len(a)-4]
        frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[len(a)-2])
        start_month=a[len(a)-2]
        grace_yn=a[len(a)-1]

    dff = pd.DataFrame(columns=['month','std_loan','flexible_loan'])
    monthly_share=round((loan_size+(interest_rate*loan_size))/12,1)
    print("VERY IMPORTANT #############################",grace_yn)
    
    selected_option2 = request.form['option']

    if grace_yn.lower()=='yes':
        #grace_txt3="If you want grace period, How many months do you need?"
        grace_txt2="Grace period applied"#.format(a[3])

        a.append(selected_option2)

        grace_txt = f"You selected the following number of months: {selected_option2} "
        #print(grace_txt3)
        grace_dur=int(selected_option2)
        grace_txt2+=" for {} months".format(grace_dur)
        # num_months=12+grace_dur
        # loc_start_month=options_month.index(start_month.lower())
                
        # updated_loan_size=loan_size*num_months/12
        # updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        # flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
        
        
        # for i in range(num_months):
        #     this_month=options_month[(loc_start_month+i)%12]
                    
        #     if i in range(grace_dur):
        #         new_line=[this_month,monthly_share,round(updated_monthly_intrest,1)]    
        #         dff.loc[i]=new_line
        #     elif i>=12:
        #         new_line=[this_month,0,round(flexible_monthly_share,1)]  
        #         dff.loc[i]=new_line
        #     else:
        #         new_line=[this_month,monthly_share,round(flexible_monthly_share,1)]    
        #         dff.loc[i]=new_line
                
        #     dff.loc[i+1]=["total",round(dff['std_loan'].sum(),1),round(dff['flexible_loan'].sum(),1)]
            
        #     tablef=tabulate(dff, headers='keys', tablefmt='psql')
        #     print(tablef)
            
        #     tablef = dff.to_html(index=False)
                  
        return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt,options_txt=grace_txt2)#,tablef=tablef),grace_period_months_txt=grace_txt3)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))
    elif grace_yn.lower()=='no':
        #df = pd.DataFrame(columns=['month','std_loan','flexible_loan'])
        #tablef = df.to_html(index=False)
        #grace_txt2_not="Grace period option NOT applied"
        grace_txt2="Grace period not applied"#.format(a[len(a)-1])
        dummy=0
        a.append(str(dummy))

        return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt,options_txt=grace_txt2)#,tablef=tablef,options_txt=grace_txt2_not)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

@app.route('/repayment_holiday',methods=['POST'])
def repayment_holiday():
    print("repayment holiday ###############################################")
    print(a)

    if len(a)<=4:
        loan_size_txt="Loan amount= {} egp".format(a[0])
        loan_size=a[0]
        frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[2])
        start_month=a[2]
        grace_yn=a[3]
        grace_months=a[4]

    else:
        loan_size_txt="Loan amount= {} egp".format(a[len(a)-5])
        loan_size=a[len(a)-5]
        frequency_txt="Dispersment starts tomorrow (aka month {})".format(a[len(a)-3])
        start_month=a[len(a)-3]
        grace_yn=a[len(a)-2]
        grace_months=a[len(a)-1]
        
    
    #grace_txt2="Grace period option applied for {grace_months} months "#.format(a[len(a)-1])
    if grace_yn.lower()=='yes':
        grace_txt2 = f"Grace period applied for {grace_months} months \n"
    elif grace_yn.lower()=='no':
        grace_txt2 = f"Grace period not applied\n"

    selected_option3 = request.form['option']
    a.append(selected_option3)
    
    # Process the selected option (You can add your own logic here)
    if selected_option3.lower()=="yes":
        holiday_txt = f"Repayment holiday applied "
    else:
        holiday_txt = f"Repayment holiday not applied "

    return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt,options_txt=grace_txt2,options2_txt=holiday_txt)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

@app.route('/repayment_holiday_months',methods=['POST'])
def repayment_holiday_months():
    print("repayment_holiday_months ###############################################")

    if len(a)<=5:
        loan_size_txt="Loan amount= {} egp".format(a[0])
        loan_size=a[0]
        frequency_txt2="Dispersment starts tomorrow (aka month {})".format(a[2])
        start_month=a[2]
        grace_yn=a[3]
        grace_months=a[4]
        holiday_yn=a[5]

    else:
        loan_size_txt="Loan amount= {} egp".format(a[len(a)-6])
        loan_size=a[len(a)-6]
        frequency_txt2="Dispersment starts tomorrow (aka month {})".format(a[len(a)-4])
        start_month=a[len(a)-4]
        grace_yn=a[len(a)-3]
        grace_months=a[len(a)-2]
        holiday_yn=a[len(a)-1]

    if grace_yn.lower()=='yes':
        grace_txt3 = f"Grace period applied for {grace_months} months \n"
    else:
        grace_txt3 = f"Grace period not applied\n"

    dff = pd.DataFrame(columns=['month','std_loan','flexible_loan'])
    monthly_share=round((loan_size+(interest_rate*loan_size))/12,1)
    
    selected_option4 = request.form['option1']
    a.append(selected_option4)
    selected_option5 = request.form['option2']
    a.append(selected_option5)
    #print("VERY IMPORTANT #############################",a)
    
    if selected_option4==' ':
        holiday_months=selected_option5
        holiday_dur=1
    elif selected_option5==' ':
        holiday_months=selected_option4
        holiday_dur=1
    else:
        holiday_months=[selected_option4,selected_option5]
        holiday_dur=2

    if holiday_yn.lower()=='yes':
        holiday_txt = f"Repayment holiday applied for {holiday_dur} months --> {holiday_months}"

        return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt2,options_txt=grace_txt3,options2_txt=holiday_txt)#tableff=tableff,,grace_period_months_txt=grace_txt3)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))
    elif holiday_yn.lower()=='no':
        #df = pd.DataFrame(columns=['month','std_loan','flexible_loan'])
        #tablef = df.to_html(index=False)
        #grace_txt2_not="Grace period option NOT applied"
        holiday_txt = f"repayment holiday not applied"

        return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt2,options_txt=grace_txt3,options2_txt=holiday_txt)#,tablef=tablef,options_txt=grace_txt2_not)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

@app.route('/final_tables',methods=['POST'])
def final_tables():
        
    print("tables ###############################################")
#    print(grace_yn,holiday_yn)

    if len(a)<=8:
        loan_size_txt="Loan amount= {} egp".format(a[0])
        loan_size=a[0]
        frequency_txt2="Dispersment starts tomorrow (aka month {})".format(a[2])
        start_month=a[2].lower()
        grace_yn=a[3]
        grace_months=a[4]
        holiday_yn=a[5]
        holiday_month1=a[6]
        holiday_month2=a[7]


    else:
        loan_size_txt="Loan amount= {} egp".format(a[len(a)-8])
        loan_size=a[len(a)-8]
        frequency_txt2="Dispersment starts tomorrow (aka month {})".format(a[len(a)-6])
        start_month=a[len(a)-6].lower()
        grace_yn=a[len(a)-5]
        grace_months=a[len(a)-4]
        holiday_yn=a[len(a)-3]
        holiday_month1=a[len(a)-2]
        holiday_month2=a[len(a)-1]
        
    #holiday_months=[holiday_month1,holiday_month2]
    if holiday_month1==' ':
        holiday_months=holiday_month2
        holiday_dur=1
    elif holiday_month2==' ':
        holiday_months=holiday_month1
        holiday_dur=1
    else:
        holiday_months=[holiday_month1,holiday_month2]
        holiday_dur=2
        
    if grace_yn.lower()=='yes':
        grace_dur=int(grace_months)
        grace_txt3 = f"Grace period applied for {grace_months} months \n"
    else:
        grace_txt3 = f"Grace period not applied\n"

    if holiday_yn.lower()=='yes':
        #holiday_dur=len(holiday_months)
        holiday_txt = f"Repayment holiday applied for months --> {holiday_months}"
    else:
        holiday_txt = f"Repayment holiday not applied"

    df = pd.DataFrame(columns=['month','std_loan','flexible_loan'])
    monthly_share=round((loan_size+(interest_rate*loan_size))/12,1)

    if grace_yn.lower()=='no' and holiday_yn.lower()=='no':
        print("???????????????????????")
        num_months=12
        loc_start_month=options_month.index(start_month)

        for i in range(num_months):
            this_month=options_month[(loc_start_month+i)%12]
            new_line=[this_month,monthly_share,monthly_share]

            df.loc[i]=new_line
                
        df.loc[i+1]=["total",round(df['std_loan'].sum(),1),round(df['flexible_loan'].sum(),1)]
        print(df)


    elif grace_yn.lower()=='yes' and holiday_yn.lower()=='no':
        num_months=12+grace_dur
        loc_start_month=options_month.index(start_month.lower())
                
        updated_loan_size=loan_size*num_months/12
        updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
        
        
        for i in range(num_months):
            this_month=options_month[(loc_start_month+i)%12]
                    
            if i in range(grace_dur):
                new_line=[this_month,monthly_share,round(updated_monthly_intrest,1)]    
                df.loc[i]=new_line
            elif i>=12:
                new_line=[this_month,0,round(flexible_monthly_share,1)]  
                df.loc[i]=new_line
            else:
                new_line=[this_month,monthly_share,round(flexible_monthly_share,1)]    
                df.loc[i]=new_line
                
        df.loc[i+1]=["total",round(df['std_loan'].sum(),1),round(df['flexible_loan'].sum(),1)]
        print(df)

    elif grace_yn.lower()=='no' and holiday_yn.lower()=='yes':
        num_months=12+holiday_dur
        loc_start_month=options_month.index(start_month.lower())
                
        updated_loan_size=loan_size*num_months/12
        updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
        
        
        x=0

        for i in range(num_months):
            this_month=options_month[(loc_start_month+i)%12]
            print(i,this_month)

            if this_month in holiday_months and x<holiday_dur:
                #covered=1
                new_line=[this_month,monthly_share,round(updated_monthly_intrest,1)]    
                df.loc[i]=new_line
                x+=1
            
            elif i>=12:
                new_line=[this_month,0,round(flexible_monthly_share,1)]  
                df.loc[i]=new_line
            else:
                new_line=[this_month,monthly_share,round(flexible_monthly_share,1)]    
                df.loc[i]=new_line
        
        df.loc[i+1]=["total",round(df['std_loan'].sum(),1),round(df['flexible_loan'].sum(),1)]
        
    elif grace_yn.lower()=='yes' and holiday_yn.lower()=='yes':
        num_months=12+holiday_dur+grace_dur
        loc_start_month=options_month.index(start_month)
        
        updated_loan_size=loan_size*num_months/12
        updated_monthly_intrest=updated_loan_size*interest_rate/num_months
        flexible_monthly_share=updated_monthly_intrest+(updated_loan_size/num_months)
         
        x=0

        for i in range(num_months):
            this_month=options_month[(loc_start_month+i)%12]
            #print(i,this_month)

            if this_month in holiday_months and x<holiday_dur and i not in range(grace_dur):
                #print(this_month)
                new_line=[this_month,monthly_share,updated_monthly_intrest]    
                df.loc[i]=new_line
                x+=1
                if i>=num_months-holiday_dur-grace_dur:
                    new_line=[this_month,0,round(updated_monthly_intrest,0)]  
                    df.loc[i]=new_line
            elif i in range(grace_dur):
                new_line=[this_month,monthly_share,round(updated_monthly_intrest,1)]    
                df.loc[i]=new_line
              
            elif i>=num_months-holiday_dur-grace_dur:
                new_line=[this_month,0,round(flexible_monthly_share,1)]  
                df.loc[i]=new_line
            else:
                new_line=[this_month,monthly_share,round(flexible_monthly_share,1)]    
                df.loc[i]=new_line 
                
        df.loc[i+1]=["total",round(df['std_loan'].sum(),1),round(df['flexible_loan'].sum(),1)]
        
    tablef=tabulate(df, headers='keys', tablefmt='psql')
            
    tablef = df.to_html(index=False)
    
    return render_template('index_new_v2.html',loan_size_txt=loan_size_txt,frequency_txt=frequency_txt2,table_final=tablef,options_txt=grace_txt3,options2_txt=holiday_txt)#,grace_period_months_txt=grace_txt3)#tmp)#+"<br/>The provided loan size is {} EGP".format(output[0]))#.append('The size of the loan is {} egp\n'.format(loan_size[0])))

