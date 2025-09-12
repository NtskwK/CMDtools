import urllib.request
import re
import time
import urllib.parse


TEST_PACKAGE = "tensorflow"
TEST_TAG = "2.0.0-cp37-cp37m-macosx_10_11_x86_64"  # 文件大小97.9MB
REPEAT_CNT = 1  # 重复次数
DOWNLOAD_TIMEOUT = 5  # 下载测试时长（秒），太短可能测不出准确速度，太长会增加测试耗时


def get_mirror_benchmark(simple_url, package_name, download_tag):
    pypi_url = f"{simple_url}/{package_name}/"
    # print(f'http get: {pypi_url}')

    t0 = time.perf_counter()
    resp = urllib.request.urlopen(pypi_url, timeout=2)
    assert resp.getcode() == 200
    response_html = resp.read().decode()
    t1 = time.perf_counter()
    resp.close()
    listing_speed = f"{1000*(t1-t0):.2f}ms"  # 计算列表响应时间

    file_link_re = re.compile(
        r'<a href="([^"]*?)".*?>{}\-(([0-9.]*?)\-.*?)\.whl</a>'.format(package_name)
    )

    n = file_link_re.findall(response_html)
    links = []

    download_link = ""
    for link, version_tag, version in n:
        links.append((tuple(map(int, version.split("."))), version_tag, link))
        if version_tag == download_tag:
            download_link = link

    links.sort(key=lambda x: x[0][2])
    links.sort(key=lambda x: x[0][1])
    links.sort(key=lambda x: x[0][0])
    lastest_version = links[-1][0]  # 得到最新版本号

    assert download_link

    package_url = urllib.parse.urljoin(pypi_url, download_link)
    # print(package_url)

    t0 = time.perf_counter()
    resp = urllib.request.urlopen(package_url, timeout=4)
    assert resp.getcode() == 200
    file_size = 0
    while 1:
        chunk = resp.read(128 * 1024)  # 每次读取128KB
        file_size += len(chunk)
        t1 = time.perf_counter()
        if t1 - t0 > DOWNLOAD_TIMEOUT:
            break
        if not chunk:
            break  # 下载完成
    resp.close()
    download_speed = f"{file_size/(t1-t0)/1024/1024:.2f}MB/s"  # 计算下载速度

    return (lastest_version, listing_speed, download_speed)


links = """
阿里云
http://mirrors.aliyun.com/pypi/simple
腾讯云
https://mirrors.cloud.tencent.com/pypi/simple
华为云
https://mirrors.huaweicloud.com/artifactory/pypi-public/simple
清华大学
https://pypi.tuna.tsinghua.edu.cn/simple
中国科学技术大学
https://mirrors.ustc.edu.cn/pypi/simple
北京外国语大学
https://mirrors.bfsu.edu.cn/pypi/web/simple
上海交通大学
https://mirror.sjtu.edu.cn/pypi/web/simple
南方科技大学
https://mirrors.sustech.edu.cn/pypi/web/simple
北京大学
https://mirrors.pku.edu.cn/pypi/web/simple
南阳理工学院
https://mirror.nyist.edu.cn/pypi/web/simple
南京工业大学
https://mirrors.njtech.edu.cn/pypi/web/simple

吉林大学
https://mirrors.jlu.edu.cn/pypi/simple
大连东软信息学院
https://mirrors.neusoft.edu.cn/pypi/web/simple
"""

link_iter = iter(links.strip().splitlines())


line_size = (10, 8, 10, 10)

print("正在测试镜像站点...")
print("\t".join(("镜像站名称", f"{TEST_PACKAGE}最新版本", "列表耗时", "下载速度")))
mirrors = []
for site_name, simple_url in zip(link_iter, link_iter):
    simple_url = simple_url.strip().rstrip("/")
    for _ in range(REPEAT_CNT):
        try:
            lastest_version, listing_speed, download_speed = get_mirror_benchmark(
                simple_url, TEST_PACKAGE, TEST_TAG
            )
            mirrors.append(
                {
                    "simple_url": simple_url,
                    "site_name": site_name,
                    "lastest_version": lastest_version,
                    "listing_speed": listing_speed,
                    "download_speed": download_speed,
                }
            )
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"{site_name} 测试失败, {e}")
            break  # 不重复测试失败项
        print(
            "\t".join(
                (
                    f"{site_name:^16}",
                    f'{".".join(map(str, lastest_version)):^10}',
                    f"{listing_speed:^10}",
                    f"{download_speed:^10}",
                )
            )
        )


fastest_mirror = max(mirrors, key=lambda x: x["download_speed"])
print(f"共测试 {len(mirrors)} 个镜像站点")
print(f"下载速度最快的镜像站点:{fastest_mirror['site_name']}")
switch = input("是否切换当前镜像？(y/n): ").lower().startswith("y")
if switch:
    import subprocess

    fast_url = fastest_mirror["simple_url"]

    result = subprocess.run(
        ["pip", "config", "set", "global.index-url", fast_url],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode == 0:
        print(f"已切换到镜像: {fast_url}")
    else:
        print(f"切换镜像失败: {result.stderr.strip()}")
