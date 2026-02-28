# Community Skills Contribution

## Summary

This PR adds **30 general-purpose skills** to the claude-scientific-skills ecosystem, contributed by the OpenClaw community.

## Skills Added

### 🛠️ Development Tools (7 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **coding-agent** | Delegate coding tasks to AI agents (Codex, Claude Code, etc.) | Development |
| **docker-essentials** | Essential Docker commands and workflows | DevOps |
| **github** | GitHub CLI automation, PR management, and issue handling | DevOps |
| **ralph-loop** | Generate Ralph Wiggum/AI agent loops for planning and building | Development |
| **mcp-builder** | Build and manage MCP (Model Context Protocol) servers | Development |
| **mcporter** | Configure and call MCP servers/tools | Development |
| **webapp-testing** | Web application testing with Playwright | Testing |

### 📚 Academic & Research (6 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **google-scholar** | Search and retrieve papers from Google Scholar | Research |
| **semanticscholar** | Semantic Scholar API integration | Research |
| **context7** | Query documentation from Context7 (500,000+ libraries) | Documentation |
| **academic-writing** | Academic paper writing assistance | Writing |
| **moltsci** | Publish and discover AI-native scientific papers | Publishing |

### ⏰ Automation (4 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **cron-automation** | Cron jobs management and monitoring | Automation |
| **get-tldr** | Quick article summarization via get-tldr.com API | Productivity |
| **browse** | Browser automation with Playwright/Selenium | Automation |
| **x-api** | X (Twitter) API for real-time search and monitoring | Social |

### 🎓 Learning & Education (4 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **video-learning** | Unified video learning system (Bilibili/YouTube) | Learning |
| **bilibili-video-analyzer** | Analyze Bilibili videos and extract knowledge | Learning |
| **youtube-video-analyzer** | Analyze YouTube videos and extract knowledge | Learning |
| **self-learning-loop** | Self-learning iteration system with skill extraction | Meta |

### 📄 Document Processing (5 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **docx** | Microsoft Word document processing | Documents |
| **pdf** | PDF processing and manipulation | Documents |
| **nano-pdf** | Natural language PDF editing | Documents |
| **pptx** | Microsoft PowerPoint processing | Documents |
| **xlsx** | Microsoft Excel processing | Documents |

### 🔍 Search & Tools (2 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **tavily-search** | Tavily AI-optimized web search | Search |
| **weather** | Weather information retrieval | Utilities |

### 📖 Meta Skills (2 skills)
| Skill | Description | Category |
|-------|-------------|----------|
| **skill-creator** | Guidelines for creating new skills | Meta |
| **skills-system** | Skills ecosystem maintenance guide | Meta |

## Key Features

### General-Purpose Design
All skills are designed to be useful to a broad audience:
- ✅ No personal configurations
- ✅ No specific user data
- ✅ Generic examples and workflows
- ✅ Clear documentation

### Documentation
Each skill includes:
- **SKILL.md**: Comprehensive documentation with examples
- **Installation**: Required dependencies
- **Quick Start**: Basic usage examples
- **Advanced Usage**: Complex scenarios
- **Best Practices**: Recommendations

### Quality Assurance
- All skills tested and validated
- Consistent formatting and structure
- Cross-references between related skills
- Community README with overview

## Directory Structure

```
community-skills/
├── README.md                 # Overview and usage guide
├── coding-agent/            # Development tools
├── docker-essentials/
├── github/
├── ... (30 skills total)
└── youtube-video-analyzer/
```

## Usage

To use any skill:
1. Copy the skill directory to your `skills/` folder
2. Install required dependencies (listed in SKILL.md)
3. Follow the examples in the documentation

## Testing

All skills have been:
- ✅ Syntax checked
- ✅ Structure validated
- ✅ Documentation reviewed

## Related

These skills complement the existing `scientific-skills/` directory by adding:
- Development and automation tools
- Learning and education systems
- Document processing capabilities
- Research and search utilities

## License

All community skills are provided under MIT License (or as specified in individual skill directories).

---

**Note**: This is a community contribution to expand the claude-scientific-skills ecosystem with general-purpose tools suitable for researchers, developers, and knowledge workers.
