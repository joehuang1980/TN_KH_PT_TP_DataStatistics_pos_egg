# TN_KH_PT_TP_DataStatistics_pos_egg

Data statistics analysis for ovitrap positive rate and egg numbers across TN, KH, PT, TP cities for mosquito surveillance and control.

## Quick Start

1. **Read CLAUDE.md first** - Contains essential rules for Claude Code
2. Follow the pre-task compliance checklist before starting any work
3. Use proper module structure under `src/`
4. Commit after every completed task

## Project Structure

```
TN_KH_PT_TP_DataStatistics_pos_egg/
├── CLAUDE.md              # Essential rules for Claude Code
├── README.md              # This file
├── .gitignore             # Git ignore patterns
├── src/                   # Source code (NEVER put files in root)
│   ├── main.py            # Main script/entry point
│   └── utils.py           # Utility functions
├── tests/                 # Test files
│   └── test_main.py       # Basic tests
├── docs/                  # Documentation
└── output/                # Generated output files
```

## Development Guidelines

- **Always search first** before creating new files
- **Extend existing** functionality rather than duplicating
- **Use Task agents** for operations >30 seconds
- **Single source of truth** for all functionality
- **Commit frequently** after each completed task
- **GitHub backup** - Push to GitHub after every commit

## Common Commands

```bash
# Run main analysis
python src/main.py

# Run tests
python -m pytest tests/

# Check code quality
python -m pylint src/

# Format code
python -m black src/

# Commit changes
git add . && git commit -m "Description"

# Backup to GitHub
git push origin main
```

## Project Purpose

This project analyzes:
- Ovitrap positive rates across four cities (TN, KH, PT, TP)
- Egg numbers for mosquito surveillance
- Statistical patterns for mosquito control purposes

## Getting Started

1. Clone or navigate to this repository
2. Read CLAUDE.md for development rules
3. Install dependencies (if any)
4. Start developing in the `src/` directory
5. Save outputs to the `output/` directory

---

**🎯 Template by Chang Ho Chien | HC AI 說人話channel | v1.0.0**
