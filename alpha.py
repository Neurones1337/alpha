#!/usr/bin/env python3

import random
import os
from itertools import product, permutations, combinations
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print
from tqdm import tqdm
import argparse

console = Console()

LEET_MAP = {
    'a': ['4', '@'], 'e': ['3', '€', '&'], 'i': ['1'],
    'o': ['0'], 's': ['$', '5'], 't': ['7']
}

SYMBOLS = ['!', '@', '#', '_', '-', '.', '*', '?', '/']
YEARS = [str(y) for y in range(1900, datetime.now().year + 1)]

def header():
    console.print(Panel.fit("[bold cyan]Alpha v1.0[/bold cyan]\n[white]By Neurones[/white]"))

def generate_leet(word):
    leet_variants = set()
    queue = [word]
    for i, char in enumerate(word):
        if char.lower() in LEET_MAP:
            new_queue = []
            for variant in queue:
                for sub in LEET_MAP[char.lower()]:
                    new_variant = variant[:i] + sub + variant[i+1:]
                    new_queue.append(new_variant)
            queue.extend(new_queue)
    leet_variants.update(queue)
    return leet_variants

def insert_special_chars(words):
    inserted = set()
    for word in words:
        for i in range(1, len(word)):
            for sym in SYMBOLS:
                inserted.add(word[:i] + sym + word[i:])
    return inserted

def generate_mutations(words, use_symbols=False, use_years=False, use_random_digits=False):
    variants = set()
    suffixes = ['123', '1234', '321']
    if use_symbols:
        suffixes += SYMBOLS
        for sym in SYMBOLS:
            suffixes.append(sym * 2)
            suffixes.append(sym * 3)

    if use_years:
        suffixes += YEARS

    for word in words:
        for suf in suffixes:
            variants.update([
                word + suf,
                suf + word,
                word.capitalize() + suf,
            ])

        if use_random_digits:
            for length in range(1, 5):
                rand_digits = ''.join(random.choices('0123456789', k=length))
                variants.update([
                    word + rand_digits,
                    rand_digits + word,
                ])

        brackets = [('(', ')'), ('[', ']'), ('{', '}'),('!','!')]
        for suf in suffixes:
            for left, right in brackets:
                variants.update([
                    f"{left}{word}{right}",
                    f"{word}{left}{suf}{right}",
                    f"{left}{word}{suf}{right}",
                    f"{word}{right}",
                    f"{left}{word}",
                ])

    for a, b in product(words, repeat=2):
        if a != b:
            variants.update([a + b, b + a, a + "_" + b])

    if use_symbols:
        variants.update(insert_special_chars(words))

    return variants

def generate_mix(words):
    mixed = set()
    for a, b in combinations(words, 2):
        for i in range(1, len(a)):
            for j in range(1, len(b)):
                mixed.update([
                    a[:i] + b[j:],
                    b[:j] + a[i:]
                ])
    return mixed

def generate_permutations(words, max_len=3):
    permuts = set()
    for n in range(2, max_len + 1):
        for combo in permutations(words, n):
            joined = ''.join(combo)
            if joined:
                permuts.add(joined)
    return permuts

def generate_variants(infos, level):
    base = set()
    for word in infos:
        base.update([word, word.lower(), word.upper(), word.capitalize(), word[::-1]])
        base.update([word + "123", word + "!"])
        if level >= 3:
            base.update(generate_leet(word))

    if level >= 2:
        base.update(generate_mutations(base, use_symbols=(level >= 3), use_years=(level >= 3)))

    if level == 4:
        base.update(generate_permutations(infos))
        base.update(generate_mix(infos))

    return base

def filter_by_length(words, min_len, max_len):
    return {w for w in words if min_len <= len(w) <= max_len}

def save_wordlist(wordlist, path, name_base):
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, f"{name_base}_clear.txt")
    with open(file_path, "w") as f:
        for w in wordlist:
            f.write(w + "\n")
    console.print(f"[green bold]+[/green bold] Wordlist sauvegardée :\n  → {file_path}")

def get_strength_level(args):
    if args.max:
        return max
    elif args._3:
        return 3
    elif args._2:
        return 2
    elif args._1:
        return 1
    return max  # par défaut

def main():
    parser = argparse.ArgumentParser(
        prog="alpha",
        description="Générateur de wordlists personnalisé avec options avancées",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-1", dest="_1", action='store_true', help="Niveau 1 – Basique : mots simples, aucune mutation")
    parser.add_argument("-2", dest="_2", action='store_true', help="Niveau 2 – Mutations simples, suffixes")
    parser.add_argument("-3", dest="_3", action='store_true', help="Niveau 3 – Leet speak, mutations avancées")
    parser.add_argument("-max", dest="max", action='store_true', help="Niveau MAX – Tout activé (leet, permutations, mix...)")
    parser.add_argument("--path", type=str, default="./output", help="Chemin de destination (défaut : ./output)")
    parser.add_argument("--name", type=str, default="wordlist", help="Nom de base du fichier généré")

    args = parser.parse_args()
    header()

    level = get_strength_level(args)
    console.print(f"[bold yellow][*][/bold yellow] Génération niveau [cyan]{level}[/cyan]...\n")

    infos = []
    infos.append(Prompt.ask("Prénom"))
    infos.append(Prompt.ask("Nom"))
    infos.append(Prompt.ask("Surnom (optionnel)", default=""))
    infos.append(Prompt.ask("Date de naissance (JJMMAAAA)", default=""))
    infos.append(Prompt.ask("Ville"))
    postal = Prompt.ask("Code postal (optionnel, 5 chiffres)", default="")
    if postal.isdigit() and len(postal) == 5:
        infos.append(postal)
        infos.append(postal[:3])
        infos.append(postal[:2])
    infos.append(Prompt.ask("Nom d’animal (optionnel)", default=""))
    extra = Prompt.ask("Autres mots clés (séparés par virgules)", default="")
    if extra:
        infos += [w.strip() for w in extra.split(',') if w.strip()]
    infos = [i for i in infos if i]

    min_len = 6 if level < 4 else 4
    max_len = 14 if level < 4 else 20

    words = generate_variants(infos, level)
    words = filter_by_length(words, min_len, max_len)
    words = sorted(words)

    console.print(f"[blue]*[/blue] [bold]{len(words)}[/bold] mots générés entre {min_len} et {max_len} caractères")

    save_wordlist(words, args.path, args.name)

if __name__ == "__main__":
    main()
