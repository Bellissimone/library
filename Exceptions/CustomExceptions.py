class GeoJsonTypeError(Exception):
    """ Quando il valore type del GeoJson non corrisponde a feature viene lanciato l'errore """
    pass


class GeoJsonGeometryTypeError(Exception):
    """ Quando la geometria contenuta nel GeoJson non risulta essere quella del formato standard (www.Geojson.org)
    viene lanciato l'errore """
    pass


class AddressValueError(Exception):
    """ Quando viene inserito un indirizzo di partenza/arrivo che non sia una TUPLA di coordinate (longitudine,
    latitudine) o una stringa contenente la via viene lanciato l'errore """
    pass


class ConstantValueError(Exception):
    """ Quando viene inserito un valore non compreso tra 1 e 1.5 viene lanciato l'errore """
    pass
