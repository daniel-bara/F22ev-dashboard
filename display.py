import pygame
import multiprocessing
pygame.init()


DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 750



clock = pygame.time.Clock()

CAN_MESSAGES_POS = (350, 450)
CAN_MESSAGES_DIM = (500, 300)

LAP_INFO_POS = (470, 100)

SPEED_POS = (920, 500)
POWER_OUTPUT_POS = (100, 500)
BATT_CHG_POS = (800, 250)
BATT_TMP_POS = (0, 250)

BATT_CHG_COL = pygame.Color('white')
BATT_TMP_COL = pygame.Color('orange')
SPEED_COL = pygame.Color('white')
POWER_OUTPUT_COL = pygame.Color('orange')
LAP_INFO_COL = pygame.Color("white")

FPS_FONT = pygame.font.SysFont("Arial", 18)
BATT_CHG_FONT = pygame.font.SysFont("lucida console", 178)
BATT_CHG_UNIT_FONT = pygame.font.SysFont("lucida sans", 42)
BATT_TMP_FONT = pygame.font.SysFont("lucida console", 178)
BATT_TMP_UNIT_FONT = pygame.font.SysFont("lucida sans", 42)
SPEED_FONT = pygame.font.SysFont("lucida console", 75)
SPEED_UNIT_FONT = pygame.font.SysFont("lucida sans", 38)
POWER_OUTPUT_FONT = pygame.font.SysFont("lucida console", 75)
POWER_OUTPUT_UNIT_FONT = pygame.font.SysFont("lucida sans", 38)
LAP_INFO_FONT = pygame.font.SysFont("lucida sans", 45)
CAN_MSG_FONT = pygame.font.SysFont("leelawadee ui", 18)

CAN_MESSAGES_LINE_SPACING = 22
CAN_MESSAGES_PADDING = 5
MAX_CAN_MESSAGE_COUNT = 13

LAP_INFO_SPACING = 55


class Fps:
    def __init__(self):
        self.fps_moving_avg = 0

    def update(self):
        self.fps_moving_avg = self.fps_moving_avg * 0.997 + int(clock.get_fps()) * 0.003
        fps = str(int(self.fps_moving_avg))
        fps_text = FPS_FONT.render(fps, True, pygame.Color("white"))
        return fps_text


class LapCounter:
    def __init__(self):
        self.total_laps = 21
        self.current_lap = 8


class CanDisplay:
    """collects CAN bus messages
    newer messages are at lower index"""

    def __init__(self, max_message_count: int):
        self.messages = []
        self.max_message_count = max_message_count

    def insert(self, message: str):
        self.messages.insert(0, message)
        self.cap_max()

    def cap_max(self):
        while len(self.messages) > self.max_message_count:
            self.messages.pop()

    def get_messages(self):
        return self.messages


class Display:
    def __init__(self):
        self.fps_counter = Fps()
        self.lap_counter = LapCounter()
        self.can_display = CanDisplay(MAX_CAN_MESSAGE_COUNT)
        self.stopped = False
        self.power_output = 5
        self.battery_temperature = 70
        self.battery_charge = 68
        self.speed = 43
        self.power_consumption_feedback_total = 3
        self.power_consumption_feedback_average = -2

    def process_message(self, msg):
        if msg.variable == "CAN":
            self.can_display.insert(msg.value)
        else:
            setattr(self, msg.variable, msg.value)

    def run(self, queue: multiprocessing.Queue):
        gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        while not self.stopped:

            if not queue.empty():
                self.process_message(queue.get())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopped = True
            gameDisplay.fill((0, 10, 10))

            # battery charge

            gameDisplay.blit(BATT_CHG_FONT.render(str(int(self.battery_charge)).rjust(3, " "), True, BATT_CHG_COL), BATT_CHG_POS)
            gameDisplay.blit(BATT_CHG_UNIT_FONT.render("%", True, BATT_CHG_COL), (BATT_CHG_POS[0] + 320, BATT_CHG_POS[1] + 98))

            # battery temperature

            gameDisplay.blit(BATT_TMP_FONT.render(str(int(self.battery_temperature)).rjust(3, " "), True, BATT_TMP_COL),
                             BATT_TMP_POS)
            gameDisplay.blit(BATT_TMP_UNIT_FONT.render("°C", True, BATT_TMP_COL), (BATT_TMP_POS[0] + 325, BATT_TMP_POS[1] + 95))

            # speed

            gameDisplay.blit(SPEED_FONT.render(str(int(self.speed)).rjust(3, " "), True, SPEED_COL), SPEED_POS)
            gameDisplay.blit(SPEED_UNIT_FONT.render("mph", True, SPEED_COL), (SPEED_POS[0] + 140, SPEED_POS[1] + 20))

            # power output

            gameDisplay.blit(POWER_OUTPUT_FONT.render(str(int(self.power_output)).rjust(3, " "), True, POWER_OUTPUT_COL),
                             POWER_OUTPUT_POS)
            gameDisplay.blit(POWER_OUTPUT_UNIT_FONT.render("kW", True, POWER_OUTPUT_COL),
                             (POWER_OUTPUT_POS[0] + 138, POWER_OUTPUT_POS[1] + 21))

            # lap info
            gameDisplay.blit(
                LAP_INFO_FONT.render(str(self.lap_counter.current_lap).rjust(2, " ") + " / " + str(self.lap_counter.total_laps) + " laps",
                                     True, LAP_INFO_COL), LAP_INFO_POS)

            power_consumption_feedback_average_text = ("+" * (self.power_consumption_feedback_average >= 1)) + \
                                                      str(int(self.power_consumption_feedback_average))
            gameDisplay.blit(LAP_INFO_FONT.render("AVG   " + power_consumption_feedback_average_text + "%",
                                                  True, LAP_INFO_COL), (LAP_INFO_POS[0], LAP_INFO_POS[1] + LAP_INFO_SPACING))


            power_consumption_feedback_total_text = ("+" * (self.power_consumption_feedback_total >= 1)) + \
                                                    str(int(self.power_consumption_feedback_total))
            gameDisplay.blit(LAP_INFO_FONT.render("LAST " + power_consumption_feedback_total_text + "%",
                                                  True, LAP_INFO_COL),
                             (LAP_INFO_POS[0], LAP_INFO_POS[1] + LAP_INFO_SPACING * 2))

            # CAN messages
            r = pygame.rect.Rect(*CAN_MESSAGES_POS, *CAN_MESSAGES_DIM)
            pygame.draw.rect(gameDisplay, pygame.Color("white"), r, 1)

            for i, m in enumerate(self.can_display.get_messages()):
                gameDisplay.blit(CAN_MSG_FONT.render(m, True, pygame.Color('white')),
                                 (CAN_MESSAGES_POS[0] + CAN_MESSAGES_PADDING,
                                  CAN_MESSAGES_POS[1] + CAN_MESSAGES_DIM[1] -
                                  CAN_MESSAGES_LINE_SPACING * i - CAN_MESSAGES_PADDING - 30))

            gameDisplay.blit(self.fps_counter.update(), (10, 0))

            pygame.display.update()
            clock.tick()

        pygame.quit()
        quit()


class Graph:
    pass

if __name__ == "__main__":
    d = Display()
    d.battery_charge = -50
    d.run(multiprocessing.Queue())