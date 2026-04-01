def get_bbox(features):
    min_lon = float('inf')
    min_lat = float('inf')
    max_lon = float('-inf')
    max_lat = float('-inf')
    
    for feature in features:
        bounded_by = feature["properties"].get('boundedBy')
        point1, point2 = bounded_by
        
        min_lon = min(min_lon, point1[0], point2[0])
        min_lat = min(min_lat, point1[1], point2[1])
        max_lon = max(max_lon, point1[0], point2[0])
        max_lat = max(max_lat, point1[1], point2[1])
    
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    return {
        'center': f'{center_lon},{center_lat}',
        'bbox': f'{min_lon},{min_lat}~{max_lon},{max_lat}'
    }