y = {
    "name": "Artem",
    "role": "KIng",
    "stats":{
        "HP": 100,
        "Mana": 50
    }
}

x = [f"{key}: {y[key]}"for key in ["name","role", y["stats"]]]
