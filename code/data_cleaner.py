import pandas as pd
import numpy as np
import os
import re 

def data_clean(df):
    """
    数据清洗
    
    Args:
        df(pd.DataFrame): 数据
        
    Returns:
        pd.DataFrame: 清洗后的数据
    """
    print("="*60)
    print("开始数据清洗")
    print("="*60)
    # 复制源数据
    df_cleaned = df.copy()

    # --- 1. 格式统一 ---
    print("--- 1. 格式统一 (列名规范化) ---")
    
    def clean_col_name(col):
        col = col.lower()  # 转换为小写
        col = re.sub(r'[\(\$\)]', '', col)  # 移除($)符号
        col = col.strip()  # 移除首尾的空格
        col = col.replace(' ', '_')         # 空格改成下划线
        col = re.sub(r'[^\w_]', '', col)    # 移除非字符、数字、下划线的字符
        return col
    # 列名规范化
    df_cleaned.columns = [clean_col_name(col) for col in df_cleaned.columns]
    
    # 将 Dealer_No 改为 Dealer_ID
    if 'dealer_no' in df_cleaned.columns:
         df_cleaned.rename(columns={'dealer_no':'dealer_id'}, inplace=True)
    
    print(f"当前规范化后的列名：{list(df_cleaned.columns)}") # 打印列名进行验证
    # 数值型数据：中位数填充 + 异常值计算
    NUMERICAL_COLS = ['price', 'annual_income']
    # 标识符数据：转换为string
    IDENTIFIER_COLS = ['car_id', 'dealer_id', 'phone']
    # 其他描述性数据
    OBJECT_COLS = ['customer_name', 'gender', 'dealer_name', 'company', 'model', 
                   'engine', 'transmission', 'color', 'body_style', 'dealer_region']

    # --- 2. 缺失数据处理 (标准流程) ---
    print("\n--- 2. 缺失数据处理 ---")
    
    missing_cols = df_cleaned.isnull().sum()
    missing_cols = missing_cols[missing_cols > 0]
    
    if missing_cols.empty:
        print("缺失数据检查: 数据集中当前无缺失值。")
    else:
        print(f"发现以下列存在缺失值:\n{missing_cols}")
        
        # 数值型数据使用中位数填充 
        for col in NUMERICAL_COLS:
            if col in missing_cols.index:
                median_val = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_val)
                print(f"   -> 数值列 '{col}' 已使用中位数 ({median_val}) 填充。")
                
        # 描述型数据使用unknow填充
        for col in OBJECT_COLS:
            if col in missing_cols.index:
                df_cleaned[col] = df_cleaned[col].fillna('unknow')
                print(f"   -> 分类列 '{col}' 已使用 unknow 填充。")
                
        print("缺失数据处理: 所有缺失值已按策略填充完成。")


    # --- 3. 重复数据处理 ---
    print("\n--- 3. 重复数据处理 ---")
    initial_rows = len(df_cleaned)
    df_cleaned.drop_duplicates(inplace=True)
    rows_dropped = initial_rows - len(df_cleaned)
    print(f"✅ 重复数据处理: 删除 {rows_dropped} 行重复数据。当前行数: {len(df_cleaned)}")

    # --- 4. 数据类型转换 ---
    print("\n--- 4. 数据类型转换 ---")
    
    # 4.1 'date' 列转换
    if 'date' in df_cleaned.columns:
        try:
            df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], format=None, errors='coerce')
            print("数据类型转换: 'date' 列已转为 datetime 类型 (使用自动推断格式)。")
        except Exception as e:
            print(f"'date' 列转换失败: {e}")
    # 4.2 标识符列转换    
    for col in IDENTIFIER_COLS:
        df_cleaned[col] = df_cleaned[col].astype(str)
        print(f"数据类型转换: {col} 列已转为 string 类型。")
    
    # --- 5. 异常值处理 ---
    print("\n--- 5. 异常值处理 ---")
    
    for col in NUMERICAL_COLS:
        if col in df_cleaned.columns and df_cleaned[col].dtype in ['int64', 'float64']:
            Q1 = df_cleaned[col].quantile(0.25)
            Q3 = df_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_mask = (df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)
            outliers_count = outliers_mask.sum()
            
            if outliers_count > 0:
                median_val = df_cleaned[col].median()
                df_cleaned.loc[outliers_mask, col] = median_val
                print(f"异常值处理: 列 '{col}' 发现并替换 {outliers_count} 个 IQR 异常值，使用中位数 {median_val} 填充。")
            else:
                print(f"异常值检查: 列 '{col}' 未发现 IQR 异常值。")
        elif col not in df_cleaned.columns:
             print(f"异常值处理跳过: 列 '{col}' 在 DataFrame 中不存在。")
        else:
             print(f"异常值处理跳过: 列 '{col}' 不是数值类型。")

    print("="*60)
    print("数据清洗完成！")
    print(f"清洗后数据形状: {df_cleaned.shape[0]}行 x {df_cleaned.shape[1]}列")
    print("="*60)
    
    return df_cleaned

def data_save(df, output_path):
    """
    保存DataFrame数据到 CSV 文件
    
    Args:
        df (pd.DataFrame): 数据
        output_path (str): 输出文件路径
        
    Returns:
        bool: 保存是否成功
    """
    print("="*60)
    print("开始保存数据")
    print("="*60)
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
        
    try:
        # 保存为新的 CSV 文件，不包含索引
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"数据保存成功！文件路径: {output_path}")
        return True
    except Exception as e:
        print(f"数据保存失败: {e}")
        return False