from graph import *

def main():
    g = FlowNetwork()
    [g.add_vertex(v) for v in ["s", "v1", "v2", "v3", "v4", "t"]]
    g.add_edge('s','v1', 16)
    g.add_edge('s','v2', 13)
    g.add_edge('v1','v2', 10)
    g.add_edge('v2','v1', 4)
    g.add_edge('v1','v3', 12)
    g.add_edge('v3','v2', 9)
    g.add_edge('v2','v4', 14)
    g.add_edge('v4','v3', 7)
    g.add_edge('v3','t', 20)
    g.add_edge('v4','t', 4)
    print g.max_flow('s','t')

main()
