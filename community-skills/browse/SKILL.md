---
name: browse
version: 1.0.0
description: |
  创建和部署浏览器自动化函数。
  自动填表、抓取数据、批量操作网页。
  浏览器自动化是 AI 助手的超能力。

author: Assistant
category: automation
dependencies:
  - playwright
  - selenium (optional)
  - puppeteer (optional)
---

# Browse 浏览器自动化

## 概述

强大的浏览器自动化工具，支持：
- 🤖 自动填表、点击、滚动
- 📊 网页数据抓取
- 🔄 批量操作网页
- 📸 网页截图和 PDF 生成
- 🔐 自动化登录流程

## 安装

```bash
# 安装 Playwright (推荐)
pip install playwright
playwright install

# 或安装 Selenium
pip install selenium webdriver-manager

# 或安装 Puppeteer (Node.js)
npm install puppeteer
```

## 快速开始

### Playwright 示例

```python
from playwright.sync_api import sync_playwright

def automate_browser():
    """基础浏览器自动化"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 访问网页
        page.goto("https://example.com")
        
        # 填写表单
        page.fill("input[name='username']", "myuser")
        page.fill("input[name='password']", "mypass")
        
        # 点击按钮
        page.click("button[type='submit']")
        
        # 等待加载
        page.wait_for_selector(".dashboard")
        
        # 截图
        page.screenshot(path="result.png")
        
        browser.close()

automate_browser()
```

## 核心功能

### 1. 自动填表

```python
from playwright.async_api import async_playwright

async def auto_fill_form(url: str, form_data: dict):
    """自动填写表单"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(url)
        
        # 填写所有字段
        for field, value in form_data.items():
            selector = f"input[name='{field}'], textarea[name='{field}'], select[name='{field}']"
            await page.fill(selector, value)
        
        # 提交
        await page.click("button[type='submit']")
        
        # 等待结果
        await page.wait_for_load_state("networkidle")
        
        result = await page.content()
        await browser.close()
        
        return result

# 使用
form_data = {
    "name": "张三",
    "email": "zhangsan@example.com",
    "company": "ABC公司"
}
result = await auto_fill_form("https://example.com/form", form_data)
```

### 2. 数据抓取

```python
async def scrape_data(url: str, selectors: dict) -> dict:
    """抓取网页数据"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        
        data = {}
        for key, selector in selectors.items():
            elements = await page.query_selector_all(selector)
            data[key] = [await el.text_content() for el in elements]
        
        await browser.close()
        return data

# 使用: 抓取文章列表
selectors = {
    "titles": "h2.article-title",
    "summaries": "p.article-summary",
    "dates": "span.publish-date"
}
articles = await scrape_data("https://news.example.com", selectors)
```

### 3. 批量操作

```python
async def batch_operations(urls: list[str], operation: callable):
    """批量操作多个网页"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        results = []
        for url in urls:
            try:
                page = await browser.new_page()
                await page.goto(url)
                
                # 执行自定义操作
                result = await operation(page)
                results.append({"url": url, "result": result, "status": "success"})
                
                await page.close()
            except Exception as e:
                results.append({"url": url, "error": str(e), "status": "failed"})
        
        await browser.close()
        return results

# 使用: 批量截图
async def screenshot_operation(page):
    filename = f"screenshot_{int(time.time())}.png"
    await page.screenshot(path=filename)
    return filename

results = await batch_operations(urls, screenshot_operation)
```

### 4. 自动化登录

```python
async def auto_login(url: str, username: str, password: str, 
                    username_selector: str = "input[name='username']",
                    password_selector: str = "input[name='password']",
                    submit_selector: str = "button[type='submit']") -> bool:
    """自动化登录流程"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # 加载已保存的登录状态
        if os.path.exists("auth.json"):
            context = await browser.new_context(storage_state="auth.json")
        
        page = await context.new_page()
        await page.goto(url)
        
        # 检查是否已登录
        if await page.query_selector(".user-profile"):
            print("已登录")
            await browser.close()
            return True
        
        # 填写登录信息
        await page.fill(username_selector, username)
        await page.fill(password_selector, password)
        await page.click(submit_selector)
        
        # 等待登录成功
        try:
            await page.wait_for_selector(".user-profile", timeout=10000)
            
            # 保存登录状态
            await context.storage_state(path="auth.json")
            
            await browser.close()
            return True
        except:
            await browser.close()
            return False
```

## 高级用法

### 拦截网络请求

```python
async def intercept_requests(url: str):
    """拦截和分析网络请求"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 拦截所有请求
        async def handle_route(route, request):
            print(f"Request: {request.url}")
            print(f"Method: {request.method}")
            print(f"Headers: {request.headers}")
            await route.continue_()
        
        await page.route("**/*", handle_route)
        await page.goto(url)
        
        await browser.close()
```

### 处理 JavaScript 渲染

```python
async def scrape_spa(url: str, wait_for_selector: str) -> str:
    """抓取单页应用 (SPA)"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(url)
        
        # 等待 JavaScript 渲染完成
        await page.wait_for_selector(wait_for_selector, timeout=30000)
        
        # 额外等待网络请求完成
        await page.wait_for_load_state("networkidle")
        
        content = await page.content()
        await browser.close()
        
        return content
```

### 生成 PDF

```python
async def generate_pdf(url: str, output_path: str):
    """将网页保存为 PDF"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(url, wait_until="networkidle")
        
        await page.pdf(
            path=output_path,
            format="A4",
            margin={"top": "20px", "bottom": "20px"}
        )
        
        await browser.close()

# 使用
await generate_pdf("https://example.com/article", "article.pdf")
```

## 与 OpenClaw 集成

```python
# 在 OpenClaw 中使用
async def scrape_with_openclaw(url: str, selectors: dict):
    """在 OpenClaw 环境中使用浏览器自动化"""
    
    # 使用 exec 运行 playwright 脚本
    script = f"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("{url}")
        
        data = {{}}
        for key, selector in {selectors}.items():
            el = await page.query_selector(selector)
            data[key] = await el.text_content() if el else None
        
        await browser.close()
        return data

result = asyncio.run(main())
print(result)
"""
    
    result = exec(command=f"python3 -c '{script}'")
    return result
```

## 常见场景

### 场景 1: 自动下载文件

```python
async def auto_download(url: str, download_dir: str = "./downloads"):
    """自动下载网页中的文件"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 设置下载路径
        context = await browser.new_context(
            accept_downloads=True
        )
        page = await context.new_page()
        
        await page.goto(url)
        
        # 等待并点击下载链接
        async with page.expect_download() as download_info:
            await page.click("a.download-link")
        
        download = await download_info.value
        await download.save_as(f"{download_dir}/{download.suggested_filename}")
        
        await browser.close()
```

### 场景 2: 表单自动化测试

```python
async def test_form_validation(url: str, test_cases: list[dict]):
    """自动化表单测试"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        results = []
        for case in test_cases:
            await page.goto(url)
            
            # 填写表单
            for field, value in case['input'].items():
                await page.fill(f"input[name='{field}']", value)
            
            await page.click("button[type='submit']")
            
            # 检查结果
            error = await page.query_selector(".error-message")
            success = await page.query_selector(".success-message")
            
            results.append({
                "case": case['name'],
                "expected": case['expected'],
                "actual": "error" if error else "success" if success else "unknown"
            })
        
        await browser.close()
        return results
```

## 最佳实践

### 1. 错误处理

```python
async def robust_automation(url: str, max_retries: int = 3):
    """健壮的错误处理"""
    for attempt in range(max_retries):
        try:
            return await perform_action(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed, retrying...")
            await asyncio.sleep(2 ** attempt)  # 指数退避
```

### 2. 资源管理

```python
# 使用上下文管理器确保资源释放
async with async_playwright() as p:
    browser = await p.chromium.launch()
    try:
        page = await browser.new_page()
        # ... 操作 ...
    finally:
        await browser.close()
```

### 3. 反检测

```python
# 设置 User-Agent 和其他参数避免被检测
browser = await p.chromium.launch(
    headless=False,
    args=[
        "--disable-blink-features=AutomationControlled",
        "--window-size=1920,1080"
    ]
)

context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)
```

## 相关技能

- [playwright-mcp](../playwright-mcp/SKILL.md) - Playwright MCP 服务器
- [webapp-testing](../webapp-testing/SKILL.md) - Web 应用测试
- [computer-use](../computer-use/SKILL.md) - 桌面自动化
- [get-tldr](../get-tldr/SKILL.md) - 文章总结

---

*"Automation is not just about saving time, it's about enabling possibilities."*
