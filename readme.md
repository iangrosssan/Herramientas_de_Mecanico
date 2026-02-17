# Herramientas de Mecánico  

Este repositorio contiene una colección de herramientas y cálculos para diseño mecánico, incluyendo hojas de cálculo, notebooks de Mathematica y referencias teóricas.  

## Contenido  

### 1. Frenos y Embragues  
**Archivo:** `frenos&embragues.nb` (Mathematica Notebook)  
- Cálculo de frenos de disco.  
- Cálculo de frenos de tambor.  

### 2. Cálculo de Engranes  
**Archivo:** `Calculo_de_Engrane.xlsx` (Excel)  
Archivo detallado para el cálculo y diseño de engranes.  
- Soporte para Engranes Rectos.  
- Soporte para Engranes Helicoidales.  

### 3. Deflection Tool (`deflection_tool`)
**Ubicación:** `deflection_tool/`
**Estado:** *Activo*
**Resultados de Validación:** `deflection_tool/VALIDATED_RESULTS.md/` (Directorio de reportes y notebooks)

Un paquete de Python modular para el cálculo de deflexión en vigas y ejes.

**Características:**
- **Entrada basada en JSON:** Defina geometría, materiales y cargas en archivos JSON claros y legibles.
- **Base de Datos de Materiales:** Soporte integrado para materiales estándar (ej. AISI 4140) y personalizados.
- **Última Verificación:** *Exitosa* (Verificado manualmente con `simple_demo.json`)
- **Cálculo de Deflexión:** Utiliza integración numérica para determinar la deflexión vertical bajo cargas de flexión.
- **Soporte de Escenarios:** Incluye ejemplos para ejes con engranes y vigas simples.

**Uso Rápido:**
```bash
python3 deflection_tool/main.py deflection_tool/examples/gear_shaft.json
```

### 4. Recursos y Referencias  
Tablas y documentos útiles del libro *Shigley's Mechanical Engineering Design*:  
- **Propiedades de Materiales:** `Shingley's A-20&21 Propiedades de Materiales.pdf`  
- **Casos de Carga en Viga:** `Shigley's A-9 Casos de Carga en Viga.pdf`  

## Requisitos  

### Python  
Si desea utilizar o contribuir a las herramientas en Python, puede instalar las dependencias necesarias con:  

```bash
pip install -r requirements.txt
```

### Otros  
- **Mathematica:** Se requiere Wolfram Mathematica o Wolfram Player para abrir los archivos `.nb`.  
- **Excel:** Microsoft Excel o compatible para abrir las hojas de cálculo `.xlsx`.  