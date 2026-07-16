from pathlib import Path
import py_compile, sys, subprocess
root=Path(__file__).resolve().parents[2]
files=list((root/'runtime'/'sims_writer_runtime'/'adapters').glob('*.py'))+[root/'runtime'/'sims_writer_runtime'/'orchestrator.py']
for f in files: py_compile.compile(str(f),doraise=True)
subprocess.run([sys.executable,str(root/'tests'/'model-adapters'/'test_model_adapters.py')],check=True)
print(f'model adapter validation: PASS ({len(files)} python files)')
