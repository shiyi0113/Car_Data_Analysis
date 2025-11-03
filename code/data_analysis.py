import numpy as np
import pandas as pd

pd.set_option('display.float_format', lambda x: '%.2f' % x)

def basic_statistics(df):
    """
    基础统计分析

    Args:
        df (pd.DataFrame): 经过清洗后的数据集。

    Returns:
        tuple:  (numeric_cols, categorical_cols)
               分别是被识别的数值型列名和分类型列名。
    """

    print("="*60)
    print("数据基础统计分析")
    print("="*60)
    
    # 数值型变量的统计描述
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print("数值型变量统计描述:")
        print(df[numeric_cols].describe())
    
    # 分类变量的统计描述
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        print(f"\n 分类变量统计 (前5个最频繁的值):")
        for col in categorical_cols: 
            print(df[col].value_counts().head())
    
    return numeric_cols, categorical_cols