import prwui
import functools
import time
from prwui.render import h, H, on
# from prwui.page import get_page

div = H('div')
h1 = H('h1')

EXTRA_CSS = '''<style>
.flex_col {
    display: flex;
    flex-direction: column;
}
.flex_row {
    display: flex;
    flex-direction: row;
}
.flex1 {
    flex: 1;
}
</style>'''

FCR = H('div', {'className': 'flex_row'})
FCC = H('div', {'className': 'flex_col'})
FE = H('div', {'className': 'flex1'})

class App(prwui.App):
    def __init__(self):
        self.page = 0

    def handle(self, event):
        if event.get('type') == 'rel_page':
            self.page += event['count']

    def render(self):
        print('render')
        print(self.page)
        return FCC(
            FE(
                FCR(
                    FE('prev', **on.click({'type':'rel_page', 'count':-1})),
                    FE(self.page),
                    FE('next', **on.click({'type':'rel_page', 'count':1})),
                )
            ),
            FE((str(time.time())+', ')*200)
        )



r = prwui.Runner(App)
r.page_manager.add_heading(EXTRA_CSS)
print(r.__dict__)
r.run()