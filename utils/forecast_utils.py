import pandas as pd

def exp_smoothing(series, alpha=0.35):
    s = [series[0]]
    for i in range(1, len(series)):
        s.append(alpha * series[i] + (1 - alpha) * s[-1])
    return s

def forecast_next(series, steps=7):
    sm = exp_smoothing(series)
    last = sm[-1]
    return [last for _ in range(steps)]

def monthly_forecast(series):
    df = pd.Series(series)
    months = df.rolling(window=30).median().dropna()
    growth = (months.iloc[-1]/months.iloc[0])**(1/max(1, len(months)-1)) - 1
    return [months.iloc[-1]*(1+growth)**i for i in range(12)]
