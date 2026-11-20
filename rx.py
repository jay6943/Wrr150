import cfg
import dev
import tip
import amzi


def rx_device(x, y):
  amzi.device(x, y)
  rx_pbs(x, y)
  return x, y


def rx_pbs(x, y):
  xshift = 4600
  dy = 25 - cfg.spbs * 0.5
  df = dev.euler(cfg.wg, cfg.radius, 180)
  x1, y1 = x + cfg.ltip, y + cfg.ch
  x2, y2 = dev.sline(x, y1 + cfg.ch, xshift)
  x3, y3 = dev.sbend(x2, y2, 30, df.dy - cfg.ch)
  x4, y4 = dev.sline(x3, y3, 100)
  x5, y5 = dev.sbend(x4, y4, 5, -dy)
  x6, y6 = dev.sline(x5, y5, cfg.lpbs)
  x7, y7 = dev.sbend(x6, y6, 5, dy)
  x8, y8 = dev.sline(x7, y7, 100)
  x9, y9 = dev.bends(x8, y8, 180, 0, 1, -1)
  dev.sline(x9, y9, x1 - x9)

  x11, y11 = x5, y5 - cfg.spbs
  x12, y12 = dev.sline(x11, y11, cfg.lpbs)
  dev.bends(x11, y11, 5, 0, -1, -1)
  dev.bends(x12, y12, 5, 0, 1, -1)

  tip.sline(x1, y1, x, '')
  tip.sline(x1, y1 + cfg.ch, x, 'PBS')


def chip(x, y):
  amzi.test_chips(x, y)
  rx_device(x, y + cfg.ch * 11)
  dev.texts(x + 6700, y + 4200, 'RX', 5, 'cc')


if __name__ == '__main__':
  chip(0, 0)
  dev.saveas(f'rx_{cfg.draft}')
