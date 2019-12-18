from api import get_friends
import time
import igraph


def get_network(users_ids, as_edgelist=True):
    t = 0
    friend_list = get_friends(users_ids, 'bdate')
    edges = []
    matrix = [[0] * len(friend_list)] * len(friend_list)

    for user_1 in range(len(friend_list)):
        friends = get_friends(friend_list[user_1]['id'], 'bdate')
        t += 1
        for user_2 in range(user_1 + 1, len(friend_list)):
            if friend_list[user_2] in friends:
                matrix[user_2][user_1] = 1
                matrix[user_1][user_2] = 1
                if as_edgelist:
                    edges.append((user_1, user_2))
        if t == 3:
            time.sleep(1)
            t = 0

    if as_edgelist:
        return edges
    return matrix


def plot_graph(user_id):
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id, True)

    draf = igraph.Graph(vertex_attrs={"shape": "circle", "label": vertices, "size": 10},
                        edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": draf.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }

    draf.simplify(multiple=True, loops=True)
    clusters = draf.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    draf.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(draf, **visual_style)


if __name__ == '__main__':
    plot_graph(83798048)