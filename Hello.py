
import pyjd # this is dummy in pyjs.
from app.Root import Root




if __name__ == '__main__':
    pyjd.setup("public/Hello.html?fred=foo#me")
    app = Root()
    app.start()

    pyjd.run()
