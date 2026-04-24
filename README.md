# 2 - DATA AUGMENTATION

Como se puede ver en la primera parte, las muestras no están equilibradas, es decir, que hay una gran diferencia de muestras de las distintas etiquetas. ([text](https://www.geeksforgeeks.org/machine-learning/handling-imbalanced-data-for-classification/))

A consecuencia de esto el modelo puede presentar varios problemas:

- El modelo se comporta mejor prediciendo las clases mayoritarias y peor para las menoritarias.
- Esto lleva a pérdida de precisión.
- Los modelos de ML tienden a tener prejuicios hacia la clase mayoritaria y la predice más frecuentemente.
- Las clases minoritarias pueden ser tratadas como ruido.
- La precisión se ve afectada porque el modelo se comporta bien solo con las clases dominantes.
- Los límites de decisión sesgados dan lugar a una generalización deficiente y a un rendimineto débil en las predicciones de la clase minoritaria.

## Técnicas para manejar los datos desbalanceados

1. Usar mejores métricas de evaluación
    - La exactitud (accuracy) no es una métrica confiable para datasets desbalanceados, en su lugar Recall y F1-score.
    - $$F1 = \frac{2 \cdot Precision \cdot Recall}{Precision + Recall}$$
    - Precision mide cuántos positivos predichos son realmente correctos.
    - Recall mide cuántos de los positivos reales ha identificado el modelo correctamente.
    - F1-score es la media armónica de precision y recall, muy usada en dataset desbalanceados.
2. **Remuestreo**
    - Ajusta el tamaño de las clases para hacerlas más balanceadas.
    - **Oversampling**: duplica o genera instancias de clases minoritarias para ayudar al modelo a aprender más patrones. (Este es el que se usa en la parte 2) Tiene riego de overfitting
    - Undersampling: elimina ejemplos de la clases mayoritarias para balancear el dataset y dar la misma importancia a todas las clases. Esto tiene el riesgo de pérdida de información relevante.
3. Clasificador Balanced Bagging
    - El Balanced Bagging Classifier es una técnica de ensemble utilizada para manejar conjuntos de datos desbalanceados. Funciona de manera similar al Bagging, pero equilibra cada muestra bootstrap para que las clases minoritarias no sean ignoradas durante el entrenamiento.
    - Los modelos estándar tienden a favorecer la clase mayoritaria, lo que provoca un bajo rendimiento en las predicciones de la clase minoritaria. El Balanced Bagging Classifier soluciona este problema realizando un remuestreo interno de los datos.
4. Synthetic Minority Oversampling Technique (SMOTE)
   - SMOTE es una técnica a nivel de dato usada para manejar datasets desbalanceados creando nuevos ejemplos sintéticos para las clases minoritarias en lugar de duplicar los existentes.
   - Utiliza métodos de interpolación entre los k-nn de un punto.
5. Otros.
   - En la web del enlace hay más métodos.

## Técnicas propuestas por el subject:
1. Flip (voltear)
2. Rotate (rotar)
3. Skew (inclinar)
4. Shear (cizallar, desplazar capas)
5. Crop  (recortar)
6. Distorsion (distorsión, deformar irregularmente)

con ejemplos de:
- Rotation
- Blur
- Contrast
- Scaling
- Illumination
- Projective

### Rotation
- Para girar un ángulo $\theta$ se multiplican las coordenadas del píxel por la matriz de rotación M

$$ M = \begin{pmatrix} cos(\theta) & -sin(\theta) \\ sin(\theta) & cos(\theta) \end{pmatrix} $$

- OpenCV permite rotación escalable con el centro (x,y) ajustable, siendo la mantriz de rotación 

$$ M = \begin{pmatrix} \alpha & \beta & (1-\alpha) · x - \beta·y \\ -\beta & \alpha & \beta·x + (1-\alpha)·y \end{pmatrix} $$
donde
$$ \alpha = escala · cos\theta \\
\beta = escala · sin\theta $$

### Flip
- Voltea la imagen en horizontal, en vertical o ambos
- Para indicar en qué eje se espcifica el flip_code, que se elige al azar entre -1, 0 y 1, siendo 0 giro alrededor del eje X, 1 (cualquier número positivo) giro alrededor del eje Y y -1 (cualquier número negativo) alrededor de ambos ejes.

### Blur
- Hay varios tipos de suavizados aplicables: 
  - Medio
  - Gaussiano
  - Mediano
  - Bilateral.
- Cambian en cómo ponderan la importancia de los píxeles vecinos del central.
- Se especifica el tamaño del kernel, que es la zona cercana que se toma como referencia.
- Cada tipo de blur pondera de forma diferente los píxeles del kernel.
- El kernel tiene dimensiones impares (ancho y alto) ya que toma los $\frac{m-1}{2}$ píxeles alrededor del píxel cental.
- cv2.blur() pondera todos los píxeles del kernel por igual haciendo la media. $n = \frac{m-1}{2}$ (radio alrededor del píxel central)
$$ K = \frac{1}{n^2} \begin{pmatrix} 1 & 1 & 1 \\ 1 & 1 & 1  \\ 1 & 1 & 1 \end{pmatrix} $$
- cv2.GaussianBlur() también promedia un vecindario, pero con pesos según una distribución gaussiana: el centro pesa más, y los vecinos lejanos pesan menos. Genera un suavizado más natural y no causa tanta distorsión en los bordes.

$$ G(x,y)=\frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}​ $$

- Mediano: toma la mediana de los píxeles vacinos y sustituye el central con este valor. Útil cuando hay ruido de "sal y pimienta".
- Bilateral: es como gaussiana pero teniendo en cuenta la similitud de los colores dando más peso a los píxeles más semejantes al central.

### Skew
- Desplaza filas o columnas de píxeles de forma lineal creando formas trapezoidales.
- Se elige aleatoriamente si el desplazamiento de los píxeles se hace en horizontal o en vertical y la intensidad de la deformación generada. Los valores 0.1 a 0.3 han sido obtenidos por tanteo.

### Shear
- Matemáticamente es lo mismo que el anterior, pero en esta ocasión se hace que también haya deformación en las dos direcciones simultáneamente auque con diferentes valores.
- Las elecciones también se hacen de forma aleatoria.
- Para evitar que si el desplazamiento es hacia la parte no visible de la imagen, se aplica una traslación en el sentido contrario para evitar que se oculte la imagen demasiado. Los desplazamientos los marca los valores $tx$ y $ty$.

