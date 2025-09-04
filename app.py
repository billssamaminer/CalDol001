from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def obtener_precio_usdt_ves():
    """
    Endpoint para obtener el precio de compra más bajo de USDT en el P2P de Binance.
    """
    try:
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

        payload = {
            "proMerchantAds": False,
            "page": 1,
            "rows": 10,
            "payTypes": ["Mercantil"],
            "countries": [],
            "publisherType": None,
            "asset": "USDT",
            "fiat": "VES",
            "tradeType": "SELL"
        }

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Host": "p2p.binance.com",
            "Origin": "https://p2p.binance.com"
        }

        respuesta = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos['data'] and len(datos['data']) > 0:
                primer_anuncio = datos['data'][1]
                precio = primer_anuncio['adv']['price']
                comerciante = primer_anuncio['advertiser']['nickName']
                disponible = primer_anuncio['adv']['surplusAmount']
                
                return jsonify({
                    "comerciante": comerciante,
                    "precio_venta": precio,
                    "cantidad_disponible": disponible,
                    "moneda": "VES",
                    "asset": "USDT"
                })
            else:
                return jsonify({"error": "No se encontraron anuncios para los criterios seleccionados."}), 404
        else:
            return jsonify({"error": f"Error en la solicitud: {respuesta.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)