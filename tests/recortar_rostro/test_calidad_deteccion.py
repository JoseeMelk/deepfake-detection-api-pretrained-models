"""
Script para crear un reporte visual de la calidad de detección de caras.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def crear_reporte_visual():
    """
    Crea un reporte visual mostrando las detecciones en las imágenes originales.
    """
    print("=== CREANDO REPORTE VISUAL ===")
    
    test_dir = "test_images"
    report_dir = os.path.join(test_dir, "reporte_visual")
    
    # Crear directorio de reporte
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        print(f"✓ Directorio de reporte creado: {report_dir}")
    
    # Extensiones de imagen soportadas
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
    
    # Buscar todas las imágenes
    imagenes = [f for f in os.listdir(test_dir) 
                if f.lower().endswith(extensiones) and not f.startswith('imagen_')]
    
    print(f"📸 Creando reporte para {len(imagenes)} imágenes")
    print("-" * 50)
    
    for i, nombre_imagen in enumerate(imagenes, 1):
        ruta_imagen = os.path.join(test_dir, nombre_imagen)
        print(f"\n[{i}/{len(imagenes)}] Analizando: {nombre_imagen}")
        
        try:
            # Cargar imagen original
            imagen_original = Image.open(ruta_imagen).convert("RGB")
            
            # Buscar imagen recortada correspondiente
            nombre_sin_ext = os.path.splitext(nombre_imagen)[0]
            ext = os.path.splitext(nombre_imagen)[1]
            nombre_recorte = f"recorte_{nombre_sin_ext}{ext}"
            ruta_recorte = os.path.join(test_dir, "resultados", nombre_recorte)
            
            if os.path.exists(ruta_recorte):
                imagen_recorte = Image.open(ruta_recorte)
                
                # Crear imagen de comparación lado a lado
                ancho_total = imagen_original.size[0] + imagen_recorte.size[0] + 20
                alto_total = max(imagen_original.size[1], imagen_recorte.size[1]) + 60
                
                imagen_comparacion = Image.new('RGB', (ancho_total, alto_total), 'white')
                
                # Pegar imagen original
                imagen_comparacion.paste(imagen_original, (10, 50))
                
                # Pegar imagen recortada
                x_recorte = imagen_original.size[0] + 20
                y_recorte = 50 + (imagen_original.size[1] - imagen_recorte.size[1]) // 2
                imagen_comparacion.paste(imagen_recorte, (x_recorte, y_recorte))
                
                # Agregar títulos
                draw = ImageDraw.Draw(imagen_comparacion)
                
                # Título para imagen original
                draw.text((10, 10), f"Original: {imagen_original.size}", fill='black')
                
                # Título para imagen recortada
                draw.text((x_recorte, 10), f"Recorte: {imagen_recorte.size}", fill='black')
                
                # Calcular estadísticas
                area_original = imagen_original.size[0] * imagen_original.size[1]
                area_recorte = imagen_recorte.size[0] * imagen_recorte.size[1]
                
                if area_recorte < area_original:
                    reduccion = (1 - area_recorte/area_original) * 100
                    estado = f"Cara detectada - Reducción: {reduccion:.1f}%"
                    color_estado = 'green'
                else:
                    estado = "Sin cambio - No se detectó cara"
                    color_estado = 'orange'
                
                # Agregar estado en la parte inferior
                draw.text((10, alto_total - 30), estado, fill=color_estado)
                
                # Guardar imagen de comparación
                nombre_reporte = f"reporte_{nombre_sin_ext}.png"
                ruta_reporte = os.path.join(report_dir, nombre_reporte)
                imagen_comparacion.save(ruta_reporte)
                
                print(f"  ✓ {estado}")
                print(f"  💾 Reporte guardado: {ruta_reporte}")
                
            else:
                print(f"  ❌ No se encontró imagen recortada")
                
        except Exception as e:
            print(f"  ❌ Error creando reporte para {nombre_imagen}: {e}")
    
    print(f"\n🎉 Reporte visual completado en: {report_dir}")

def analizar_calidad_deteccion():
    """
    Analiza la calidad de las detecciones basándose en el tamaño y proporción.
    """
    print("\n=== ANÁLISIS DE CALIDAD DE DETECCIÓN ===")
    
    test_dir = "test_images"
    results_dir = os.path.join(test_dir, "resultados")
    
    if not os.path.exists(results_dir):
        print("❌ No hay resultados para analizar")
        return
    
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
    originales = [f for f in os.listdir(test_dir) 
                 if f.lower().endswith(extensiones) and not f.startswith('imagen_')]
    
    print(f"{'Imagen':<20} {'Tamaño Cara':<12} {'% de Imagen':<12} {'Proporción':<12} {'Calidad'}")
    print("-" * 80)
    
    for original in originales:
        try:
            # Abrir imagen original
            ruta_original = os.path.join(test_dir, original)
            img_original = Image.open(ruta_original)
            
            # Buscar imagen recortada correspondiente
            nombre_sin_ext = os.path.splitext(original)[0]
            ext = os.path.splitext(original)[1]
            nombre_recorte = f"recorte_{nombre_sin_ext}{ext}"
            ruta_recorte = os.path.join(results_dir, nombre_recorte)
            
            if os.path.exists(ruta_recorte):
                img_recorte = Image.open(ruta_recorte)
                
                # Calcular métricas
                area_original = img_original.size[0] * img_original.size[1]
                area_recorte = img_recorte.size[0] * img_recorte.size[1]
                porcentaje = (area_recorte / area_original) * 100
                
                # Calcular proporción (aspecto ratio)
                proporcion = img_recorte.size[0] / img_recorte.size[1]
                
                # Evaluar calidad
                if img_original.size == img_recorte.size:
                    calidad = "Sin detección"
                elif 0.5 <= porcentaje <= 25 and 0.8 <= proporcion <= 1.3:
                    calidad = "✓ Excelente"
                elif 0.1 <= porcentaje <= 40 and 0.6 <= proporcion <= 1.6:
                    calidad = "✓ Buena"
                else:
                    calidad = "⚠️ Revisar"
                
                print(f"{original[:19]:<20} {str(img_recorte.size):<12} {porcentaje:>8.1f}%    {proporcion:>8.2f}     {calidad}")
                
            else:
                print(f"{original[:19]:<20} {'Error':<12} {'Error':<12} {'Error':<12} {'❌ Error'}")
                
        except Exception as e:
            print(f"{original[:19]:<20} {'Error':<12} {'Error':<12} {'Error':<12} {'❌ Error'}")

if __name__ == "__main__":
    crear_reporte_visual()
    analizar_calidad_deteccion()
