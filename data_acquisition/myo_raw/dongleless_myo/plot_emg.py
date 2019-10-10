# def plot(arg):
# 	try:
# 		import pygame
# 		from pygame.locals import *
# 		HAVE_PYGAME = True
# 	except ImportError:
# 		HAVE_PYGAME = False
#
# 	if HAVE_PYGAME:
# 		w, h = 1200, 400
# 		scr = pygame.display.set_mode((w, h))
#
# 		last_vals = None
# def plot(scr, vals):
# 	DRAW_LINES = True
#
# 	global last_vals
# 	if last_vals is None:
# 		last_vals = vals
# 		return
#
# 	D = 5
# 	scr.scroll(-D)
# 	scr.fill((0,0,0), (w - D, 0, w, h))
# 	for i, (u, v) in enumerate(zip(last_vals, vals)):
# 		if DRAW_LINES:
# 			pygame.draw.line(scr, (0,255,0),
# 				(w - D, int(h/8 * (i+1 - u))),
# 				(w, int(h/8 * (i+1 - v))))
# 			pygame.draw.line(scr, (255,255,255),
# 				(w - D, int(h/8 * (i+1))),
# 				(w, int(h/8 * (i+1))))
# 		else:
# 			c = int(255 * max(0, min(1, v)))
# 			scr.fill((c, c, c), (w - D, i * h / 8, D, (i + 1) * h / 8 - i * h / 8));
#
# 	pygame.display.flip()
# 	last_vals = vals

	#m = MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
