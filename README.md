# Practica3_MSR
## Gráfica posición de ruedas vs tiempo:
<img width="1920" height="1080" alt="Pos_Ruedas_Tiempo" src="https://github.com/user-attachments/assets/677c7b35-fe76-40b3-978d-3ba56e960b2a" />
La gráfica muestra la evolución de la posición angular de las ruedas obtenida desde el topic joint_states mientras el robot realizaba la misión de recoger y mover los cubos y finalmente avanzar 10 m. Cada línea corresponde a una rueda distinta, que parecen dos lineas debido a que las ruedas de cada lado avanzan de igual manera superponiendose las lineas, y los cambios en las curvas reflejan los movimientos del robot: tramos planos indican que estuvo detenido o manipulando los cubos, subidas suaves corresponden a desplazamientos hacia delante y las diferencias grandes entre ruedas aparecen cuando el robot gira o se reorienta, ya que en esos momentos unas ruedas giran más que otras e incluso algunas pueden hacerlo en sentido contrario, produciendo valores negativos. Por eso al final se observan cambios más bruscos, asociados a los giros necesarios para completar las maniobras antes del avance recto final.

## Gráfica aceleración vs tiempo:
<img width="1920" height="1080" alt="Aceleracion_Tiempo" src="https://github.com/user-attachments/assets/7ef95b67-2535-4640-afb3-b2c780c34ab2" />
La gráfica muestra la aceleración total medida por la IMU a lo largo del tiempo, calculada a partir de las aceleraciones en los tres ejes (X, Y y Z). Para obtener esta aceleración total se combinan las componentes. Los valores relativamente bajos y estables corresponden a momentos en los que el robot estaba detenido o moviéndose suavemente, mientras que los numerosos picos aparecen durante las maniobras de giro, aceleraciones, frenadas y cambios bruscos de dirección realizados al recoger y colocar los cubos. Los picos más altos del final se deben probablemente a movimientos rápidos, vibraciones mecánicas, correcciones fuertes de trayectoria o pequeñas sacudidas del robot al girar sobre sí mismo, ya que la IMU es muy sensible a cambios repentinos de movimiento y orientación. Explicando las tres variaciones iniciales, la primera es cuando avanzamos a coger el cubo verde, la segunda cuando giramos a coger el cubo azul, y la tercera variación pequeña es cuando giramos a dejar el cubo azul encima del rojo, ya después todas las variaciones y cambios bruscos se deben a los giros y avances para llegar a los 10 metros.

## Gráfica de gasto vs tiempo: 
<img width="1920" height="1080" alt="Grafica_Joint_Tiempo" src="https://github.com/user-attachments/assets/4061d166-e4ed-4f44-84c1-ec332ccb316d" />
La gráfica representa la evolución de la fuerza/esfuerzo aplicado en el brazo y el gripper durante toda la maniobra. Los distintos niveles y tramos estables corresponden a momentos en los que el brazo adopta posiciones concretas para recoger, transportar y colocar los cubos, mientras que las variaciones y pequeños picos aparecen cuando el manipulador realiza movimientos de ajuste o sujeta los objetos. En la parte final se observan cambios mucho más bruscos y picos de gran magnitud debido a los giros y aceleraciones realizados por la base móvil durante el desplazamiento final y las reorientaciones del robot. Estos movimientos generan inercias y desplazamientos en el brazo, por lo que el sistema de control aplica fuerzas mayores para compensarlos y mantener el brazo y el gripper en la posición deseada, provocando así las oscilaciones y picos visibles en la gráfica.

## Imagen sujetando el cubo verde en el aire:
<img width="1863" height="1007" alt="Captura desde 2026-05-07 18-27-20" src="https://github.com/user-attachments/assets/6aad3f85-901c-4b20-b12d-39f1a3c981c3" />

## Imagen a  punto de colocar el cubo azul en sobre el rojo:
<img width="1920" height="1080" alt="rojoencimaazul" src="https://github.com/user-attachments/assets/6e124070-95f5-4ea1-b4bd-f8d995370201" />

## Imagen TF:
[Enlace para la descarga](https://github.com/user-attachments/files/27488058/tf.pdf) 
<img width="1697" height="920" alt="Captura desde 2026-05-07 17-56-42" src="https://github.com/user-attachments/assets/628c823f-b627-4dae-b5e5-d2c13d72c3db" />

## Imagen RVIZ de Joint State Publisher
<img width="1863" height="1007" alt="Captura desde 2026-05-07 18-18-35" src="https://github.com/user-attachments/assets/932dfc27-48e9-4d46-9a2e-323b6fc82402" />


## Enlace descarga ROSBAG:
https://drive.google.com/file/d/1v_vWztG4xynhkGLdQVnlzI2oNfzhqpLa/view?usp=drive_link







