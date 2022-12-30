import pandas as pd
import numpy as np
import pickle
import inflection
import math

from datetime import datetime, timedelta

class Rossmann(object):
    def __init__(self):
        self.home_path = ''

        # scalers
        self.competition_distance_scaler = pickle.load(open('parameter/competition_distance_scaler.pkl', 'rb'))
        self.competition_open_since_scaler = pickle.load(open('parameter/competition_open_since_scaler.pkl', 'rb'))
        self.competition_duration_scaler = pickle.load(open('parameter/competition_duration_scaler.pkl', 'rb'))

        self.promo2_since_scaler = pickle.load(open('parameter/promo2_since_scaler.pkl', 'rb'))
        self.promo_time_week_scaler = pickle.load(open('parameter/promo_time_week_scaler.pkl', 'rb'))
        self.week_of_year_scaler = pickle.load(open('parameter/week_of_year_scaler.pkl', 'rb'))

        # encoders
        self.store_type_encoder = pickle.load(open('parameter/store_type_encoder.pkl', 'rb'))

    def data_cleaning(self, df1):
        # rename columns 
        snakecase = lambda x: inflection.underscore( x )

        df1.columns = list( map( snakecase, df1.columns.values ) )

        # change 'date' dtype
        df1['date'] = pd.to_datetime( df1['date'] )

        # Tratando valores NAs
        df1['competition_distance'].fillna(0, inplace=True)
        df1['promo_interval'].fillna(0, inplace=True)
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)
        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].weekofyear if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)
        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)

        # changing dtypes of varibles
        # competition_open_since_year -> int
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(int)

        # competition_open_since_month -> int
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(int)

        # promo2_since_year -> int
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(int)

        # promo2_since_week -> int
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(int)

        return df1

    def feature_engineering(self, df2):
        # day
        df2['day'] = df2['date'].dt.day

        # month
        df2['month'] = df2['date'].dt.month

        # year
        df2['year'] = df2['date'].dt.year

        # week_of_year
        df2['week_of_year'] = df2['date'].dt.weekofyear

        # year_week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')

        # assortment
        assortment_map = {'a': 'basic', 'b': 'extra', 'c': 'extended'}
        df2['assortment'] = df2['assortment'].map(assortment_map)

        # state_holiday
        state_holiday_map = { 'a': 'public holiday', 'b': 'Easter holiday', 'c': 'Christmas', '0': 'regular_day'}
        df2['state_holiday'] = df2['state_holiday'].map(state_holiday_map)

        # competition_open_since
        df2['competition_open_since'] = df2.apply(lambda x: datetime(year=x['competition_open_since_year'] if x['competition_open_since_year'] != 0 else x['date'].year, \
            month=x['competition_open_since_month'] if x['competition_open_since_month'] != 0 else x['date'].month, day=1), axis=1)

        # competition_duration
        df2['competition_duration'] = df2.apply(lambda x: np.round((x['date'] - x['competition_open_since']).days / 30).astype(int) if x['date'] > x['competition_open_since']  else 0, axis=1)

        # promo2_since
        df2['promo2_since'] = df2.apply(lambda x: f"{x['promo2_since_year']}-{x['promo2_since_week']}" if  x['promo2_since_year'] != 0 else x['date'].strftime('%Y-%W'), axis=1)

        df2['promo2_since'] = df2['promo2_since'].apply( lambda x: datetime.strptime( x + '-1', '%Y-%W-%w' ) - timedelta( days=7 ) )

        df2['promo_time_week'] = ( ( df2['date'] - df2['promo2_since'] ) / 7 ).apply(lambda x: x.days ).astype( int )

        # promo_interval
        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', \
            8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        df2['month_map'] = df2['month'].map( month_map )
        df2['is_promo'] = df2[['promo_interval', 'month_map']].apply( lambda x: 0 if x['promo_interval'] == 0 else 1 \
            if x['month_map'] in x['promo_interval'].split( ',' ) else 0, axis=1 ).astype('bool')
        df2.loc[(df2['promo_time_week'] == 0) & (df2['is_promo'] == 1), 'promo_time_week'] = 1

        # Data Filtering
        #  rows
        df2 = df2[df2['open'] == True]

        # columns
        df2 = df2.drop(columns=['open', 'promo_interval', 'month_map'])

        return df2

    def data_preparation(self, df3):
        # Scaler
        # competition_distance -> RobustScaler
        df3['competition_distance'] = self.competition_distance_scaler.fit_transform(df3[['competition_distance']].values)

        # competition_open_since -> RobustScaler
        df3['competition_open_since'] = self.competition_open_since_scaler.fit_transform(df3[['competition_open_since']].values)

        # competition_duration -> RobustScaler
        df3['competition_duration'] = self.competition_duration_scaler.fit_transform(df3[['competition_duration']].values)

        # promo2_since -> MinMaxScaler
        df3['promo2_since'] = self.promo2_since_scaler.fit_transform(df3[['promo2_since']].values)

        # promo_time_week -> MinMaxScaler
        df3['promo_time_week'] = self.promo_time_week_scaler.fit_transform(df3[['promo_time_week']].values)

        # week_of_year -> MinMaxScaler
        df3['week_of_year'] = self.week_of_year_scaler.fit_transform(df3[['week_of_year']].values)

        # Encoders
        # promo, school_holiday, promo2, is_promo -> OneHot
        df3 = pd.get_dummies( df3, prefix=['state_holiday'], columns=['state_holiday'] )

        # store_type -> Label *
        df3['store_type'] = self.store_type_encoder.fit_transform(df3['store_type'])

        # assortment - Ordinal Encoding
        assortment_dict = {'basic': 1,  'extra': 2, 'extended': 3}
        df3['assortment'] = df3['assortment'].map( assortment_dict )

        # Transformations
        # cicles
        # day of week
        df3['day_of_week_sin'] = df3['day_of_week'].apply( lambda x: np.sin( x * ( 2. * np.pi/7 ) ) )
        df3['day_of_week_cos'] = df3['day_of_week'].apply( lambda x: np.cos( x * ( 2. * np.pi/7 ) ) )

        # month
        df3['month_sin'] = df3['month'].apply( lambda x: np.sin( x * ( 2. * np.pi/12 ) ) )
        df3['month_cos'] = df3['month'].apply( lambda x: np.cos( x * ( 2. * np.pi/12 ) ) )

        # day 
        df3['day_sin'] = df3['day'].apply( lambda x: np.sin( x * ( 2. * np.pi/30 ) ) )
        df3['day_cos'] = df3['day'].apply( lambda x: np.cos( x * ( 2. * np.pi/30 ) ) )

        # week of year
        df3['week_of_year_sin'] = df3['week_of_year'].apply( lambda x: np.sin( x * ( 2. * np.pi/52 ) ) )
        df3['week_of_year_cos'] = df3['week_of_year'].apply( lambda x: np.cos( x * ( 2. * np.pi/52 ) ) )

        # Feature Selection
        cols_selected = ['store','promo','store_type',
        'assortment','competition_distance','competition_open_since_month','competition_open_since_year','promo2','promo2_since_week',
        'promo2_since_year','competition_duration','promo_time_week','day_of_week_sin','day_of_week_cos',
        'month_sin','month_cos','day_sin','day_cos','week_of_year_sin','week_of_year_cos',]

        return df3[cols_selected]

    def get_prediction(self, model, original_data, test_data):
        # prediction
        pred = model.predict(test_data)

        # join pred into the original data
        original_data['prediction'] = np.expm1(pred)

        return original_data.to_json(orient='records', date_format='iso')