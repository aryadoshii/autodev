"""Save generated project to disk"""
import json
import os
from pathlib import Path

def save_project_to_disk(project_data: dict, output_dir: str = "generated_projects/priority-todo-list"):
    """Save all generated files to disk"""
    
    base_path = Path(output_dir)
    base_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Saving project to: {base_path.absolute()}\n")
    
    # 1. Save Database files
    db_schema = project_data.get('db_schema', {})
    backend_path = base_path / 'backend'
    (backend_path / 'app' / 'models').mkdir(parents=True, exist_ok=True)
    
    # Save models
    if db_schema.get('models'):
        models_code = db_schema.get('base_imports', '') + "\n\n"
        for model_name, model_code in db_schema['models'].items():
            models_code += f"{model_code}\n\n"
        
        with open(backend_path / 'app' / 'models' / 'models.py', 'w') as f:
            f.write(models_code)
        print("✅ backend/app/models/models.py")
    
    # 2. Save Backend files
    backend = project_data.get('backend', {})
    
    # main.py
    if backend.get('main_app'):
        with open(backend_path / 'app' / 'main.py', 'w') as f:
            f.write(backend['main_app'])
        print("✅ backend/app/main.py")
    
    # routes
    routes_path = backend_path / 'app' / 'routes'
    routes_path.mkdir(parents=True, exist_ok=True)
    
    if backend.get('auth'):
        with open(routes_path / 'auth.py', 'w') as f:
            f.write(backend['auth'])
        print("✅ backend/app/routes/auth.py")
    
    for route_name, route_code in backend.get('routes', {}).items():
        with open(routes_path / f'{route_name}.py', 'w') as f:
            f.write(route_code)
        print(f"✅ backend/app/routes/{route_name}.py")
    
    # schemas
    schemas_path = backend_path / 'app' / 'schemas'
    schemas_path.mkdir(parents=True, exist_ok=True)
    
    for schema_name, schema_code in backend.get('schemas', {}).items():
        with open(schemas_path / f'{schema_name}.py', 'w') as f:
            f.write(schema_code)
        print(f"✅ backend/app/schemas/{schema_name}.py")
    
    # dependencies.py
    if backend.get('dependencies'):
        with open(backend_path / 'app' / 'dependencies.py', 'w') as f:
            f.write(backend['dependencies'])
        print("✅ backend/app/dependencies.py")
    
    # config.py
    if backend.get('config'):
        with open(backend_path / 'app' / 'config.py', 'w') as f:
            f.write(backend['config'])
        print("✅ backend/app/config.py")
    
    # 3. Save Frontend files
    frontend = project_data.get('frontend', {})
    frontend_path = base_path / 'frontend'
    src_path = frontend_path / 'src'
    
    # App.jsx
    if frontend.get('app'):
        src_path.mkdir(parents=True, exist_ok=True)
        with open(src_path / 'App.jsx', 'w') as f:
            f.write(frontend['app'])
        print("✅ frontend/src/App.jsx")
    
    # main.jsx
    if frontend.get('main'):
        with open(src_path / 'main.jsx', 'w') as f:
            f.write(frontend['main'])
        print("✅ frontend/src/main.jsx")
    
    # components
    components_path = src_path / 'components'
    components_path.mkdir(parents=True, exist_ok=True)
    
    for comp_name, comp_code in frontend.get('components', {}).items():
        with open(components_path / f'{comp_name}.jsx', 'w') as f:
            f.write(comp_code)
        print(f"✅ frontend/src/components/{comp_name}.jsx")
    
    # pages
    pages_path = src_path / 'pages'
    pages_path.mkdir(parents=True, exist_ok=True)
    
    for page_name, page_code in frontend.get('pages', {}).items():
        with open(pages_path / f'{page_name}.jsx', 'w') as f:
            f.write(page_code)
        print(f"✅ frontend/src/pages/{page_name}.jsx")
    
    # contexts
    contexts_path = src_path / 'contexts'
    contexts_path.mkdir(parents=True, exist_ok=True)
    
    for context_name, context_code in frontend.get('contexts', {}).items():
        with open(contexts_path / f'{context_name}.jsx', 'w') as f:
            f.write(context_code)
        print(f"✅ frontend/src/contexts/{context_name}.jsx")
    
    # services
    services_path = src_path / 'services'
    services_path.mkdir(parents=True, exist_ok=True)
    
    if frontend.get('services'):
        with open(services_path / 'api.js', 'w') as f:
            f.write(frontend['services'])
        print("✅ frontend/src/services/api.js")
    
    # config files
    config = frontend.get('config', {})
    if config.get('package_json'):
        with open(frontend_path / 'package.json', 'w') as f:
            f.write(config['package_json'])
        print("✅ frontend/package.json")
    
    if config.get('tailwind_config'):
        with open(frontend_path / 'tailwind.config.js', 'w') as f:
            f.write(config['tailwind_config'])
        print("✅ frontend/tailwind.config.js")
    
    if config.get('vite_config'):
        with open(frontend_path / 'vite.config.js', 'w') as f:
            f.write(config['vite_config'])
        print("✅ frontend/vite.config.js")
    
    # 4. Save Tests
    tests = project_data.get('tests', {})
    tests_path = base_path / 'tests'
    
    # backend tests
    backend_tests_path = tests_path / 'backend'
    backend_tests_path.mkdir(parents=True, exist_ok=True)
    
    for test_name, test_code in tests.get('backend', {}).items():
        with open(backend_tests_path / f'{test_name}.py', 'w') as f:
            f.write(test_code)
        print(f"✅ tests/backend/{test_name}.py")
    
    # frontend tests
    frontend_tests_path = tests_path / 'frontend'
    frontend_tests_path.mkdir(parents=True, exist_ok=True)
    
    for test_name, test_code in tests.get('frontend', {}).items():
        with open(frontend_tests_path / f'{test_name}.jsx', 'w') as f:
            f.write(test_code)
        print(f"✅ tests/frontend/{test_name}.jsx")
    
    # e2e tests
    e2e_tests_path = tests_path / 'e2e'
    e2e_tests_path.mkdir(parents=True, exist_ok=True)
    
    for test_name, test_code in tests.get('e2e', {}).items():
        with open(e2e_tests_path / f'{test_name}.js', 'w') as f:
            f.write(test_code)
        print(f"✅ tests/e2e/{test_name}.js")
    
    # 5. Save Deployment files
    deployment = project_data.get('deployment', {})
    docker = deployment.get('docker', {})
    
    if docker.get('backend_dockerfile'):
        with open(backend_path / 'Dockerfile', 'w') as f:
            f.write(docker['backend_dockerfile'])
        print("✅ backend/Dockerfile")
    
    if docker.get('frontend_dockerfile'):
        with open(frontend_path / 'Dockerfile', 'w') as f:
            f.write(docker['frontend_dockerfile'])
        print("✅ frontend/Dockerfile")
    
    if docker.get('docker_compose'):
        with open(base_path / 'docker-compose.yml', 'w') as f:
            f.write(docker['docker_compose'])
        print("✅ docker-compose.yml")
    
    if docker.get('dockerignore'):
        with open(base_path / '.dockerignore', 'w') as f:
            f.write(docker['dockerignore'])
        print("✅ .dockerignore")
    
    # CI/CD
    ci_cd = deployment.get('ci_cd', {})
    if ci_cd.get('github_actions'):
        github_path = base_path / '.github' / 'workflows'
        github_path.mkdir(parents=True, exist_ok=True)
        with open(github_path / 'ci-cd.yml', 'w') as f:
            f.write(ci_cd['github_actions'])
        print("✅ .github/workflows/ci-cd.yml")
    
    # Environment files
    env = deployment.get('env', {})
    if env.get('backend_env'):
        with open(backend_path / '.env.example', 'w') as f:
            f.write(env['backend_env'])
        print("✅ backend/.env.example")
    
    if env.get('frontend_env'):
        with open(frontend_path / '.env.example', 'w') as f:
            f.write(env['frontend_env'])
        print("✅ frontend/.env.example")
    
    # 6. Save Documentation
    docs = project_data.get('documentation', {})
    
    for doc_name, doc_content in docs.items():
        filename = f"{doc_name.upper().replace('_', '-')}.md"
        with open(base_path / filename, 'w') as f:
            f.write(doc_content)
        print(f"✅ {filename}")
    
    print(f"\n🎉 Project saved successfully to: {base_path.absolute()}")
    print(f"\n📂 Open in VS Code: code {base_path.absolute()}")


# Load the execution log and save
if __name__ == "__main__":
    with open('execution_log.json', 'r') as f:
        log_data = json.load(f)
    
    print("⚠️  This script needs the project_data from the completed run.")
    print("The project_data is currently in memory from the last run.")
    print("\nTo save the project, modify dev_crew.py to call save_project_to_disk()")