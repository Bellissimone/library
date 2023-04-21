import BoundPathGenerator
from BoundPathGenerator import BoundPathGenerator as b

coo1 = (14.214380353256928, 42.466981383166086)
coo2 = (14.211496555923873, 42.470460983110144)
constraint = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                    [
                        [
                            14.21312407787255,
                            42.469476780236505
                        ],
                        [
                            14.212376297517693,
                            42.46821135380216
                        ],
                        [
                            14.214883561062578,
                            42.46793014445399
                        ],
                        [
                            14.215719315576393,
                            42.469022527536964
                        ],
                        [
                            14.214429027904515,
                            42.47023386074369
                        ],
                        [
                            14.21312407787255,
                            42.469476780236505
                        ]
                    ]
                ],
                "type": "Polygon"
            }
        }
x = b(constraint, b.MODE_CYCLING_ROAD).get_bound_path(coo1, coo2)
print(x)