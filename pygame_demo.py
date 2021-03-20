import pygame

pygame.init()

DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 750

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# black = (0, 0, 0)
# white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
CAN_MESSAGES_POS = (350, 450)
CAN_MESSAGES_DIM = (500, 300)

BATT_CHG_POS = (1000, 300)
BATT_TMP_POS = (950, 450)
SPEED_POS = (100, 300)
POWER_OUTPUT_POS = (100, 450)
LAP_INFO_POS = (400, 50)

BATT_CHG_COL = pygame.Color('white')
BATT_TMP_COL = pygame.Color('orange')
SPEED_COL = pygame.Color('white')
POWER_OUTPUT_COL = pygame.Color('orange')
LAP_INFO_COL = pygame.Color("white")

FPS_FONT = pygame.font.SysFont("Arial", 18)
BATT_CHG_FONT = pygame.font.SysFont("Arial", 68)
BATT_TMP_FONT = pygame.font.SysFont("Arial", 42)
CAN_MSG_FONT = pygame.font.SysFont("leelawadee ui", 18)
SPEED_FONT = pygame.font.SysFont("lucida sans", 78)
MPH_FONT = pygame.font.SysFont("lucida sans", 42)
POWER_OUTPUT_FONT = pygame.font.SysFont("Arial", 68)
LAP_INFO_FONT = pygame.font.SysFont("Arial", 32)

CAN_MESSAGES_LINE_SPACING = 22
CAN_MESSAGES_PADDING = 5


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


fps_counter = Fps()
lap_counter = LapCounter()
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    gameDisplay.fill((0, 10, 10))

    r = pygame.rect.Rect(*CAN_MESSAGES_POS, *CAN_MESSAGES_DIM)
    pygame.draw.rect(gameDisplay, pygame.Color("white"), r, 1)

    battery_charge = 68
    gameDisplay.blit(BATT_CHG_FONT.render(str(int(battery_charge)) + "%", True, BATT_CHG_COL), BATT_CHG_POS)

    battery_temperature = 115
    gameDisplay.blit(BATT_CHG_FONT.render(str(int(battery_temperature)) + " °C", True, BATT_TMP_COL), BATT_TMP_POS)

    speed = 43
    gameDisplay.blit(SPEED_FONT.render(str(int(speed)).rjust(3, " ") , True, SPEED_COL), SPEED_POS)
    gameDisplay.blit(MPH_FONT.render("mph", True, SPEED_COL), (SPEED_POS[0]+130, SPEED_POS[1]+40))

    power_output = 5
    gameDisplay.blit(BATT_CHG_FONT.render(str(int(power_output)) + " kW", True, POWER_OUTPUT_COL), POWER_OUTPUT_POS)

    # lap info
    gameDisplay.blit(LAP_INFO_FONT.render(str(lap_counter.current_lap) + " / " + str(lap_counter.total_laps) + " laps",
                                          True, LAP_INFO_COL), LAP_INFO_POS)
    power_consumption_feedback_average = -2
    power_consumption_feedback_average_text = ("+" * (power_consumption_feedback_average >= 1)) + \
                                              str(int(power_consumption_feedback_average))
    gameDisplay.blit(LAP_INFO_FONT.render("AVG   " + power_consumption_feedback_average_text + "%",
                                          True, LAP_INFO_COL), (LAP_INFO_POS[0], LAP_INFO_POS[1]+40))

    power_consumption_feedback_total = 3
    power_consumption_feedback_total_text = ("+" * (power_consumption_feedback_total >= 1)) + \
                                            str(int(power_consumption_feedback_total))
    gameDisplay.blit(LAP_INFO_FONT.render("LAST " + power_consumption_feedback_total_text + "%",
                                          True, LAP_INFO_COL), (LAP_INFO_POS[0], LAP_INFO_POS[1]+80))

    can_messages = ["Ready to drive mode active", "Powerup started"]
    for i, m in enumerate(can_messages):
        gameDisplay.blit(CAN_MSG_FONT.render(m, True, pygame.Color('white')),
                         (CAN_MESSAGES_POS[0] + CAN_MESSAGES_PADDING,
                          CAN_MESSAGES_POS[1] + CAN_MESSAGES_LINE_SPACING * i + CAN_MESSAGES_PADDING))

    gameDisplay.blit(fps_counter.update(), (10, 0))

    pygame.display.update()
    clock.tick()

pygame.quit()
quit()


class Graph:
    pass
