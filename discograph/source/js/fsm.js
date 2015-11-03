var DiscographFsm = machina.Fsm.extend({
    initialize: function(options) {},
    namespace: 'discograph',
    initialState: 'uninitialized',
    states: {
        'uninitialized': {
            'request-network': function(entityKey) {
                this.requestNetwork(entityKey);
            },
            'request-random': function() {
                this.requestRandom();
            },
        },
        'viewing-network': {
            '_onEnter': function() {
                this.toggleNetwork(true);
            },
            '_onExit': function() {
                this.toggleNetwork(false);
            },
            'request-network': function(entityKey) {
                this.requestNetwork(entityKey);
            },
            'request-random': function() {
                this.requestRandom();
            },
            'show-radial': function() {
                if (dg.network.pageData.selectedNodeKey) {
                    this.requestRadial(dg.network.pageData.selectedNodeKey);
                }
            },
            'select-entity': function(entityKey) {
                dg_network_selectNode(entityKey);
            },
        },
        'viewing-radial': {
            '_onEnter': function() {
                d3.select('#timelineLayer').remove();
                dg_timeline_chartRadial();
            },
            '_onExit': function() {
                d3.select('#timelineLayer').remove();
            },
            'request-network': function(entityKey) {
                this.requestNetwork(entityKey);
            },
            'request-random': function() {
                this.requestRandom();
            },
            'show-network': function() {
                this.transition('viewing-network');
            },
        },
        'requesting': {
            '_onEnter': function(fsm, entityKey, pushHistory) {
                this.toggleLoading(true);
            },
            '_onExit': function() {
                this.toggleLoading(false);
            },
            'errored': function(error) {
                this.handleError(error);
            },
            'received-network': function(data, pushHistory, params) {
                var params = {'roles': $('#filter select').val()};
                var key = data.center.key;
                dg.network.data.json = JSON.parse(JSON.stringify(data));
                document.title = 'Disco/graph: ' + data.center.name;
                $(document).attr('body').id = key;
                if (pushHistory === true) {
                    dg_history_pushState(key, params);
                }
                dg.network.data.pageCount = data.pages;
                dg.network.pageData.currentPage = 1;
                if (1 < data.pages) {
                    $('#paging').fadeIn();
                } else {
                    $('#paging').fadeOut();
                }
                dg_network_processJson(data);
                dg_network_selectPage(1);
                dg_network_startForceLayout();
                dg_network_selectNode(dg.network.data.json.center.key);
                this.transition('viewing-network');
            },
            'received-random': function(data) {
                this.requestNetwork(data.center, true);
            },
            'received-radial': function(data) {
                dg.timeline.data = data;
                dg.timeline.byYear = d3.nest()
                    .key(function(d) { return d.year; })
                    .key(function(d) { return d.category; })
                    .entries(data.results);
                dg.timeline.byRole = d3.nest()
                    .key(function(d) { return d.role; })
                    .rollup(function(leaves) { return leaves.length; })
                    .entries(dg.timeline.data.results);
                this.transition('viewing-radial');
            },
        },
    },
    handleError: function(error) {
        var message = 'Something went wrong!';
        var status = error.status;
        if (status == 0) {
            status = 404;
        } else if (status == 429) {
            message = 'Hey, slow down, buddy. Give it a minute.'
        }
        var text = [
            '<div class="alert alert-danger alert-dismissible" role="alert">',
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">',
            '<span aria-hidden="true">&times;</span>',
            '</button>',
            '<strong>' + status + '!</strong> ' + message,
            '</div>'
            ].join('');
        $('#flash').append(text);
        this.transition('viewing-network');
    },
    getNetworkURL: function(entityKey) {
        var entityType = entityKey.split('-')[0];
        var entityId = entityKey.split('-')[1];
        var url = '/api/' + entityType + '/network/' + entityId;
        var params = {'roles': $('#filter select').val()};
        if (params.roles) {
            url += '?' + decodeURIComponent($.param(params));
        }
        return url;
    },
    getRandomURL: function() {
        return '/api/random?' + Math.floor(Math.random() * 1000000);
    },
    getRadialURL: function(entityKey) {
        var entityType = entityKey.split("-")[0];
        var entityId = entityKey.split("-")[1];
        return '/api/' + entityType+ '/timeline/' + entityId;
    },
    requestNetwork: function(entityKey, pushHistory) {
        this.transition('requesting');
        var self = this;
        d3.json(this.getNetworkURL(entityKey), function(error, data) {
            if (error) {
                this.handleError(error);
            } else {
                self.handle('received-network', data, pushHistory);
            }
        });
    },
    requestRadial: function(entityKey) {
        this.transition('requesting');
        var self = this;
        d3.json(this.getRadialURL(entityKey), function(error, data) {
            if (error) {
                this.handleError(error);
            } else {
                self.handle('received-radial', data);
            }
        });
    },
    requestRandom: function() {
        this.transition('requesting');
        var self = this;
        d3.json(this.getRandomURL(), function(error, data) {
            if (error) {
                this.handleError(error);
            } else {
                self.handle('received-random', data);
            }
        });
    },
    selectEntity: function(entityKey) {
        dg_network_selectNode(entityKey);
    },
    selectNextPage: function() {
        dg_network_selectPage(dg_network_getNextPage());
    },
    selectPreviousPage: function() {
        dg_network_selectPage(dg_network_getPrevPage());
    },
    selectPage: function(page) {
        dg_network_selectPage(page);
    },
    showNetwork: function() {
        this.handle('show-network');
    },
    showRadial: function() {
        this.handle('show-radial');
    },
    toggleNetwork: function(status) {
        if (status) {
            if (1 < dg.network.data.json.pages) {
                $('#paging').fadeIn();
            } else {
                $('#paging').fadeOut();
            }
            dg.network.layers.root.transition()
                .delay(250)
                .duration(1000)
                .style('opacity', 1)
                .each('end', function(d, i) {
                    dg.network.layers.link.selectAll('.link')
                        .classed('noninteractive', false);
                    dg.network.layers.node.selectAll('.node')
                        .classed('noninteractive', false);
                    dg.network.forceLayout.start()
                });
        } else {
            $('#paging').fadeOut();
            dg.network.forceLayout.stop()
            dg.network.layers.root.transition()
                .duration(250)
                .style('opacity', 0.333);
            dg.network.layers.link.selectAll('.link')
                .classed('noninteractive', true);
            dg.network.layers.node.selectAll('.node')
                .classed('noninteractive', true);
        }
    },
    toggleLoading: function(status) {
        if (status) {
            var input = dg_loading_makeArray();
            var data = input[0], extent = input[1];
            $('#page-loading')
                .removeClass('glyphicon-random')
                .addClass('glyphicon-animate glyphicon-refresh');
        } else {
            var data = [], extent = [0, 0];
            $('#page-loading')
                .removeClass('glyphicon-animate glyphicon-refresh')
                .addClass('glyphicon-random');
        }
        dg_loading_update(data, extent);
    },
});

dg.fsm = new DiscographFsm();