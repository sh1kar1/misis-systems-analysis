import json
import math

def compute_membership(x, points):
    if x <= points[0][0]:
        return points[0][1]
    if x >= points[-1][0]:
        return points[-1][1]
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        if x1 <= x <= x2:
            if x1 == x2:
                return max(y1, y2)
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    
    return 0.0

def fuzzify(temperature, temp_membership_functions):
    degrees = {}
    for term in temp_membership_functions["температура"]:
        term_id = term["id"]
        points = term["points"]
        degrees[term_id] = compute_membership(temperature, points)
    return degrees

def apply_rules(activation_levels, rules, control_membership_functions, step=0.1):
    min_s = float('inf')
    max_s = float('-inf')
    
    for term in control_membership_functions["температура"]:
        points = term["points"]
        for point in points:
            min_s = min(min_s, point[0])
            max_s = max(max_s, point[0])
    
    fuzzy_sets = []
    
    for rule in rules:
        input_term = rule[0]
        output_term = rule[1]
        activation = activation_levels.get(input_term, 0)
        
        if activation > 0:
            output_points = None
            for term in control_membership_functions["температура"]:
                if term["id"] == output_term:
                    output_points = term["points"]
                    break
            
            if output_points:
                s_values = []
                mu_values = []
                
                current_s = min_s
                while current_s <= max_s:
                    mu_output = compute_membership(current_s, output_points)
                    mu_activated = min(activation, mu_output)
                    
                    s_values.append(current_s)
                    mu_values.append(mu_activated)
                    current_s += step
                
                fuzzy_sets.append((s_values, mu_values))
    
    return fuzzy_sets, min_s, max_s, step

def union_fuzzy_sets(fuzzy_sets):
    if not fuzzy_sets:
        return [], []
    
    s_values = fuzzy_sets[0][0]
    union_mu = [0] * len(s_values)    
    for i in range(len(s_values)):
        max_val = 0
        for s_vals, mu_vals in fuzzy_sets:
            if i < len(mu_vals):
                max_val = max(max_val, mu_vals[i])
        union_mu[i] = max_val
    
    return s_values, union_mu

def defuzzify_first_max(s_values, mu_values):
    if not mu_values:
        return 0.0
    max_mu = max(mu_values)
    for i, mu in enumerate(mu_values):
        if mu == max_mu:
            return s_values[i]
    
    return s_values[0]

def main(temp_mf_json, control_mf_json, rules_json, current_temperature):
    try:
        temp_mf = json.loads(temp_mf_json)
        control_mf = json.loads(control_mf_json)
        rules = json.loads(rules_json)
        
        activation_levels = fuzzify(current_temperature, temp_mf)
        
        fuzzy_sets, min_s, max_s, step = apply_rules(
            activation_levels, rules, control_mf
        )
        
        if fuzzy_sets:
            s_values, union_mu = union_fuzzy_sets(fuzzy_sets)
            optimal_control = defuzzify_first_max(s_values, union_mu)
            return round(optimal_control, 2)
        else:
            return 0.0
            
    except Exception as e:
        print(f"Ошибка при выполнении нечеткого управления: {e}")
        return 0.0

if __name__ == "__main__":
    temp_mf_json = '''
    {
        "температура": [
            {
                "id": "холодно",
                "points": [
                    [0, 1],
                    [18, 1],
                    [22, 0],
                    [50, 0]
                ]
            },
            {
                "id": "комфортно",
                "points": [
                    [18, 0],
                    [22, 1],
                    [24, 1],
                    [26, 0]
                ]
            },
            {
                "id": "жарко",
                "points": [
                    [0, 0],
                    [24, 0],
                    [26, 1],
                    [50, 1]
                ]
            }
        ]
    }
    '''
    
    control_mf_json = '''
    {
        "температура": [
            {
                "id": "интенсивно",
                "points": [
                    [0, 0],
                    [0, 1],
                    [5, 1],
                    [8, 0]
                ]
            },
            {
                "id": "умеренно",
                "points": [
                    [5, 0],
                    [8, 1],
                    [13, 1],
                    [16, 0]
                ]
            },
            {
                "id": "слабо",
                "points": [
                    [13, 0],
                    [18, 1],
                    [23, 1],
                    [26, 0]
                ]
            }
        ]
    }
    '''
    
    rules_json = '''
    [
        ["холодно", "интенсивно"],
        ["нормально", "умеренно"],
        ["жарко", "слабо"]
    ]
    '''
    
    test_temperatures = [16, 20, 25, 28]
    
    for temp in test_temperatures:
        result = main(temp_mf_json, control_mf_json, rules_json, temp)
        print(f"Температура: {temp}°C -> Оптимальное управление: {result}")
