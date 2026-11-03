import ast

p = open("build_faces.py", "rb").read()
lines = p.split(bytes((10,)))
lines[3] = lines[3] + b"wah" + bytes((34,))
open("build_faces.py", "wb").write(bytes((10,)).join(lines))
ast.parse(open("build_faces.py").read())
print("patched+parsed")
