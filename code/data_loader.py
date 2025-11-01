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

def main():
    print("="*60)
    print("数据加载模块")
    print("="*60)
    
    # 加载数据
    df = load_car_data()

if __name__ == "__main__":
    main()
