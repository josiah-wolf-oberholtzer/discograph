dg.network = {
    dimensions: [0, 0],
    forceLayout: null,
    isUpdating: false,
    newNodeCoords: [0, 0],
    data: {
        json: null,
        nodeMap: d3.map(),
        linkMap: d3.map(),
        maxDistance: 0,
        pageCount: 1,
        },
    pageData: {
        currentPage: 1,
        links: [],
        nodes: [],
        selectedNodeKey: null,
        },
    selections: {
        halo: null,
        hull: null,
        node: null,
        link: null,
        text: null,
        },
    layers: {
        root: null,
        halo: null,
        text: null,
        node: null,
        link: null,
        },
    };
