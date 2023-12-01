import logging
from flask import Flask, request, jsonify

# Configure logging for NRF
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)

# Statically defined service profiles for AMF and SMF
# In a real-world scenario, this might involve dynamic registration and discovery mechanisms
registered_services = {
    "amf": {"service_endpoint": "http://amf-service:80"},  # Adjust the AMF endpoint as needed
    "smf": {"service_endpoint": "http://smf-service:82"}  # Adjust the SMF endpoint as needed
}

@app.route('/nrf/register', methods=['POST'])
def register_service():
    data = request.get_json()
    service_name = data.get("service_name")
    service_endpoint = data.get("service_endpoint")

    if not service_name or not service_endpoint:
        logging.error("NRF: Missing service name or endpoint in registration")
        return jsonify({"error": "Missing service name or endpoint"}), 400

    registered_services[service_name] = {"service_endpoint": service_endpoint}
    logging.info(f"NRF: Service {service_name} registered with endpoint {service_endpoint}")
    return jsonify({"message": f"Service {service_name} registered successfully"})

@app.route('/nrf/discover/<service_name>', methods=['GET'])
def discover_service(service_name):
    service_profile = registered_services.get(service_name)
    if service_profile:
        logging.info(f"NRF: Provided discovery information for {service_name}")
        return jsonify(service_profile)
    else:
        logging.error(f"NRF: Service {service_name} not found in registry")
        return jsonify({"error": f"Service {service_name} not found"}), 404


