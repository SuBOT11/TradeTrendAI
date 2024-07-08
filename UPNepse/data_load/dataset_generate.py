
import pandas as pd
import json
import os


def get_cleaned_f_data(company):
    with open(f'/mnt/d/CollegeProject/UPNepse/data_preparation/financial_data_transform/data/{company}/financials.json','r') as fj:

        fin_json = json.load(fj)
    df = pd.DataFrame(fin_json)
    df['start_date'] = pd.to_datetime(df['start_date'],unit='ms')
    df['end_date'] = pd.to_datetime(df['end_date'],unit='ms')
    df.drop('fiscal_year',axis=1,inplace=True)
    for col in df.columns:
            if  col not in ['symbol','start_date','end_date']:
                    df[col] = df[col].astype(float)

    zero_columns = df.columns[df.eq(0).all()]
    df.drop(zero_columns,axis=1,inplace=True)
    zero_counts = (df == 0).sum()
    columns_to_drop = zero_counts[zero_counts >= 3].index
    df.drop(columns_to_drop,axis=1,inplace=True)
    df.sort_values(by='start_date',inplace=True)
    df.reset_index(drop=True,inplace=True)


    new_rows = []
    for idx, row in df.iterrows():
        dates = pd.date_range(start=row['start_date'], end=row['end_date'])
        column_to_remove = ['end_date']

        values = [row[col] for col in df.columns if col not in ['start_date', 'end_date']]
        new_columns = [col for col in df.columns if col not in column_to_remove]
        for date in dates:
                new_row = {col: value for col, value in zip(new_columns, [date] + values)}

                new_rows.append(new_row)

    new_df = pd.DataFrame(new_rows)
    return new_df


def get_cleaned_d_data(company):
    with open(f'/mnt/d/CollegeProject/UPNepse/data_preparation/dividend_data_transform/data/{company}/dividend.json','r') as fj:
        data_json = json.load(fj)
    
    dividend_df = pd.DataFrame(data_json)
    dividend_df['book_closure_date']
    
    change_col = ['bonus_dividend','cash_dividend']
    dividend_df[change_col] = dividend_df[change_col].astype(float)
    dividend_df['start_date'] = pd.to_datetime(dividend_df['start_date'],unit='ms')
    dividend_df['end_date'] = pd.to_datetime(dividend_df['end_date'],unit='ms')
    dividend_df['book_closure_date'] = pd.to_datetime(dividend_df['book_closure_date'])
    dividend_df.drop('fiscal_year',axis=1,inplace=True)
    dividend_df.drop('dividend_growth_rate',axis=1,inplace=True)
    dividend_df.sort_values(by='start_date',inplace=True)
    dividend_df.reset_index(drop=True,inplace=True)
    new_dividend_rows = []
    for idx, row in dividend_df.iterrows():
        dates = pd.date_range(start=row['start_date'], end=row['end_date'])
        column_to_remove = ['end_date']
    
        values = [row[col] for col in dividend_df.columns if col not in ['start_date', 'end_date']]
        new_columns = [col for col in dividend_df.columns if col not in column_to_remove]
        for date in dates:
                new_row = {col: value for col, value in zip(new_columns, [date] + values)}
    
                new_dividend_rows.append(new_row)
        
    new_dividend_df = pd.DataFrame(new_dividend_rows)
    new_dividend_df['book_closure_flag'] = 0
    new_dividend_df.loc[new_dividend_df['start_date'] == new_dividend_df['book_closure_date'], 'book_closure_flag'] = 1
    new_dividend_df.drop(['book_closure_date','symbol'],axis=1,inplace=True)

    return new_dividend_df


def get_cleaned_stock_data(company):

    stock_df = pd.read_parquet(f'/mnt/d/CollegeProject/UPNepse/data_preparation/stock_data_preparation/data/{company}.parquet')
    stock_df['gap_up'] = stock_df['Open'] - stock_df['Close'].shift(1) 
    stock_df['gap_down'] = stock_df['Close'].shift(1) - stock_df['Open']
    stock_df['price_change'] = stock_df['Close'].pct_change() * 100
    stock_df.fillna(method='bfill', inplace=True)
    stock_df.fillna(method='ffill', inplace=True)
    return stock_df
    


def merge_all_data(company):
    print(company)
    fdf = get_cleaned_f_data(company)
    fdf.rename(columns={'start_date':'date'},inplace=True)
    fdf['date'] = pd.to_datetime(fdf['date'])
    ddf = get_cleaned_d_data(company)
    ddf.rename(columns={'start_date':'date'},inplace=True)
    ddf['date'] = pd.to_datetime(ddf['date'])
    sdf = get_cleaned_stock_data(company)
    sdf.rename(columns={'Date':'date'},inplace=True)
    sdf['date'] = pd.to_datetime(sdf['date'])
    with open('/mnt/d/CollegeProject/UPNepse/data_preparation/news_data_transform/data/news.json','r') as nf:
        news_json = json.load(nf)
        for news in news_json:
            if company in news:
                news_df = pd.DataFrame({'date':news[company]})
                news_df['date'] = pd.to_datetime(news_df['date'])


    
    merged_df = pd.merge(sdf, fdf, on='date', how='left') 
    merged_df = pd.merge(merged_df, ddf, on='date', how='left') 
    merged_df['news_flag'] = merged_df['date'].isin(news_df['date']).astype(int)

    merged_df = merged_df[merged_df['date'] >= pd.to_datetime('2016-07-14')]
    try:
        merged_df['bonus_dividend']  = merged_df['bonus_dividend'].astype(float)
    except Exception as e:
        print(e)

    merged_df['symbol'] = merged_df['symbol'].astype(str)
    merged_df['symbol'].fillna(method='bfill',inplace=True)
    columns_with_missing_values = merged_df.columns[merged_df.isnull().any()].tolist()
    for col in columns_with_missing_values:
        merged_df[col] = merged_df[col].interpolate()


    merged_df.dropna(inplace=True)
    return merged_df
    





def generate_dataset():
    companies = []
    companies = os.listdir('/mnt/d/CollegeProject/UPNepse/data_preparation/dividend_data_transform/data')
    column_list = ['date', 'Close', 'Open', 'High', 'Low', 'Volume', 'SMA_20', 'SMA_100',
       'EMA_20', 'EMA_100', 'RSI_14', 'ROC_12', 'ATR_14', 'SD_20', 'OBV',
       'ADX_14', 'symbol', 'ShareCapital', 'ReserveAndFunds',
       'LoansAndBorrowings', 'DepositLiabilities', 'OtherLiabilities',
       'TotalCapital&Liabilities', 'CashBalance', 'BalanceWithNepalRastraBank',
       'BalanceWithBanks/FinancialInstitutions', 'MoneyAtCallAndShortNotice',
       'Loans,AdvancesAndBillsPurchased', 'FixedAssets', 'OtherAssets',
       'TotalAssets', 'InterestIncome', 'InterestExpenses',
       'NetInterestIncome', 'Commission&OtherOperatingIncome',
       'TotalOperatingIncome', 'StaffExpenses', 'OtherOperatingExpenses',
       'OperatingProfitBeforeProvisionForPossibleLosses',
       'ProvisionForPossibleLosses', 'OperatingProfit',
       'ProfitFromRegularActivities', 'NetProfitAfterConsideringAllActivities',
       'ProvisionForStaffBonus', 'ProvisionForIncomeTax',
       "I.CurrentYear'STaxProvision",
       "Iii.CurrentYear'SDeferredTaxExpenses(Income)", 'NetProfit/(Loss)',
       'CreditToDepositRatio', 'A.CoreCapital', 'B.SupplementaryCapital',
       'C.TotalCapitalFund', 'Liquidity(Crr)',
       'NonPerformingLoans(Npl)ToTotalLoans', 'Wt.AverageInterestRateSpread',
       'TotalNo.OfEmployees', 'bonus_dividend', 'cash_dividend',
       'book_closure_flag', 'news_flag']
    merged_dataset_df = pd.DataFrame(columns=column_list)
    
    for company in companies:
        
        dataset_df = merge_all_data(company)
        print(dataset_df.shape)
        merged_dataset_df = pd.concat([merged_dataset_df,dataset_df],join='inner',ignore_index=True)
        dataset_df.to_parquet(f'/mnt/d/CollegeProject/UPNepse/data_load/data/{company}.parquet')

        
    print(merged_dataset_df.shape)
    merged_dataset_df.to_parquet('final_dataset.parquet')
generate_dataset()