"""
Script para probar la función recortar_cara con imágenes reales.
"""
from app.utils.cut_out_face import cut_out_face as recortar_cara
from PIL import Image
import os
import time

def probar_todas_las_imagenes():
    """
    Prueba la función de recorte con todas las imágenes en test_images.
    """
    print("=== PRUEBA CON IMÁGENES REALES ===")
    
    # Directorio de imágenes
    test_dir = "test_images"
    results_dir = os.path.join(test_dir, "resultados")
    
    # Crear directorio de resultados
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"✓ Directorio de resultados creado: {results_dir}")
    
    # Extensiones de imagen soportadas
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
    
    # Buscar todas las imágenes
    imagenes = [f for f in os.listdir(test_dir) 
                if f.lower().endswith(extensiones) and not f.startswith('imagen_')]
    
    if not imagenes:
        print("❌ No se encontraron imágenes para probar")
        return
    
    print(f"📸 Encontradas {len(imagenes)} imágenes para probar")
    print("-" * 50)
    
    for i, nombre_imagen in enumerate(imagenes, 1):
        ruta_imagen = os.path.join(test_dir, nombre_imagen)
        print(f"\n[{i}/{len(imagenes)}] Procesando: {nombre_imagen}")
        
        try:
            # Cargar imagen
            imagen = Image.open(ruta_imagen)
            print(f"  ✓ Imagen cargada: {imagen.size} - {imagen.mode}")
            
            # Medir tiempo de procesamiento
            inicio = time.time()
            resultado = recortar_cara(imagen)
            tiempo = time.time() - inicio
            
            if resultado:
                # Guardar resultado
                nombre_sin_ext = os.path.splitext(nombre_imagen)[0]
                ext = os.path.splitext(nombre_imagen)[1]
                nombre_resultado = f"recorte_{nombre_sin_ext}{ext}"
                ruta_resultado = os.path.join(results_dir, nombre_resultado)
                
                resultado.save(ruta_resultado)
                
                # Mostrar estadísticas
                print(f"  ✓ Procesado en {tiempo:.2f}s")
                print(f"  ✓ Original: {imagen.size}")
                print(f"  ✓ Recortado: {resultado.size}")
                
                # Verificar si se detectó cara
                if resultado.size == imagen.size:
                    print(f"  ⚠️  No se detectaron caras - imagen sin cambios")
                else:
                    print(f"  🎯 ¡Cara detectada y recortada!")
                    
                    # Calcular reducción de tamaño
                    area_original = imagen.size[0] * imagen.size[1]
                    area_recorte = resultado.size[0] * resultado.size[1]
                    reduccion = (1 - area_recorte/area_original) * 100
                    print(f"  📊 Reducción de área: {reduccion:.1f}%")
                
                print(f"  💾 Guardado: {ruta_resultado}")
                
            else:
                print(f"  ❌ Error: La función devolvió None")
                
        except Exception as e:
            print(f"  ❌ Error procesando {nombre_imagen}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*50)
    print("🎉 ¡Prueba completada!")
    print(f"📁 Resultados guardados en: {results_dir}")
    
    # Mostrar resumen de archivos creados
    resultados = [f for f in os.listdir(results_dir) if f.startswith('recorte_')]
    print(f"📸 {len(resultados)} imágenes procesadas guardadas")

def mostrar_comparacion():
    """
    Muestra una comparación de tamaños antes y después.
    """
    print("\n=== COMPARACIÓN DE TAMAÑOS ===")
    
    test_dir = "test_images"
    results_dir = os.path.join(test_dir, "resultados")
    
    if not os.path.exists(results_dir):
        print("❌ No hay resultados para comparar")
        return
    
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
    originales = [f for f in os.listdir(test_dir) 
                 if f.lower().endswith(extensiones) and not f.startswith('imagen_')]
    
    print(f"{'Imagen Original':<20} {'Tamaño Original':<15} {'Tamaño Recorte':<15} {'Cambio'}")
    print("-" * 70)
    
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
                
                if img_original.size == img_recorte.size:
                    cambio = "Sin cambio"
                else:
                    cambio = "✓ Recortada"
                
                print(f"{original:<20} {str(img_original.size):<15} {str(img_recorte.size):<15} {cambio}")
            else:
                print(f"{original:<20} {str(img_original.size):<15} {'No procesada':<15} {'Error'}")
                
        except Exception as e:
            print(f"{original:<20} {'Error':<15} {'Error':<15} {str(e)[:20]}")

if __name__ == "__main__":
    probar_todas_las_imagenes()
    mostrar_comparacion()
