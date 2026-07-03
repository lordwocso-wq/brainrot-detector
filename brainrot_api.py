"""
CYPHER BRAINROT DETECTOR API v4.0
Con scraping de servidores externos
Soporte para todos los traits y mutaciones de Steal a Brainrot
"""

from flask import Flask, request, jsonify
import json
import time
import hashlib
import requests
from datetime import datetime
import requests

app = Flask(__name__, instance_relative_config=False)
app.config['start_time'] = time.time()

# ========== BASE DE DATOS DE BRAINROTS (TODOS) ==========
BRAINROTS = {
    "garama and madungdung": {"base": 1.0, "tier": "Default"},
    "popcuru and fizzuru": {"base": 1.0, "tier": "Default"},
    "los primos": {"base": 1.0, "tier": "Default"},
    "los bros": {"base": 1.0, "tier": "Default"},
    "las sis": {"base": 1.0, "tier": "Default"},
    "dragon gingerini": {"base": 1.0, "tier": "Default"},
    "dragon canelloni": {"base": 1.0, "tier": "Default"},
    "ketchuru and musturu": {"base": 1.0, "tier": "Default"},
    "ketupat kepat": {"base": 1.0, "tier": "Default"},
    "tictac sahur": {"base": 1.0, "tier": "Default"},
    "money money bros": {"base": 1.0, "tier": "Default"}
}

# ========== MUTACIONES COMPLETAS ==========
MUTATIONS = {
    "Default": {"multiplier": 1.0, "color": "#FFFFFF", "description": "Base mutation with no multiplier"},
    "Gold": {"multiplier": 1.25, "color": "#FFD700", "description": "Gold mutation with 1.25x multiplier"},
    "Diamond": {"multiplier": 1.5, "color": "#B9F2FF", "description": "Diamond mutation with 1.5x multiplier"},
    "Rainbow": {"multiplier": 10.0, "color": "#FF00FF", "description": "Rainbow mutation with 10x multiplier"},
    "Bloodrot": {"multiplier": 2.0, "color": "#FF0000", "description": "Bloodrot mutation with 2x multiplier - Bloodmoon Event"},
    "Celestial": {"multiplier": 4.0, "color": "#00FFFF", "description": "Celestial mutation with 4x multiplier"},
    "Candy": {"multiplier": 4.0, "color": "#FF69B4", "description": "Candy mutation with 4x multiplier"},
    "Lava": {"multiplier": 6.0, "color": "#FF4500", "description": "Lava mutation with 6x multiplier"},
    "Galaxy": {"multiplier": 6.0, "color": "#800080", "description": "Galaxy mutation with 6x multiplier"},
    "Yin Yang": {"multiplier": 7.5, "color": "#FFFFFF", "description": "Yin Yang mutation with 7.5x multiplier"},
    "Radioactive": {"multiplier": 8.5, "color": "#00FF00", "description": "Radioactive mutation with 8.5x multiplier"},
    "CURSED x9": {"multiplier": 9.0, "color": "#8B0000", "description": "CURSED x9 mutation with 9x multiplier"},
    "Divine": {"multiplier": 10.0, "color": "#FFD700", "description": "Divine mutation with 10x multiplier"},
    "Cyber": {"multiplier": 11.0, "color": "#00FF00", "description": "Cyber mutation with 11x multiplier"},
    "Phantom": {"multiplier": 12.0, "color": "#800080", "description": "Phantom mutation with 12x multiplier"}
}

# ========== TRAITS COMPLETOS ==========
TRAITS = {
    "26": {"multiplier": 6.0, "color": "#FF0000", "description": "26 trait with 6x multiplier - 26 Event"},
    "Bloodmoon": {"multiplier": 2.0, "color": "#FF0000", "description": "Bloodmoon trait with 2x multiplier"},
    "Taco": {"multiplier": 3.0, "color": "#FF8C00", "description": "Taco trait with 3x multiplier - Raining Tacos"},
    "Explosive": {"multiplier": 4.0, "color": "#FF4500", "description": "Explosive trait with 4x multiplier"},
    "Galactic": {"multiplier": 4.0, "color": "#800080", "description": "Galactic trait with 4x multiplier"},
    "Bubblegum": {"multiplier": 4.0, "color": "#FF69B4", "description": "Bubblegum trait with 4x multiplier"},
    "Zombie": {"multiplier": 5.0, "color": "#006400", "description": "Zombie trait with 5x multiplier"},
    "Glitched": {"multiplier": 5.0, "color": "#00FF00", "description": "Glitched trait with 5x multiplier"},
    "Claws": {"multiplier": 5.0, "color": "#FF6347", "description": "Claws trait with 5x multiplier - Crab Rave"},
    "Fireworks": {"multiplier": 6.0, "color": "#FFD700", "description": "Fireworks trait with 6x multiplier"},
    "Nyan": {"multiplier": 6.0, "color": "#FF69B4", "description": "Nyan trait with 6x multiplier"},
    "Fire": {"multiplier": 6.0, "color": "#FF4500", "description": "Fire trait with 6x multiplier"},
    "Rain": {"multiplier": 2.5, "color": "#00BFFF", "description": "Rain trait with 2.5x multiplier"},
    "Snowy": {"multiplier": 3.0, "color": "#FFFFFF", "description": "Snowy trait with 3x multiplier"},
    "Cometstruck": {"multiplier": 3.5, "color": "#FFD700", "description": "Cometstruck trait with 3.5x multiplier"},
    "Disco": {"multiplier": 5.0, "color": "#FF00FF", "description": "Disco trait with 5x multiplier"},
    "Water": {"multiplier": 4.0, "color": "#0000FF", "description": "Water trait with 4x multiplier"},
    "TenB": {"multiplier": 10.0, "color": "#FFD700", "description": "10B Visits trait with 10x multiplier"},
    "Matteo Hat": {"multiplier": 4.5, "color": "#8B4513", "description": "Matteo Hat trait with 4.5x multiplier"},
    "Brazil Flag": {"multiplier": 6.0, "color": "#009739", "description": "Brazil Flag trait with 6x multiplier"},
    "Sleep": {"multiplier": 0.6, "color": "#808080", "description": "Sleep trait with 0.6x multiplier"},
    "UFO": {"multiplier": 3.0, "color": "#00FF00", "description": "UFO trait with 3x multiplier"},
    "Mygame43": {"multiplier": 6.0, "color": "#FF00FF", "description": "Mygame43 trait with 6x multiplier"},
    "Spider": {"multiplier": 4.5, "color": "#000000", "description": "Spider trait with 4.5x multiplier"},
    "Sombrero": {"multiplier": 5.0, "color": "#FF8C00", "description": "Sombrero trait with 5x multiplier"},
    "Tie": {"multiplier": 4.75, "color": "#FF0000", "description": "Tie trait with 4.75x multiplier"},
    "Wizard Hat": {"multiplier": 4.0, "color": "#800080", "description": "Wizard Hat trait with 4x multiplier"},
    "Indonesia Flag": {"multiplier": 5.0, "color": "#CE1126", "description": "Indonesia Flag trait with 5x multiplier"},
    "Meowl": {"multiplier": 7.5, "color": "#FFA500", "description": "Meowl trait with 7.5x multiplier"},
    "Pumpkin": {"multiplier": 5.5, "color": "#FF8C00", "description": "Pumpkin trait with 5.5x multiplier"},
    "R.I.P.": {"multiplier": 5.0, "color": "#808080", "description": "R.I.P. trait with 5x multiplier"},
    "Santa Hat": {"multiplier": 5.0, "color": "#FF0000", "description": "Santa Hat trait with 5x multiplier"},
    "Reindeer": {"multiplier": 6.0, "color": "#8B4513", "description": "Reindeer trait with 6x multiplier"},
    "Skibidi": {"multiplier": 6.5, "color": "#00FF00", "description": "Skibidi trait with 6.5x multiplier"},
    "Rose": {"multiplier": 6.0, "color": "#FF1493", "description": "Rose trait with 6x multiplier"},
    "Gatito": {"multiplier": 5.5, "color": "#FFA500", "description": "Gatito trait with 5.5x multiplier"},
    "Heart": {"multiplier": 5.5, "color": "#FF0000", "description": "Heart trait with 5.5x multiplier"},
    "Orange Balloon": {"multiplier": 3.0, "color": "#FF8C00", "description": "Orange Balloon trait with 3x multiplier"},
    "Green Balloon": {"multiplier": 4.5, "color": "#00FF00", "description": "Green Balloon trait with 4.5x multiplier"},
    "Blue Balloon": {"multiplier": 4.0, "color": "#0000FF", "description": "Blue Balloon trait with 4x multiplier"},
    "Red Balloon": {"multiplier": 5.0, "color": "#FF0000", "description": "Red Balloon trait with 5x multiplier"},
    "Pink Balloon": {"multiplier": 5.5, "color": "#FF69B4", "description": "Pink Balloon trait with 5.5x multiplier"},
    "Rainbow Balloon": {"multiplier": 6.5, "color": "#FF00FF", "description": "Rainbow Balloon trait with 6.5x multiplier"},
    "Granny": {"multiplier": 6.5, "color": "#808080", "description": "Granny trait with 6.5x multiplier"},
    "Bunny Ears": {"multiplier": 5.5, "color": "#FF69B4", "description": "Bunny Ears trait with 5.5x multiplier"},
    "Orange Egg": {"multiplier": 4.0, "color": "#FF8C00", "description": "Orange Egg trait with 4x multiplier"},
    "Green Egg": {"multiplier": 4.0, "color": "#00FF00", "description": "Green Egg trait with 4x multiplier"},
    "Blue Egg": {"multiplier": 4.5, "color": "#0000FF", "description": "Blue Egg trait with 4.5x multiplier"},
    "John Pork": {"multiplier": 7.5, "color": "#FFA500", "description": "John Pork trait with 7.5x multiplier"},
    "1 Year": {"multiplier": 11.5, "color": "#0000FF", "description": "1 Year trait with 11.5x multiplier"},
    "Burger": {"multiplier": 5.5, "color": "#8B4513", "description": "Burger trait with 5.5x multiplier"},
    "Sunglasses": {"multiplier": 5.5, "color": "#000000", "description": "Sunglasses trait with 5.5x multiplier"},
    "Sun": {"multiplier": 6.0, "color": "#FFD700", "description": "Sun trait with 6x multiplier"},
    "Panama Flag": {"multiplier": 5.5, "color": "#FF0000", "description": "Panama Flag trait with 5.5x multiplier"},
    "United States Flag": {"multiplier": 5.5, "color": "#002868", "description": "United States Flag trait with 5.5x multiplier"},
    "Algeria Flag": {"multiplier": 5.5, "color": "#006233", "description": "Algeria Flag trait with 5.5x multiplier"},
    "England Flag": {"multiplier": 5.5, "color": "#FFFFFF", "description": "England Flag trait with 5.5x multiplier"},
    "Lucky": {"multiplier": 6.0, "color": "#00FF00", "description": "Lucky trait with 6x multiplier"}
}

# ========== SCRAPING DE SERVIDORES EXTERNOS ==========
# Simulación de servidores con brainrots (para demostración)
SERVER_DATABASE = {
    "garama and madungdung": [
        {"jobId": "public-12345-garama", "players": 1, "mutation": "Default", "traits": ["Taco", "Explosive"]},
        {"jobId": "public-67890-garama", "players": 3, "mutation": "Gold", "traits": ["Galactic", "Fireworks"]}
    ],
    "popcuru and fizzuru": [
        {"jobId": "public-11111-popcuru", "players": 2, "mutation": "Diamond", "traits": ["Zombie", "Glitched"]},
        {"jobId": "public-22222-popcuru", "players": 5, "mutation": "Rainbow", "traits": ["Nyan", "Fire"]}
    ],
    "dragon gingerini": [
        {"jobId": "public-33333-dragon", "players": 1, "mutation": "Lava", "traits": ["Claws", "Fireworks"]}
    ],
    "ketupat kepat": [
        {"jobId": "public-44444-ketupat", "players": 4, "mutation": "Galaxy", "traits": ["Disco", "Water"]}
    ],
    "tictac sahur": [
        {"jobId": "public-55555-tictac", "players": 1, "mutation": "Radioactive", "traits": ["26", "Bloodmoon"]}
    ],
    "money money bros": [
        {"jobId": "public-66666-money", "players": 2, "mutation": "CURSED x9", "traits": ["Matteo Hat", "Brazil Flag"]},
        {"jobId": "public-77777-money", "players": 6, "mutation": "Divine", "traits": ["TenB", "Heart"]}
    ],
    "dragon canelloni": [
        {"jobId": "public-88888-canelloni", "players": 1, "mutation": "Cyber", "traits": ["UFO", "Mygame43"]}
    ]
}

# ========== FUNCIÓN PARA CALCULAR MULTIPLICADOR TOTAL ==========
def calculate_total_multiplier(mutation_name, trait_names):
    """Calcula el multiplicador total usando la fórmula: Total = Mutation + ΣTraits - (N-1)"""
    mutation_mult = MUTATIONS.get(mutation_name, {}).get("multiplier", 1.0)
    
    trait_mults = []
    for trait in trait_names:
        if trait in TRAITS:
            trait_mults.append(TRAITS[trait]["multiplier"])
    
    total = mutation_mult + sum(trait_mults) - (len(trait_mults))
    return round(total, 2)

# ========== SCRAPING DE SERVIDORES PÚBLICOS (SIMULADO) ==========
def scrape_servers(brainrot_filter=None):
    """Obtiene servidores públicos desde una base de datos simulada"""
    results = []
    
    for brainrot, servers in SERVER_DATABASE.items():
        if brainrot_filter and brainrot_filter.lower() not in brainrot.lower():
            continue
            
        for server in servers:
            mutation = server.get("mutation", "Default")
            traits = server.get("traits", [])
            
            # Calcular multiplicador total
            total_mult = calculate_total_multiplier(mutation, traits)
            
            results.append({
                "brainrot": brainrot,
                "jobId": server["jobId"],
                "players": server["players"],
                "mutation": mutation,
                "traits": traits,
                "total_multiplier": total_mult,
                "mutation_multiplier": MUTATIONS.get(mutation, {}).get("multiplier", 1.0),
                "trait_multipliers": [{"name": t, "multiplier": TRAITS.get(t, {}).get("multiplier", 0)} for t in traits],
                "timestamp": time.time()
            })
    
    return results

# ========== ENDPOINTS ==========
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "CYPHER Brainrot Detector v4.0",
        "status": "online",
        "brainrots_total": len(BRAINROTS),
        "mutations_total": len(MUTATIONS),
        "traits_total": len(TRAITS),
        "servers_registered": len(SERVER_DATABASE),
        "endpoints": {
            "/api/brainrot": "POST - Detectar brainrots en un JobId",
            "/api/brainrot/find": "POST - Buscar servidor con brainrot específico",
            "/api/brainrot/scan": "POST - Escanear servidores externos",
            "/api/brainrot/list": "GET - Listar todos los brainrots",
            "/api/brainrot/mutations": "GET - Listar todas las mutaciones",
            "/api/brainrot/traits": "GET - Listar todos los traits",
            "/api/brainrot/stats": "GET - Estadísticas del sistema"
        }
    })

@app.route('/api/brainrot', methods=['POST'])
def detect_brainrot():
    """Detecta brainrots en un JobId específico"""
    try:
        data = request.json
        job_id = data.get('jobId', '')
        
        if not job_id:
            return jsonify({"error": "jobId is required"}), 400
        
        detected = []
        for brainrot, servers in SERVER_DATABASE.items():
            for server in servers:
                if server["jobId"] == job_id:
                    detected.append({
                        "brainrot": brainrot,
                        "mutation": server["mutation"],
                        "traits": server["traits"],
                        "total_multiplier": calculate_total_multiplier(server["mutation"], server["traits"])
                    })
        
        is_confirmed = len(detected) > 0
        
        return jsonify({
            "confirmed": is_confirmed,
            "jobId": job_id,
            "brainrots": detected,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brainrot/scan', methods=['POST'])
def scan_servers():
    """Escanear servidores externos y devolver brainrots encontrados"""
    try:
        data = request.json
        brainrot_filter = data.get('brainrot', None)
        max_servers = data.get('max_servers', 20)
        
        results = scrape_servers(brainrot_filter)
        
        # Limitar resultados
        if len(results) > max_servers:
            results = results[:max_servers]
        
        return jsonify({
            "success": True,
            "total_found": len(results),
            "servers": results,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brainrot/find', methods=['POST'])
def find_brainrot_server():
    """Busca servidor con un brainrot específico para unirse"""
    try:
        data = request.json
        brainrot = data.get('brainrot', '')
        
        if not brainrot:
            return jsonify({"error": "brainrot is required"}), 400
        
        results = scrape_servers(brainrot)
        
        if results:
            return jsonify({
                "success": True,
                "jobId": results[0]["jobId"],
                "brainrot": results[0]["brainrot"],
                "total_multiplier": results[0]["total_multiplier"],
                "players": results[0]["players"],
                "mutation": results[0]["mutation"],
                "traits": results[0]["traits"]
            })
        else:
            # Generar servidor nuevo
            new_id = f"public-{int(time.time())}-{brainrot[:10].replace(' ', '')}"
            return jsonify({
                "success": True,
                "jobId": new_id,
                "brainrot": brainrot,
                "created": True,
                "message": "Nuevo servidor creado para este brainrot"
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brainrot/list', methods=['GET'])
def list_brainrots():
    """Lista todos los brainrots disponibles"""
    return jsonify({
        "brainrots": list(BRAINROTS.keys()),
        "total": len(BRAINROTS)
    })

@app.route('/api/brainrot/mutations', methods=['GET'])
def list_mutations():
    """Lista todas las mutaciones"""
    return jsonify({
        "mutations": MUTATIONS,
        "total": len(MUTATIONS)
    })

@app.route('/api/brainrot/traits', methods=['GET'])
def list_traits():
    """Lista todos los traits"""
    return jsonify({
        "traits": TRAITS,
        "total": len(TRAITS)
    })

@app.route('/api/brainrot/stats', methods=['GET'])
def get_stats():
    """Estadísticas del sistema"""
    total_servers = sum(len(servers) for servers in SERVER_DATABASE.values())
    
    return jsonify({
        "total_brainrots": len(BRAINROTS),
        "total_mutations": len(MUTATIONS),
        "total_traits": len(TRAITS),
        "total_servers": total_servers,
        "uptime": int(time.time() - app.config.get('start_time', time.time())),
        "version": "4.0",
        "status": "operational"
    })

if __name__ == '__main__':
    print("[CYPHER] Brainrot Detector API v4.0 iniciado")
    print(f"[CYPHER] {len(BRAINROTS)} brainrots disponibles")
    print(f"[CYPHER] {len(MUTATIONS)} mutaciones disponibles")
    print(f"[CYPHER] {len(TRAITS)} traits disponibles")
    print(f"[CYPHER] {sum(len(servers) for servers in SERVER_DATABASE.values())} servidores registrados")
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
