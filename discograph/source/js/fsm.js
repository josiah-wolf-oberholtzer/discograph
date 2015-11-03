var DiscographFSM = new machina.Fsm({
    initialize: function(options) {},
    namespace: 'discograph',
    initialState: 'viewing-graph',
    states: {
        'viewing-graph': {
            '_onEnter': function() {}
            '_onExit': function() {}
            'request-graph': function() {}, 
            'request-random': function() {}, 
            'show-radial': function() {}, 
            },
        'viewing-radial': {
            '_onEnter': function() {}
            '_onExit': function() {}
            'request-graph': function() {}, 
            'request-random': function() {}, 
            'show-graph': function() {}, 
            },
        'requesting-graph': {
            '_onEnter': function() {}
            '_onExit': function() {}
            'errored': function() {},
            'received-graph': function() {},
            },
        'requesting-random': {
            '_onEnter': function() {}
            '_onExit': function() {}
            'errored': function() {},
            'received-random': function() {},
            },
        'requesting-radial': {
            '_onEnter': function() {}
            '_onExit': function() {}
            'errored': function() {},
            'received-timeline': function() {},
            },
        'errored': {
            'show-graph': function() {},
            },
    },
});