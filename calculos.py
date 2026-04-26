import math

def obtener_k(condicion, peso_kg=70):
    k_base = {
        "Aire libre, sin ropa":    0.083,
        "Ropa ligera":             0.065,
        "Ropa gruesa / cobija":    0.050,
        "Sumergido en agua fría":  0.120,
        "Sumergido en agua tibia": 0.090,
    }
    k = k_base.get(condicion, 0.083)
    factor_peso = (70 / peso_kg) ** 0.5
    return round(k * factor_peso, 4)

def algor_mortis(temp_corporal, temp_ambiente, k):
    if temp_corporal <= temp_ambiente:
        return None
    ratio = (temp_corporal - temp_ambiente) / (37 - temp_ambiente)
    return round((-1 / k) * math.log(ratio), 2)

def rigor_mortis(grado):
    rangos = {
        "ausente":   (0,  3,  "Muerte muy reciente"),
        "parcial":   (2,  8,  "Primeras horas"),
        "completo":  (6,  14, "Varias horas"),
        "cediendo":  (12, 36, "Más de 12 horas"),
    }
    return rangos.get(grado, (0, 0, "Desconocido"))

def livor_mortis(estado):
    estados = {
        "no fijado": (0, 8,  "Lividez presente, no fija"),
        "fijado":    (8, 48, "Cuerpo no movido tras la muerte"),
    }
    return estados.get(estado, (0, 0, "Desconocido"))

def Factor_Eh(temp_amb):
    if temp_amb <= 15.0:
        Eh = 1.5
    elif temp_amb <= 25.0:
        Eh = 1.0
    elif temp_amb <= 35.0:
        Eh = 0.5
    else:
        Eh = 0.2
    return Eh

def glaiseter(temp_rect, Eh):
    
    hgla = (36.7 - temp_rect) * Eh

    return round (hgla,2)

def estimar(temp_corp, temp_amb, condicion, peso,
            grado_rigor, estado_livor, temp_rect):
    k        = obtener_k(condicion, peso)
    t_algor  = algor_mortis(temp_corp, temp_amb, k)
    rigor    = rigor_mortis(grado_rigor)
    livor    = livor_mortis(estado_livor)
    Eh       = Factor_Eh(temp_amb)
    hgla     = glaiseter(temp_rect, Eh)
    estimaciones = []
    if t_algor:
        estimaciones.append(t_algor)
        estimaciones.append((rigor[0] + rigor[1]) / 2)
        estimaciones.append((livor[0] + rigor[1]) / 2)
        

    centro   = round(sum(estimaciones) / len(estimaciones), 2)
    rango_lo = max(0, round(centro - 2, 1))
    rango_hi = round(centro + 2, 1)
    confianza = min(95, 60 + len(estimaciones) * 10)

    return {
        "algor_h":   t_algor,
        "rigor":     rigor,
        "livor":     livor,
        "centro":    centro,
        "rango":     (rango_lo, rango_hi),
        "confianza": confianza,
        "k":         k,
        "Eh":        Eh,
        "hgla":      hgla
    }
