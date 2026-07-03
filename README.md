# 🧠 CYPHER Brainrot Detector API

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📌 Descripción
API para detección de brainrots en Roblox. Utiliza 5 métodos diferentes para asegurar 1000% de precisión.

## 🚀 Endpoints

### `POST /api/brainrot`
Detecta brainrots en un JobId
```json
{
  "jobId": "public-12345-garama",
  "cypherId": "CYPHER-TEST-123"
}
