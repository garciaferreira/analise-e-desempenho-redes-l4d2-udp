import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

PASTA_CAPTURAS = "capturas_l4d2"
CENARIOS = ["baseline", "moderado", "critico"]

print("Iniciando varredura dos arquivos .pcap...")

dados = {
    "baseline": {"pacotes": []},
    "moderado": {"pacotes": []},
    "critico": {"pacotes": []}
}

for arquivo in os.listdir(PASTA_CAPTURAS):
    if not arquivo.endswith(".pcap"): continue
    
    caminho = os.path.join(PASTA_CAPTURAS, arquivo)
    tamanho_kb = os.path.getsize(caminho) / 1024.0 
    
    for cenario in CENARIOS:
        if cenario in arquivo:
            dados[cenario]["pacotes"].append(tamanho_kb)

def calcular_ic_95(array_dados):
    if len(array_dados) < 2 or np.var(array_dados) == 0:
        return np.mean(array_dados) if array_dados else 0, 0.0

    media = np.mean(array_dados)
    intervalo = st.t.interval(0.95, len(array_dados)-1, loc=media, scale=st.sem(array_dados))
    margem_erro = media - intervalo[0]
    return media, margem_erro

resultados_media = []
resultados_erro = []

for cenario in CENARIOS:
    media, erro = calcular_ic_95(dados[cenario]["pacotes"])
    resultados_media.append(media)
    resultados_erro.append(erro)
    print(f"[{cenario.upper()}] Volume Médio: {media:.2f} KB | Margem de Erro (95% CI): ±{erro:.2f} KB")

plt.figure(figsize=(10, 6))
barras = plt.bar(CENARIOS, resultados_media, yerr=resultados_erro, capsize=10, 
                 color=['#4CAF50', '#FF9800', '#F44336'], alpha=0.8, edgecolor='black')

plt.title('Impacto das Anomalias no Tráfego UDP (Left 4 Dead 2)', fontsize=14)
plt.ylabel('Volume de Tráfego Capturado (Kilobytes)', fontsize=12)
plt.xlabel('Cenários de Degradação (netem)', fontsize=12)

plt.ylim(bottom=0)

for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval / 2, f'{yval:.1f} KB', 
             ha='center', va='center', color='white', fontweight='bold', fontsize=11)

plt.savefig('grafico_resultados_ic95.png', dpi=300, bbox_inches='tight')
print("\nAnálise concluída! O gráfico foi salvo como 'grafico_resultados_ic95.png'.")
