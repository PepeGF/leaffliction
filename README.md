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
