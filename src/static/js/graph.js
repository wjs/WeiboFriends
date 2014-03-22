function WeiboGraph(ele) {
	// var ele = ele = document.getElementById(elementID);
	typeof(ele)=='string' && (ele=document.getElementById(ele));
	var w = ele.clientWidth,
		h = ele.clientHeight,
		self = this;
	this.force = d3.layout.force().gravity(.05)
								.distance(function() { return (Math.random() + 0.6) * 200; })
								.charge(-800).size([w, h]);
	this.nodes = this.force.nodes();
	this.links = this.force.links();
	this.vis = d3.select(ele)
				.append("svg:svg")
             	.attr("width", w)
             	.attr("height", h)
             	.attr("pointer-events", "all");
	
	this.force.on("tick", function(x) {
		self.vis.selectAll('g.node')
				.attr('transform', function(d) { return 'translate('+d.x+','+d.y+')'; });	
		self.vis.selectAll('line.link')
				.attr('x1', function(d) { return d.source.x; })
				.attr('y1', function(d) { return d.source.y; })
				.attr('x2', function(d) { return d.target.x; })
				.attr('y2', function(d) { return d.target.y; });
	});
}

WeiboGraph.prototype.doZoom = function() {
	d3.select(this).select('g')
					.attr('transform', 'translate('+d3.event.translate+') scale('+d3.event.scale+')');
}

WeiboGraph.prototype.addNode = function(node) {
	this.nodes.push(node);
}

WeiboGraph.prototype.addNodes = function(nodes) {
	if (Object.prototype.toString.call(nodes) == '[object Array]') {
		var self = this;
		nodes.forEach(function(node) {
			self.addNode(node);
		});
	}
}

WeiboGraph.prototype.addLink = function(source, target) {
	this.links.push({source: this.findNode(source), 
					target: this.findNode(target)});
}

WeiboGraph.prototype.addLinks = function(links) {
	if (Object.prototype.toString.call(links) == '[object Array]') {
		var self = this;
		links.forEach(function(link) {
			self.addLink(link['source'], link['target']);
		});
	}
}

WeiboGraph.prototype.removeNode = function(uid) {
	var i = 0,
		n = this.findNode(uid),
		links = this.links;
	while (i < links.length) {
		links[i]['source']==n || links[i]['target']==n ? links.splice(i, 1) : ++i;
	}
	this.nodes.splice(this.findNodeIndex(uid), 1);
}

WeiboGraph.prototype.findNode = function(uid) {
	var nodes = this.nodes;
	for (var i in nodes) {
		if (nodes[i]['uid'] == uid)
			return nodes[i];
	}
	return null;
}

WeiboGraph.prototype.findNodeIndex = function(uid) {
	var nodes = this.nodes;
	for (var i in nodes) {
		if (nodes[i]['uid'] == uid)
			return i;
	}
	return -1;
}

WeiboGraph.prototype.update = function() {
	var link = this.vis.selectAll('line.link')
						.data(this.links, function(d) { return d.source.uid + '-' + d.target.uid; })
						.attr('class', function(d) { return 'link'; });

	link.enter().insert('svg:line', 'g.node')
				.attr('class', function(d) { return 'link'; });

	link.exit().remove();

	var node = this.vis.selectAll('g.node')
						.data(this.nodes, function(d) { return d.uid; });

	var nodeEnter = node.enter().append('svg:g')
						.attr('class', 'node')
						.call(this.force.drag);

	nodeEnter.append('svg:image')
			.attr('class', 'circle')
			.attr('xlink:href', function(d) { return "http://ww4.sinaimg.cn/large/412e82dbjw1dsbnxezrrpj.jpg";})
			.attr('x', '-32px')
			.attr('y', '-32px')
			.attr('width', '64px')
			.attr('height', '64px')
			.on('dblclick',function(d){ 
				alert(d.uid);
			})

	nodeEnter.append('svg:text')
			.attr('class', 'nodetext')
			.attr('dx', 15)
			.attr('dy', -35)
			.text(function(d) { return d.nick });

	node.exit().remove();

	this.force.start();
}

/*-- Init global variable ---------------------------------------*/
var weiboGraph = new WeiboGraph('graph');