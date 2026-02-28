---
name: semanticscholar
version: 1.0.0
description: |
  Unofficial Python client for Semantic Scholar APIs. Search academic papers, 
  authors, citations, and recommendations. Perfect for literature reviews and 
  research discovery.
  
  Semantic Scholar provides free access to 200M+ academic papers across all 
  scientific domains with AI-powered paper discovery and citation analysis.

author: Assistant
category: literature
license: MIT
homepage: https://github.com/danielnsilva/semanticscholar
requirements:
  - semanticscholar>=0.8.0
  - pandas>=1.3.0
  - matplotlib>=3.4.0
  
examples:
  - name: Search papers by keyword
    description: Find papers on a specific topic
    prompt: |
      Search Semantic Scholar for papers about "deep learning for protein folding" 
      from 2020-2024. Return the top 10 results with title, authors, year, 
      citation count, and abstract.
      
  - name: Get paper details
    description: Retrieve detailed information about a specific paper
    prompt: |
      Get detailed information about the paper with Semantic Scholar ID 
      "649def34f8be52c8b66281af98ae884c09aef38b". Include abstract, authors, 
      citations, references, and related papers.
      
  - name: Find influential papers
    description: Discover highly-cited papers in a field
    prompt: |
      Find the top 20 most cited papers on "transformer architecture" from 
      Semantic Scholar. Sort by citation count and show the venue for each paper.
      
  - name: Author search and profile
    description: Search for authors and their publications
    prompt: |
      Search for author "Yann LeCun" on Semantic Scholar and get his profile 
      including paper count, citation count, h-index, and recent publications.
      
  - name: Citation analysis
    description: Analyze citation network for a paper
    prompt: |
      For the paper "Attention Is All You Need", get all papers that cite it 
      (citations) and papers it references. Analyze the citation patterns.
      
  - name: Batch paper analysis
    description: Analyze multiple papers for literature review
    prompt: |
      I have a list of paper IDs. Use Semantic Scholar to fetch details for 
      all of them and create a summary table with title, year, citations, 
      and key findings.

quickstart: |
  ## Installation
  
  ```bash
  uv pip install semanticscholar pandas matplotlib
  ```
  
  ## Basic Usage
  
  ```python
  from semanticscholar import SemanticScholar
  
  # Initialize client
  sch = SemanticScholar()
  
  # Search papers
  results = sch.search_paper('deep learning', limit=10)
  
  # Get paper details
  paper = sch.get_paper('10.1038/nature14539')
  
  # Search authors
  authors = sch.search_author('Geoffrey Hinton', limit=5)
  ```

best_practices: |
  ## Rate Limiting
  
  Semantic Scholar API has rate limits:
  - Default: 100 requests/5 minutes
  - Be respectful and add delays between batch requests
  - Use `time.sleep(0.1)` between requests in loops
  
  ## Search Tips
  
  - Use specific keywords for better results
  - Combine multiple keywords with AND/OR
  - Use quotes for exact phrase matching
  - Filter by year range for recent research
  
  ## Error Handling
  
  Always handle potential API errors:
  
  ```python
  from semanticscholar import SemanticScholar, SemanticScholarException
  
  sch = SemanticScholar()
  
  try:
      paper = sch.get_paper('invalid-id')
  except SemanticScholarException as e:
      print(f"API Error: {e}")
  except Exception as e:
      print(f"Unexpected error: {e}")
  ```
  
  ## Working with Results
  
  ```python
  # Convert to DataFrame for analysis
  import pandas as pd
  
  papers = sch.search_paper('machine learning', limit=50)
  df = pd.DataFrame([
      {
          'title': p.title,
          'year': p.year,
          'citations': p.citationCount,
          'venue': p.venue
      }
      for p in papers
  ])
  
  # Analyze trends
  yearly_counts = df.groupby('year').size()
  ```

references:
  - https://github.com/danielnsilva/semanticscholar
  - https://api.semanticscholar.org/api-docs/
  - https://www.semanticscholar.org/

related_skills:
  - academic-writing
  - literature-review
  - citation-management
  - openalex
  - pubmed

tags:
  - literature-search
  - academic-papers
  - citations
  - research-discovery
  - semantic-scholar
---

# Semantic Scholar Skill

Search and analyze 200M+ academic papers with AI-powered discovery.

## Overview

Semantic Scholar is a free, AI-powered research tool for scientific literature. 
This skill provides access through an unofficial Python client to:

- 🔍 **Paper Search**: Find papers by keywords, title, or DOI
- 👤 **Author Profiles**: Discover researchers and their work
- 📊 **Citation Analysis**: Track paper impact and citation networks
- 💡 **Paper Recommendations**: Get AI-suggested related papers
- 📈 **Trend Analysis**: Analyze publication trends over time

## Key Features

### Paper Search
- Full-text search across 200M+ papers
- Filter by year, venue, fields of study
- Sort by relevance or citation count
- Access abstracts, PDFs, and citations

### Author Discovery
- Search for researchers by name
- View author profiles with metrics
- Browse author publication lists
- Track h-index and citation counts

### Citation Networks
- Get papers that cite a given paper
- View references cited by a paper
- Analyze citation patterns
- Discover influential works

## Common Workflows

### Literature Review
1. Search for papers on your topic
2. Identify highly-cited key papers
3. Get recommendations for related work
4. Analyze citation networks
5. Export results for your review

### Research Discovery
1. Find recent papers in your field
2. Track citations to seminal works
3. Discover emerging research trends
4. Identify key authors and institutions

### Citation Analysis
1. Get citation counts for papers
2. Analyze citation networks
3. Find influential papers in a field
4. Track research impact over time

## API Limitations

- **Rate Limit**: 100 requests per 5 minutes (default)
- **No API Key Required**: Free tier available
- **Academic Use**: Designed for research and education
- **Data Coverage**: Computer science, biomedicine, and more

## Examples

### Search and Filter
```python
from semanticscholar import SemanticScholar

sch = SemanticScholar()

# Search with filters
results = sch.search_paper(
    'transformer architecture',
    year='2020-2024',
    fields_of_study=['Computer Science'],
    limit=20
)

for paper in results:
    print(f"{paper.title} ({paper.year}) - {paper.citationCount} citations")
```

### Get Paper Details
```python
# By Semantic Scholar ID
paper = sch.get_paper('649def34f8be52c8b66281af98ae884c09aef38b')

# By DOI
paper = sch.get_paper('DOI:10.1038/nature14539')

# By arXiv ID
paper = sch.get_paper('ARXIV:1706.03762')

print(f"Title: {paper.title}")
print(f"Abstract: {paper.abstract[:500]}...")
print(f"Citations: {paper.citationCount}")
```

### Batch Analysis
```python
import pandas as pd
from semanticscholar import SemanticScholar

sch = SemanticScholar()

# Search for papers
papers = sch.search_paper('CRISPR gene editing', limit=100)

# Convert to DataFrame
data = []
for paper in papers:
    data.append({
        'title': paper.title,
        'year': paper.year,
        'citations': paper.citationCount,
        'venue': paper.venue,
        'authors': ', '.join([a.name for a in paper.authors[:3]])
    })

df = pd.DataFrame(data)

# Analyze trends
yearly = df.groupby('year').agg({
    'citations': 'sum',
    'title': 'count'
}).rename(columns={'title': 'paper_count'})

print(yearly)
```

### Citation Network
```python
# Get paper with citations and references
paper = sch.get_paper(
    '10.1038/nature14539',
    include_citations=True,
    include_references=True
)

print(f"Cited by: {len(paper.citations)} papers")
print(f"References: {len(paper.references)} papers")

# Top citing papers
for citation in sorted(paper.citations, 
                       key=lambda x: x.citationCount or 0, 
                       reverse=True)[:5]:
    print(f"  - {citation.title} ({citation.citationCount} citations)")
```

## Tips for Effective Searches

1. **Be Specific**: Use precise technical terms
2. **Use Quotes**: For exact phrase matching
3. **Combine Terms**: Use AND/OR for complex queries
4. **Filter by Year**: Focus on recent research
5. **Check Venues**: Filter by top conferences/journals

## Integration with Other Skills

Combine with:
- **academic-writing**: For literature review writing
- **citation-management**: For bibliography management
- **pubmed**: For biomedical literature
- **openalex**: For alternative academic search

## Resources

- [Semantic Scholar](https://www.semanticscholar.org/)
- [API Documentation](https://api.semanticscholar.org/api-docs/)
- [Python Client GitHub](https://github.com/danielnsilva/semanticscholar)
