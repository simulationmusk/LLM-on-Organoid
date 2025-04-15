import os

CAMERA_IP = os.getenv("CAMERA_IP", "172.30.1.43")
CAMERA_PORT = int(os.getenv("CAMERA_PORT", 3005))
DB_IP = os.getenv("DB_IP", "172.30.2.215")
DB_PORT = int(os.getenv("DB_PORT", 8088))
DB_TIMEOUT = int(os.getenv("DB_TIMEOUT", 6000))
DB_TOKEN = os.getenv(
    "DB_TOKEN",
    "uBQYMh5To57O20MUJP_7hv84wQOiPNfC0Nrrdtj9b4vdovLf1DICVX1t15wpKsnOuqOhu2sEIsFWRnXf5r8dtQ==",
)
INTAN_SOCK_TIMEOUT = float(os.getenv("INTAN_SOCK_TIMEOUT", 0.3))
INTAN_SERVICE_IP = os.getenv("INTAN_SOFTWARE_IP", "172.30.1.165")
INTAN_SERVICE_PORT = int(os.getenv("INTAN_SOFTWARE_PORT", 5051))
MONGO_DB_IP = os.getenv("MONGO_DB_IP", "172.30.1.43")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD", "5YFXfZCnd6sKv7")
MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT", 27018))
MONGO_DB_USER = os.getenv("MONGO_DB_USER", "npuser")
PRIZMATIX_PORT = int(os.getenv("PRIZMATIX_PORT", 3001))
PUMP_1_IP = os.getenv("PUMP_1_IP", "172.30.2.216")
PUMP_2_IP = os.getenv("PUMP_2_IP", "172.30.2.131")
PUMP_3_IP = os.getenv("PUMP_3_IP", "172.30.2.131")
PUMP_PORT = int(os.getenv("PUMP_PORT", 3000))
TRIGGER_IP = os.getenv("TRIGGER_IP", "172.30.1.165")
TRIGGER_IP_PORT = os.getenv("TRIGGER_IP_PORT", 5010)
TRIGGER_UV_PORT = int(os.getenv("TRIGGER_UV_PORT", 5002))
TRIGGER_UV_TIMEOUT = float(os.getenv("TRIGGER_UV_TIMEOUT", 0.3))
