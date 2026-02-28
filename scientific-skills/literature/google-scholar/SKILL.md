---
name: google-scholar
version: 1.0.0
description: |
  Unofficial Python client for Google Scholar using scholarly library.
  Search academic papers, authors, citations, and publications.
  Free alternative to official APIs with no rate limits.
  
  Google Scholar provides access to scholarly literature across various disciplines.
  This skill uses the scholarly Python library to search and retrieve academic data.

author: Assistant
category: literature
license: MIT
homepage: https://github.com/scholarly-python-package/scholarly
requirements:
  - scholarly>=1.7.0
  - pandas>=1.3.0
  - matplotlib>=3.4.0
  
examples:
  - name: Search papers by keyword
    description: Find papers on a specific topic
    prompt: |
      Search Google Scholar for papers about "transformer architecture" 
      from 2020-2024. Return the top 10 results with title, authors, year, 
      citation count, and abstract.
      
  - name: Get author profile
    description: Search for an author and their publications
    prompt: |
      Search Google Scholar for author "Geoffrey Hinton" and get his profile
      including affiliation, interests, citation count, and recent publications.
      
  - name: Find highly cited papers
    description: Discover influential papers in a field
    prompt: |
      Find the top 20 most cited papers on "deep learning" from Google Scholar.
      Sort by citation count and show the venue for each paper.
      
  - name: Search author publications
    description: Get all publications by an author
    prompt: |
      Find all publications by "Yann LeCun" on Google Scholar, 
      sorted by year (newest first). Include citation counts.
      
  - name: Citation analysis
    description: Analyze citation network
    prompt: |
      Find papers that cite "Attention Is All You Need" on Google Scholar.
      Show the top 10 citing papers with their citation counts.

quickstart: |
  ## Installation
  
  ```bash
  uv pip install scholarly pandas matplotlib
  ```
  
  ## Basic Usage
  
  ```python
  from scholarly import scholarly
  
  # Search papers
  search_query = scholarly.search_pubs('deep learning')
  paper = next(search_query)
  
  # Get author
  author = scholarly.search_author('Geoffrey Hinton')
  
  # Get citations
  citations = scholarly.search_citedby(paper['pub_url'])
  ```

best_practices: |
  ## Rate Limiting
  
  Google Scholar has implicit rate limits:
  - Add delays between requests: `time.sleep(0.5)`
  - Use proxy rotation for large batches
  - Cache results to avoid repeated queries
  
  ## Search Tips
  
  - Use specific keywords for better results
  - Combine multiple keywords with AND/OR
  - Use quotes for exact phrase matching
  - Filter by year for recent research
  
  ## Error Handling
  
  Always handle potential errors:
  
  ```python
  from scholarly import scholarly, MaxTriesExceededException
  
  try:
      author = next(scholarly.search_author('Name'))
  except MaxTriesExceededException:
      print("Rate limit hit, try again later")
  except StopIteration:
      print("No results found")
  except Exception as e:
      print(f"Error: {e}")
  ```
  
  ## Working with Results
  
  ```python
  # Convert to DataFrame for analysis
  import pandas as pd
  
  papers = list(scholarly.search_pubs('machine learning'))
  df = pd.DataFrame([
      {
          'title': p['bib']['title'],
          'year': p['bib'].get('pub_year'),
          'citations': p['num_citations'],
          'author': p['bib']['author'][0] if p['bib'].get('author') else 'Unknown'
      }
      for p in papers[:50]
  ])
  
  # Analyze trends
  yearly_counts = df.groupby('year').size()
  ```

references:
  - https://github.com/scholarly-python-package/scholarly
  - https://scholar.google.com/
  - https://pypi.org/project/scholarly/

related_skills:
  - semanticscholar
  - academic-writing
  - literature-review
  - citation-management

tags:
  - literature-search
  - academic-papers
  - citations
  - research-discovery
  - google-scholar
  - scholarly
---

# Google Scholar Skill

Search and analyze scholarly literature using Google Scholar.

## Overview

Google Scholar is a freely accessible web search engine that indexes scholarly literature. 
This skill provides access through the `scholarly` Python library to:

- 🔍 **Paper Search**: Find papers by keywords, title, or author
- 👤 **Author Profiles**: Discover researchers and their work
- 📊 **Citation Analysis**: Track paper impact and citation networks
- 📈 **Publication Lists**: Get complete author publication history

## Key Features

### Paper Search
- Full-text search across scholarly articles
- Filter by year, author, publication
- Sort by relevance or citation count
- Access abstracts and citations

### Author Discovery
- Search for researchers by name
- View author profiles with metrics
- Browse author publication lists
- Track citation counts and h-index

### Citation Networks
- Get papers that cite a given paper
- Analyze citation patterns
- Discover influential works

## Common Workflows

### Literature Review
1. Search for papers on your topic
2. Identify highly-cited key papers
3. Get author information
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

- **Rate Limiting**: Google Scholar may block excessive requests
- **No Official API**: Uses web scraping (scholarly library)
- **Captcha**: May encounter captcha for large batches
- **Data Coverage**: Varies by discipline

## Examples

### Search Papers
```python
from scholarly import scholarly

# Search papers
search_query = scholarly.search_pubs('transformer architecture')

# Get first 10 results
papers = []
for _ in range(10):
    try:
        paper = next(search_query)
        papers.append(paper)
    except StopIteration:
        break

for paper in papers:
    print(f"{paper['bib']['title']} ({paper['bib'].get('pub_year')}) - {paper['num_citations']} citations")
```

### Get Author Details
```python
# Search for author
search_query = scholarly.search_author('Geoffrey Hinton')
author = next(search_query)

# Fill in full author details
author = scholarly.fill(author)

print(f"Name: {author['name']}")
print(f"Affiliation: {author.get('affiliation', 'N/A')}")
print(f"Citations: {author.get('citedby', 0)}")
print(f"h-index: {author.get('hindex', 0)}")
print(f"Interests: {', '.join(author.get('interests', []))}")

# Get publications
publications = author.get('publications', [])
for pub in publications[:5]:
    print(f"  - {pub['bib']['title']} ({pub['bib'].get('pub_year')})")
```

### Batch Analysis
```python
import pandas as pd
from scholarly import scholarly

# Search for papers
search_query = scholarly.search_pubs('machine learning')

# Collect data
data = []
for _ in range(50):
    try:
        paper = next(search_query)
        data.append({
            'title': paper['bib']['title'],
            'year': paper['bib'].get('pub_year'),
            'citations': paper['num_citations'],
            'author': paper['bib']['author'][0] if paper['bib'].get('author') else 'Unknown',
            'venue': paper['bib'].get('venue', 'N/A')
        })
    except StopIteration:
        break

df = pd.DataFrame(data)

# Analyze trends
yearly = df.groupby('year').agg({
    'citations': 'sum',
    'title': 'count'
}).rename(columns={'title': 'paper_count'})

print(yearly)
```

### Cited By (Papers that cite this paper)
```python
# First get a paper
search_query = scholarly.search_pubs('Attention Is All You Need')
paper = next(search_query)
paper = scholarly.fill(paper)

# Get papers that cite this one
citedby_query = scholarly.search_citedby(paper)

print(f"Papers citing '{paper['bib']['title']}':")
for _ in range(10):
    try:
        citing_paper = next(citedby_query)
        print(f"  - {citing_paper['bib']['title']} ({citing_paper['num_citations']} citations)")
    except StopIteration:
        break
```

## Tips for Effective Searches

1. **Be Specific**: Use precise technical terms
2. **Use Quotes**: For exact phrase matching
3. **Combine Terms**: Use AND/OR for complex queries
4. **Check Author Names**: Verify spelling
5. **Filter by Year**: Focus on recent research

## Integration with Other Skills

Combine with:
- **semanticscholar**: For alternative academic search
- **academic-writing**: For literature review writing
- **citation-management**: For bibliography management

## Comparison: Google Scholar vs Semantic Scholar

| Feature | Google Scholar | Semantic Scholar |
|---------|---------------|------------------|
| **Data Coverage** | Broader (all disciplines) | Focused (CS, Medicine) |
| **API** | Unofficial (scholarly) | Official API |
| **Rate Limits** | Strict (scraping) | 100 req/5min |
| **Citation Data** | Yes | Yes + influential citations |
| **Open Access** | Mixed | More open access PDFs |
| **Best For** | Broad search, author metrics | Deep analysis, CS papers |

**Recommendation**: Use both for comprehensive research!

## Resources

- [scholarly GitHub](https://github.com/scholarly-python-package/scholarly)
- [Google Scholar](https://scholar.google.com/)
- [PyPI: scholarly](https://pypi.org/project/scholarly/)

## Troubleshooting

### MaxTriesExceededException
**Solution**: Add delays between requests
```python
import time

for _ in range(10):
    paper = next(search_query)
    time.sleep(0.5)  # Add delay
```

### Captcha Issues
**Solution**: Use proxy rotation or reduce request frequency

### No Results
**Solution**: Try different keywords or check spelling

---

*"Standing on the shoulders of giants"* — Bernard of Chartres
