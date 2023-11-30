import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

class DelayModel:

    FEATURES_COLS = [
        "OPERA_Latin American Wings",
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air"
    ]

    def __init__(self):
        self._model = None

    def preprocess(self, data: pd.DataFrame, target_column: str = None):
        data['period_day'] = data['Fecha-I'].apply(self.get_period_day)
        data['high_season'] = data['Fecha-I'].apply(self.is_high_season)
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')],
            axis=1
        )[self.FEATURES_COLS]

        target = data['delay']

        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

        n_y0 = len(y_train[y_train == 0])
        n_y1 = len(y_train[y_train == 1])
        scale = n_y0 / n_y1

        x_train2, x_test2, y_train2, y_test2 = train_test_split(features[self.FEATURES_COLS], target, test_size=0.33,
                                                                random_state=42)

        self._model = LogisticRegression(class_weight={1: n_y0 / len(y_train), 0: n_y1 / len(y_train)})
        self._model.fit(x_train2, y_train2)
        
        target = data[['delay']]

        if target_column:
            return features, target
        else:
            return features

    def fit(self, features: pd.DataFrame, target: pd.DataFrame):
        self._model.fit(features, target)

    def predict(self, features: pd.DataFrame):
        return self._model.predict(features[self.FEATURES_COLS]).tolist()

    @staticmethod
    def get_period_day(date):
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()

        if morning_min <= date_time <= morning_max:
            return 'mañana'
        elif afternoon_min <= date_time <= afternoon_max:
            return 'tarde'
        elif (evening_min <= date_time <= evening_max) or (night_min <= date_time <= night_max):
            return 'noche'

    @staticmethod
    def is_high_season(fecha):
        fecha_año = int(fecha.split('-')[0])
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year=fecha_año)
        range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year=fecha_año)
        range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year=fecha_año)
        range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year=fecha_año)
        range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year=fecha_año)
        range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year=fecha_año)
        range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year=fecha_año)
        range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year=fecha_año)

        if (range1_min <= fecha <= range1_max) or (range2_min <= fecha <= range2_max) or \
                (range3_min <= fecha <= range3_max) or (range4_min <= fecha <= range4_max):
            return 1
        else:
            return 0

    @staticmethod
    def get_min_diff(data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
        return min_diff
