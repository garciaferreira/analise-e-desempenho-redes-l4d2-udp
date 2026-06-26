import os
import subprocess

INTERFACE = "wlp2s0"
REPETITIONS = 30
DURATION_SEC = 60

TMP_DIR = "/tmp/capturas_l4d2"
FINAL_DIR = os.path.join(os.getcwd(), "capturas_l4d2")

os.makedirs(TMP_DIR, exist_ok=True)
os.system(f"sudo chmod 777 {TMP_DIR}")
os.makedirs(FINAL_DIR, exist_ok=True)

def clear_netem():
    os.system(f"sudo tc qdisc del dev {INTERFACE} root > /dev/null 2>&1")

def apply_netem(delay, jitter, loss):
    clear_netem()
    cmd = f"sudo tc qdisc add dev {INTERFACE} root netem delay {delay} {jitter} loss {loss}"
    os.system(cmd)

def record_traffic(filename):
    print(f"Gravando tráfego do jogo por {DURATION_SEC} segundos... ({filename})")
    filepath = os.path.join(TMP_DIR, filename)
    cmd = f"sudo tshark -i {INTERFACE} -a duration:{DURATION_SEC} -f 'udp' -w {filepath} 2>/dev/null"
    subprocess.run(cmd, shell=True)

print("Iniciando bateria de testes automatizados do SUT...")
clear_netem()

for i in range(1, REPETITIONS + 1):
    print(f"\n--- INICIANDO REPETIÇÃO {i}/{REPETITIONS} ---")
    
    print("Cenário 1: Baseline (Rede Mista Limpa)")
    clear_netem()
    record_traffic(f"rep_{i}_nivel_1_baseline.pcap")
    
    print("Cenário 2: Moderado (50ms latência, 20ms jitter, 2% perda)")
    apply_netem("50ms", "20ms", "2%")
    record_traffic(f"rep_{i}_nivel_2_moderado.pcap")
    
    print("Cenário 3: Crítico (150ms latência, 50ms jitter, 10% perda)")
    apply_netem("150ms", "50ms", "10%")
    record_traffic(f"rep_{i}_nivel_3_critico.pcap")

clear_netem()
print("\nFinalizando testes... Movendo arquivos para a sua pasta final.")
os.system(f"sudo mv {TMP_DIR}/*.pcap {FINAL_DIR}/ 2>/dev/null")
print("Tudo pronto! Arquivos salvos e regras restauradas.")
