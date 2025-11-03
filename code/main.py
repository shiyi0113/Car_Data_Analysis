import os
from data_loader import data_load
from data_cleaner import data_clean,data_save
from data_analysis import basic_statistics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(BASE_DIR, '..', 'data', 'Car_Sales_data.csv')
clean_file = os.path.join(BASE_DIR, '..', 'data', 'Cleaned_Car_Sales_data.csv')

def run_project():
    """
    项目主流程执行函数
    """
    print("\n*** 开始汽车销售数据分析 ***\n")
    
    # 1. 数据加载
    df = data_load(data_file)
    if df is None:
        print(f"数据加载失败！")
        return    
    
    # 2. 数据清洗
    df_clean = data_clean(df)
    data_save(df_clean,clean_file)  # 保存

    # 3. 基础数据分析
    numeric_cols, categorical_cols = basic_statistics(df_clean)
    # 4. 后续操作
    print("\n*** 分析流程结束 ***")

if __name__ == "__main__":
    run_project()