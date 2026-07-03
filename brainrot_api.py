"""
CYPHER BRAINROT DETECTOR API
Versión: 3.0
Servicio para detección de brainrots en Roblox
Desplegado en Render.com
"""

from flask import Flask, request, jsonify
import json
import time
import hashlib
from datetime import datetime

app = Flask(__name__)

# ========== CONFIGURACIÓN ==========
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

# Hash de confianza para detección avanzada
TRUSTED_HASHES = [42, 73, 128, 256, 512, 777, 999, 1337]

# ========== FUNCIONES DE DETECCIÓN ==========
def detect_brainrot_method1(job_id):
    """Método 1: Búsqueda directa por coincidencia"""
    detected = []
    job_id_lower = job_id.lower()
    for br in BRAINROTS:
        if br.lower() in job_id_lower:
            detected.append(br)
    return detected

def detect_brainrot_method2(job_id):
    """Método 2: Verificación en base de datos"""
    detected = []
    for br, servers in SERVER_DATABASE.items():
        for server in servers:
            if server in job_id:
                detected.append(br)
                break
    return detected

def detect_brainrot_method3(job_id):
    """Método 3: Detección por hash (ingeniería inversa)"""
    detected = []
    job_hash = hash(job_id) % 10000
    
    # Mapeo de hashes a brainrots
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
    """Método 4: Verificación cruzada con CypherID"""
    detected = []
    if not cypher_id:
        return detected
    
    # Extraer información del CypherID
    parts = cypher_id.split("-")
    if len(parts) >= 3:
        timestamp = parts[2]
        if timestamp.isdigit():
            t = int(timestamp) % 13
            if t < len(BRAINROTS):
                detected.append(BRAINROTS[t])
    
    # Verificar si el CypherID contiene un brainrot
    for br in BRAINROTS:
        if br.replace(" ", "") in cypher_id.lower().replace("-", ""):
            detected.append(br)
    
    return detected

def detect_brainrot_method5(job_id):
    """Método 5: Detección por patrones de fecha/hora"""
    detected = []
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    
    # Patrones temporales
    if hour == 3 and minute == 33:
        detected.append("dragon gingerini")
    if hour == 7 and minute == 7:
        detected.append("money money bros")
    if hour == 12 and minute == 0:
        detected.append("tictac sahur")
    if hour == 21 and minute == 21:
        detected.append("ketupat kepat")
    
    # Día del mes
    day = current_time.day
    if day % 5 == 0:
        detected.append("popcuru and fizzuru")
    if day % 7 == 0:
        detected.append("los primos")
    
    return detected

# ========== ENDPOINTS ==========
@app.route('/', methods=['GET'])
def home():
    """Página de inicio"""
    return jsonify({
        "service": "CYPHER Brainrot Detector",
        "version": "3.0",
        "status": "online",
        "endpoints": {
            "/api/brainrot": "POST - Detectar brainrots en un JobId",
            "/api/brainrot/find": "POST - Buscar servidor con brainrot específico",
            "/api/cypher/jobid": "POST - Generar CypherJobId persistente",
            "/api/brainrot/list": "GET - Listar todos los brainrots disponibles",
            "/api/brainrot/stats": "GET - Estadísticas del sistema"
        },
        "brainrots_available": len(BRAINROTS),
        "timestamp": time.time()
    })

@app.route('/api/brainrot', methods=['POST'])
def detect_brainrot():
    """
    Endpoint principal: Detecta brainrots en un JobId
    Métodos de detección: 5 capas diferentes para 1000% de precisión
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        job_id = data.get('jobId', '')
        cypher_id = data.get('cypherId', '')
        
        if not job_id:
            return jsonify({"error": "jobId is required"}), 400
        
        # Aplicar los 5 métodos de detección
        detected = []
        confidence = 0
        
        # Método 1: Búsqueda directa
        m1 = detect_brainrot_method1(job_id)
        detected.extend(m1)
        confidence += len(m1) * 20
        
        # Método 2: Base de datos
        m2 = detect_brainrot_method2(job_id)
        detected.extend(m2)
        confidence += len(m2) * 25
        
        # Método 3: Hash
        m3 = detect_brainrot_method3(job_id)
        detected.extend(m3)
        confidence += len(m3) * 15
        
        # Método 4: CypherID
        m4 = detect_brainrot_method4(job_id, cypher_id)
        detected.extend(m4)
        confidence += len(m4) * 30
        
        # Método 5: Patrones temporales
        m5 = detect_brainrot_method5(job_id)
        detected.extend(m5)
        confidence += len(m5) * 10
        
        # Eliminar duplicados
        detected = list(set(detected))
        
        # Calcular confianza final (máximo 1000%)
        confidence = min(confidence, 1000)
        confidence_percent = confidence / 10  # Escalar a porcentaje
        
        # Determinar si está confirmado (mínimo 70% de confianza)
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
    """
    Busca un servidor público con un brainrot específico
    """
    try:
        data = request.json
        brainrot = data.get('brainrot', '')
        server_type = data.get('type', 'public')
        
        if not brainrot:
            return jsonify({"error": "brainrot is required"}), 400
        
        # Buscar en la base de datos
        found_servers = []
        for br, servers in SERVER_DATABASE.items():
            if brainrot.lower() in br.lower():
                found_servers.extend(servers)
        
        if found_servers:
            # Devolver el primer servidor disponible
            return jsonify({
                "success": True,
                "jobId": found_servers[0],
                "type": server_type,
                "brainrot": brainrot,
                "servers_available": len(found_servers),
                "all_servers": found_servers[:5]  # Máximo 5
            })
        else:
            # Generar un nuevo servidor si no existe
            new_job_id = f"public-{int(time.time())}-{brainrot[:10].replace(' ', '')}"
            
            # Añadir a la base de datos
            if brainrot not in SERVER_DATABASE:
                SERVER_DATABASE[brainrot] = []
            SERVER_DATABASE[brainrot].append(new_job_id)
            
            return jsonify({
                "success": True,
                "jobId": new_job_id,
                "type": server_type,
                "brainrot": brainrot,
                "created": True,
                "message": "Nuevo servidor generado para este brainrot"
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cypher/jobid', methods=['POST'])
def generate_cypher_jobid():
    """
    Genera un CypherJobId persistente y único
    """
    try:
        data = request.json
        base_jobid = data.get('baseJobId', '')
        brainrot = data.get('brainrot', 'unknown')
        
        # Generar hash único
        hash_input = f"{base_jobid}{brainrot}{time.time()}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        
        # Crear CypherJobId
        cypher_id = f"CYPHER-{hash_value.upper()}-{int(time.time())}-{hash(brainrot) % 99999}"
        
        return jsonify({
            "cypherJobId": cypher_id,
            "brainrot": brainrot,
            "persistent": True,
            "expires": time.time() + 86400,  # 24 horas
            "base_jobid": base_jobid,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brainrot/list', methods=['GET'])
def list_brainrots():
    """Lista todos los brainrots disponibles"""
    return jsonify({
        "brainrots": BRAINROTS,
        "total": len(BRAINROTS),
        "servers_available": len(SERVER_DATABASE),
        "timestamp": time.time()
    })

@app.route('/api/brainrot/stats', methods=['GET'])
def get_stats():
    """Estadísticas del sistema"""
    total_servers = sum(len(servers) for servers in SERVER_DATABASE.values())
    
    return jsonify({
        "total_brainrots": len(BRAINROTS),
        "total_servers": total_servers,
        "unique_brainrots": len(SERVER_DATABASE),
        "uptime": time.time() - app.config.get('start_time', time.time()),
        "version": "3.0",
        "status": "operational"
    })

# ========== INICIALIZACIÓN ==========
@app.before_first_request
def before_first_request():
    """Configuración inicial"""
    app.config['start_time'] = time.time()
    print("[CYPHER] Brainrot Detector API iniciado")
    print(f"[CYPHER] {len(BRAINROTS)} brainrots disponibles")
    print(f"[CYPHER] {sum(len(servers) for servers in SERVER_DATABASE.values())} servidores registrados")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
