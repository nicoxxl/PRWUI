import prwui
import functools
import time
from prwui.render import h, H, on
try:
    import psutil
except ModuleNotFoundError:
    print('Need psutils')
    import sys; sys.exit(1)

EXTRA_CSS = '''<style>
body {
    background: black;
    color: green;
    font-family: monospace;
}

table {
    border-collapse: collapse;
}

th {
    text-align: left;
} 
th, td {
    padding: 5px;
}

table, th, td, button {
    border: 1px solid green;
}
button {
    background: #010;
    color: green;
}
</style>'''



class App(prwui.App):
    def __init__(self):
        self.state = {}
        self.cols = ['pid', 'name', 'username', 'nice', 'cmdline']

    def handle(self, event):
        assert 'type' in event, 'No "type" in event'
        if event['type'] == 'refresh':
            pass

    def render(self):
        return h('div', {}, h('button', {**on.click({'type':'refresh'})}, 'refresh'), h('br', {}), h('br', {}), self.process_table())

    def process_table(self):

        return h('table', {}, 
            # h('tr', {}, h('td', {**on.click({'type':'nop'})}, time.time())),
            h('tr', {},
                *(h('th', {}, col) for col in self.cols)
            ),
            *self.process_rows()
        )

    def process_rows(self):
        attrs = self.cols
        for process in psutil.process_iter(attrs=attrs):
            yield h('tr', {}, 
                *(h('td', {}, self.strify(process.info[atr])) for atr in attrs)
            )
    def strify(self, obj):
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, (list, tuple)):
            return ' '.join(obj)
        else:
            return str(obj)


r = prwui.Runner(App)
r.page_manager.add_heading(EXTRA_CSS)
print(r.__dict__)
r.run()
