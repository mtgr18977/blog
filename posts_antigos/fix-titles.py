#!/usr/bin/env python3
"""
fix_titles.py
Corrige o frontmatter dos posts scrapeados:
substitui o `title` pelo conteúdo do primeiro `#` no corpo do arquivo.

Uso:
    python fix_titles.py posts_completos/
"""

import sys
import re
from pathlib import Path

pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
arquivos = list(pasta.glob("*.md"))

if not arquivos:
    print(f"Nenhum .md encontrado em {pasta}")
    sys.exit(1)

corrigidos = 0
sem_h1 = []

for f in arquivos:
    texto = f.read_text(encoding="utf-8")

    # Extrai o primeiro # do corpo (fora do frontmatter)
    h1 = re.search(r"^#\s+(.+)$", texto, re.MULTILINE)
    if not h1:
        sem_h1.append(f.name)
        continue

    titulo = h1.group(1).strip()

    # Substitui apenas o campo title: no frontmatter
    novo = re.sub(r"(?m)^title:.*$", f"title: {titulo}", texto, count=1)

    if novo != texto:
        f.write_text(novo, encoding="utf-8")
        print(f"✓ {f.name}  →  {titulo}")
        corrigidos += 1

print(f"\n{corrigidos}/{len(arquivos)} arquivos corrigidos.")
if sem_h1:
    print(f"\n⚠️  Sem H1 encontrado:")
    for n in sem_h1:
        print(f"   {n}")