# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

# check_imports.py
import os

# Lista de librerías estándar (simplificada)
STANDARD_LIBS = {
    'sys', 'os', 'math', 'random', 'time', 'typing',
    'dataclasses', 'json', 're', 'pathlib', 'itertools',
    'collections', 'datetime', 'functools', 'string'
}

# Librerías permitidas por ti
ALLOWED_EXTERNAL = {'pygame', 'pytmx'}

def is_external(lib):
    return lib not in STANDARD_LIBS and lib not in ALLOWED_EXTERNAL

def extract_imports_from_line(line):
    tokens = line.replace(',', ' ').split()
    imports = []
    if line.startswith('import '):
        imports = [token.strip() for token in tokens[1:]]
    elif line.startswith('from '):
        imports = [tokens[1].strip()]
    return imports

def scan_imports(folder):
    used_libraries = set()

    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('import') or line.startswith('from'):
                            libs = extract_imports_from_line(line)
                            used_libraries.update(libs)

    return used_libraries

if __name__ == "__main__":
    folder = '.'  # Carpeta raíz del proyecto
    libs = scan_imports(folder)

    external_libs = sorted([lib for lib in libs if is_external(lib)])

    if external_libs:
        print("⚠️  Librerías externas detectadas (revisa si realmente las usas):")
        for lib in external_libs:
            print(f" - {lib}")
    else:
        print("✅ Solo se están usando 'pygame' y/o 'pytmx' como librerías externas.")
