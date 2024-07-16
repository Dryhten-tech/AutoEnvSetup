import os
import subprocess
from packaging import version


def create_venv(env_name, python_version):
    """使用conda创建一个新的虚拟环境，并指定Python版本"""
    try:
        subprocess.run(["conda", "create", "-n", env_name, f"python={python_version}", "-y"], check=True)
        print(f"虚拟环境 {env_name} 创建成功。")
    except subprocess.CalledProcessError as e:
        print(f"创建虚拟环境时出错：{e}")


def check_environment_exists(env_name, use_conda=False):
    """检查虚拟环境是否存在"""
    if use_conda:
        try:
            envs = subprocess.check_output(["conda", "info", "--envs"], text=True)
            if env_name not in envs and env_name != 'base':
                return False
        except subprocess.CalledProcessError:
            return False
    else:
        venv_dir = os.path.join(env_name, 'Scripts') if os.name == 'nt' else os.path.join(env_name, 'bin')
        if not os.path.exists(venv_dir):
            return False
    return True


def activate_environment(env_name, use_conda=False):
    """激活虚拟环境"""
    if use_conda:
        if env_name == 'base':
            return
        subprocess.run(f"conda activate {env_name}", shell=True, check=True)
    else:
        activate_script = os.path.join(env_name, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(env_name,
                                                                                                             'bin',
                                                                                                             'activate')
        subprocess.run(['cmd.exe', '/c', f'{activate_script}'], check=True) if os.name == 'nt' else subprocess.run(
            ['source', activate_script], shell=True, check=True)


def deactivate_environment(use_conda=False):
    """退出当前激活的虚拟环境"""
    if use_conda:
        subprocess.run("conda deactivate", shell=True, check=True)
    else:
        subprocess.run("deactivate", shell=True, check=True)


def install_packages(requirements_path):
    """安装或升级包，同时处理各种问题，并按速度顺序尝试不同的镜像源"""
    mirrors = [
        ("https://pypi.tuna.tsinghua.edu.cn/simple", "清华大学"),
        ("https://mirrors.aliyun.com/pypi/simple/", "阿里云"),
        ("https://pypi.douban.com/simple", "豆瓣"),
        ("https://pypi.org/simple/", "官方PyPI"),
        ("https://pypi.mirrors.ustc.edu.cn/simple/", "中国科学技术大学"),
        ("https://mirrors.tongji.edu.cn/pypi/web/simple/", "同济大学"),
        ("https://mirrors.nju.edu.cn/pypi/web/simple/", "南京大学"),
        ("https://pypi.hustunique.com/simple/", "华中科技大学"),
        ("https://mirrors.cloud.tencent.com/pypi/simple/", "腾讯云"),
        ("https://mirrors.huaweicloud.com/repository/pypi/simple/", "华为云")
    ]

    for mirror_url, mirror_name in mirrors:
        try:
            subprocess.run(["pip", "install", "-r", requirements_path, "--upgrade", "--index-url=" + mirror_url],
                           check=True)
            print(f"所有包已通过 {mirror_name} 镜像源安装完成。")
            return  # 成功后退出循环
        except subprocess.CalledProcessError as e:
            error_message = str(e)
            if any(keyword in error_message for keyword in ["ConnectionError", "timeout", "NetworkError"]):
                print(f"使用 {mirror_name} 镜像源安装包时遇到网络问题：{error_message}")
                print(f"正在尝试下一个镜像源。")
            elif "PermissionError" in error_message:
                print("权限错误：请以管理员权限运行此脚本或检查您的文件权限设置。")
                break  # 不再尝试其他镜像源
            elif "FileNotFoundError" in error_message:
                print("找不到pip或Python解释器：请确保它们已正确安装并添加到系统路径中。")
                break  # 不再尝试其他镜像源
            elif "KeyboardInterrupt" in error_message:
                print("操作被用户中断。")
                break  # 不再尝试其他镜像源
            else:
                print(f"安装包时遇到未知错误：{error_message}")
                print("这可能是由于多种原因导致的，包括但不限于软件冲突、系统资源不足或Python环境配置问题。")
                break  # 不再尝试其他镜像源
    print("所有镜像源都无法使用或遇到其他问题，程序无法自动解决。请根据上述提示进行手动排查。")


def is_valid_python_version(python_version):
    """判断给定的python_version是否是一个有效的Python版本号字符串"""
    try:
        version.parse(python_version)
        return True
    except version.InvalidVersion:
        return False


def main():
    print("本程序将会检测环境并自动安装未安装的包或更新不匹配的版本,有自动检查镜像源速度的功能\n")

    use_conda = input("您是否使用Conda激活环境？(y/n): ").lower() == 'y'
    env_name = input("请输入虚拟环境的名称(留空则使用base环境): ")

    if env_name and not check_environment_exists(env_name, use_conda):
        if input(f"虚拟环境 {env_name} 不存在，是否创建(使用conda)？(y/n): ").lower() == 'y':
            while True:  # 内部循环用于获取有效的Python版本
                python_version = input("请输入要用于虚拟环境的Python版本(留空则默认3.10): ")
                if not python_version:
                    python_version = "3.10"
                    break
                elif is_valid_python_version(python_version):
                    break
                else:
                    print("无效的Python版本号，请重新输入。")
            create_venv(env_name, python_version)
        else:
            print("不创建新的虚拟环境，程序已退出。")
            return

    requirements_path = input("请输入requirements文件的路径(留空则使用当前目录下的默认文件): ")
    requirements_path = os.path.join(os.getcwd(), requirements_path) if not os.path.isabs(
        requirements_path) else requirements_path

    if not os.path.exists(requirements_path):
        print(f"文件 {requirements_path} 不存在。")
        return

    try:
        print("开始自动安装环境依赖")
        install_packages(requirements_path)
    except Exception as e:
        print(f"在处理环境或包安装时发生错误：{e}")
    finally:
        deactivate_environment(use_conda)


if __name__ == "__main__":
    main()
