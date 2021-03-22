MATCH (n:Node)
WITH n, distance(point({latitude:toFloat('53.509905'), longitude:toFloat('-113.541233')}), n.location )AS d
ORDER BY d
  LIMIT 1
RETURN n
