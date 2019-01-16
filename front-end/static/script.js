var svg_html = "";
var commit_count = 0;
var commits = new Array();
var init_depth = 0

class Commit {
    constructor(message, parent, branch, description){
        // FIXME esta no creo que sea la forma de definir un atributo estático
        Commit.X = 120;
        this.id = commit_count;
        commit_count++;
        this.parent = parent;

        if (this.parent){
            this.parent.add_child(this);
        }

        this.radius = 5;
        this.message = message;
        this.description = description;
        this.branch = branch;
        this.children = new Array();
    }
    set_pos(){
        if (this.parent){
            this.x = this.parent.x - 20 * this.parent.children.indexOf(this);
            this.y = init_depth - 20 * this.id;
        }else{
            this.x = Commit.X
            this.y = init_depth;
        }

    }
    add_child(child){
        this.children.push(child);
    }
    draw() {
        svg_html += `<circle id=commit${this.id} class=commit onmouseenter="showTooltip(evt, commit${this.id}, '${this.description}', '${this.id}');"  onmouseout="hideTooltip();"
        cx= ${this.x} cy= ${this.y} r=${this.radius}
        fill='red'></circle>`

        var font_size = 15;
        var separator = Commit.X  + this.radius*2;
        var width = 0;
        var cumulated_bg_width = 0;
        if (this.branch){
            for (var i=0; i<this.branch.length; i++){
                // Just to know the width of the text
                document.getElementById('dumb_svg').innerHTML = `<text id='dumb_text' font-family="Arial" font-size=font_size>${this.branch[i]}</text>`;
                width = document.getElementById('dumb_text').getBBox().width;

                svg_html += `<rect id=branch_rect x=${separator + cumulated_bg_width} y=${this.y-9} rx="1" ry="1" width=${width*1.1} height=${font_size*1.15}
                style="fill:green;stroke:black;stroke-width:1;opacity:1" />
                <text x=${separator + cumulated_bg_width + font_size*0.2} y=${this.y + this.radius}
                fill="white" font-family="Arial" font-size=font_size>
                ${this.branch[i]}
                </text>`
                separator += font_size;
                cumulated_bg_width += width*1.1;
                }
        }

        svg_html += `<text x=${separator + cumulated_bg_width} y=${this.y + this.radius}
        fill="black" font-family="Arial" font-size="10">
        ${this.message}
        </text>`
    }
}

class Link {
    constructor(c1, c2){
        this.c1=c1;
        this.c2=c2;
        if (c1.x != c2.x){
            this.elbow_x = c2.x;
            this.elbow_y = (c1.y + c2.y) * 0.5;
        }
        else{
            this.elbow_x = null
        }
    }
    draw(){
        if (this.elbow_x == null){
            svg_html += `<line x1=${this.c1.x} y1=${this.c1.y}
            x2=${this.c2.x} y2=${this.c2.y}
            style="stroke:rgb(0,0,0);stroke-width:2" />`
            }
        else{
            svg_html += `<line x1=${this.c1.x} y1=${this.c1.y}
            x2=${this.elbow_x} y2=${this.elbow_y}
            style="stroke:rgb(0,0,0);stroke-width:2" />`
            svg_html += `<line x1=${this.elbow_x} y1=${this.elbow_y}
            x2=${this.c2.x} y2=${this.c2.y}
            style="stroke:rgb(0,0,0);stroke-width:2" />`
        }
    }
}

class ToolTip{
    constructor(){
        this.x = 999;
        this.y = 999;
        this.font_size = 30;
    }
    draw(){
        svg_html += `<rect id=tooltip_rect x="999" y="999" rx="10" ry="10" width="200" height="50"
        style="fill:red;stroke:black;stroke-width:5;opacity:0.9" />
        <text id=tooltip_text x=999 y=999
        fill="black" font-family="Arial" font-size=${this.font_size}>
        GROMENAUER
        </text>`
    }
    move(x, y, message, id){
        document.getElementById('tooltip_text').innerHTML = message;
        var width = document.getElementById('tooltip_text').getBBox().width;
        document.getElementById('tooltip_text').setAttribute('x', x + 30);
        document.getElementById('tooltip_text').setAttribute('y', y + 10);
        document.getElementById('tooltip_rect').setAttribute('x', x + 10);
        document.getElementById('tooltip_rect').setAttribute('y', y - 25);
        document.getElementById('tooltip_rect').setAttribute('width', width+35);
    }
}

var toolTip = new ToolTip();
//toolTip.draw();

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
                commits.push(new Commit(data['message'], null, data['branch'], data['description']));
                }
            else{
                // alert(false);
                commits.push(new Commit(data['message'], commits[data['parent']], data['branch'], data['description']));
            }
        });
        render()
    });
}

function render(){
//    console.log(commits.length);
//    console.log(commits);
//    console.log(commits.length);
    init_depth = 20 * commit_count + 50;
    var first = commits[0];
    first.set_pos();
    draw(first);
    toolTip.draw();
    document.getElementById('svg').innerHTML = svg_html;
    }

function showTooltip(event, object, message, id){
    console.log(id, message);
    toolTip.move(object.cx.animVal.value, object.cy.animVal.value, message)
}

function hideTooltip(){
    toolTip.move(999, 999, 'Gromenauer')
}

read_json();