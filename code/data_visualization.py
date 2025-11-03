import os
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from scipy import stats

def setup_matplotlib_for_plotting():
    # warnings.filterwarnings('default') 
    plt.switch_backend("Agg") # 绘图后端（backend）切换为 "Agg"

    plt.style.use("seaborn-v0_8") # 使用 Matplotlib 内置的 "seaborn-v0_8" 风格
    sns.set_palette("husl")       # 将调色板设置为 "husl"
    
    # 字体设置
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "方正黑体", "SimHei", "黑体", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False # 将负号的 Unicode 处理关闭

def create_distribution_plots(df, numeric_cols, output_dir):
    """
    创建数据分布图

    """
    print("="*60)
    print("数据分布可视化")
    print("="*60)
    setup_matplotlib_for_plotting()  # 基础绘图配置
    os.makedirs(output_dir, exist_ok=True)

    # 1. 价格分布图
    if 'price' in df.columns:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('汽车价格分析', fontsize=16, fontweight='bold')
        
        # 价格直方图
        axes[0, 0].hist(df['price'].dropna(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('汽车价格分布')
        axes[0, 0].set_xlabel('价格 ($)')
        axes[0, 0].set_ylabel('频数')
        
        # 价格箱线图
        axes[0, 1].boxplot(df['price'].dropna())
        axes[0, 1].set_title('汽车价格箱线图')
        axes[0, 1].set_ylabel('价格 ($)')
        
        # 价格Q-Q图
        stats.probplot(df['price'].dropna(), dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('价格正态性检验 (Q-Q图)')
        
        # 价格统计信息
        axes[1, 1].text(0.1, 0.8, f'平均价格: ${df["price"].mean():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.7, f'中位数价格: ${df["price"].median():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.6, f'标准差: ${df["price"].std():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.5, f'最小值: ${df["price"].min():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.4, f'最大值: ${df["price"].max():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].set_title('价格统计摘要')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/01_价格分布分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("价格分布图已保存")

    # 2. 收入分布图
    if 'annual_income' in df.columns:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('客户年收入分析', fontsize=16, fontweight='bold')
        
        # 收入直方图
        axes[0, 0].hist(df['annual_income'].dropna(), bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 0].set_title('客户年收入分布')
        axes[0, 0].set_xlabel('年收入 ($)')
        axes[0, 0].set_ylabel('频数')
        
        # 收入箱线图
        axes[0, 1].boxplot(df['annual_income'].dropna())
        axes[0, 1].set_title('客户年收入箱线图')
        axes[0, 1].set_ylabel('年收入 ($)')
        
        # 收入Q-Q图
        stats.probplot(df['annual_income'].dropna(), dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('收入正态性检验 (Q-Q图)')
        
        # 收入统计信息
        axes[1, 1].text(0.1, 0.8, f'平均收入: ${df["annual_income"].mean():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.7, f'中位数收入: ${df["annual_income"].median():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.6, f'标准差: ${df["annual_income"].std():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.5, f'最小值: ${df["annual_income"].min():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.4, f'最大值: ${df["annual_income"].max():.2f}', transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].set_title('收入统计摘要')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/02_收入分布分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("收入分布图已保存")
    
    # 3. 分类变量分布图
    categorical_cols_to_plot = ['company', 'model', 'body_style', 'transmission', 'color']
    
    for col in categorical_cols_to_plot:
        if col in df.columns:
            plt.figure(figsize=(12, 8))
            
            # 获取前10个最频繁的值
            top_values = df[col].value_counts().head(10)
            
            # 创建条形图
            plt.subplot(2, 1, 1)
            top_values.plot(kind='bar', color='coral')
            plt.title(f'{col} 分布 (前10名)')
            plt.xlabel(col)
            plt.ylabel('数量')
            plt.xticks(rotation=45)
            
            # 创建饼图
            plt.subplot(2, 1, 2)
            plt.pie(top_values.values, labels=top_values.index, autopct='%1.1f%%', startangle=90)
            plt.title(f'{col} 市场份额 (前10名)')
            
            plt.tight_layout()
            safe_col_name = col.replace(' ', '_').replace('/', '_')
            plt.savefig(f'{output_dir}/03_{safe_col_name}_分布分析.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"{col} 分布图已保存")
