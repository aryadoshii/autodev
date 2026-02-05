# 🚀 AutoDev - AI-Powered Full-Stack Application Generator

**AutoDev** is a multi-agent AI system that generates complete, production-ready full-stack applications from natural language descriptions in under 2 minutes.

## 🎯 Overview

AutoDev orchestrates **7 specialized AI agents** to collaboratively build:
- ⚡ FastAPI backend with SQLAlchemy ORM
- ⚛️ React frontend with modern UI
- 🧪 Comprehensive test suites
- 🐳 Docker deployment configs
- 📚 Complete documentation

**Powered by:** CrewAI framework + Qwen3-Coder-30B (via Qubrid API)

## ✨ Key Features

- **Multi-Agent Architecture**: 7 specialized agents working together
- **Production-Ready Code**: Includes auth, error handling, tests, deployment
- **Fast Generation**: Complete applications in 60-120 seconds
- **Smart Parsing**: 5-strategy fallback parser handles LLM variations
- **Docker-Ready**: One-command deployment

## 📊 Performance Metrics

- **Generation Time**: 60-120 seconds
- **Files Generated**: 15-30 files per application
- **Success Rate**: 95%+
- **Cost**: ~$0.10-0.20 per generation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Qubrid API key

### Installation
```bash
# Clone and setup
git clone <repo-url>
cd autodev
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your QUBRID_API_KEY
```

### Usage
```bash
# Run AutoDev
python -m workflows.dev_crew

# Enter requirements when prompted:
# Example: "Build a todo app with user authentication"
```

## 📁 Project Structure
```
autodev/
├── workflows/           # Main orchestration logic
│   ├── dev_crew.py     # Multi-agent coordinator
│   └── save_project.py # File generation
├── environment/         # Configuration
│   ├── agents.yaml     # Agent definitions
│   ├── tasks.yaml      # Task definitions
│   └── settings.py     # Environment config
├── agents/             # Agent implementations
├── services/           # Utility functions
└── output/
    └── projects/       # Generated applications
```

## 🎨 Generated Project Structure
```
MyApp_20260123_161712/
├── backend/            # FastAPI + SQLAlchemy
├── frontend/           # React + Components
├── tests/             # Unit + Integration tests
├── docs/              # API documentation
├── docker-compose.yml
└── README.md
```

## 🛠️ Built By

**Arya Doshi**  
Generative AI Engineer @ QubridAI

## 📝 License

MIT License
