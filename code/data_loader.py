import numpy as np
import pandas as pd
import os

def load_car_data(file_path='../data/car_data.csv'):
    """
    加载汽车数据
    
    Args:
        file_path (str): 数据文件路径
        
    Returns:
        pd.DataFrame: 加载的汽车数据
    """
    print("="*60)
    print("数据加载")
    print("="*60)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        
        # 使用pandas加载CSV数据
        df = pd.read_csv(file_path, encoding='utf-8')
        
        print(f"数据加载成功！")
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        return df
    
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None

def data_overview(df):
    """
    数据概览
    Args:
        df(pd.DataFrame):汽车数据
    Returns:
        dict:数据概览信息
    """
    print("\n"+"="*60)
    print("数据概览")
    print("="*60)
    if df is None:
        return None
    # 基本数据
    print(f"数据形状：{df.shape[0]}行 x {df.shape[1]}列")
    print(f"数据类型：\n{df.dtypes}")
    
    # 缺失值统计
    print("=== 缺失值统计 ===")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df))*100
    missing_info = pd.DataFrame({
        "缺失数量":missing_data,
        "缺失比例(%)":missing_percent
    })
    print(missing_info[missing_info['缺失数量'] > 0])

    # 数值型变量统计
    print("=== 数值型变量统计 ===")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols)>0:
        print(df[numeric_cols].describe())
    
    # 类别型变量统计
    print("=== 类别型变量统计 ===")
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        print(df[col].value_counts().head())
        print("\n")
    
    # 返回概览信息
    overview={
        'shape':df.shape,
        'columns':list(df.columns),
        'dtypes':df.dtypes.to_dict(),
        'missing_values':missing_data.to_dict(),
        'numeric_columns':list(numeric_cols),
        'categorical_columns':list(categorical_cols)
    }

    return overview
def validate_data(df):
    """
    数据验证
    Args:
        df(pd.DataFrame):汽车数据

    Returns:
        dict:验证结果
    """

    if df is None:
        return None
    print("\n"+"="*60)
    print("数据验证")
    print("="*60)

    validation_results = {}

    # 检查重复行
    duplicates = df.duplicated().sum()
    validation_results['duplicates']=duplicates
    print(f"重复行数量：{duplicates}")

    # 检查数值型变量的异常值 - IQR方法
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}

    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            col_outliers = df[(df[col]<lower_bound)|(df[col]>upper_bound)]
            outliers[col]={
                'count':len(col_outliers),
                'percentage':(len(col_outliers)/len(df))*100,
                'bounds':(lower_bound,upper_bound)
            }
            print(f"{col}: {len(col_outliers)} 个异常值 ({(len(col_outliers) / len(df)) * 100:.1f}%)")
    
    validation_results['outliers'] = outliers

    # === 检查数据一致性 ===
    # 检查价格是否合理
    if '价格(万元)' in df.columns:
        price_issues = df[(df['价格(万元)']<=0)|df['价格(万元)']>200]
        print(f"价格异常：{len(price_issues)} 辆")
        validation_results['price_issues'] = len(price_issues)
    
    # 检查功率是否合理
    if '发动机功率(马力)' in df.columns:
        power_issues = df[(df['发动机功率(马力)']<=0)|df['发动机功率(马力)']>500]
        print(f"功率异常：{len(power_issues)} 辆")
        validation_results['power_issues'] = len(power_issues)
    
    return validation_results

def main():
    # 加载数据
    df = load_car_data()
    if df is not None:
        # 数据概览
        overview = data_overview(df)
        # 数据验证
        validation = validate_data(df)
        print("数据加载与初步分析成功！")
        return df, overview, validation
    else:
        print(f"数据加载失败！")
        return None, None, None


if __name__ == "__main__":
    df, overview, validation = main()
