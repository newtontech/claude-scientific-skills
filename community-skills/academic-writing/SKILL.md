---
name: academic-writing
version: 1.0.0
description: |
  辅助学术论文写作，包括文献管理、引用格式化、论文润色等。
  支持 LaTeX 辅助、翻译、语法检查等功能。

author: Assistant
category: academic
dependencies:
  - python3
---

# 学术写作技能

## 功能描述
辅助学术论文写作，包括文献管理、引用格式化、论文润色等。

## 主要功能

### 1. 文献管理
- 搜索论文（使用 litpapermeta MCP）
- 获取 BibTeX 条目
- 管理引用库
- 检查引用完整性

### 2. 引用格式化
- 自动生成 BibTeX
- 检查引用格式
- 修复不完整的引用
- 去重引用

### 3. 论文润色
- 语法检查
- 表达优化
- 学术用语建议
- 翻译辅助

### 4. LaTeX 辅助
- 语法检查
- 编译辅助
- 模板生成
- 格式规范

## 使用方法

### 搜索论文
```bash
# 使用 litpapermeta MCP
mcporter call litpapermeta.search_paper_with_openalex query="关键词" limit:10
```

### 获取 BibTeX
```bash
# 通过 DOI
mcporter call litpapermeta.get_bibtex_from_doi doi="10.xxxx/xxxxx"

# 或使用脚本
python ~/.openclaw/workspace/scripts/bibtex_complete.py "论文标题"
```

### 管理引用
```bash
# 添加到项目
echo "BibTeX 条目" >> body/COEreference.bib

# 检查引用
python ~/.openclaw/workspace/scripts/check_citations.py
```

### LaTeX 编译
```bash
# 单次编译
xelatex -synctex=1 COEmain.tex

# 自动监控
~/.openclaw/workspace/scripts/latex_watch.sh COEmain.tex
```

## 配置

### MCP 服务器
确保 `mcporter.json` 包含：
- litpapermeta（已安装）
- scholar-gateway（需要授权）
- arxiv（可选）
- semantic-scholar（可选）

### 工作流程
1. 搜索文献 → 获取 BibTeX
2. 添加到 .bib 文件
3. 在 LaTeX 中引用
4. 编译检查

## 工具脚本

### bibtex_complete.py
自动补全 BibTeX 条目

### latex_watch.sh
LaTeX 自动编译监控

### check_citations.py
检查引用完整性

## 示例

### 示例 1：搜索并添加文献
```bash
# 1. 搜索
python bibtex_complete.py "perovskite solar cell efficiency"

# 2. 选择文献

# 3. 保存到 bib 文件
```

### 示例 2：修复不完整的引用
```bash
# 1. 识别不完整的引用
python check_citations.py

# 2. 使用 litpapermeta 补全
mcporter call litpapermeta.get_paper_details_with_crossref doi="..."

# 3. 更新 bib 文件
```

## 注意事项

1. **引用完整性**
   - 确保所有作者都列出
   - 检查 DOI 是否有效
   - 验证年份和期刊

2. **LaTeX 编译**
   - 使用 XeLaTeX 编译中文
   - 保持 synctex 文件
   - 定期清理缓存

3. **版本控制**
   - 定期提交到 Git
   - 保留编译日志
   - 备份重要文件

## 相关技能

- mcporter: MCP 服务器管理
- github: 版本控制
- tavily-search: 网络搜索

## 更新日志

- 2026-02-24: 初始版本
