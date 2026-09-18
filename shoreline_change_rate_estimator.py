import pandas as pd
import numpy as np
from datetime import datetime

def estimate_shoreline_change_rates(df, convention="seaward_positive"):
    """
    Estimates shoreline change rates from repeated shore-normal position measurements.
    
    Args:
        df: DataFrame with 'date' (YYYY-MM-DD) and 'position_m' columns
        convention: 'seaward_positive' or 'landward_positive'
    
    Returns:
        Dictionary containing:
        - data: processed DataFrame with additional columns
        - end_point_rate: end-point rate calculation
        - regression_rate: linear regression rate
        - r_squared: coefficient of determination
        - confidence_interval: 95% confidence interval for regression rate
        - num_points: number of valid data points
        - date_range: tuple of first and last dates
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Apply convention transformation if needed
    if convention == "landward_positive":
        df["position_m"] = df["position_m"] * -1
    
    # Clean and validate data
    df = df.dropna(subset=['date', 'position_m'])
    df = df[df['date'].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}$')]
    df['position_m'] = pd.to_numeric(df['position_m'], errors='coerce')
    df = df.dropna(subset=['position_m'])
    
    if len(df) < 2:
        raise ValueError("At least two valid data points are required")
    
    # Sort by date
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # Convert dates to decimal years
    def date_to_decimal_year(date):
        year = date.year
        start_of_year = datetime(year, 1, 1)
        next_year = datetime(year + 1, 1, 1)
        year_duration = (next_year - start_of_year).days
        day_of_year = (date - start_of_year).days
        return year + day_of_year / year_duration
    
    df['decimal_year'] = df['date'].apply(date_to_decimal_year)
    
    # Prepare data arrays
    x = df['decimal_year'].values
    y = df['position_m'].values
    n = len(x)
    
    # Calculate means
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    # Calculate linear regression parameters
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    
    if denominator == 0:
        raise ValueError("Cannot calculate regression: all time values are identical")
    
    regression_rate = numerator / denominator
    intercept = y_mean - regression_rate * x_mean
    
    # Calculate fitted values and statistics
    fitted_values = intercept + regression_rate * x
    df['fitted_values'] = fitted_values
    
    # Calculate R-squared
    ss_total = np.sum((y - y_mean) ** 2)
    ss_residual = np.sum((y - fitted_values) ** 2)
    r_squared = 1 - (ss_residual / ss_total) if ss_total != 0 else 0
    
    # Calculate standard error of the slope
    mse = ss_residual / (n - 2)  # mean squared error
    std_error_slope = np.sqrt(mse / denominator)
    
    # Calculate 95% confidence interval for slope
    # Using t-distribution with n-2 degrees of freedom
    alpha = 0.05
    dof = n - 2
    t_value = abs(np.percentile(np.random.standard_t(dof, size=100000), alpha/2*100))  # Approximation
    # More precise calculation using scipy if available, but we'll implement manually
    # For more accurate t-value, we'll use the formula for t-distribution quantile
    # Using approximation based on normal distribution for large samples
    # For smaller samples, this is a simplification
    if n > 30:
        # For large samples, t approaches normal
        t_95 = 1.96
    else:
        # Approximate t-values for common degrees of freedom
        t_vals = {
            1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
            9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
            16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 24: 2.064, 30: 2.042
        }
        t_95 = t_vals.get(dof, 2.0)  # Default to 2.0 for dof not in table
    
    margin_of_error = t_95 * std_error_slope
    confidence_interval = (regression_rate - margin_of_error, regression_rate + margin_of_error)
    
    # Calculate end-point rate
    end_point_rate = (y[-1] - y[0]) / (x[-1] - x[0])
    
    # Get date range
    date_range = (df['date'].iloc[0].strftime('%Y-%m-%d'), df['date'].iloc[-1].strftime('%Y-%m-%d'))
    
    return {
        'data': df,
        'end_point_rate': end_point_rate,
        'regression_rate': regression_rate,
        'r_squared': r_squared,
        'confidence_interval': confidence_interval,
        'num_points': n,
        'date_range': date_range
    }
