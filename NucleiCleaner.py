import json
import sys

def clean_key(key):
    """Nettoie les clés en supprimant les espaces superflus."""
    return key.strip() if isinstance(key, str) else key

def clean_value(value):
    """Nettoie les valeurs de type chaîne de caractères."""
    if isinstance(value, str):
        return value.strip()
    return value

def normalize_language(lang):
    """Normalise le langage vers l'un des formats CodeForge acceptés."""
    lang = clean_value(lang).lower()
    if "python" in lang or "nuclei" in lang:
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

def normalize_severity(sev):
    """Normalise la sévérité en minuscules."""
    sev = clean_value(sev).lower()
    if sev in ["critical", "high", "medium", "low"]:
        return sev
    return "medium"  # Fallback

def clean_list(lst):
    """Nettoie une liste en supprimant les chaînes vides ou nulles."""
    if not isinstance(lst, list):
        return []
    return [clean_value(item) for item in lst if clean_value(item)]

def convert_parameters(params):
    """Convertit la liste des paramètres au format CodeForge."""
    if not isinstance(params, list):
        return []
    
    cleaned_params = []
    for p in params:
        p = {clean_key(k): clean_value(v) for k, v in p.items()}
        param_obj = {
            "name": p.get("name", "unknown"),
            "datatype": p.get("datatype", "string"),
            "required": bool(p.get("required", False)),
            "description": p.get("description", "")
        }
        
        # Le champ 'default' est optionnel
        if "default" in p and p["default"]:
            param_obj["default"] = str(p["default"])
        elif "default_value" in p and p["default_value"]:
            param_obj["default"] = str(p["default_value"])
            
        cleaned_params.append(param_obj)
    return cleaned_params

def convert_variables(variables):
    """Convertit la liste des variables globales au format CodeForge."""
    if not isinstance(variables, list):
        return []
    
    cleaned_vars = []
    for v in variables:
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

def convert_function(func):
    """Convertit un objet fonction individuel au format CodeForge."""
    # Nettoyer toutes les clés de l'objet fonction
    f = {clean_key(k): clean_value(v) for k, v in func.items()}
    
    # Extraction et nettoyage des CVEs et Tags
    cve_list = clean_list(f.get("cve", []))
    tags_list = clean_list(f.get("tags", []))
    
    # Construction de l'objet returns
    returns_data = f.get("returns", {})
    if isinstance(returns_data, dict):
        returns_obj = {
            "datatype": clean_value(returns_data.get("datatype", "Finding")),
            "description": clean_value(returns_data.get("description", ""))
        }
    else:
        returns_obj = {"datatype": "Finding", "description": ""}

    # Récupération du score CVSS (optionnel, doit être un nombre)
    cvss_score = f.get("cvss_score")
    try:
        cvss_score = float(cvss_score) if cvss_score is not None else None
    except (ValueError, TypeError):
        cvss_score = None

    # Construction de l'objet fonction final
    codeforge_func = {
        "id": f.get("id", ""),
        "name": f.get("name", ""),
        "language": normalize_language(f.get("language", "Nuclei/HTTP")),
        "famille": f.get("famille", "WebApp"),
        "description": f.get("description", ""),
        "severity": normalize_severity(f.get("severity", "medium")),
        "detection": f.get("detection", ""),
        "parameters": convert_parameters(f.get("parameters", [])),
        "returns": returns_obj,
        "source": f.get("source", ""),
        "source_original": f.get("source", "")
    }
    
    # Ajout des champs optionnels s'ils existent
    if cve_list:
        codeforge_func["cve"] = cve_list
    else:
        codeforge_func["cve"] = []
        
    if tags_list:
        codeforge_func["tags"] = tags_list
    else:
        codeforge_func["tags"] = []
        
    if cvss_score is not None:
        codeforge_func["cvss_score"] = cvss_score

    return codeforge_func

def main():
    input_file = "QwNuclei.json"
    output_file = "QwNuclei_CodeForge.json"
    
    print(f"Lecture du fichier source : {input_file} ...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{input_file}' est introuvable.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Erreur de format JSON : {e}")
        sys.exit(1)

    print("Conversion des données en cours...")
    
    # Conversion des variables
    variables_raw = data.get("variables", [])
    codeforge_variables = convert_variables(variables_raw)
    
    # Conversion des fonctions
    functions_raw = data.get("functions", [])
    codeforge_functions = [convert_function(func) for func in functions_raw]
    
    # Assemblage du résultat final
    output_data = {
        "functions": codeforge_functions,
        "variables": codeforge_variables
    }
    
    print(f"Écriture du fichier de sortie : {output_file} ...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print(f"Conversion terminée avec succès !")
    print(f" - {len(codeforge_functions)} fonctions converties.")
    print(f" - {len(codeforge_variables)} variables converties.")

if __name__ == "__main__":
    main()