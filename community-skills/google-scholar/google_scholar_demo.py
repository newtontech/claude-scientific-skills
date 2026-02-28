#!/usr/bin/env python3
"""
Google Scholar Skill - Quick Test & Demo
使用 scholarly 库搜索 Google Scholar
"""

import sys
import json
from scholarly import scholarly

def search_papers(query, num_results=10):
    """搜索论文"""
    print(f"🔍 搜索: {query}")
    print("-" * 60)
    
    search_query = scholarly.search_pubs(query)
    papers = []
    
    for i in range(num_results):
        try:
            paper = next(search_query)
            papers.append(paper)
            
            title = paper['bib'].get('title', 'N/A')
            year = paper['bib'].get('pub_year', 'N/A')
            citations = paper.get('num_citations', 0)
            authors = paper['bib'].get('author', ['Unknown'])
            
            print(f"{i+1}. {title}")
            print(f"   作者: {', '.join(authors[:3])}")
            print(f"   年份: {year} | 引用: {citations}")
            print()
            
        except StopIteration:
            break
        except Exception as e:
            print(f"错误: {e}")
            continue
    
    return papers

def search_author(name):
    """搜索作者"""
    print(f"👤 搜索作者: {name}")
    print("-" * 60)
    
    try:
        search_query = scholarly.search_author(name)
        author = next(search_query)
        author = scholarly.fill(author)
        
        print(f"姓名: {author.get('name', 'N/A')}")
        print(f"机构: {author.get('affiliation', 'N/A')}")
        print(f"引用数: {author.get('citedby', 0)}")
        print(f"h-index: {author.get('hindex', 0)}")
        print(f"i10-index: {author.get('i10index', 0)}")
        print(f"研究领域: {', '.join(author.get('interests', [])[:5])}")
        print()
        
        # 显示最新5篇论文
        print("最新论文:")
        publications = author.get('publications', [])
        for pub in publications[:5]:
            title = pub['bib'].get('title', 'N/A')
            year = pub['bib'].get('pub_year', 'N/A')
            print(f"  - {title} ({year})")
        
        return author
        
    except StopIteration:
        print("未找到该作者")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  python {sys.argv[0]} search \"machine learning\" [数量]")
        print(f"  python {sys.argv[0]} author \"Geoffrey Hinton\"")
        print()
        print("示例:")
        print(f"  python {sys.argv[0]} search \"deep learning\" 5")
        print(f"  python {sys.argv[0]} author \"Yann LeCun\"")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        
        query = sys.argv[2]
        num = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        papers = search_papers(query, num)
        
        # 保存结果
        output_file = f"scholar_search_{query.replace(' ', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {output_file}")
        
    elif command == "author":
        if len(sys.argv) < 3:
            print("请提供作者姓名")
            sys.exit(1)
        
        name = sys.argv[2]
        author = search_author(name)
        
        if author:
            # 保存结果
            output_file = f"scholar_author_{name.replace(' ', '_')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(author, f, ensure_ascii=False, indent=2)
            print(f"\n💾 结果已保存到: {output_file}")
    
    else:
        print(f"未知命令: {command}")
        print("可用命令: search, author")
        sys.exit(1)

if __name__ == "__main__":
    main()
