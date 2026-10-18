# Proyecto: Sistema de Reconocimiento de Gestos Manuales mediante Visión Artificial

## 1.- EL. IEE. Descripción de la problemática u oportunidad de negocio

En múltiples ámbitos —educativo, médico, industrial y de servicios— la interacción sin contacto se ha vuelto esencial, ya sea por razones de higiene, ergonomía o accesibilidad. Paralelamente, las personas con discapacidad auditiva enfrentan barreras significativas en la comunicación diaria, limitando su inclusión social y oportunidades laborales. Aunque existen tecnologías de asistencia, muchas dependen de hardware especializado, son costosas o difíciles de usar, lo que restringe su adopción.

Según la Organización Mundial de la Salud (2021), más de 430 millones de personas viven con pérdida auditiva significativa. A su vez, el mercado global de interfaces sin contacto supera los 30 mil millones de dólares, impulsado por sectores que requieren nuevas formas de interacción seguras y eficientes. Esta realidad representa una oportunidad clara para desarrollar soluciones accesibles, sin hardware adicional, basadas únicamente en visión artificial.

El proyecto **Signotec** responde a esta necesidad con una herramienta multiplataforma que traduce gestos manuales en texto, facilitando la inclusión digital. Su diseño ligero y de bajo costo permite su implementación en entornos educativos, sanitarios, industriales y domésticos.

Este proyecto se alinea con el eje transversal de **inclusión social e innovación tecnológica**, al proponer una solución que integra inteligencia artificial y visión por computadora para romper barreras de comunicación y democratizar el acceso a la tecnología.

## 2.- EL. IEE. Descripción de la propuesta de valor

La mayoría de las personas sordas o con dificultades del habla dependen actualmente de intérpretes humanos, guantes sensores o aplicaciones especializadas que requieren hardware adicional costoso y procesos de calibración complejos, lo cual limita su adopción masiva y genera frustración.

Los usuarios buscan una solución económica, intuitiva y plug-and-play, capaz de integrarse en dispositivos convencionales sin periféricos extras, que ofrezca reconocimiento preciso de gestos y una experiencia de comunicación fluida en entornos educativos, laborales y sociales.

**Signotec** propone un software multiplataforma que, mediante una cámara estándar y algoritmos de visión artificial, captura, segmenta y analiza gestos manuales en tiempo real. Incluye un módulo de calibración automática de umbral de color e iluminación, permite definir y personalizar hasta 20 gestos, y exporta la salida como texto, voz o eventos de control para aplicaciones externas.

Entre sus atributos destacan: bajo costo de implementación, compatibilidad con Windows, Linux, macOS y dispositivos embebidos como Raspberry Pi; módulos de configuración intuitiva; y robustez ante variaciones de luz. Estos beneficios satisfacen la necesidad de accesibilidad, independencia y usabilidad que demandan los usuarios.

La propuesta será validada a través de sesiones estructuradas con expertos, con el objetivo de construir el Mapa de Propuesta de Valor de Osterwalder y demostrar la correspondencia entre los atributos funcionales del sistema y las necesidades reales identificadas en los usuarios finales.

## 3.- EL. IEE. Descripción técnica de la solución

El sistema Signotec está implementado en Python con OpenCV como núcleo de procesamiento visual. Se encuentra en fase funcional con pruebas en laboratorio y entornos controlados. El flujo de trabajo incluye captura de video, conversión a HSV, segmentación por tono de piel, limpieza con filtros morfológicos, detección de contornos y cálculo de convexidades para inferir la configuración de los dedos.

A través de reglas heurísticas y relaciones geométricas se identifican gestos definidos por el usuario. El modelo no depende de redes neuronales complejas, por lo que su rendimiento es estable en equipos sin GPU.

El sistema se ejecuta en Windows, Linux, macOS y placas embebidas como Raspberry Pi. Entre sus atributos destacan: no requiere hardware adicional, se adapta a iluminación variable y permite exportar salidas como texto o comandos.

Entre los riesgos técnicos se encuentra la dependencia de condiciones visuales (iluminación, contraste), los cuales se abordan con un módulo de calibración interactiva y normalización de características visuales. También se prevé que futuras versiones incluyan una red neuronal ligera para mejorar la precisión en gestos más complejos.

Las barreras de implementación incluyen la falta de alfabetización digital en ciertos usuarios, posibles retos legales en entornos clínicos y limitaciones presupuestarias para implementación masiva. Para mitigarlas, se contempla un modelo de distribución open source y una guía técnica accesible.

Signotec representa una alternativa robusta, escalable y de alta aplicabilidad en contextos de inclusión tecnológica.

## 4.- EL. IEE. Análisis de mercado

## 5.- EL. IEE. Propiedad intelectual

## 6.- EL. IEE. Fuentes consultadas

- OpenCV Documentation – https://docs.opencv.org  
- Documentación oficial de MediaPipe y ejemplos de implementación de Hands Tracking  
- Tutoriales oficiales de Python para OpenCV  
- Organización Mundial de la Salud (OMS). https://www.who.int/es/news-room/fact-sheets/detail/deafness-and-hearing-loss#:~:text=M%C3%A1s%20del%205%C2%A0,una%20de%20cada%20diez  
- DataIntelo – Global Sign Language Translator Market Report. https://dataintelo.com/report/global-sign-language-translator-market#:~:text=The%20global%20sign%20language%20translator,of



## 7.- EL. IEE. Resumen

### Resumen

**Signotec** es un sistema multiplataforma de visión artificial e IA ligera que traduce gestos de lenguaje de señas en texto o audio en tiempo real, sin requerir hardware especializado. Utiliza cámaras convencionales y algoritmos de segmentación en HSV, filtrado morfológico, detección de contornos y análisis de convexidades para inferir posiciones de dedos y palmas. Su arquitectura basada en OpenCV y MediaPipe garantiza un rendimiento constante en Windows, Linux, macOS y dispositivos embebidos (por ejemplo, Raspberry Pi).

La propuesta responde a la necesidad de más de 430 millones de personas con pérdida auditiva en el mundo (OMS, 2021) y aprovecha un mercado global de interfaces sin contacto proyectado en USD 1.5 mil millones para 2032 (TCAC 10–15 %). Signotec ofrece calibración automática de iluminación y tono de piel, permite personalizar hasta 20 gestos, y exporta salidas como texto, comandos y síntesis de voz. Estas características satisfacen la demanda de soluciones accesibles, plug-and-play y de bajo costo en ámbitos educativos, médicos, industriales y domésticos.

El proyecto se validará mediante sesiones de Design Thinking y talleres con expertos para construir el Mapa de Propuesta de Valor de Osterwalder, garantizando la alineación de atributos técnicos con las expectativas reales de los usuarios. Bajo licencia GPL v3, fomenta la colaboración comunitaria, mientras que los servicios de soporte, mantenimiento y consultoría se protegen con contratos profesionales. Signotec constituye una herramienta escalable, inclusiva y de alto impacto social, que democratiza la comunicación y promueve la autonomía de personas con discapacidad auditiva.

