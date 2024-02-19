def sip_calculator(annual_rate,principal,years,step_up = 0, inflation = 0,is_lumpsum = False):
    '''
    Handles Lump Sum, SIP, SIP With Step Up and 
    Inflation Adjusted Calculations
    '''
    lst = []
    if not is_lumpsum:
        months =  years * 12
        monthly_return = 0
        for i in range(0,months):
            monthly_return = (principal + (step_up if i > 12 else 0) + monthly_return) * (1 + (annual_rate - inflation) / 12)
            if(i % 12 == 0):
                lst.append(monthly_return)
    else:
        returnAmt = principal * ((1 + (annual_rate - inflation)) ** years)
        lst.append(returnAmt)
    return lst

def calculate_Fv(rate, nper, pmt, pv):
    fv = pv * ((1 + rate) ** nper) + pmt * (((1 + rate) ** nper - 1) / rate)
    return fv

def calculate_Pmt(rate,nper,pv,fv=0):
    if rate == 0:
        return -(pv + fv) / nper
    else:
        pmt = (rate * (pv + fv)) / ((1 + rate) ** nper - 1)
        return pmt
    
def retirement_portfolio_balance_swp_calculator(
    ppf_amt,pf_amt,nsc_amt, postal_amt, bank_amt, company_amt,insurance_amt, annual_amt_rate,
    equity_portfolio, balanced_portfolio, non_liquid_debt_portfolio, liquid_portfolio, 
    equity_rate,balanced_rate,non_liquid_rate, liquid_rate,swp_rate,
    sip,rd, sip_rate = 0.07,rd_rate = 0.08, year = 10,step_up = 0, inflation = 0
    ):
    '''
    calculate retirement balance and swp value 
    '''
    retirment_tracker = {}
    for i in range(0,year):
        if i == 0:
           retirment_tracker['ppf'] = [(1 + (annual_amt_rate - inflation)) * ppf_amt]
           retirment_tracker['pf'] = [(1 + (annual_amt_rate - inflation)) * pf_amt]
           retirment_tracker['nsc'] = [(1 + (annual_amt_rate - inflation)) * nsc_amt]
           retirment_tracker['postal'] = [(1 + (annual_amt_rate - inflation)) * postal_amt]
           retirment_tracker['bank'] = [(1 + (annual_amt_rate - inflation)) * bank_amt]
           retirment_tracker['company'] = [(1 + (annual_amt_rate - inflation)) * company_amt]
           retirment_tracker['insurance'] = [(1 + (annual_amt_rate - inflation)) * insurance_amt]
           retirment_tracker['equity'] = [(1 + (equity_rate - inflation)) * equity_portfolio]
           retirment_tracker['balanced'] = [(1 + (balanced_rate - inflation)) * balanced_portfolio]
           retirment_tracker['non_liquid'] = [(1 + (non_liquid_rate - inflation)) * non_liquid_debt_portfolio]
           retirment_tracker['liquid'] = [(1 + (liquid_rate - inflation)) * liquid_portfolio]
           retirment_tracker['sip'] = [calculate_Fv(sip_rate / 12,(i + 1) * 12,sip,0)]
           retirment_tracker['rd'] = [calculate_Fv(rd_rate / 12,(i + 1)  * 12,rd,0)]
        else:
            retirment_tracker['ppf'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['ppf'][-1])
            retirment_tracker['pf'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['pf'][-1])
            retirment_tracker['nsc'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['nsc'][-1])
            retirment_tracker['postal'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['postal'][-1])
            retirment_tracker['bank'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['bank'][-1])
            retirment_tracker['company'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['company'][-1])
            retirment_tracker['insurance'].append((1 + (annual_amt_rate - inflation)) * retirment_tracker['insurance'][-1])
            retirment_tracker['equity'].append((1 + (equity_rate - inflation)) * retirment_tracker['equity'][-1])
            retirment_tracker['balanced'].append((1 + (balanced_rate - inflation)) * retirment_tracker['balanced'][-1])
            retirment_tracker['non_liquid'].append((1 + (non_liquid_rate - inflation)) * retirment_tracker['non_liquid'][-1])
            retirment_tracker['liquid'].append((1 + (liquid_rate - inflation)) * retirment_tracker['liquid'][-1])
            retirment_tracker['sip'].append(calculate_Fv(sip_rate / 12,(i + 1)  * 12,sip,0))
            retirment_tracker['rd'].append(calculate_Fv(rd_rate / 12,(i + 1)  * 12,rd,0))
    retirment_tracker['final'] = []
    for i in range(year):
        valuation = 0
        for scheme in retirment_tracker:
            if scheme == 'final':
                break
            valuation += retirment_tracker[scheme][i]
        retirment_tracker['final'].append({ "balance":valuation,"swp":0.08 * valuation })
    return retirment_tracker

def calculate_total_return_with_lumpsum_and_sip(initial_lumpsum,principal,rate,years):
    return calculate_Fv(rate/12,years*12,principal,initial_lumpsum)

def calculate_differential_returns_by_age(age,retirement, corpus, rate,inflation = 0):
    result = {}
    result['monthly'] = calculate_Pmt((rate - inflation)/12,(retirement - age) * 12,0,corpus)
    result['yearly'] = result['monthly'] * 12
    return result

def calculate_Pv(rate, nper, pmt, fv=0):
    if rate == 0:
        return -(fv + pmt * nper)
    else:
        pv = pmt * ((1 - (1 + rate) ** -nper) / rate) + fv / (1 + rate) ** nper
        return pv

def calculate_required_sip_amt(current_age, retirement_age, rate, inflation, monthly_expense, assumed_future_return,assumed_future_inflation,residual_amt):
    amout_required_monthly = calculate_Fv(inflation,retirement_age - current_age,0,monthly_expense)
    print((assumed_future_return - assumed_future_inflation)/12,12*(100-retirement_age),amout_required_monthly,residual_amt)
    required_capital = calculate_Pv((assumed_future_return - assumed_future_inflation)/12,12*(100-retirement_age),amout_required_monthly,residual_amt)
    required_sip_amt = calculate_Pmt((rate - inflation) / 12,12 * (retirement_age - current_age),0,required_capital)
    result ={"Required SIP Amount":required_sip_amt,"Required Capital":required_capital,"Monthly Required Amount":amout_required_monthly}
    return result
    
    
def distributor_commission_calculator(sip_amt,rate,commission_rate,time):
    val = []
    dict = {}
    for i in range(time):
        info = {}
        info['aum'] = (12 * sip_amt) * (i + 1)
        info['aum'] = calculate_Fv(rate / 12,(i + 1) * 12,sip_amt,0)
        info['commission'] = (commission_rate / 100) * info['aum']
        info['value_at_' + str(time) + "_years"] = calculate_Fv(rate,time - (i + 1),0,info['commission'])
        val.append(info)
    dict['val'] = val
    dict['total_commission'] = sum([info['commission'] for info in dict['val']])
    dict['cumulative_val_at_' + str(time) + "_years"] = sum([info['value_at_' + str(time) + "_years"] for info in dict['val']])
    return dict

def revenue_model_sip_book_size_one_time_book_size(sip_book_size,rate,commission,equity_aum,time):
    val = []
    for i in range(time):
        info = {}
        info['sip_book_size_future_value'] =  calculate_Fv(rate / 12,(i + 1) * 12,sip_book_size,0)
        info['sip_book_size_commission'] =   (commission / 100) * info['sip_book_size_future_value']
        info['equity_aum_future_value'] = calculate_Fv(rate,(i + 1),0,equity_aum)
        info['equity_aum_commission'] = (commission / 100) * info['equity_aum_future_value']
        info['gross_commission'] = info['sip_book_size_commission'] + info['equity_aum_commission']
        val.append(info)
    return val

def difference_between_insurance_and_sip_commission(invest_amount,insurance_commission_avg,cap_appreciation_rate,trail,time):
    val = []
    result = {}
    for i in range(time):
        info = {}
        info['insurance_paid_amount'] = insurance_commission_avg * invest_amount
        if i == 0:
            info['cap_appreciation'] = cap_appreciation_rate * invest_amount
            info['cumulative_value'] = invest_amount + info['cap_appreciation']
        else:
            info['cap_appreciation'] = (invest_amount  + val[i - 1]['cumulative_value']) * cap_appreciation_rate
            info['cumulative_value'] = val[i - 1]['cumulative_value'] + invest_amount + info['cap_appreciation']
        info['upfront_tail'] = (trail / 100) * info['cumulative_value']
        val.append(info)
    result['val'] = val
    result['total_insurance_commission'] = sum([info['insurance_paid_amount'] for info in result['val']])
    result['total_upfront_trail'] = sum([info['upfront_tail'] for info in result['val']])
    return result

if __name__ == "__main__":
    val = retirement_portfolio_balance_swp_calculator(
    200000,200000,200000, 200000, 200000, 200000,200000, 0.065,
    100000, 100000, 100000, 100000, 
    0.12,0.1,0.08, 0.06,0.08,
    4500,3000, 0.12,0.065, 10,0,0
    )
    #print(val['final'])
    #print(calculate_total_return_with_lumpsum_and_sip(2500000,5000,0.12,10))
    #print(calculate_differential_returns_by_age(25,60,10000000,0.12))
    #print(calculate_required_sip_amt(24,60,0.12,0.04,40000,0.07,0.02,20000000))
    #print(distributor_commission_calculator(10000,0.12,0.75,35))
    #print(revenue_model_sip_book_size_one_time_book_size(1250000,0.1,0.5,80000000,35))
    print(difference_between_insurance_and_sip_commission(100000,0.225,0.12,0.5,20))