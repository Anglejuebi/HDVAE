from setuptools import setup

def load_requirements():
    try:
        with open("requirements.txt", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("error! Cannot find requirements.txt file")
        return []

if __name__ == "__main__":
    setup(
        name="HDVAE",
        version="1.0.0",
        description="HDVAE: identifying spatial domains in spatial transcriptomics data with Hierarchical Decoupled Variational Autoencoder",
        url="https://github.com/Anglejuebi/HDVAE",
        author="JunHua Yu",
        author_email="Angle_Yu@e.gzhu.edu.cn",
        license="MIT",
        packages=["HDVAE"],
        install_requires=load_requirements(),
        zip_safe=False,
        include_package_data=True,
        long_description=""" In this study, we proposed HDVAE (Hierarchical Decoupled Variational Autoencoder) which significantly improved the identification ability of the spatial domain in ST data through multi-hop graph convolution and hierarchical decoupling structure. Its core innovation lies in using multi-hop graph convolution to expand the receptive field of spots and capture long-distance spatial dependencies, while achieving hierarchical decoupling of local and global features through a series of HDVAE Blocks, and ensuring semantic consistency between levels by combining cross-level similarity constraints. Compared to other advanced methods, HDVAE shows significant advantages in tests on multiple platforms. The ARI on the human DLPFC dataset is improved to 0.7182, and the iLISI score of the batch effect correction task reaches 1.97. Moreover, the model, through lightweight variational inference and implicit multi-hop computation, reduces the CUDA memory occupation (only 239MB) while being compatible with single-cell high-resolution data (such as Stereo-seq) and large-scale tissue sections, verifying its cross-platform robustness. These advantages make HDVAE an advanced tool in the current field of spatial omics that combines both accuracy and efficiency. """,
        long_description_content_type="text/markdown",
    )
