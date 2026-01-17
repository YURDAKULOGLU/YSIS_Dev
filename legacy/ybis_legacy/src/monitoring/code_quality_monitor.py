import os
import ast
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def check_for_regressions(file, code_complexity, previous_complexity) -> dict:
    """
    Kod karmaklk metriklerinde gerilemeleri kontrol eder.

    Args:
        file (str): Dosya ad
        code_complexity (dict): Mevcut kod karmakl bilgileri
        previous_complexity (dict): nceki kod karmakl bilgileri

    Returns:
        dict: Gerileme varsa detaylar ieren bir szlk, yoksa bo bir szlk dndrr.
    """
    regression_details = {}
    if code_complexity['lines'] > previous_complexity['lines']:
        regression_details['lines'] = f"Satrlar: {code_complexity['lines']} (nceki: {previous_complexity['lines']})"
    if code_complexity['functions'] > previous_complexity['functions']:
        regression_details['functions'] = f"Fonksiyonlar: {code_complexity['functions']} (nceki: {previous_complexity['functions']})"
    if code_complexity['classes'] > previous_complexity['classes']:
        regression_details['classes'] = f"Snflar: {code_complexity['classes']} (nceki: {previous_complexity['classes']})"

    if regression_details:
        logging.warning(f"{file} dosyasnda gerileme algland:\n" + "\n".join([f"  - {detail}" for detail in regression_details.values()]))
        return regression_details
    return {}

def monitor_code_quality(directory_path):
    """
    Monitor key metrics for AI code quality in all Python files within the given directory.
    Key metrics include: lines of code, number of functions, and number of classes.
    """
    logging.info("Starting code quality monitoring...")

    # Load previous complexity data if it exists
    history_file = os.path.join(directory_path, 'code_complexity_history.json')
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
    except FileNotFoundError:
        history_data = {}

    # Iterate over all Python files in the directory
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    logging.error(f"Failed to read file {file_path}: {str(e)}", exc_info=True)
                    continue
                tree = ast.parse(content)
                code_complexity = {
                    "lines": len(content.splitlines()),
                    "functions": sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)),
                    "classes": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
                }
                logging.info(f"Parsing file: {file_path}")
                logging.info(f"Code Complexity of {file}: Lines={code_complexity['lines']}, Functions={code_complexity['functions']}, Classes={code_complexity['classes']}")

                # Check for regressions
                regression_details = {}
                if file in history_data:
                    previous_complexity = history_data[file]
                    regression_details = check_for_regressions(file, code_complexity, previous_complexity)

                # Update history data
                history_data[file] = code_complexity

                # Log regression detection result
                if regression_details:
                    logging.warning(f"Regression detected in {file}:\n" + "\n".join([f"  - {detail}" for detail in regression_details.values()]))
                else:
                    logging.info(f"No regression detected in {file}. Complexity remains the same.")

                # Update history data
                history_data[file] = code_complexity

    # Save updated complexity data
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to write history file {history_file}: {str(e)}", exc_info=True)
