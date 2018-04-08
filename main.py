import pyglet

class Window(pyglet.window.Window):

  def __init__(self):
    super(Window, self).__init__()
    self.set_size(800, 800)




if __name__ == '__main__':
  widnow = Window()
  pyglet.app.run()