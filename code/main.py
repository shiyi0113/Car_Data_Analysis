import os
from data_loader import data_load
from data_cleaner import data_clean

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(BASE_DIR, '..', 'data', 'Car_Sales_data.csv')

def run_project():
    """
    项目主流程执行函数
    """
    print("\n*** 开始汽车销售数据分析项目 ***\n")
    
    # 1. 数据加载
    df = data_load(data_file)
    if df is None:
        print(f"数据加载失败！")
        return    
    
    # 2. 数据清洗
    df_clean = data_clean(df)
    
    # 3. 后续操作
    
    print("\n*** 项目流程结束 ***")

if __name__ == "__main__":
    run_project()