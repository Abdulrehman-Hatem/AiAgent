import os

print("cwd:", os.getcwd())
for root, dirs, files in os.walk("."):
    # skip __pycache__ contents listing detail
    for f in files:
        p = os.path.join(root, f)
        print(p, os.path.getsize(p))
