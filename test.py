from BoundPathGenerator import BoundPathGenerator as b

coo1 = "Via Don Giovanni Bosco, 13, Ortona, CH"
coo2 = (14.400661192897076, 42.35357837926156)
constraint_polygon = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              14.40115513592292,
              42.351707600345094
            ],
            [
              14.40044509282265,
              42.35097752517484
            ],
            [
              14.400969907288214,
              42.350121957542854
            ],
            [
              14.402621529280594,
              42.34992802726089
            ],
            [
              14.403455058137325,
              42.35066952216877
            ],
            [
              14.403408750977746,
              42.35149086016378
            ],
            [
              14.40115513592292,
              42.351707600345094
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
constraint_point = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [
            14.40261381142264,
            42.34929489776334
        ],
        "type": "Point"
    }
}
constraint_line_string = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            14.402598375702894,
            42.34931771335138
          ],
          [
            14.402552068544708,
            42.350287368194046
          ],
          [
            14.402752732898307,
            42.351074488772525
          ],
          [
            14.40276816861811,
            42.35219241120319
          ]
        ],
        "type": "LineString"
      }
    }
x = b(constraint_point, b.MODE_CYCLING_ROAD).get_bound_path(coo1, coo2)
print(x)
