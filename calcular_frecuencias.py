#!/usr/bin/env python3
"""
CALCULADORA DE FRECUENCIAS DE FALLA
Para rodamientos de rodillos cónicos Timken
"""

import math
import json

def calcular_frecuencias_falla(d_interno, D_externo, numero_elementos, diametro_elemento, angulo_contacto, rpm):
    """
    Calcula las frecuencias de falla características de un rodamiento
    
    Parámetros:
        d_interno: Diámetro interno en mm
        D_externo: Diámetro externo en mm  
        numero_elementos: Número de rodillos o bolas
        diametro_elemento: Diámetro del rodillo/bola en mm
        angulo_contacto: Ángulo de contacto en grados
        rpm: Velocidad de rotación en revoluciones por minuto
    
    Retorna:
        dict con BPFO, BPFI, FTF, BSF y sus armónicas
    """
    
    # Calcular diámetro primitivo
    Pd = (d_interno + D_externo) / 2
    
    # Convertir ángulo a radianes
    beta_rad = math.radians(angulo_contacto)
    
    # Calcular razón de diámetros
    bd_pd = diametro_elemento / Pd
    
    # Factor común
    cos_beta = math.cos(beta_rad)
    
    # Frecuencia de rotación en Hz
    f_rot = rpm / 60
    
    # BPFO - Ball Pass Frequency Outer race (Pista Externa)
    # Indica defectos en la pista externa
    BPFO = (numero_elementos / 2) * (1 - bd_pd * cos_beta) * f_rot
    
    # BPFI - Ball Pass Frequency Inner race (Pista Interna)
    # Indica defectos en la pista interna
    BPFI = (numero_elementos / 2) * (1 + bd_pd * cos_beta) * f_rot
    
    # FTF - Fundamental Train Frequency (Frecuencia de la Jaula)
    # Indica defectos en la jaula
    FTF = (1 / 2) * (1 - bd_pd * cos_beta) * f_rot
    
    # BSF - Ball Spin Frequency (Frecuencia de Giro del Elemento)
    # Indica defectos en los rodillos/bolas
    BSF = (Pd / (2 * diametro_elemento)) * (1 - (bd_pd * cos_beta)**2) * f_rot
    
    # Calcular órdenes (múltiplos de la frecuencia de rotación)
    orden_BPFO = BPFO / f_rot
    orden_BPFI = BPFI / f_rot
    orden_FTF = FTF / f_rot
    orden_BSF = BSF / f_rot
    
    resultados = {
        'parametros': {
            'd_interno_mm': d_interno,
            'D_externo_mm': D_externo,
            'diametro_primitivo_mm': Pd,
            'numero_elementos': numero_elementos,
            'diametro_elemento_mm': diametro_elemento,
            'angulo_contacto_grados': angulo_contacto,
            'rpm': rpm,
            'frecuencia_rotacion_hz': round(f_rot, 2)
        },
        'frecuencias': {
            'BPFO': {
                'hz': round(BPFO, 2),
                'orden': round(orden_BPFO, 2),
                'descripcion': 'Pista Externa (Outer Race)',
                'armonicas': {
                    '2x': round(BPFO * 2, 2),
                    '3x': round(BPFO * 3, 2)
                }
            },
            'BPFI': {
                'hz': round(BPFI, 2),
                'orden': round(orden_BPFI, 2),
                'descripcion': 'Pista Interna (Inner Race)',
                'armonicas': {
                    '2x': round(BPFI * 2, 2),
                    '3x': round(BPFI * 3, 2)
                }
            },
            'FTF': {
                'hz': round(FTF, 2),
                'orden': round(orden_FTF, 2),
                'descripcion': 'Jaula (Cage)',
                'armonicas': {
                    '2x': round(FTF * 2, 2),
                    '3x': round(FTF * 3, 2)
                }
            },
            'BSF': {
                'hz': round(BSF, 2),
                'orden': round(orden_BSF, 2),
                'descripcion': 'Elemento Rodante (Rolling Element)',
                'armonicas': {
                    '2x': round(BSF * 2, 2),
                    '3x': round(BSF * 3, 2)
                }
            }
        }
    }
    
    return resultados

def imprimir_resultados(resultados):
    """Imprime los resultados de forma legible"""
    print("\n" + "="*70)
    print("FRECUENCIAS DE FALLA CALCULADAS")
    print("="*70)
    
    params = resultados['parametros']
    print(f"\n📊 PARÁMETROS DEL RODAMIENTO:")
    print(f"   Diámetro interno (d):      {params['d_interno_mm']:.3f} mm")
    print(f"   Diámetro externo (D):      {params['D_externo_mm']:.3f} mm")
    print(f"   Diámetro primitivo (Pd):   {params['diametro_primitivo_mm']:.3f} mm")
    print(f"   Número de elementos:       {params['numero_elementos']}")
    print(f"   Diámetro elemento (Bd):    {params['diametro_elemento_mm']:.3f} mm")
    print(f"   Ángulo de contacto (β):    {params['angulo_contacto_grados']:.1f}°")
    print(f"   Velocidad de rotación:     {params['rpm']} RPM ({params['frecuencia_rotacion_hz']} Hz)")
    
    freqs = resultados['frecuencias']
    print(f"\n🎯 FRECUENCIAS CARACTERÍSTICAS:\n")
    
    for tipo, datos in freqs.items():
        print(f"   {tipo} - {datos['descripcion']}")
        print(f"   ├─ Frecuencia: {datos['hz']} Hz")
        print(f"   ├─ Orden: {datos['orden']}x RPM")
        print(f"   └─ Armónicas: 2x={datos['armonicas']['2x']} Hz, 3x={datos['armonicas']['3x']} Hz")
        print()
    
    print("="*70)

# Ejemplo de uso con rodamiento típico
if __name__ == '__main__':
    print("\n🔧 CALCULADORA DE FRECUENCIAS DE FALLA - RODAMIENTOS TIMKEN\n")
    
    # EJEMPLO 1: Rodamiento 30302 @ 1500 RPM
    print("📋 EJEMPLO 1: Timken 30302")
    print("   (Rodamiento de rodillos cónicos, serie 30)")
    
    # Parámetros estimados para 30302
    # Nota: Estos valores deben obtenerse del catálogo completo o mediciones
    resultados1 = calcular_frecuencias_falla(
        d_interno=15.0,          # mm
        D_externo=42.0,          # mm
        numero_elementos=14,     # Típico para esta serie (estimado)
        diametro_elemento=6.5,   # mm (estimado basado en geometría)
        angulo_contacto=15.0,    # grados (típico para rodillos cónicos)
        rpm=1500
    )
    
    imprimir_resultados(resultados1)
    
    # EJEMPLO 2: Mismo rodamiento a 3000 RPM
    print("\n\n📋 EJEMPLO 2: Timken 30302 @ 3000 RPM")
    
    resultados2 = calcular_frecuencias_falla(
        d_interno=15.0,
        D_externo=42.0,
        numero_elementos=14,
        diametro_elemento=6.5,
        angulo_contacto=15.0,
        rpm=3000
    )
    
    imprimir_resultados(resultados2)
    
    # Guardar un ejemplo en JSON
    with open('/home/claude/ejemplo_frecuencias.json', 'w') as f:
        json.dump(resultados1, f, indent=2)
    
    print("\n✅ Ejemplo guardado en: ejemplo_frecuencias.json")
    
    print("\n" + "="*70)
    print("💡 NOTAS IMPORTANTES:")
    print("="*70)
    print("""
    1. Para cálculos precisos, se necesitan los datos geométricos exactos
       del fabricante (número de rodillos, diámetro de rodillos, ángulo).
       
    2. Estos valores pueden encontrarse en:
       - Catálogos técnicos detallados
       - Hojas de especificaciones del fabricante
       - Mediciones directas del rodamiento
    
    3. Las frecuencias calculadas son para rodamiento en condiciones ideales.
       Las frecuencias reales pueden variar ligeramente debido a:
       - Deslizamiento de los elementos
       - Carga aplicada
       - Temperatura de operación
       - Lubricación
    
    4. En análisis de vibraciones, buscar picos en:
       - BPFO y sus armónicas: defectos en pista externa
       - BPFI y sus armónicas: defectos en pista interna
       - FTF: problemas de jaula o lubricación
       - BSF: defectos en elementos rodantes
    
    5. Bandas laterales alrededor de BPFO/BPFI espaciadas por FTF
       indican defectos distribuidos en la pista.
    """)
