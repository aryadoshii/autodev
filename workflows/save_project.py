"""
FIXED: Project Saver - Actually writes files to disk
"""

import os
import json
from pathlib import Path
from datetime import datetime
from loguru import logger


def save_project_to_disk(project_data: dict, app_name: str, output_dir: str) -> Path:
    """
    Save project files to disk with proper structure
    
    Args:
        project_data: Dict containing all agent outputs
        app_name: Name of the application
        output_dir: Base output directory
    
    Returns:
        Path to saved project
    """
    
    # Create project directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = f"{app_name}_{timestamp}"
    project_path = Path(output_dir) / project_name
    
    print("\n" + "="*70)
    print("💾 SAVING PROJECT TO DISK")
    print("="*70)
    print(f"📁 Location: {project_path}")
    
    # Create base directories
    backend_dir = project_path / "backend"
    frontend_dir = project_path / "frontend"
    tests_dir = project_path / "tests"
    docs_dir = project_path / "docs"
    
    for dir_path in [backend_dir, frontend_dir, tests_dir, docs_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Counter for tracking saved files
    files_saved = 0
    
    # ========================================
    # 1. SAVE BACKEND FILES
    # ========================================
    print("\n🔧 Saving backend files...")
    backend_data = project_data.get('backend', {})
    db_schema_data = project_data.get('db_schema', {})
    
    # Combine backend and database files
    all_backend_files = {**backend_data, **db_schema_data}
    
    for filename, content in all_backend_files.items():
        if not filename or not content:
            continue
            
        # Determine file path
        if '/' in filename:
            # Has subdirectory (e.g., "app/models.py")
            file_path = backend_dir / filename
        else:
            # Root backend file (e.g., "main.py")
            file_path = backend_dir / filename
        
        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  ✅ {file_path.relative_to(project_path)}")
            files_saved += 1
        except Exception as e:
            logger.error(f"Failed to write {filename}: {e}")
    
    # ========================================
    # 2. SAVE FRONTEND FILES
    # ========================================
    print("\n⚛️  Saving frontend files...")
    frontend_data = project_data.get('frontend', {})
    
    for filename, content in frontend_data.items():
        if not filename or not content:
            continue
        
        # Handle paths like "src/App.jsx" or "App.jsx"
        if filename.startswith('src/') or filename.startswith('components/'):
            file_path = frontend_dir / filename
        else:
            file_path = frontend_dir / filename
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  ✅ {file_path.relative_to(project_path)}")
            files_saved += 1
        except Exception as e:
            logger.error(f"Failed to write {filename}: {e}")
    
    # ========================================
    # 3. SAVE TEST FILES
    # ========================================
    print("\n🧪 Saving test files...")
    tests_data = project_data.get('tests', {})
    
    for filename, content in tests_data.items():
        if not filename or not content:
            continue
        
        # Handle paths like "backend/test_main.py" or "test_main.py"
        if 'backend/' in filename:
            file_path = tests_dir / filename.replace('backend/', '')
        elif 'frontend/' in filename:
            file_path = tests_dir / filename.replace('frontend/', '')
        else:
            file_path = tests_dir / filename
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  ✅ {file_path.relative_to(project_path)}")
            files_saved += 1
        except Exception as e:
            logger.error(f"Failed to write {filename}: {e}")
    
    # ========================================
    # 4. SAVE DEPLOYMENT FILES
    # ========================================
    print("\n🐳 Saving deployment files...")
    deployment_data = project_data.get('deployment', {})
    
    for filename, content in deployment_data.items():
        if not filename or not content:
            continue
        
        # Dockerfile goes to respective directories
        if filename == "Dockerfile":
            file_path = backend_dir / filename
        elif "frontend" in filename and "Dockerfile" in filename:
            file_path = frontend_dir / "Dockerfile"
        elif filename == "docker-compose.yml":
            file_path = project_path / filename
        elif ".github" in filename:
            # Handle CI/CD files like ".github/workflows/ci.yml"
            file_path = project_path / filename
        else:
            file_path = project_path / filename
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  ✅ {file_path.relative_to(project_path)}")
            files_saved += 1
        except Exception as e:
            logger.error(f"Failed to write {filename}: {e}")
    
    # ========================================
    # 5. SAVE DOCUMENTATION
    # ========================================
    print("\n📚 Saving documentation...")
    docs_data = project_data.get('documentation', {})
    
    for filename, content in docs_data.items():
        if not filename or not content:
            continue
        
        # README.md and API.md go to root
        if filename in ["README.md", "API.md", "CONTRIBUTING.md"]:
            file_path = project_path / filename
        else:
            file_path = docs_dir / filename
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  ✅ {file_path.relative_to(project_path)}")
            files_saved += 1
        except Exception as e:
            logger.error(f"Failed to write {filename}: {e}")
    
    # ========================================
    # 6. CREATE STANDARD FILES
    # ========================================
    print("\n⚙️  Creating standard configuration files...")
    
    # .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Node
node_modules/
npm-debug.log
yarn-error.log

# Environment
.env
.env.local

# Database
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db
"""
    (project_path / ".gitignore").write_text(gitignore_content)
    print(f"  ✅ .gitignore")
    files_saved += 1
    
    # backend/requirements.txt (if not already created)
    if not (backend_dir / "requirements.txt").exists():
        requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
bcrypt==4.1.1
"""
        (backend_dir / "requirements.txt").write_text(requirements)
        print(f"  ✅ backend/requirements.txt")
        files_saved += 1
    
    # frontend/package.json (if not already created)
    if not (frontend_dir / "package.json").exists():
        package_json = {
            "name": app_name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.18.0",
                "axios": "^1.6.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test"
            }
        }
        (frontend_dir / "package.json").write_text(json.dumps(package_json, indent=2))
        print(f"  ✅ frontend/package.json")
        files_saved += 1
    
    # ========================================
    # 7. SAVE PROJECT METADATA
    # ========================================
    print("\n📊 Saving project metadata...")
    pm_spec = project_data.get('pm_spec', {})
    
    metadata = {
        "app_name": app_name,
        "timestamp": timestamp,
        "specification": pm_spec,
        "files_generated": files_saved,
        "generated_by": "AutoDev v1.0"
    }
    
    (project_path / "project_metadata.json").write_text(json.dumps(metadata, indent=2))
    print(f"  ✅ project_metadata.json")
    files_saved += 1
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "="*70)
    print("✅ PROJECT SAVED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📁 Project Location: {project_path}")
    print(f"📄 Total Files Saved: {files_saved}")
    print(f"\n🚀 Quick Start:")
    print(f"  1. cd {project_path}")
    print(f"  2. docker-compose up -d")
    print(f"  3. Open http://localhost:3000")
    print(f"\n💡 VS Code: code {project_path}\n")
    
    return project_path


if __name__ == "__main__":
    # Test with sample data
    test_data = {
        'backend': {
            'main.py': 'from fastapi import FastAPI\n\napp = FastAPI()\n',
            'models.py': 'from sqlalchemy import Column, Integer\n'
        },
        'frontend': {
            'src/App.jsx': 'import React from "react";\n\nfunction App() {}\n'
        },
        'documentation': {
            'README.md': '# Test App\n\nThis is a test.'
        }
    }
    
    save_project_to_disk(test_data, "TestApp", "output/test_projects")
    print("\n✅ Test completed! Check output/test_projects/")