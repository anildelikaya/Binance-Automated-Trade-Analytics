import pandas as pd
from datetime import datetime
from glob import glob
from database.db_utils import insert_data, create_table


def load_all_previous_data(folder_path, file_pattern):
    datetime_columns = ['Date_UTC_IN', 'Date_UTC_OUT']
    timedelta_column = 'Trade_Duration'

    all_files = glob(f"{folder_path}/{file_pattern}")
    all_dfs = [pd.read_csv(file, parse_dates=datetime_columns,converters={timedelta_column: pd.to_timedelta}) for file in all_files]
    if all_dfs:

        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def process_data(data,all_previous_data):

    ####################### Importing DATA ######################################
    # read exel file in desktop in my ubuntu and
    df = data
    df['Date(UTC)'] = pd.to_datetime(df['Date(UTC)'])

    ####################### Extracting DATA ######################################
    # Identify changes between zero and non-zero values
    df['is_zero'] = df['Realized Profit'] == 0
    df['group'] = df['is_zero'].ne(df['is_zero'].shift()).cumsum()

    # Group by the changes and aggregate
    result = df.groupby('group').agg({
        'Date(UTC)': 'first',
        'Symbol': 'first',
        'Side':'first',
        'Price': 'mean',
        'Quantity': 'sum',
        'Amount': 'sum',
        'Fee': 'sum',
        'Realized Profit': 'sum',
    }).sort_values(by='group').reset_index(drop=True)

    #

    # Rename columns
    df_out = result[result['Realized Profit'] != 0].reset_index(drop=True)
    df_out.columns = [col + '_OUT' if i < len(df_out.columns) - 1 else col for i, col in enumerate(df_out.columns)]
    df_in = result[result['Realized Profit'] == 0].reset_index(drop=True)
    df_in.columns = [col + '_IN' if i < len(df_in.columns) - 1 else col for i, col in enumerate(df_in.columns)]
    df_in = df_in.drop('Realized Profit', axis=1)

    

    # Merge the two dataframes
    df_in = df_in.reset_index(drop=True)
    df_out = df_out.reset_index(drop=True)
    df_combined = pd.concat([df_in, df_out], axis=1)
    df_combined.rename(columns={'Date(UTC)_IN': 'Date_UTC_IN', 'Date(UTC)_OUT': 'Date_UTC_OUT','Realized Profit': 'Realized_Profit'}, inplace=True)
    ############################## Feature Extraction #################################333
    # Create 'Trade_Duration' column
    df_combined['Trade_Duration'] = df_combined['Date_UTC_OUT'] - df_combined['Date_UTC_IN']
    # Create 'Position' column
    df_combined['Position'] = df_combined['Side_IN'].apply(lambda x: 'LONG' if x == 'BUY' else 'SHORT')
    # Create 'Total_Fee' column
    df_combined['Total_Fee'] = df_combined['Fee_IN'] + df_combined['Fee_OUT']
    # Create 'Percentage' column
    df_combined['Percentage'] = ((df_combined['Price_OUT'] - df_combined['Price_IN']) / df_combined['Price_IN']) * 100
    # Create 'Earning' column
    df_combined['Earning'] =   df_combined['Realized_Profit'] - df_combined['Total_Fee']

    df_combined.sort_values(by='Date_UTC_IN',inplace=True)
    df_combined.reset_index(drop=True, inplace=True)

    # Create KASA
    start_money = 927
    df_combined['Total_Money'] = df_combined['Earning'].cumsum() + start_money

    #dasdsa
    df_combined['Leverage'] = 100* df_combined['Realized_Profit']/ df_combined.Percentage/20

    # Final Representation
    column_order = [
        'Date_UTC_IN', 'Date_UTC_OUT','Trade_Duration', 'Symbol_IN', 
        'Position','Price_IN', 'Price_OUT','Percentage', 'Quantity_IN', 
        'Amount_IN', 'Amount_OUT', 'Fee_IN', 'Fee_OUT','Total_Fee', 'Realized_Profit','Earning','Total_Money', 'Leverage'
    ]
    df_combined = df_combined[column_order]

    # If previous data is provided, remove duplicates
    if not all_previous_data.empty:
        # Create tuples of the key columns for comparison
        key_columns = ['Date_UTC_IN', 'Date_UTC_OUT']
        df_key_tuples = df_combined[key_columns].apply(tuple, axis=1)
        previous_data_key_tuples = all_previous_data[key_columns].apply(tuple, axis=1)

        # Perform an anti-join to keep only rows in df that are not in all_previous_data
        df_combined = df_combined[~df_key_tuples.isin(previous_data_key_tuples)]
    return df_combined

def save_processed_data(df,output_folder):
    # Check if there are new unique rows to save
    if not df.empty:
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_folder}/Processed_Trade_History_{timestamp}.csv"
        # Save the processed DataFrame to a new csv file
        df.to_csv(output_path, index=False)

    else:
        print("No new unique rows to save.")

def data_processor_and_db_insert(df):

    #input_path = file_path
    output_folder = './data/processed'
    file_pattern = "Processed_Trade_History_*.csv"
    table_name = 'TRADE_HISTORY'

    # Load all previous processed data
    all_previous_data = load_all_previous_data(output_folder, file_pattern)

    processed_df = process_data(df,all_previous_data)
    save_processed_data(processed_df, output_folder)

    if not processed_df.empty:
        create_table()

        # Convert DataFrame to a list of tuples for insertion
        data_tuples = list(processed_df.itertuples(index=False, name=None))

        # Insert data into the database
        insert_data(data_tuples,table_name,processed_df.columns )




if __name__ == '__main__':

    input_path = './data/raw/Export Trade History.xlsx'
    
    df = pd.read_excel(input_path, engine='openpyxl')
    data_processor_and_db_insert(df)




    

