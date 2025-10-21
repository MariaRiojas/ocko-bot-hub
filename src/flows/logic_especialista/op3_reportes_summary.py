# src/flows/logic_especialista/op3_reportes_summary.py

def process_reportes_summary():
    """Opción 3: Muestra un resumen de los reportes comunitarios recibidos."""
    
    # Nota: En un entorno real, esto consultaría la base de datos de reportes generados por el Comunero (Opción 3)
    
    reportes_pendientes = 4
    reportes_en_revision = 2
    
    return (
        f"📝 *RESUMEN DE REPORTES COMUNITARIOS*\n"
        f" - **{reportes_pendientes}** Reportes Pendientes de Revisión.\n"
        f" - **{reportes_en_revision}** Reportes en Proceso (Asignados).\n\n"
        f"Últimos Reportes (Ej: RPT-2025-45, RPT-2025-46).\n"
        f"Acción: Ingrese el número de reporte para ver foto, ubicación y observación."
    )