from easygraphics import *

def main():
    init_graph(800, 600)
    img = load_image("images/speedometer_hand.jpg")
    set_render_mode(RenderMode.RENDER_MANUAL)
    x = 0

    while is_run():

        if delay_jfps(60):
            clear_device()
            img.scale(2, 2)
            x += 1

            draw_image((get_width() - img.get_width()) // 2+x,
                       (get_height() - img.get_height()) // 2, img)
    easy_run(main)
    img.close()
    close_graph()

easy_run(main)