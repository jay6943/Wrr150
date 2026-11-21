import cfg
import dev
import voa
import tip
import amzi


def tx_device(x, y):
  amzi.device(x, y)
  tx_voa(x, y)
  return x, y


def tx_voa(x, y):
  xshift = 4600
  df = dev.euler(cfg.wg, cfg.radius, 180)
  x1, y1 = x + cfg.ltip, y + cfg.ch
  x2, y2 = dev.sline(x, y1 + cfg.ch, xshift)
  x3, y3 = dev.sbend(x2, y2, 30, df.dy - cfg.ch)
  x4, y4 = dev.sline(x3, y3, 100)
  x5, y5 = voa.device(x4, y4, 10)
  x6, y6 = dev.sline(x5, y5, 100)
  x7, y7 = dev.bends(x6, y6, 180, 0, 1, -1)
  dev.sline(x7, y7, x1 - x7)

  tip.sline(x1, y1, x, '')
  tip.sline(x1, y1 + cfg.ch, x, 'VOA')


def chip(x, y):
  amzi.test_chips(x, y)
  tx_device(x, y + cfg.ch * 11)
  dev.texts(x + 3700, y + 4200, 'TX', 5, 'cc')


if __name__ == '__main__':
  chip(0, 0)
  dev.saveas(f'tx_{cfg.draft}')
