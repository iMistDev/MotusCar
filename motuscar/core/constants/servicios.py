# carga de servicios para mecanicos
TIPOS = [
    ('taller', 'Taller'),
    ('particular', 'Particular'),
]
ESPECIALIDAD = [
    ('lubricentro', 'Lubricentro'),
    ('electrico', 'Eléctrico'),
    ('vulcanizacion', 'Vulcanización'),
    ('mecanica', 'Mecánica'),
    ('pintura', 'Pintura'),
]
SERVICIOS_POR_ESPECIALIDAD = {
    'lubricentro': [
        'Cambio de aceite',
        'Cambio de filtro de aire'
    ],
    'electrico': [
        'Revisión de sistema eléctrico',
        'Cambio de batería'
    ],
    'vulcanizacion': [
        'Parche de neumático',
        'Cambio de neumático'
    ],
    'mecanica': [
        'Revisión de frenos',
        'Alineación y balanceo'
    ],
    'pintura': [
        'Pintado de parachoques',
        'Pintado completo'
    ]
}