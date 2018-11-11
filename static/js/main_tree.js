var maintree;

function initialize() {

    var canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        tree = TREE.create("Parent"),
        nodes = TREE.getNodeList(tree),
        currNode = tree,
        add_child_button = document.getElementById("add_child"),
        remove_node = document.getElementById("remove_node");
        
    canvas.addEventListener("click", function (event) {
        var x = event.pageX - canvas.offsetLeft,
            y = event.pageY - canvas.offsetTop;
        for (var i = 0; i < nodes.length; i++) {
            if (x > nodes[i].xPos && x < nodes[i].xPos + nodes[i].width && y > nodes[i].yPos && y < nodes[i].yPos + nodes[i].height) {
                currNode.selected(false);
                nodes[i].selected(true);
                currNode = nodes[i];
                TREE.clear(context);
                TREE.draw(context, tree);
                updatePage(currNode);
                break;
            }
        }
    }, false);

    add_child_button.addEventListener('click', function (event) {
        var person = prompt("Enter The Child's Name");
        if (person == null){
            return;
        }
        currNode.addChild(TREE.create(person));
        currNode.selected(false);
        TREE.clear(context);
        nodes = TREE.getNodeList(tree);
        TREE.draw(context, tree);
    }, false);

    remove_node.addEventListener('click', function (event) {
        TREE.destroy(currNode);
        currNode.selected(false);
        TREE.clear(context);
        nodes = TREE.getNodeList(tree);
        TREE.draw(context, tree);
    }, false);
    
    context.canvas.width = document.getElementById("main").offsetWidth;
    context.canvas.height = document.getElementById("main").offsetHeight;
    nodes = TREE.getNodeList(tree);
    TREE.draw(context, tree);
    maintree = tree;
}

function updatePage(tree) {
    var info_panel = document.getElementById("information_panel");
    var info_panel_html = "Name: "+tree.text;
    info_panel.innerHTML = info_panel_html;
}