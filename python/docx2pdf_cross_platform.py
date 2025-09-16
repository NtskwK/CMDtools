import subprocess
from pathlib import Path
from tkinter.filedialog import askopenfilename


def convert_docx_to_pdf(docx_path: Path, outdir: Path):
    """
    使用LibreOffice将DOCX文件转换为PDF文件。

    Args:
      docx_path: DOCX文件的路径。
      pdf_path: PDF文件的路径。
    """
    try:
        res = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                docx_path,
                "--outdir",
                outdir,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print(res.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise RuntimeError(
            f"转换失败！请检查LibreOffice是否安装并配置到环境变量中。\n{e}"
        ) from e
    if not outdir.joinpath(docx_path.stem + ".pdf").exists():
        raise RuntimeError("转换失败！未知错误！")


docx_path = Path(
    askopenfilename(
        title="请选择word文件",
        filetypes=[("Word文件", "*.docx;*.doc")],
    )
)

# pdf_path = Path("./page.pdf").resolve().__str__()
target_dir = Path("./").resolve()

convert_docx_to_pdf(docx_path, target_dir)
