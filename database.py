import sqlite3
from datetime import datetime

DB_FILE = "forense.db"

def crear_db():
    """Crea la tabla si no existe todavía."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS casos (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre               TEXT,
            fecha                TEXT,
            temperatura_corporal REAL,
            temperatura_ambiente REAL,
            humedad              REAL,
            factor_enfriamiento  REAL,
            peso                 REAL,
            temperatura_rectal   REAL,
            rigor_mortis         TEXT,
            livor_mortis         TEXT,
            tiempo_estimado      REAL,
            rango_lo             REAL,
            rango_hi             REAL,
            nivel_confianza      INTEGER
        )
    """)
    conn.commit()
    conn.close()

def guardar_caso(nombre, params, resultado):
    """Guarda un caso nuevo en la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO casos (
            nombre, fecha,
            temperatura_corporal, temperatura_ambiente,
            humedad, factor_enfriamiento, peso,
            temperatura_rectal, rigor_mortis, livor_mortis,
            tiempo_estimado, rango_lo, rango_hi, nivel_confianza
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nombre,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        params["temp_corp"],
        params["temp_amb"],
        params.get("humedad", 0),
        params.get("factor_en", 0.083),
        params["peso"],
        params.get("temp_rect", params["temp_corp"]),
        params["rigor"],
        params["livor"],
        resultado["centro"],
        resultado["rango"][0],
        resultado["rango"][1],
        resultado["confianza"],
    ))
    conn.commit()
    conn.close()

def cargar_casos():
    """Retorna todos los casos como lista de diccionarios."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM casos ORDER BY id DESC")
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    # Convierte cada fila en un diccionario {columna: valor}
    return [dict(zip(columnas, fila)) for fila in filas]

def eliminar_caso(caso_id):
    """Elimina un caso por su ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM casos WHERE id = ?", (caso_id,))
    conn.commit()
    conn.close()