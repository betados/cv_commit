var svg_html = "";
var commit_count = 0;
var commits = new Array();
var init_depth = 0

class Commit {
    constructor(message, parent){
        this.id = commit_count;
        commit_count++;
        this.parent = parent;

        if (this.parent){
            this.parent.add_child(this);
        }

        this.radius = 5;
        this.message = message;
        this.children = new Array();
    }
    set_pos(){
        if (this.parent){
            this.x = this.parent.x - 20 * this.parent.children.indexOf(this);
            this.y = init_depth - 20 * this.id;
        }else{
            this.x = 40
            this.y = init_depth;
        }

    }
    add_child(child){
        this.children.push(child);
    }
    draw() {
        svg_html += `<circle id=commit${this.id} class=commit onmouseenter="showTooltip(evt, commit${this.id}, '${this.message}');"  onmouseout="hideTooltip();"
        cx= ${this.x} cy= ${this.y} r=${this.radius}
        fill='red'></circle>`

        // FIXME font-family not working
        svg_html += `<text x=${40  + this.radius*2} y=${this.y + this.radius}
        fill="black" font-family="Calibri" font-size="10">
        ${this.message}
        </text>`
    }
}

class Link {
    constructor(c1, c2){
        this.c1=c1;
        this.c2=c2;
    }
    draw(){
        svg_html += `<line x1=${this.c1.x} y1=${this.c1.y}
        x2=${this.c2.x} y2=${this.c2.y}
        style="stroke:rgb(0,0,0);stroke-width:2" />`
    }
}

class ToolTip{
    constructor(){
        this.x = 999;
        this.y = 999;
    }
    draw(){
        svg_html += `<rect id=rect x="999" y="999" rx="10" ry="10" width="200" height="50"
        style="fill:red;stroke:black;stroke-width:5;opacity:0.5" />
        <text id=text x=999 y=999
        fill="black" font-family="Calibri" font-size="30">
        GROMENAUER
        </text>`
    }
    move(x, y, message){
//        print(document.getElementById('text'))
        document.getElementById('text').innerHTML = message;
        document.getElementById('text').setAttribute('x', x + 30);
        document.getElementById('text').setAttribute('y', y + 10);
        document.getElementById('rect').setAttribute('x', x + 10);
        document.getElementById('rect').setAttribute('y', y - 25);
        document.getElementById('rect').setAttribute('width', (message.length+4) * 13);
    }
}

function draw(last) {
    for (var i=0; i<last.children.length; i++){
        last.children[i].set_pos();
        new Link(last, last.children[i]).draw();
        draw(last.children[i]);
    }
    last.draw();
}

function read_json(){
    jQuery.support.cors = true;
    return $.getJSON("static/commits.json", function(json) {
       jQuery.each(eval(json), function(name, data){
            //  alert( name + ": " + data['message'] +','+data['parent']);
            if (data['parent'] == null){
                // alert(true);
                commits.push(new Commit(data['message'], null));
                }
            else{
                // alert(false);
                commits.push(new Commit(data['message'], commits[data['parent']]));
            }
        });

    });
}

read_json();
var toolTip = new ToolTip();
toolTip.draw();

window.onload = function(){
    console.log(commits)

    // Waiting for the read_json() to finish
    //alert('Reading');

    init_depth = 20 * commit_count + 50;
    var first = commits[0];

    first.set_pos();
    draw(first);


    document.getElementById('svg').innerHTML = svg_html;
}

function showTooltip(event, object, message){
    console.log(message);
    toolTip.move(object.cx.animVal.value, object.cy.animVal.value, message)
}

function hideTooltip(){
    toolTip.move(999, 999, 'Gromenauer')
}
