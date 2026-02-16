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

### 3. Deflexión (En Mantenimiento)  
**Estado:** *Temporalmente Bajo Mantenimiento*  

Herramienta para el cálculo de **Tensión de Von Mises** y **Deflexión Máxima Uniaxial**.  

**Casos Soportados:**  
- **Viga en Voladizo:** Superposición de Fuerza Vertical, Carga Lineal Distribuida y Momento Flector.  
- **Viga Simplemente Apoyada:** Fuerza Puntual y Carga Distribuida (*actualmente limitada a una carga distribuida a la vez*).  

**Características:**  
- Permite usar la tabla de descomposición e ingresar simultáneamente la sumatoria de momentos.  

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