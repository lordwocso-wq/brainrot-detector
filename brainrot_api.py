"""
CYPHER BRAINROT DETECTOR API v3.1
Compatible con Python 3.14+
"""

import sys
import os
import json
import time
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify

# ========== CONFIGURACIÓN INICIAL ==========
# Fix para Python 3.14 - definir manualmente el path
app = Flask(__name__, instance_relative_config=False)
app.config['start_time'] = time.time()

# ========== LISTA DE BRAINROTS ==========
BRAINROTS = [
    "garama and madungdung",
    "popcuru and fizzuru",
    "los primos",
    "los bros",
    "las sis",
    "dragon gingerini",
    "dragon canelloni",
    "ketchuru and musturu",
    "ketupat kepat",
    "tictac sahur",
    "money money bros"
]

# Base de datos de servidores con brainrots
SERVER_DATABASE = {
    "garama and madungdung": [
        "public-12345-garama",
        "public-67890-garama",
        "public-11223-garama"
    ],
    "popcuru and fizzuru": [
        "public-11111-popcuru",
        "public-22222-popcuru",
        "public-33333-popcuru"
    ],
    "los primos": [
        "public-44444-primos",
        "public-55555-primos"
    ],
    "los bros": [
        "public-66666-bros"
    ],
    "las sis": [
        "public-77777-sis"
    ],
    "dragon gingerini": [
        "public-88888-gingerini",
        "public-99999-gingerini"
    ],
    "dragon canelloni": [
        "public-10101-canelloni"
    ],
    "ketchuru and musturu": [
        "public-12121-ketchuru",
        "public-13131-musturu"
    ],
    "ketupat kepat": [
        "public-14141-ketupat",
        "public-15151-ketupat"
    ],
    "tictac sahur": [
        "public-16161-tictac"
    ],
    "money money bros": [
        "public-17171-money",
        "public-18181-money"
    ]
}

# ========== FUNCIONES DE DETECCIÓN ==========
def detect_brainrot_method1(job_id):
    """Método 1: Búsqueda directa"""
    detected = []
    job_id_lower = job_id.lower()
    for br in BRAINROTS:
        if br.lower() in job_id_lower:
            detected.append(br)
    return detected

def detect_brainrot_method2(job_id):
    """Método 2: Base de datos"""
    detected = []
    for br, servers in SERVER_DATABASE.items():
        for server in servers:
            if server in job_id:
                detected.append(br)
                break
    return detected

def detect_brainrot_method3(job_id):
    """Método 3: Hash"""
    detected = []
    job_hash = hash(job_id) % 10000
    
    hash_map = {
        42: "garama and madungdung",
        73: "popcuru and fizzuru",
        128: "dragon gingerini",
        256: "ketupat kepat",
        512: "money money bros",
        777: "tictac sahur",
        999: "dragon canelloni",
        1337: "ketchuru and musturu"
    }
    
    for h, br in hash_map.items():
        if job_hash == h or job_hash % h == 0:
            detected.append(br)
    
    return detected

def detect_brainrot_method4(job_id, cypher_id):
    """Método 4: CypherID"""
    detected = []
    if not cypher_id:
        return detected
    
    for br in BRAINROTS:
        if br.replace(" ", "") in cypher_id.lower().replace("-", ""):
            detected.append(br)
    
    return detected

def detect_brainrot_method5(job_id):
    """Método 5: Patrones temporales"""
    detected = []
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    
    if hour == 3 and minute == 33:
        detected.append("dragon gingerini")
    if hour == 7 and minute == 7:
        detected.append("money money bros")
    if hour == 12 and minute == 0:
        detected.append("tictac sahur")
    if hour == 21 and minute == 21:
        detected.append("ketupat kepat")
    
    day = current_time.day
    if day % 5 == 0:
        detected.append("popcuru and fizzuru")
    if day % 7 == 0:
        detected.append("los primos")
    
    return detected

# ========== ENDPOINTS ==========
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "CYPHER Brainrot Detector",
        "version": "3.1",
        "status": "online",
        "endpoints": {
            "/api/brainrot": "POST - Detectar brainrots",
            "/api/brainrot/find": "POST - Buscar servidor",
            "/api/cypher/jobid": "POST - Generar CypherJobId",
            "/api/brainrot/list": "GET - Listar brainrots"
        },
        "timestamp": time.time()
    })

@app.route('/api/brainrot', methods=['POST'])
def detect_brainrot():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        job_id = data.get('jobId', '')
        cypher_id = data.get('cypherId', '')
        
        if not job_id:
            return jsonify({"error": "jobId is required"}), 400
        
        detected = []
        confidence = 0
        
        # Método 1
        m1 = detect_brainrot_method1(job_id)
        detected.extend(m1)
        confidence += len(m1) * 20
        
        # Método 2
        m2 = detect_brainrot_method2(job_id)
        detected.extend(m2)
        confidence += len(m2) * 25
        
        # Método 3
        m3 = detect_brainrot_method3(job_id)
        detected.extend(m3)
        confidence += len(m3) * 15
        
        # Método 4
        m4 = detect_brainrot_method4(job_id, cypher_id)
        detected.extend(m4)
        confidence += len(m4) * 30
        
        # Método 5
        m5 = detect_brainrot_method5(job_id)
        detected.extend(m5)
        confidence += len(m5) * 10
        
        detected = list(set(detected))
        confidence = min(confidence, 1000)
        confidence_percent = confidence / 10
        
        is_confirmed = confidence_percent >= 70 and len(detected) > 0
        
        return jsonify({
            "confirmed": is_confirmed,
            "brainrots": detected,
            "confidence": confidence_percent,
            "methods_used": {
                "direct_match": len(m1) > 0,
                "database": len(m2) > 0,
                "hash": len(m3) > 0,
                "cypher_id": len(m4) > 0,
                "temporal": len(m5) > 0
            },
            "total_brainrots_found": len(detected),
            "timestamp": time.time(),
            "job_id_checked": job_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brainrot/find', methods=['POST'])
def find_brainrot_server():
    try:
        data = request.json
        brainrot = data.get('brainrot', '')
        server_type = data.get('type', 'public')
        
        if not brainrot:
            return jsonify({"error": "brainrot is required"}), 400
        
        found_servers = []
        for br, servers in SERVER_DATABASE.items():
            if brainrot.lower() in br.lower():
                found_servers.extend(servers)
        
        if found_servers:
            return jsonify({
                "success": True,
                "jobId": found_servers[0],
                "type": server_type,
                "brainrot": brainrot,
                "servers_available": len(found_servers)
            })
        else:
            new_job_id = f"public-{int(time.time())}-{brainrot[:10].replace(' ', '')}"
            return jsonify({
                "success": True,
                "jobId": new_job_id,
                "type": server_type,
                "brainrot": brainrot,
                "created": True
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cypher/jobid', methods=['POST'])
def generate_cypher_jobid():
    try:
        data = request.json
        base_jobid = data.get('baseJobId', '')
        brainrot = data.get('brainrot', 'unknown')
        
        hash_input = f"{base_jobid}{brainrot}{time.time()}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        
        cypher_id = f"CYPHER-{hash_value.upper()}-{int(time.time())}-{hash(brainrot) % 99999}"
        
        return jsonify({
            "cypherJobId": cypher_id,
            "brainrot": brainrot,
            "persistent": True,
            "expires": time.time() + 86400,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brainrot/list', methods=['GET'])
def list_brainrots():
    return jsonify({
        "brainrots": BRAINROTS,
        "total": len(BRAINROTS),
        "servers_available": len(SERVER_DATABASE),
        "timestamp": time.time()
    })

@app.route('/api/brainrot/stats', methods=['GET'])
def get_stats():
    total_servers = sum(len(servers) for servers in SERVER_DATABASE.values())
    return jsonify({
        "total_brainrots": len(BRAINROTS),
        "total_servers": total_servers,
        "unique_brainrots": len(SERVER_DATABASE),
        "uptime": int(time.time() - app.config.get('start_time', time.time())),
        "version": "3.1",
        "status": "operational"
    })

# ========== INICIALIZACIÓN ==========
print("[CYPHER] Brainrot Detector API v3.1 iniciado")
print(f"[CYPHER] {len(BRAINROTS)} brainrots disponibles")
print(f"[CYPHER] Servidor corriendo en puerto 10000")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
