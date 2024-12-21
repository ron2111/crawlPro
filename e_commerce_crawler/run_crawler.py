import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent)
sys.path.append(project_root)

from src.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())