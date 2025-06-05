import scanpy as sc
import pandas as pd
import numpy as np


def mclust_R(adata, n_clusters, use_rep='HDVAE', key_added='HDVAE', random_seed=2023):
    """
    使用 R 的 mclust 算法进行聚类分析。
    参数：
    - adata: AnnData 对象，包含了嵌入表示和相关数据。
    - n_clusters: 聚类的类别数。
    - use_rep: 用于聚类的嵌入表示 (默认为 'HDVAE')，即 adata.obsm 中的一个键。
    - key_added: 聚类结果存储在 adata.obs 中的键名称 (默认为 'HDVAE')。
    - random_seed: 随机种子，确保结果的可重复性 (默认为 2023)。
    """
    import os  # 导入 os 模块，用于环境变量的设置
    os.environ['R_HOME'] = '/scbio4/tools/R/R-4.0.3_openblas/R-4.0.3'
    # 设置 R 的环境变量，确保 Python 能正确调用 R 环境。

    modelNames = 'EEE'
    # 定义 mclust 中的模型名称，'EEE' 表示协方差矩阵是等方差且同向的高斯模型。

    np.random.seed(random_seed)
    # 设置 numpy 的随机种子，确保随机数生成的结果可重复。

    import rpy2.robjects as robjects
    # 导入 rpy2.robjects 模块，用于在 Python 中调用 R 函数。

    robjects.r.library("mclust")
    # 加载 R 中的 mclust 库，这是一个用于聚类的包。

    import rpy2.robjects.numpy2ri
    # 导入 numpy2ri 模块，用于在 numpy 和 R 数据对象之间进行转换。

    rpy2.robjects.numpy2ri.activate()
    # 激活 numpy 和 R 数据之间的自动转换功能，使 numpy 数据可以直接传递给 R。

    r_random_seed = robjects.r['set.seed']
    # 获取 R 中的 `set.seed` 函数，用于设置 R 的随机种子。

    r_random_seed(random_seed)
    # 设置 R 的随机种子，确保 R 中的结果也可重复。

    rmclust = robjects.r['Mclust']
    # 获取 R 中的 `Mclust` 函数，这是 mclust 包中的核心聚类函数。

    res = rmclust(rpy2.robjects.numpy2ri.numpy2rpy(adata.obsm[use_rep]), n_clusters, modelNames)
    # 调用 R 的 `Mclust` 函数对数据进行聚类：
    # - 将 adata.obsm[use_rep]（即嵌入表示）从 numpy 转换为 R 的数据格式。
    # - n_clusters 表示聚类类别数。
    # - modelNames 指定使用的协方差矩阵模型。
    # 返回的结果是 R 对象，包含聚类的详细信息。

    mclust_res = np.array(res[-2])
    # 从 R 的返回结果中提取聚类标签。
    # `res[-2]` 通常是 mclust 返回对象中的类别标签，将其转换为 numpy 数组。

    adata.obs[key_added] = mclust_res
    # 将聚类结果存储到 AnnData 对象的 obs 属性中，键名为 key_added。

    adata.obs[key_added] = adata.obs[key_added].astype('int')
    # 将聚类结果的类型转换为整数类型。

    adata.obs[key_added] = adata.obs[key_added].astype('category')
    # 将聚类结果进一步转换为类别类型（category），节省内存并便于后续分析。

    return adata
    # 返回更新后的 AnnData 对象，其中包含聚类结果。


def configure_r_environment():
    import ctypes

    # 显式加载 R 的 LAPACK/BLAS 库
    try:
        ctypes.CDLL(r"D:\R-4.4.2\bin\x64\Rblas.dll")
        ctypes.CDLL(r"D:\R-4.4.2\bin\x64\Rlapack.dll")
        # print("Rblas.dll 和 Rlapack.dll 加载成功！")
    except Exception as e:
        print(f"加载失败：{e}")

    import os
    import sys
    from pathlib import Path
    import ctypes

    # 强制加载 R 的 DLL
    r_bin = Path("D:/R-4.4.2/bin/x64")
    ctypes.CDLL(str(r_bin / "Rblas.dll"))  # 先加载 BLAS
    ctypes.CDLL(str(r_bin / "Rlapack.dll"))  # 再加载 LAPACK

    # 设置环境变量
    os.environ['R_HOME'] = str(r_bin.parent.parent)  # 指向 D:\R-4.4.2
    os.environ['PATH'] = f"{r_bin};{os.environ.get('PATH', '')}"

    # 初始化 rpy2
    import rpy2.robjects as robjects
    from rpy2.rinterface_lib import openrlib
    openrlib.rlib.R_set_command_line_arguments(0, [])

    # 运行测试代码
    test_code = '''
        x <- matrix(c(1,2,3,4), 2, 2)
        # print("Testing simple SVD:")
        try({
            result <- La.svd(x)
            # print(result)
        }, silent=FALSE)
    '''
    result = robjects.r(test_code)
    # print(result)

    # 首先设置所有必要的环境变量
    os.environ['R_HOME'] = 'D:/R-4.4.2'
    os.environ['R_USER'] = os.path.expanduser('~')
    os.environ['PATH'] = 'D:/R-4.4.2/bin/x64;' + os.environ['PATH']
    # 明确设置LAPACK库的路径
    os.environ['R_LIBS'] = 'D:/R-4.4.2/library'