"""
Project Serialization Module
Saves generated projects to disk with proper organization
Each project gets its own timestamped folder
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict

def save_project_to_disk(
    project_data: Dict, 
    app_name: str = None,
    output_base_dir: str = "output/projects"
) -> Path:
    """
    Save all generated files to disk in a properly organized structure
    
    Args:
        project_data: Complete project data from orchestrator
        app_name: Name of the application (extracted from PM spec)
        output_base_dir: Base directory for all projects
    
    Returns:
        Path to the saved project
    """
    
    # Get app name from project data if not provided
    if not app_name:
        app_name = project_data.get('pm_spec', {}).get('app_name', 'generated-app')
    
    # Create timestamped project folder
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    project_folder_name = f"{app_name}_{timestamp}"
    
    base_path = Path(output_base_dir) / project_folder_name
    base_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*70}")
    print(f"💾 SAVING PROJECT TO DISK")
    print(f"{'='*70}")
    print(f"📁 Location: {base_path.absolute()}\n")
    
    # ================================================================
    # 1. BACKEND STRUCTURE
    # ================================================================
    print("🔧 Creating backend structure...")
    
    db_schema = project_data.get('db_schema', {})
    backend = project_data.get('backend', {})
    
    backend_path = base_path / 'backend'
    app_path = backend_path / 'app'
    
    # Create backend folder structure
    (app_path / 'api').mkdir(parents=True, exist_ok=True)
    (app_path / 'api' / 'routes').mkdir(parents=True, exist_ok=True)
    (app_path / 'core').mkdir(parents=True, exist_ok=True)
    (app_path / 'models').mkdir(parents=True, exist_ok=True)
    (app_path / 'schemas').mkdir(parents=True, exist_ok=True)
    
    # Save database models
    if db_schema.get('models'):
        models_code = db_schema.get('base_imports', '') + "\n\n"
        for model_name, model_code in db_schema['models'].items():
            models_code += f"{model_code}\n\n"
        
        (app_path / 'models' / 'database.py').write_text(models_code)
        print("  ✅ backend/app/models/database.py")
    
    # Save main.py
    if backend.get('main_app'):
        (app_path / 'main.py').write_text(backend['main_app'])
        print("  ✅ backend/app/main.py")
    
    # Save auth routes
    if backend.get('auth'):
        (app_path / 'api' / 'routes' / 'auth.py').write_text(backend['auth'])
        print("  ✅ backend/app/api/routes/auth.py")
    
    # Save model routes
    for route_name, route_code in backend.get('routes', {}).items():
        (app_path / 'api' / 'routes' / f'{route_name}.py').write_text(route_code)
        print(f"  ✅ backend/app/api/routes/{route_name}.py")
    
    # Save schemas
    for schema_name, schema_code in backend.get('schemas', {}).items():
        (app_path / 'schemas' / f'{schema_name}.py').write_text(schema_code)
        print(f"  ✅ backend/app/schemas/{schema_name}.py")
    
    # Save core files
    if backend.get('dependencies'):
        (app_path / 'core' / 'dependencies.py').write_text(backend['dependencies'])
        print("  ✅ backend/app/core/dependencies.py")
    
    if backend.get('config'):
        (app_path / 'core' / 'config.py').write_text(backend['config'])
        print("  ✅ backend/app/core/config.py")
    
    # Create __init__.py files
    for init_path in [app_path, app_path / 'api', app_path / 'api' / 'routes', 
                      app_path / 'core', app_path / 'models', app_path / 'schemas']:
        (init_path / '__init__.py').touch()
    
    # ================================================================
    # 2. FRONTEND STRUCTURE
    # ================================================================
    print("\n⚛️  Creating frontend structure...")
    
    frontend = project_data.get('frontend', {})
    frontend_path = base_path / 'frontend'
    src_path = frontend_path / 'src'
    
    # Create frontend folder structure
    (src_path / 'components').mkdir(parents=True, exist_ok=True)
    (src_path / 'pages').mkdir(parents=True, exist_ok=True)
    (src_path / 'contexts').mkdir(parents=True, exist_ok=True)
    (src_path / 'services').mkdir(parents=True, exist_ok=True)
    (src_path / 'utils').mkdir(parents=True, exist_ok=True)
    (src_path / 'assets').mkdir(parents=True, exist_ok=True)
    (frontend_path / 'public').mkdir(parents=True, exist_ok=True)
    
    # Save main files
    if frontend.get('app'):
        (src_path / 'App.jsx').write_text(frontend['app'])
        print("  ✅ frontend/src/App.jsx")
    
    if frontend.get('main'):
        (src_path / 'main.jsx').write_text(frontend['main'])
        print("  ✅ frontend/src/main.jsx")
    
    # Save components
    for comp_name, comp_code in frontend.get('components', {}).items():
        (src_path / 'components' / f'{comp_name}.jsx').write_text(comp_code)
        print(f"  ✅ frontend/src/components/{comp_name}.jsx")
    
    # Save pages
    for page_name, page_code in frontend.get('pages', {}).items():
        (src_path / 'pages' / f'{page_name}.jsx').write_text(page_code)
        print(f"  ✅ frontend/src/pages/{page_name}.jsx")
    
    # Save contexts
    for context_name, context_code in frontend.get('contexts', {}).items():
        (src_path / 'contexts' / f'{context_name}.jsx').write_text(context_code)
        print(f"  ✅ frontend/src/contexts/{context_name}.jsx")
    
    # Save services
    if frontend.get('services'):
        (src_path / 'services' / 'api.js').write_text(frontend['services'])
        print("  ✅ frontend/src/services/api.js")
    
    # Save config files
    config = frontend.get('config', {})
    if config.get('package_json'):
        (frontend_path / 'package.json').write_text(config['package_json'])
        print("  ✅ frontend/package.json")
    
    if config.get('vite_config'):
        (frontend_path / 'vite.config.js').write_text(config['vite_config'])
        print("  ✅ frontend/vite.config.js")
    
    if config.get('tailwind_config'):
        (frontend_path / 'tailwind.config.js').write_text(config['tailwind_config'])
        print("  ✅ frontend/tailwind.config.js")
    
    # Create index.html
    index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{app_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>""".format(app_name=app_name)
    
    (frontend_path / 'index.html').write_text(index_html)
    print("  ✅ frontend/index.html")
    
    # Create CSS file
    css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
"""
    (src_path / 'index.css').write_text(css_content)
    print("  ✅ frontend/src/index.css")
    
    # ================================================================
    # 3. TESTS STRUCTURE
    # ================================================================
    print("\n🧪 Creating tests structure...")
    
    tests = project_data.get('tests', {})
    tests_path = base_path / 'tests'
    
    # Backend tests
    backend_tests_path = tests_path / 'backend'
    backend_tests_path.mkdir(parents=True, exist_ok=True)
    
    for test_name, test_code in tests.get('backend', {}).items():
        (backend_tests_path / f'{test_name}.py').write_text(test_code)
        print(f"  ✅ tests/backend/{test_name}.py")
    
    # Frontend tests
    frontend_tests_path = tests_path / 'frontend'
    frontend_tests_path.mkdir(parents=True, exist_ok=True)
    
    for test_name, test_code in tests.get('frontend', {}).items():
        (frontend_tests_path / f'{test_name}.jsx').write_text(test_code)
        print(f"  ✅ tests/frontend/{test_name}.jsx")
    
    # E2E tests
    e2e_tests_path = tests_path / 'e2e'
    e2e_tests_path.mkdir(parents=True, exist_ok=True)
    
    for test_name, test_code in tests.get('e2e', {}).items():
        (e2e_tests_path / f'{test_name}.js').write_text(test_code)
        print(f"  ✅ tests/e2e/{test_name}.js")
    
    # ================================================================
    # 4. DEPLOYMENT STRUCTURE
    # ================================================================
    print("\n🐳 Creating deployment configuration...")
    
    deployment = project_data.get('deployment', {})
    docker = deployment.get('docker', {})
    
    # Backend Dockerfile
    if docker.get('backend_dockerfile'):
        (backend_path / 'Dockerfile').write_text(docker['backend_dockerfile'])
        print("  ✅ backend/Dockerfile")
    
    # Frontend Dockerfile
    if docker.get('frontend_dockerfile'):
        (frontend_path / 'Dockerfile').write_text(docker['frontend_dockerfile'])
        print("  ✅ frontend/Dockerfile")
    
    # Docker Compose
    if docker.get('docker_compose'):
        (base_path / 'docker-compose.yml').write_text(docker['docker_compose'])
        print("  ✅ docker-compose.yml")
    
    # .dockerignore
    if docker.get('dockerignore'):
        (base_path / '.dockerignore').write_text(docker['dockerignore'])
        print("  ✅ .dockerignore")
    
    # CI/CD
    ci_cd = deployment.get('ci_cd', {})
    if ci_cd.get('github_actions'):
        github_path = base_path / '.github' / 'workflows'
        github_path.mkdir(parents=True, exist_ok=True)
        (github_path / 'ci-cd.yml').write_text(ci_cd['github_actions'])
        print("  ✅ .github/workflows/ci-cd.yml")
    
    # Environment files
    env = deployment.get('env', {})
    if env.get('backend_env'):
        (backend_path / '.env.example').write_text(env['backend_env'])
        print("  ✅ backend/.env.example")
    
    if env.get('frontend_env'):
        (frontend_path / '.env.example').write_text(env['frontend_env'])
        print("  ✅ frontend/.env.example")
    
    # ================================================================
    # 5. DOCUMENTATION
    # ================================================================
    print("\n📚 Creating documentation...")
    
    docs = project_data.get('documentation', {})
    
    doc_files = {
        'readme': 'README.md',
        'api': 'API.md',
        'architecture': 'ARCHITECTURE.md',
        'setup': 'SETUP.md',
        'contributing': 'CONTRIBUTING.md',
        'troubleshooting': 'TROUBLESHOOTING.md',
    }
    
    for doc_key, filename in doc_files.items():
        if doc_key in docs:
            (base_path / filename).write_text(docs[doc_key])
            print(f"  ✅ {filename}")
    
    # ================================================================
    # 6. ROOT CONFIGURATION FILES
    # ================================================================
    print("\n⚙️  Creating root configuration files...")
    
    # .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
venv/
.venv/
ENV/

# Environment Variables
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp

# Logs
*.log
logs/

# Database
*.db
*.sqlite

# Node
node_modules/
package-lock.json

# Build
dist/
build/

# OS
.DS_Store
Thumbs.db
"""
    (base_path / '.gitignore').write_text(gitignore_content)
    print("  ✅ .gitignore")
    
    # Backend requirements.txt
    backend_requirements = """fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0
alembic==1.13.1
python-dotenv==1.0.0
"""
    (backend_path / 'requirements.txt').write_text(backend_requirements)
    print("  ✅ backend/requirements.txt")
    
    # ================================================================
    # 7. PROJECT METADATA
    # ================================================================
    print("\n📊 Saving project metadata...")
    
    metadata = {
        'project_name': app_name,
        'generated_at': timestamp,
        'project_type': project_data.get('pm_spec', {}).get('app_type', 'Unknown'),
        'tech_stack': {
            'backend': 'FastAPI',
            'frontend': 'React + Vite',
            'database': 'PostgreSQL',
            'styling': 'Tailwind CSS',
        },
        'statistics': {
            'models': len(db_schema.get('models', {})),
            'backend_routes': len(backend.get('routes', {})),
            'frontend_components': len(frontend.get('components', {})),
            'frontend_pages': len(frontend.get('pages', {})),
            'backend_tests': len(tests.get('backend', {})),
            'frontend_tests': len(tests.get('frontend', {})),
            'e2e_tests': len(tests.get('e2e', {})),
        }
    }
    
    (base_path / 'project_metadata.json').write_text(json.dumps(metadata, indent=2))
    print("  ✅ project_metadata.json")
    
    # ================================================================
    # COMPLETION SUMMARY
    # ================================================================
    print(f"\n{'='*70}")
    print(f"✅ PROJECT SAVED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"\n📁 Project Location: {base_path.absolute()}")
    print(f"\n📂 Project Structure:")
    print(f"""
    {project_folder_name}/
    ├── backend/              # FastAPI backend
    │   ├── app/
    │   │   ├── api/routes/   # API endpoints
    │   │   ├── core/         # Config & dependencies
    │   │   ├── models/       # Database models
    │   │   └── schemas/      # Pydantic schemas
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── frontend/             # React frontend
    │   ├── src/
    │   │   ├── components/   # Reusable components
    │   │   ├── pages/        # Page components
    │   │   ├── contexts/     # React contexts
    │   │   └── services/     # API services
    │   ├── package.json
    │   └── Dockerfile
    ├── tests/                # Test suites
    │   ├── backend/
    │   ├── frontend/
    │   └── e2e/
    ├── .github/workflows/    # CI/CD
    ├── docker-compose.yml
    ├── README.md
    └── API.md
    """)
    
    print(f"\n🚀 Quick Start:")
    print(f"  1. cd {base_path.absolute()}")
    print(f"  2. docker-compose up -d")
    print(f"  3. Open http://localhost:3000")
    
    print(f"\n💡 VS Code: code {base_path.absolute()}\n")
    
    return base_path


def get_next_project_path(app_name: str, base_dir: str = "output/projects") -> Path:
    """
    Generate unique project path with timestamp
    
    Args:
        app_name: Application name
        base_dir: Base directory for projects
    
    Returns:
        Unique path for the new project
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    project_name = f"{app_name}_{timestamp}"
    return Path(base_dir) / project_name
