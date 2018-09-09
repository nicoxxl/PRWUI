MAGIC_JS = '''setTimeout(function() {
    var ws = new WebSocket("ws://127.0.0.1:8080/ws");
    var root = document.getElementsByTagName("body")[0];
    // var old_node = {type:'div', props:{id:'app'}, children:['']};
    var old_node = undefined;
    var t_ev = performance.now();
    function event_manager(e) {
        // console.log('event_manager');
        // console.log(e);
        // console.log(this);
        // console.log('__'+e.type);
        let data = this.getAttribute('__'+e.type)
        // console.log(data);
        ws.send(data);
        t_ev = performance.now();
    }

    function is_custom_prop(name) {
        return (name[0]==='o' && name[1]==='n');
    }

    function set_prop(target, name, value) {
        if (is_custom_prop(name)) {
            // Event
            if (name[0]==='o' && name[1]==='n') {
                let event_name = name.slice(2).toLowerCase();
                target.setAttribute('__'+event_name, value);
                target.addEventListener(event_name, event_manager);
            }
            return;
        } else if (name === 'className') {
            target.setAttribute('class', value);
        } else if (typeof value === 'boolean') {
            if (value) {
                target.setAttribute(name, value);
                target[name] = true;
            } else {
                target[name] = false;
            }
        } else {
            target.setAttribute(name, value);
        }
    }

    function remove_prop(target, name) {
        if (is_custom_prop(name)) {
            return;
        } else if (name === 'className') {
            target.removeAttribute('class');
        } else if (typeof value === 'boolean') {
            target.removeAttribute(name);
            target[name] = false;
        } else {
            target.removeAttribute(name);
        }
    }

    function set_props(target, props) {
        Object.keys(props).forEach(name => {
            set_prop(target, name, props[name]);
        });
    }

    function create_element(node) {
        // console.debug('create_element', node);
        if (typeof node === 'string' || typeof node === 'number') {
            return document.createTextNode(node);
        }
        const element = document.createElement(node.type);
        set_props(element, node.props || {});
        if (node.children.length) {
            node.children.map(create_element).forEach(element.appendChild.bind(element));
        }
        return element;
    }

    function update_prop(target, name, new_val, old_val) {
        if (new_val===undefined) {
            remove_prop(target, name);
        } else if (!old_val || new_val !== old_val) {
            set_prop(target, name, new_val);
        }
    }

    function update_props(target, new_props, old_props) {
        const props = Object.assign({}, new_props, old_props);
        Object.keys(props).forEach(name => {
            update_prop(target, name, new_props[name], old_props[name]);
        });
    }

    function update_element(parent, new_node, old_node, index = 0) {
        // console.debug('update_element', {parent, new_node, old_node, index});
        if (old_node  === undefined) {
            // console.log('update_element', 'no old nide', old_node, new_node);
            parent.appendChild(create_element(new_node));
        } else if (new_node === undefined) {
            // console.log('update_element', 'no new node');
            parent.removeChild(
                parent.childNodes[index]
            )
        } else if (changed(new_node, old_node)) {
            // console.log('update_element', 'node changed', create_element(new_node), parent.childNodes[index]);
            parent.replaceChild(create_element(new_node), parent.childNodes[index]);
        } else if (new_node.type) {
            update_props(
                parent.childNodes[index],
                new_node.props,
                old_node.props
            );

            const new_length = new_node.children.length || 0;
            const old_length = old_node.children.length || 0;
            for (let i = 0; i < new_length || i < old_length; i++) {
                const new_child = new_node.children[i];
                const old_child = old_node.children[i];
                // console.log('update_element', 'i=',i,',',new_child, old_child);
                update_element(
                    parent.childNodes[index],
                    new_child,
                    old_child,
                    i
                );
            }
        }
    }

    function changed(node1, node2) {
        if (typeof node1 !== typeof node2) {
            // console.debug('changed', 'typeof');
            return true;
        } 
        if ((typeof node1 === 'string' || typeof node1 === 'number') && node1 !== node2) {
            // console.debug('changed', 'string');
            return true;
        }
        if (node1.type !== node2.type) {
            // console.debug('changed', 'type');
            return true;
        }
        return false;
    }


    ws.onopen = function() {
        ws.send(JSON.stringify(
            {
                type: '@@browser/init',
            }
        ));
    }
    ws.onmessage = function (evt) { 
        var t0 = performance.now();
        var received_msg = evt.data;
        // console.log(received_msg);
        new_node = JSON.parse(received_msg);
        console.log('---------------------------');
        console.log(new_node);
        update_element(root, new_node, old_node);
        old_node = new_node;
        var t1 = performance.now();
        console.log('timing', t1-t0, t1-t_ev);
    };
    ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        ws.close();
    };
    /* 
    setInterval(function() {
        t_ev = performance.now();
        ws.send('{}');
        console.log('plop');
    }, 300);/* */
});'''

class PageManager:
    def __init__(self, extra_heading=None):
        if extra_heading is None:
            extra_heading = []
        self.extra_heading = extra_heading
    
    def __call__(self):
        return '''<html><head>
<script>
{js}
</script>
{head}
</head><body></body></html>'''.format(js=MAGIC_JS, head='\n'.join(self.extra_heading))

    def add_heading(self, heading):
        self.extra_heading.append(heading)