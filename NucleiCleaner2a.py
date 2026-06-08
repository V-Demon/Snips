import json
import sys
import argparse
import os
from collections import Counter
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

console = Console()

# ==============================================================================
# FONCTIONS DE NETTOYAGE ET NORMALISATION
# ==============================================================================

def clean_key(key):
    return key.strip() if isinstance(key, str) else key

def clean_value(value):
    if isinstance(value, str):
        return value.strip()
    return value

def normalize_language(lang, force_lang=None):
    if force_lang:
        return force_lang
    
    lang = clean_value(lang).strip().lower()
    if "python" in lang or "nuclei" in lang or "http" in lang:
        return "Python"
    elif "csharp" in lang or "c#" in lang:
        return "CSharp"
    elif "javascript" in lang or "js" in lang:
        return "JavaScript"
    elif "powershell" in lang or "ps" in lang:
        return "PowerShell"
    elif "bash" in lang or "sh" in lang:
        return "Bash"
    return "Python"  # Fallback par défaut

def normalize_severity(sev, min_severity="low"):
    sev = clean_value(sev).strip().lower()
    severity_levels = ["critical", "high", "medium", "low"]
    
    if sev in severity_levels:
        # Vérifier le filtre de sévérité minimale
        if severity_levels.index(sev) > severity_levels.index(min_severity):
            return None  # Sera filtré
        return sev
    return "medium" if severity_levels.index("medium") <= severity_levels.index(min_severity) else None

def clean_list(lst):
    if not isinstance(lst, list):
        return []
    return [clean_value(item) for item in lst if clean_value(item)]

def convert_parameters(params):
    if not isinstance(params, list):
        return []
    cleaned_params = []
    for p in params:
        if not isinstance(p, dict): continue
        p = {clean_key(k): clean_value(v) for k, v in p.items()}
        param_obj = {
            "name": p.get("name", "unknown"),
            "datatype": p.get("datatype", "string"),
            "required": bool(p.get("required", False)),
            "description": p.get("description", "")
        }
        if "default" in p and p["default"]:
            param_obj["default"] = str(p["default"])
        elif "default_value" in p and p["default_value"]:
            param_obj["default"] = str(p["default_value"])
        cleaned_params.append(param_obj)
    return cleaned_params

def convert_variables(variables):
    if not isinstance(variables, list):
        return []
    cleaned_vars = []
    for v in variables:
        if not isinstance(v, dict): continue
        v = {clean_key(k): clean_value(val) for k, val in v.items()}
        var_obj = {
            "id": v.get("id", ""),
            "name": v.get("name", ""),
            "datatype": v.get("datatype", "string"),
            "description": v.get("description", "")
        }
        if "default_value" in v and v["default_value"]:
            var_obj["default"] = str(v["default_value"])
        cleaned_vars.append(var_obj)
    return cleaned_vars

def convert_function(func, args, stats):
    f = {clean_key(k): clean_value(v) for k, v in func.items() if isinstance(func, dict)}
    
    # Normalisation avec prise en compte des options de bidouillage
    severity = normalize_severity(f.get("severity", "medium"), args.min_severity)
    if severity is None:
        stats['filtered_out'] += 1
        return None # Filtré
        
    stats['severities'][severity] += 1
    
    language = normalize_language(f.get("language", "Nuclei/HTTP"), args.force_lang)
    stats['languages'][language] += 1

    cve_list = clean_list(f.get("cve", []))
    tags_list = clean_list(f.get("tags", []))
    
    # Ajout du tag personnalisé si demandé
    if args.add_tag and args.add_tag not in tags_list:
        tags_list.append(args.add_tag)

    returns_data = f.get("returns", {})
    returns_obj = {
        "datatype": clean_value(returns_data.get("datatype", "Finding")) if isinstance(returns_data, dict) else "Finding",
        "description": clean_value(returns_data.get("description", "")) if isinstance(returns_data, dict) else ""
    }

    cvss_score = f.get("cvss_score")
    try:
        cvss_score = float(cvss_score) if cvss_score is not None else None
    except (ValueError, TypeError):
        cvss_score = None

    codeforge_func = {
        "id": f.get("id", ""),
        "name": f.get("name", ""),
        "language": language,
        "famille": f.get("famille", "WebApp"),
        "description": f.get("description", ""),
        "severity": severity,
        "detection": f.get("detection", ""),
        "parameters": convert_parameters(f.get("parameters", [])),
        "returns": returns_obj,
        "source": f.get("source", ""),
        "source_original": f.get("source", ""),
        "cve": cve_list if cve_list else [],
        "tags": tags_list if tags_list else []
    }
    
    if cvss_score is not None:
        codeforge_func["cvss_score"] = cvss_score

    return codeforge_func

# ==============================================================================
# LOGIQUE PRINCIPALE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🛠️ NucleiCleaner Pro : Nettoie et normalise les JSON Nuclei pour CodeForge.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-i", "--input", default="QwNuclei.json", help="Fichier JSON source (défaut: QwNuclei.json)")
    parser.add_argument("-o", "--output", default="QwNuclei_CodeForge.json", help="Fichier JSON de sortie (défaut: QwNuclei_CodeForge.json)")
    parser.add_argument("--min-severity", choices=["low", "medium", "high", "critical"], default="low", 
                        help="Sévérité minimale à conserver (défaut: low)")
    parser.add_argument("--force-lang", choices=["Python", "CSharp", "JavaScript", "PowerShell", "Bash"], 
                        help="Force toutes les fonctions dans ce langage")
    parser.add_argument("--add-tag", help="Ajoute un tag personnalisé à toutes les fonctions")
    parser.add_argument("--dry-run", action="store_true", help="Mode test : ne pas écrire le fichier de sortie")

    args = parser.parse_args()

    console.print(Panel.fit(
        "[bold cyan]🚀 NucleiCleaner PRO[/bold cyan]\n"
        f"Source: [yellow]{args.input}[/yellow] | Cible: [green]{args.output}[/green]\n"
        f"Options: Min Severity=[magenta]{args.min_severity}[/magenta]" + 
        (f" | Force Lang=[blue]{args.force_lang}[/blue]" if args.force_lang else "") +
        (f" | Add Tag=[green]{args.add_tag}[/green]" if args.add_tag else ""),
        border_style="cyan"
    ))

    if not os.path.exists(args.input):
        console.print(f"[bold red]❌ Erreur : Le fichier '{args.input}' est introuvable.[/bold red]")
        sys.exit(1)

    console.print("[dim]Lecture du fichier source...[/dim]")
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[bold red]❌ Erreur de format JSON : {e}[/bold red]")
        sys.exit(1)

    variables_raw = data.get("variables", [])
    functions_raw = data.get("functions", [])
    
    console.print(f"[dim]Found {len(variables_raw)} variables and {len(functions_raw)} functions.[/dim]")

    stats = {
        'filtered_out': 0,
        'languages': Counter(),
        'severities': Counter()
    }

    codeforge_variables = convert_variables(variables_raw)
    codeforge_functions = []

    # Barre de progression stylée
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Conversion des fonctions...", total=len(functions_raw))
        
        for func in functions_raw:
            result = convert_function(func, args, stats)
            if result:
                codeforge_functions.append(result)
            progress.advance(task)

    output_data = {
        "functions": codeforge_functions,
        "variables": codeforge_variables
    }

    # Affichage des statistiques
    table = Table(title="📊 Statistiques de Conversion", show_header=True, header_style="bold magenta")
    table.add_column("Métrique", style="cyan")
    table.add_column("Valeur", justify="right")
    
    table.add_row("Variables converties", str(len(codeforge_variables)))
    table.add_row("Fonctions converties", f"[green]{len(codeforge_functions)}[/green]")
    table.add_row("Fonctions filtrées (sévérité)", f"[yellow]{stats['filtered_out']}[/yellow]")
    
    table.add_section()
    table.add_row("[bold]Répartition Langages[/bold]", "")
    for lang, count in stats['languages'].most_common():
        table.add_row(f"  {lang}", str(count))
        
    table.add_section()
    table.add_row("[bold]Répartition Sévérités[/bold]", "")
    for sev in ["critical", "high", "medium", "low"]:
        if stats['severities'][sev] > 0:
            color = "red" if sev == "critical" else "orange1" if sev == "high" else "yellow" if sev == "medium" else "green"
            table.add_row(f"  [{color}]{sev.upper()}[/{color}]", str(stats['severities'][sev]))

    console.print(table)

    if args.dry_run:
        console.print("[bold yellow]⚠️ DRY-RUN ACTIVÉ : Aucun fichier n'a été écrit.[/bold yellow]")
    else:
        console.print(f"[dim]Écriture du fichier de sortie : {args.output}...[/dim]")
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        console.print("[bold green]✅ Conversion terminée avec succès ![/bold green]")

if __name__ == "__main__":
    main()