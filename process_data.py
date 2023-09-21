from sklearn.linear_model import LinearRegression


def process_data(df):
    grouped_data = df.groupby(['Ano', 'Mês'])['Quantidade'].sum().reset_index()

    grouped_data = grouped_data[['Mês', 'Quantidade']].copy()
    grouped_data['Mes Sequencial'] = range(1, len(grouped_data) + 1)
    grouped_data['Média Móvel'] = grouped_data['Quantidade'].rolling(window=6, min_periods=1).mean()
    grouped_data['Média Móvel + 20%'] = grouped_data['Média Móvel'] * 1.2

    quantile_25 = grouped_data['Quantidade'].quantile(0.25)
    quantile_50 = grouped_data['Quantidade'].quantile(0.50)
    quantile_75 = grouped_data['Quantidade'].quantile(0.75)

    q25_list = []
    q50_list = []
    q75_list = []

    # Iterate through each row in the DataFrame
    for index, row in grouped_data.iterrows():
        # Get the current month
        current_month = row['Mes Sequencial']
        
        # Filter the DataFrame to include only past months (months before or including the current month)
        past_data = grouped_data[grouped_data['Mes Sequencial'] <= current_month]
        
        # Calculate the quantiles for the "Quantity" column of past_data
        q25 = past_data['Quantidade'].quantile(0.25)
        q50 = past_data['Quantidade'].quantile(0.50)
        q75 = past_data['Quantidade'].quantile(0.75)
        
        # Append the quantiles to the respective lists
        q25_list.append(q25)
        q50_list.append(q50)
        q75_list.append(q75)

    # Append the quantiles to the original DataFrame
    grouped_data['Q25'] = q25_list
    grouped_data['Q50'] = q50_list
    grouped_data['Q75'] = q75_list

    return {'data': grouped_data, 'quantile_25': quantile_25, 'quantile_50': quantile_50, 'quantile_75': quantile_75}


def calc_slope(df):
    processed_data = process_data(df)
    data = processed_data['data']
    last_data = data[['Mes Sequencial', 'Quantidade']].copy().tail(3)

    model = LinearRegression()

    X = last_data['Mes Sequencial'].values.reshape(-1, 1)
    y = last_data['Quantidade']
    # Fit the model to the data'
    model.fit(X, y)

    # Get the slope (trend) and intercept
    slope = model.coef_[0]

    return round(slope)

def calc_demand(df):
    grouped_data = df.groupby(['Ano', 'Mês'])['Quantidade'].sum().reset_index()
    q75 = grouped_data['Quantidade'].quantile(0.75)
    last_month_quantity = grouped_data['Quantidade'].iloc[-1]
    demand = last_month_quantity - q75
    return demand


