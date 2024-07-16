# AutoEnvSetup
AutoEnvSetup 是一款强大的 Python 脚本，旨在简化开发环境的搭建过程以及依赖管理。它通过自动化虚拟环境的创建、指定 Python 版本以及安装 `requirements.txt` 文件中的所有依赖包，极大地提升了开发者的效率。其主要特性包括：
# 环境检测与依赖安装脚本

## 环境
- Python 3.10 或更高版本

## 依赖
- `subprocess`
- `os`
- `packaging.version`

## 功能
- 检测和管理虚拟环境（支持 Conda 和标准虚拟环境）。
- 自动创建虚拟环境并指定 Python 版本。
- 安装或更新 `requirements.txt` 文件中列出的所有依赖包。
- 支持多个 PyPI 镜像源，以提高安装速度和成功率。
- 错误处理和用户反馈。

## 使用方法

### 运行脚本
- 确保 Python 和必要的依赖已安装。
- 运行脚本，脚本会引导你完成环境检测和依赖安装的流程。

### 交互式输入
- 选择是否使用 Conda 环境。
- 输入虚拟环境名称（留空使用 base 环境）。
- 如果虚拟环境不存在，询问是否创建。
- 输入 Python 版本（留空默认为 3.10）。
- 提供 `requirements.txt` 文件的路径（留空使用当前目录下默认文件）。

### 依赖安装
- 脚本将尝试从多个镜像源安装包，直至成功或所有源均失败。
- 在安装过程中处理各种常见错误，如网络问题、权限问题等。

## 注意事项
- 确保有适当的权限执行脚本和安装包。
- 脚本依赖于 `conda` 和 `pip` 的正确配置。
- 对于非标准的 Python 安装或复杂的环境配置，可能需要额外的手动干预。

## 技术细节

### 虚拟环境管理
- 使用 `conda` 或标准 Python `venv` 模块创建和激活环境。
- 检查环境存在性，避免重复创建。

### 包安装
- 尝试多个 PyPI 镜像源，优先使用国内镜像提高下载速度。
- 错误处理机制确保在遇到问题时给出明确的反馈。

## 贡献指南
- 如需改进或修复，请提交 Pull Request。
- 报告问题时，请附上详细的错误信息和步骤。

---

## 版权与许可
- 本脚本遵循 MIT 许可协议。
- 作者不承担因使用本脚本而导致的任何直接或间接损失。
- 欢迎社区成员贡献代码、文档和测试案例。

---

## 联系方式
- 如有任何疑问或建议，请通过以下方式联系：
  - 邮件: [你的邮箱]
  - GitHub: [你的GitHub用户名]

---

## 更新日志
- **2024-07-15**: 初始版本发布，包含基本功能和错误处理。
- **计划更新**:
  - 增加对更多镜像源的支持。
  - 提升错误处理的智能化和用户体验。
  - 优化性能和稳定性。
