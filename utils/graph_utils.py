import sys
import json

###############################
# WRITE GRAPH TO FILE FORMATS #
###############################
# Write to .json
def write_json(graph, fname):
    output_fname = fname + ".json"
    json_graph = dict()
    json_graph['nodes'] = {'name': n for n in graph['nodes']}
    # 'source': 0, 'target': 0, 'value': 0
    json_graph['links'] = [{'source': graph['edges'][k][0], 'target': graph['edges'][k][1], 'value': graph['edges'][k][2]} for k in range(len(graph['edges']))]
    with open(output_fname, "w+") as fout:
        json.dump(json_graph, fout)
    return output_fname

# Write to .gexf
def write_gexf(graph, fname):
    output_fname = fname + ".gexf"
    print("Generating .gexf file for graph with {} Nodes | {} Edges".format(len(graph['nodes']), len(graph['edges'])))
    # Write Actual file in proper format
    gexf_header = """<?xml version="1.0" encoding="UTF-8"?>
    <gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
        <meta lastmodifieddate="2009-03-20">
            <creator>devYaoYH</creator>
            <description>Linguistic Association Network Graph</description>
        </meta>
        <graph mode="static" defaultedgetype="undirected">
            <nodes>"""
    gexf_footer = """            </edges>
        </graph>
    </gexf>"""
    with open(output_fname, "w+") as fout:
        fout.write(gexf_header)
        # Extract All Nodes Information
        for i, node in enumerate(graph['nodes']):
            fout.write("                <node id=\"{}\" label=\"{}\" />\n".format(i, node))
        fout.write("            </nodes>\n            <edges>\n")
        # Extract All Edges Information
        for i, tup in enumerate(graph['edges']):
            source, target, value = tup
            fout.write("                <edge id=\"{}\" source=\"{}\" target=\"{}\" />\n".format(i, source, target))
        fout.write(gexf_footer)
    return output_fname

# Raw unit edge format
def write_raw(graph, fname):
    output_fname = fname + ".graph"
    with open(fname + ".graph", "w+") as fout:
        for source, target, value in graph['edges']:
            fout.write(f"{graph['nodes'][source]},{graph['nodes'][target]},{value}\n")
    return output_fname

def debug_json(graph, fname):
    output_fname = fname + "_log.json"
    with open(output_fname, "w+") as fout:
        json.dump(graph, fout)
    return output_fname