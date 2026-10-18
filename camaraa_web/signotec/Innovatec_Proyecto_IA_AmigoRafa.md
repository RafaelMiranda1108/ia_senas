# Proyecto: Sistema de Reconocimiento de Gestos Manuales mediante Visión Artificial

## 1.- EL. IEE. Descripción de la problemática u oportunidad de negocio

En múltiples ámbitos —educativo, industrial, médico y de servicios— la interacción sin contacto se ha vuelto un requisito indispensable debido a preocupaciones de higiene, ergonomía y accesibilidad. Paralelamente, las personas con discapacidad auditiva o del habla enfrentan dificultades continuas para comunicarse con su entorno, lo cual repercute en su inclusión social y oportunidades laborales. A pesar de la existencia de ciertos dispositivos de ayuda, muchas soluciones dependen de hardware costoso, interfaces poco intuitivas o requieren supervisión especializada, lo que limita su adopción masiva.

Por otro lado, tras la pandemia, la demanda de sistemas de control basados en visión confirman una tendencia de mercado creciente: el uso de cámaras convencionales para interpretar gestos y señales manuales, sin necesidad de dispositivos adicionales. Esta situación revela un nicho para desarrollar una solución de bajo costo que utilice únicamente técnicas de visión artificial (visión por computadora) para detectar y procesar gestos de manos en tiempo real. Al eliminar la necesidad de modelos de inteligencia artificial complejos o hardware especializado, se logra un producto accesible y de fácil implementación en dispositivos convencionales.

Las estadísticas de la Organización Mundial de la Salud indican que más de 430 millones de personas viven con pérdida auditiva significativa, mientras que el mercado global de interfaces sin contacto se proyecta en decenas de miles de millones de dólares en los próximos cinco años. Instituciones educativas, hospitales, plantas industriales y plataformas de servicios remotos requieren sistemas que interpreten señales gestuales de forma estandarizada y confiable. La ausencia de soluciones sencillas basadas únicamente en visión artificial presenta una oportunidad de negocio sólida: desarrollar un software ligero, multiplataforma y asequible que promueva la inclusión y modernización de procesos en diversos sectores.

## 2.- EL. IEE. Descripción de la propuesta de valor

Nuestra propuesta consiste en un sistema de reconocimiento de gestos manuales construido sobre técnicas de visión artificial. El software procesa la señal de vídeo en tiempo real, segmenta zonas de interés mediante umbrales de color y diferencias de fondo, y aplica análisis de contornos y convexidad para identificar posiciones de dedos y palmas. Gracias a esta aproximación, el rendimiento es constante en procesadores de gama baja y cámaras estándar.

El producto es multiplataforma: corre en Windows, Linux, macOS y dispositivos embebidos con Linux (por ejemplo, Raspberry Pi), sin requerir GPU dedicada. Ofrece un módulo de calibración intuitivo que ajusta parámetros de segmentación según iluminación y tono de piel, y un panel de configuración para definir hasta 20 gestos personalizados. La salida en pantalla puede configurarse en texto, señales auditivas o eventos de control (por ejemplo, enviar comandos a una aplicación externa).

Este enfoque reduce el coste de licenciamiento y entrenamiento de modelos, facilita la integración en proyectos existentes y minimiza la curva de aprendizaje de los usuarios finales. Al centrarse en métodos comprobados de visión por computadora —filtros morfológicos, análisis de forma y seguimiento de contornos—, garantizamos robustez en entornos controlados e iluminación variable, ofreciendo un equilibrio ideal entre precisión, velocidad y accesibilidad.

## 3.- EL. IEE. Descripción técnica de la solución

El sistema está desarrollado en Python utilizando OpenCV como motor principal de visión artificial. El flujo de procesamiento comprende:

1. **Captura de imagen**: Adquisición de frames desde la cámara.
2. **Preprocesamiento**: Conversión a espacio de color HSV, aplicación de filtros de suavizado y operación de sustracción de fondo dinámico.
3. **Segmentación**: Umbralización basada en histograma de tonos de piel y en diferencias respecto al fondo, seguida de filtros morfológicos (erosión y dilatación) para limpiar ruido.
4. **Detección de contornos**: Identificación de contorno máximo correspondiente a la mano y cálculo de su convex hull y defectos de convexidad para localizar posiciones de dedos.
5. **Extracción de características**: Cálculo de ángulos entre puntos clave de la mano, proporciones de segmentos y relaciones espaciales.
6. **Clasificación heurística**: Definición de reglas basadas en número de defectos y distribución angular para reconocer gestos predefinidos (por ejemplo, “pulgar arriba”, “victoria”, “mano abierta”).


## 4.- EL. IEE. Análisis de mercado


## 5.- EL. IEE. Propiedad intelectual



## 6.- EL. IEE. Fuentes consultadas

- OpenCV Documentation – docs.opencv.org  
- Artículos de Google Scholar sobre convex hull y defectos en visión por computadora  
- Tutoriales oficiales de Python para OpenCV  

## 7.- EL. IEE. Resumen