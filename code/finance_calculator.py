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
    

if __name__ == "__main__":
    val = retirement_portfolio_balance_swp_calculator(
    200000,200000,200000, 200000, 200000, 200000,200000, 0.065,
    100000, 100000, 100000, 100000, 
    0.12,0.1,0.08, 0.06,0.08,
    4500,3000, 0.12,0.065, 10,0,0
    )
    #print(val['final'])
    #print(calculate_total_return_with_lumpsum_and_sip(2500000,5000,0.12,10))