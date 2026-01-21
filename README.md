# 🚀 AutoDev - AI Full-Stack Development Team

An autonomous software development system where AI agents collaborate to create complete web applications from natural language requirements.

## 📋 Project Status

**Current Phase:** Phase 1 - Foundation Setup (Week 1)

✅ **Completed:**
- Project structure setup
- Qwen3-Coder API client integration
- Product Manager Agent (requirements analysis)
- Configuration management
- Core utilities and logging

🚧 **In Progress:**
- Database Architect Agent
- Backend Developer Agent
- Frontend Developer Agent
- QA Engineer Agent
- DevOps Agent
- Technical Writer Agent
- Streamlit Professional UI

## 🏗️ Architecture

```
User Input → Streamlit UI → CrewAI Orchestrator → 7 Specialized Agents → Generated Application
                                                           ↓
                                                   Qwen3-Coder API (Qubrid)
```

### 7 Specialized Agents

1. **Product Manager** - Requirements analysis and project planning ✅
2. **Database Architect** - Schema design and optimization 🚧
3. **Backend Developer** - API and business logic 🚧
4. **Frontend Developer** - UI/UX and React components 🚧
5. **QA Engineer** - Test automation and quality assurance 🚧
6. **DevOps** - Deployment and infrastructure automation 🚧
7. **Technical Writer** - Documentation generation 🚧

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Qubrid AI Platform account with API key
- Git (optional, for repository management)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd autodev
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your QUBRID_API_KEY
```

5. **Verify setup:**
```bash
python test_setup.py
```

If all tests pass, you're ready to go! 🎉

## 📁 Project Structure

```
autodev/
├── src/
│   ├── agents/              # AI agent implementations
│   │   ├── product_manager.py  ✅
│   │   ├── database_architect.py  🚧
│   │   ├── backend_developer.py  🚧
│   │   ├── frontend_developer.py  🚧
│   │   ├── qa_engineer.py  🚧
│   │   ├── devops.py  🚧
│   │   └── technical_writer.py  🚧
│   ├── tools/               # CrewAI tools and utilities
│   ├── crews/               # CrewAI crew configurations
│   ├── models/              # Data models
│   ├── utils/               # Utility modules
│   │   ├── qwen_client.py   ✅
│   │   └── config.py        ✅
│   └── ui/                  # Streamlit UI components
│       ├── components/
│       ├── pages/
│       └── styles/
├── templates/               # Code generation templates
│   ├── backend/
│   ├── frontend/
│   ├── database/
│   ├── deployment/
│   └── tests/
├── generated_projects/      # Output directory for generated apps
├── tests/                   # Unit and integration tests
├── logs/                    # Application logs
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## 🔧 Configuration

Edit `.env` file:

```env
# Required: Qubrid AI Platform API
QUBRID_API_KEY=your_api_key_here
QUBRID_BASE_URL=https://api.qubrid.ai/v1
QWEN_MODEL=Qwen3-Coder-30B-A3B

# Optional: GitHub Integration
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_username

# Optional: Deployment Platforms
VERCEL_TOKEN=your_vercel_token
RAILWAY_TOKEN=your_railway_token
```

## 🎯 Usage (Coming Soon)

Once complete, AutoDev will work like this:

```bash
# Start the Streamlit UI
streamlit run src/ui/app.py

# Or use the CLI
python autodev.py "Build a task management app with user auth"
```

**Example Interaction:**

1. Describe your app in natural language
2. Watch 7 AI agents collaborate in real-time
3. Review generated code and tests
4. Download or deploy with one click

## 🧪 Testing

```bash
# Run setup verification
python test_setup.py

# Run all tests (when implemented)
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📊 Current Implementation Progress

| Component | Status | Completion |
|-----------|--------|------------|
| Project Setup | ✅ Complete | 100% |
| Qwen3-Coder Client | ✅ Complete | 100% |
| Configuration | ✅ Complete | 100% |
| Product Manager Agent | ✅ Complete | 100% |
| Database Architect | 🚧 In Progress | 0% |
| Backend Developer | 🚧 Planned | 0% |
| Frontend Developer | 🚧 Planned | 0% |
| QA Engineer | 🚧 Planned | 0% |
| DevOps | 🚧 Planned | 0% |
| Technical Writer | 🚧 Planned | 0% |
| Streamlit UI | 🚧 Planned | 0% |
| **Overall** | **🚧 In Progress** | **15%** |

## 📝 Development Roadmap

### Week 1: Foundation ✅ (Current)
- [x] Project structure
- [x] Qwen3-Coder integration
- [x] Product Manager Agent
- [ ] Database Architect Agent

### Week 2: Core Development Agents
- [ ] Backend Developer Agent
- [ ] Frontend Developer Agent
- [ ] Agent integration tests

### Week 3: Quality & Infrastructure
- [ ] QA Engineer Agent
- [ ] DevOps Agent
- [ ] End-to-end testing

### Week 4: Documentation & UI
- [ ] Technical Writer Agent
- [ ] Streamlit UI (basic version)
- [ ] File management system

### Week 5: Advanced Features
- [ ] Git integration
- [ ] Deployment automation
- [ ] Code quality validation

### Week 6: Polish & Testing
- [ ] UI/UX refinement
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] Demo and deployment

## 🛠️ Tech Stack

- **AI Framework:** CrewAI
- **LLM:** Qwen3-Coder-30B via Qubrid AI Platform
- **UI:** Streamlit
- **Language:** Python 3.11+
- **Testing:** pytest, pytest-asyncio
- **Code Quality:** ruff, black
- **Version Control:** Git
- **Logging:** loguru

## 📖 Documentation

- [Architecture Overview](docs/architecture/overview.md) (Coming soon)
- [Agent Specifications](docs/architecture/agents.md) (Coming soon)
- [API Reference](docs/api/README.md) (Coming soon)
- [Contributing Guide](CONTRIBUTING.md) (Coming soon)

## 🤝 Contributing

This is currently a solo development project. Contributions will be welcome after the initial release.

## 📄 License

[License TBD]

## 🙏 Acknowledgments

- **Qubrid AI Platform** for Qwen3-Coder API access
- **CrewAI** for the multi-agent framework
- **Anthropic** for Claude AI assistance in development

## 📞 Contact

For questions or feedback: [Your contact information]

---

**Built with ❤️ using AI-powered development**

*Last updated: January 2026*
