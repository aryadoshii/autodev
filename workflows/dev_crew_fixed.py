# Just the fixed _load_yaml function - we'll patch it

def _load_yaml(self, relative_path):
    """Load YAML file from project root"""
    # Get the project root (parent of workflows/)
    project_root = Path(__file__).parent.parent
    path = project_root / relative_path
    with open(path, 'r') as f:
        return yaml.safe_load(f)
