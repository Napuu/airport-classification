geojson to shapefile (helps at exporting stuff to earthengine)
ogr2ogr -nlt POINT -skipfailures OUTPUT.shp INPUT.json OGRGeoJSON
