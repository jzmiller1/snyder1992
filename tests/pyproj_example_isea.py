from pyproj import CRS, Transformer
crs_4326 = CRS("EPSG:4326")
crs_isea = CRS("+proj=isea +orient=pole +R=6378137")

transformer_isea = Transformer.from_crs(crs_4326, crs_isea)

wgs84_coord = [52.6226386, -144.0]
snyder = transformer_isea.transform(*wgs84_coord)

print(wgs84_coord)
print(snyder[0]/0.91038328153090290025, snyder[1]/0.91038328153090290025)
print(snyder[0], snyder[1])
print(crs_isea.get_geod())

