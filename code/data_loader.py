import pandas as pd
import os

def data_load(file_path = None):
    """
    数据加载
    
    Args:
        file_path (str): 数据文件路径
        
    Returns:
        pd.DataFrame: 加载的汽车数据
    """

    print("="*60)
    print("数据加载")
    print("="*60)
    
    try:
        if file_path is None:
            print("请传入文件路径。")
            return None 
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        
        df = pd.read_csv(file_path, encoding='utf-8')
        
        print(f"数据加载成功！")
        print(f"数据形状：{df.shape[0]}行 x {df.shape[1]}列")
        print(f"数据基本信息:")
        df.info()
        print(f"前5行数据:\n{df.head()}")
        return df
    
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None