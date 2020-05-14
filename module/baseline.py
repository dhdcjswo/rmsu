import numpy as np

class Baseline():
    """Calculate baseline predictions."""

    def __init__(self, train_data):
        """Simple heuristic-based transductive learning to fill in missing
        values in data matrix."""
        self.predict(train_data.copy())

    def predict(self, train_data):
        raise NotImplementedError(
            'baseline prediction not implemented for base class')

    def rmse(self, test_data):
        """Calculate root mean squared error for predictions on test data."""
        I = ~np.isnan(test_data)   # indicator for missing values
        N = I.sum()                # number of non-missing values
        sqerror = abs(test_data - self.predicted) ** 2  # squared error array
        mse = sqerror[I].sum() / N                 # mean squared error
        return np.sqrt(mse)      
        

    def __str__(self):
        return split_title(self.__class__.__name__)


# Implement the 3 baselines.

class UniformRandomBaseline(Baseline):
    """결측치를 random하게 샘플링한 값으로 보간"""

    def predict(self, train_data):
        nan_mask = np.isnan(train_data)
        masked_train = np.ma.masked_array(train_data, nan_mask)
        pmin, pmax = masked_train.min(), masked_train.max()
        N = nan_mask.sum()
        train_data[nan_mask] = np.random.uniform(pmin, pmax, N)
        self.predicted = train_data


class GlobalMeanBaseline(Baseline):
    """결측치를 전체 평균 값으로 보간"""

    def predict(self, train_data):
        nan_mask = np.isnan(train_data)
        train_data[nan_mask] = train_data[~nan_mask].mean()
        self.predicted = train_data


class MeanOfMeansBaseline(Baseline):
    """결측치를 유저평균,영화평균,전체평균의 평균값으로 채움"""

    def predict(self, train_data):
        nan_mask = np.isnan(train_data)
        masked_train = np.ma.masked_array(train_data, nan_mask)
        global_mean = masked_train.mean()
        user_means = masked_train.mean(axis=1)
        item_means = masked_train.mean(axis=0)
        self.predicted = train_data.copy()
        n, m = train_data.shape
        for i in range(n):
            for j in range(m):
                if np.ma.isMA(item_means[j]):
                    self.predicted[i, j] = np.mean(
                        (global_mean, user_means[i]))
                else:
                    self.predicted[i, j] = np.mean(
                        (global_mean, user_means[i], item_means[j]))


