from datetime import date
from datetime import timedelta


def get_lunes_semana(fecha: date):
    """
    Get Monday of the week.
    """
    fecha = fecha - timedelta(days=fecha.weekday())
    return fecha


def get_rango_fechas(fecha_inicio: date):
    """
    Get range of dates.

    :param fecha_inicio: Start date.
    :return: List of dates.
    """
    fecha_fin = fecha_inicio + timedelta(days=6)
    
    rango_fechas = []
    
    while fecha_inicio <= fecha_fin:
        rango_fechas.append(fecha_inicio)
        fecha_inicio += timedelta(days=1)
    
    return rango_fechas
