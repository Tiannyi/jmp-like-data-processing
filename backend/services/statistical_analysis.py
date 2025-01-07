import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any
from sklearn.linear_model import LinearRegression

class StatisticalAnalysis:
    @staticmethod
    def calculate_basic_stats(data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic statistical measures for numerical columns"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        stats_dict = {}
        
        for col in numeric_cols:
            stats_dict[col] = {
                "mean": data[col].mean(),
                "std": data[col].std(),
                "variance": data[col].var(),
                "min": data[col].min(),
                "max": data[col].max(),
                "median": data[col].median(),
                "q1": data[col].quantile(0.25),
                "q3": data[col].quantile(0.75)
            }
        
        return stats_dict

    @staticmethod
    def perform_anova(data: pd.DataFrame, factors: List[str], response: str) -> Dict[str, Any]:
        """Perform one-way ANOVA"""
        groups = [group[response].values for name, group in data.groupby(factors[0])]
        f_stat, p_value = stats.f_oneway(*groups)
        
        return {
            "f_statistic": f_stat,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

    @staticmethod
    def regression_analysis(
        data: pd.DataFrame,
        dependent: str,
        independent: List[str]
    ) -> Dict[str, Any]:
        """Perform multiple linear regression"""
        X = data[independent]
        y = data[dependent]
        
        model = LinearRegression()
        model.fit(X, y)
        
        return {
            "r_squared": model.score(X, y),
            "coefficients": dict(zip(independent, model.coef_)),
            "intercept": model.intercept_,
            "predictions": model.predict(X).tolist()
        }
