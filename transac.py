import requests
from lib import graph, queue
from graphviz import Source
import sys

def get_transactions(address):
    """
    Returns the list of addresses that have performed an outbound transaction

    """
    tmp = []
    result = []
    url = f"https://blockstream.info/api/address/{address}/txs"
    response = requests.get(url)
    if not response.ok:
        print("Connexion error")
        return []
    data = response.json()
    for txid in data:
        for transaction in txid["vout"]:
            try:
                destination = transaction["scriptpubkey_address"]
                if address == destination:
                    tmp = []
                    break
                else:
                    if not destination in result:
                        tmp.append(transaction["scriptpubkey_address"])
            except:
                pass
        result+=tmp
        tmp = []


    return result


def build_graph(G, address, loop):
    """
    Create an oriented graph with all the connected addresses

    """
    q = queue.Queue()
    q.enqueue(address)
    q.enqueue(None)
    while not q.isempty():
        x = q.dequeue()

        if x == None:
            if loop == 0:
                return G
            if not q.isempty():
                q.enqueue(None)
                loop -= 1
        else:
            add_list = get_transactions(x)
            for add in add_list:
                if not add in G.labels:
                    G.addvertex(1, add)
                    q.enqueue(add)
                G.addedge(G.labels.index(x), G.labels.index(add))

    return G


def start(address, depth=2, filename='output'):
    G = graph.Graph(1, True, [address])
    G = build_graph(G, address, depth)
    s = graph.todot(G)
    g = Source(s)
    g.render(filename, format='pdf')


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 1:
        print("\nUsage : main.py your_btc_add depth (optionnal) output_file_name (optionnal)\n\nthe default depth is 3\nthe default file name is 'output.pdf'")
    else:
        if argc == 3:
            start(sys.argv[1], int(sys.argv[2]))
        elif argc == 4:
            start(sys.argv[1], int(sys.argv[2]), sys.argv[3])
        else:
            start(sys.argv[1])
