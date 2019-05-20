//initialize a topology component
var topo = new nx.graphic.Topology({
  width: 1000,
  height: 364,
  showIcon: false,
  nodeConfig: {
    label: 'model.name'
  }
});

nx.define("MyLayer", nx.graphic.Topology.Layer, {
  methods: {
    draw: function() {
      
      //
      var img = new nx.graphic.Image({
      	src:'http://127.0.0.1:5000/floor_image',
        x:0,
        y:0
      })
      
      // register topology event
      this.topology().on("zoomend", function() {
        this._update();
      }, this);
      this.topology().on("resetzooming", function() {
        this._update();
      }, this);
      // append to topology stage
      img.attach(this);
    },
    _update: function() {
      
    }
  }
});

//set data
topo.on('ready', function() {
  topo.data(topologyData);
});

topo.on('topologyGenerated', function() {
  topo.prependLayer('mylayer', 'MyLayer');
})



//create app
var app = new nx.ui.Application();
//attach topo to app;
topo.attach(app);

var topologyData = {
  nodes: [{"y": 21, "x": 277, "id": 0, "name": "C4CB6B600C13"},{"y": 19, "x": 275, "id": 1, "name": "C4CB6B600CC3"},{"y": 30.684364, "x": 400.88367, "id": 2, "name": "C4CB6B600CBF"}]
};
