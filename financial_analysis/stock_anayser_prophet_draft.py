import fbprophet    # Prophet requires columns ds (Date) and y (value)

# gm = gm.rename(columns={'Date': 'ds', 'cap': 'y'})      # Put market cap in billions
# gm['y'] = gm['y'] / 1e9     # Make the prophet model and fit on the data
# gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15)
# gm_prophet.fit(gm)
