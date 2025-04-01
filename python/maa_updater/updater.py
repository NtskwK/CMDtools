from os import path
import re
from urllib3 import PoolManager, ProxyManager, exceptions
from zipfile import ZipFile
from argparse import ArgumentParser
from json import loads
from psutil import process_iter
import sys
from loguru import logger

class config:
    work_dir = path.dirname(path.abspath(__file__))
    github_api_url = "http://api.github.com/repos/MaaAssistantArknights/MaaAssistantArknights/releases/latest"
    github_proxy = "http://gh-proxy.natsuu.top/"
    default_proxy = "http://127.0.0.1:7890"
    default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"


config = config()


def get_http_manager(proxies=None):
    """
    获取 HTTP 管理器实例，支持代理和自定义请求头。

    :param proxies: 代理配置
    :return: urllib3.PoolManager 或 urllib3.ProxyManager 实例
    """
    headers = {"User-Agent": config.default_user_agent}
    if proxies:
        return ProxyManager(proxies["http"], headers=headers)
    return PoolManager(headers=headers)


def download_file(url, dest_path, overwrite=False, proxies=None):
    """
    下载文件到指定路径，支持覆盖已存在的文件。

    :param url: 文件的下载链接
    :param dest_path: 保存文件的路径
    :param overwrite: 是否覆盖已存在的文件
    :param proxies: 代理配置
    """
    if path.exists(dest_path) and not overwrite:
        logger.info(f"文件已存在: {dest_path}")
        return

    http = get_http_manager(proxies)

    try:
        logger.info(f"开始下载: {url}")
        with http.request("GET", url, preload_content=False) as response:
            if response.status == 200:
                with open(dest_path, "wb") as file:
                    for chunk in response.stream(8192):
                        file.write(chunk)
                logger.info(f"文件已下载: {dest_path}")
            else:
                logger.error(f"下载失败，状态码: {response.status}")
    except exceptions.HTTPError as e:
        logger.error(f"下载失败: {e}")


def extract_zip(zip_path, extract_to, overwrite=False):
    """
    解压 ZIP 文件到指定目录，支持覆盖已存在的文件。

    :param zip_path: ZIP 文件路径
    :param extract_to: 解压目标目录
    :param overwrite: 是否覆盖已存在的文件
    """
    if not path.exists(zip_path):
        logger.error(f"ZIP 文件不存在: {zip_path}")
        return

    with ZipFile(zip_path, "r") as zip_ref:
        for file in zip_ref.namelist():
            file_path = path.join(extract_to, file)
            if path.exists(file_path) and not overwrite:
                logger.info(f"文件已存在，跳过: {file_path}")
                break
            zip_ref.extract(file, extract_to)

    logger.info(f"文件已解压！")


def get_latest_release_download_url(use_gitproxy=True, proxies=None):
    """
    获取最新的 release 下载链接。

    :param use_gitproxy: 是否使用代理 URL
    :param proxies: 代理配置
    :return: 下载链接或 None
    """
    pattern = re.compile(r"MAA-v(\d+\.\d+\.\d+)-win-x64\.zip")
    http = get_http_manager(proxies)

    try:
        response = http.request("GET", config.github_api_url, timeout=10.0)
        if response.status == 200:
            release_data = loads(response.data.decode("utf-8"))
            for asset in release_data.get("assets", []):
                if pattern.match(asset["name"]):
                    download_url = asset["browser_download_url"]
                    if use_gitproxy:
                        download_url = config.github_proxy + download_url
                    logger.info(f"找到下载链接: {download_url}")
                    return download_url

            logger.warning("未找到 ZIP 文件的下载链接。")
        else:
            logger.error(f"获取 release 信息失败，状态码: {response.status}")
    except exceptions.HTTPError as e:
        logger.exception(f"获取 release 信息时发生网络错误: {e}")
    except ValueError as e:
        logger.exception(f"解析 release 信息时发生错误: {e}")
    return None


def check_maa_running():
    """
    检查是否有 MAA.exe 进程正在运行。
    如果检测到运行，则发出警告并退出程序。
    """
    for process in process_iter(attrs=["name"]):
        if process.info["name"] == "MAA.exe":
            logger.warning("检测到 MAA.exe 正在运行，请先关闭后再执行更新操作。")
            exit(1)


def configure_logging():
    """
    配置 loguru 日志记录器。
    如果发生错误，则将日志写入文件。
    """
    logger.remove()  # 移除默认的日志处理器
    logger.add(
        sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>"
    )
    logger.add(
        "error.log",
        level="ERROR",
        format="<red>{time:YYYY-MM-DD HH:mm:ss}</red> | <level>{message}</level>",
        rotation="1 MB",  # 日志文件大小超过 1 MB 时自动切分
        retention="1 days",  # 保留 7 天的日志文件
        backtrace=True,  # 捕获完整的回溯信息
        diagnose=True,  # 提供详细的错误诊断信息
        enqueue=True,  # 异步写入日志文件
    )


def main():
    # 配置日志
    configure_logging()

    # 启动前检查
    check_maa_running()

    parser = ArgumentParser(description="MAA 更新工具")
    parser.add_argument("--no-overwrite", action="store_true", help="不覆盖已存在的文件")
    parser.add_argument(
        "--no-gitproxy", action="store_true", help="是否禁用 GitHub 代理"
    )
    parser.add_argument(
        "--proxy",
        nargs="?",
        const=config.default_proxy,
        help="启用代理（可选指定代理地址）",
    )
    args = parser.parse_args()

    overwrite = not args.no_overwrite
    use_proxy = not args.no_gitproxy
    proxy = args.proxy
    proxies = {"http": proxy, "https": proxy} if proxy else None

    logger.info(f"覆盖模式: {'启用' if overwrite else '禁用'}")
    logger.info(f"GitHub 代理: {'禁用' if not use_proxy else '启用'}")
    logger.info(f"代理设置: {'启用' if proxy else '禁用'}")
    if proxy:
        logger.info(f"代理地址: {proxy}")

    # 获取最新 release 的下载链接
    download_url = get_latest_release_download_url(
        use_gitproxy=use_proxy, proxies=proxies
    )
    if download_url:
        logger.info(f"最新的下载链接: {download_url}")
        filename = download_url.split("/")[-1]

        zip_path = path.join(config.work_dir, filename)
        download_file(download_url, zip_path, overwrite=overwrite, proxies=proxies)
        extract_zip(zip_path, config.work_dir, overwrite=overwrite)
    else:
        logger.error("未能获取到最新的下载链接。")


if __name__ == "__main__":
    main()
