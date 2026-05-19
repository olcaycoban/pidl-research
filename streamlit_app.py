"""
Streamlit Cloud entry point (same app as research_app.py).
"""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "research_app.py"), run_name="__main__")
