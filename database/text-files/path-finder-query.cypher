
// the two CALL methods could be done on the python side
// the first match finds the starting node (its a node on a bikepath I like)
// in order to find cycles match p for (start)...(start)

// this returns query exactly 15 hop paths
// could do [:Way*3..15] for paths between 3 and 15 hops
// the more paths the exponentially higher the runtime

// p is a list of nodes and edges before being separated by builtin nodes(p) and relationships(p)

match (start:Node {id: "2815578994"}) // pick a point on keilor
match p = (start)-[:Way*15]-(:Node) // get a path
CALL { // calculate distnace of p
    with p
    UNWIND relationships(p) as w
    with sum(w.dist) as d
    return d
}
CALL { // calculate # of bike segments in path
    with p
    UNWIND relationships(p) as w
    with w as W
    where W.pathType = "bike"
    with count(W) as c
    return c
}
with *, nodes(p) AS nodes
with *, relationships(p) as ways
return c, d, nodes, ways
order by d
