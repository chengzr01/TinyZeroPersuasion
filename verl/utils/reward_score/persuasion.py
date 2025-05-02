import requests

def extract_response(solution_str):
    return solution_str.split("<argument>")[1].split("</argument>")[0]

def get_updated_belief(response, claim, initial_belief):
    url = "http://localhost:15000/static"
    payload = {
        "claim": claim,
        "initial_belief": initial_belief,
        "response": response,
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("receiver", "")
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def compute_belief_difference(updated_belief, initial_belief):
    return len(updated_belief) - len(initial_belief)

def compute_score(solution_str, claim, initial_belief):
    """
    The scoring function for persuasion task.
    """
    response = extract_response(solution_str)
    updated_belief = get_updated_belief(response, claim, initial_belief)
    score = compute_belief_difference(updated_belief, initial_belief)
    
    return score