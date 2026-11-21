import cfg
import dev
import psw
import voa
import pbs
import tip
import y2x2


def delay(x, y, dx, dy, num):
  radius = cfg.radius
  r1 = dev.euler(cfg.wg, radius, 90)
  r2 = dev.euler(cfg.wg, radius + cfg.dr, 90)
  r3 = dev.euler(cfg.wg, radius + cfg.dr * 0.5, 90)
  d2 = r1.dx - r2.dx + cfg.dr
  d3 = r1.dx - r3.dx + cfg.dr * 0.5
  x1 = x + r2.dx + (num + 0.5) * cfg.dr
  x2 = x1 + dx - d2 * (num - 1)
  
  for i in range(num):
    ch = radius + (i + 1) * cfg.dr + dy
    y1 = y + radius + num * cfg.dr + dy
    for j, cur in enumerate(['in', 'out']):
      dl = [0, cfg.dr * 0.5][j]
      dt = [0, d3][j]
      y2 = y1 - ch - dl
      y3 = y1 + ch + dl
      y4 = y2 + cfg.dr
      x3 = x1 - i * d2 - dt
      x4 = x2 + i * d2 + dt
      cfg.radius = radius + (i + 1) * cfg.dr + dl
      x5, y5 = dev.bends(x4, y2, 90, 0, 1, 1)
      x5, y6 = dev.bends(x4, y3, 90, 0, 1, -1)
      x6, y7 = dev.bends(x3, y3, 90, 0, -1, -1)
      x6, y8 = dev.bends(x3, y4, 90, 0, -1, 1)

      dev.tline(x5, y5, y6 - y5)
      dev.tline(x6, y8, y7 - y8)
      dev.sline(x3, y3, x4 - x3)
      dev.sline(x3, y4, x4 - x3 - d2)

      if 'i' in cur: x11, y11 = x4, y2
      if 'o' in cur: x12, y12 = x4, y2

  # 중심부 오른쪽 내각 곡선 도파로
  cfg.radius = radius
  ch = radius + dy
  x41, y41, y42 = x2 - d2, y1 - ch, y1 + ch
  x43, y43 = dev.bends(x41, y41, 90, 0, 1, 1)
  x44, y44 = dev.bends(x41, y42, 90, 0, 1, -1)
  dev.tline(x43, y43, y44 - y43)
  
  # 중심 곡선 도파로
  dl = cfg.dr * 0.5
  x51 = x1 + dx * 0.5 - x41 + x43
  x52 = x1 + dx * 0.5 + x41 - x43
  y51 = y41 + dl
  x53, y53 = dev.bends(x51, y42, 90, 0, -1, -1)
  x54, y54 = dev.bends(x52, y51, 90, 0, 1, 1)
  dev.sline(x41, y42, x51 - x41)
  dev.tline(x53, y53, y54 - y53)

  # 중심부 왼쪽 및 오른쪽 외각 곡선 도파로
  cfg.radius = radius + dl
  ch = radius + dy + dl
  x61, x62 = x1 + dt, x2 - dt
  y61, y62, y63 = y1 + ch, y1 - ch + dl * 2, y1 - ch
  x65, y65 = dev.bends(x61, y61, 90, 0, -1, -1)
  x66, y66 = dev.bends(x61, y62, 90, 0, -1, 1)
  x67, y67 = dev.bends(x62, y63, 90, 0, 1, 1)
  x68, y68 = dev.bends(x62, y61, 90, 0, 1, -1)
  dev.sline(x52, y51, x61 - x52)
  dev.tline(x66, y66, y65 - y66)
  dev.sline(x61, y61, x62 - x61)
  dev.tline(x67, y67, y68 - y67)

  # 출력 도파로
  i = num - 0.5
  cfg.radius = radius + (i + 1) * cfg.dr + dl
  ch = radius + (i + 1) * cfg.dr + dy
  y72, y73, y74 = y1 - ch - dl, y1 + ch + dl, y2 + dl
  x73, x74 = x1 - i * d2 - dt, x2 + i * d2 + dt
  x75, y75 = dev.bends(x74, y72, 90, 0, 1, 1)
  x75, y76 = dev.bends(x74, y73, 90, 0, 1, -1)
  x76, y77 = dev.bends(x73, y73, 90, 0, -1, -1)
  x76, y78 = dev.bends(x73, y74, 90, 0, -1, 1)
  dev.tline(x75, y75, y76 - y75)
  dev.tline(x76, y77, y78 - y77)
  dev.sline(x73, y73, x74 - x73)

  # 정렬 도파로
  i = num
  cfg.radius = radius + (i + 1) * cfg.dr + dl
  ch = radius + (i + 1) * cfg.dr + dy
  y83 = y1 + ch + dl
  x83, x84 = x1 - i * d2 - dt, x2 + i * d2 + dt
  x85, y85 = dev.bends(x84, y83, 90, 0, 1, -1)
  x86, y86 = dev.bends(x83, y83, 90, 0, -1, -1)
  dev.sline(x83, y83, x84 - x83)

  xp = [x11, x73, x12, x74, x85, x86]
  yp = [y11, y74, y12, y72, y85, y86]

  cfg.radius = radius

  return xp, yp


def device(x, y):
  # 정렬 도파로
  xstart = x + cfg.ltip
  x10, y10 = dev.bends(xstart, y + cfg.ch * 6, 90, 0, 1, 1)

  # 광 스위치
  angle, dy = 10, cfg.ch * 2
  dy2x2 = cfg.ch * 0.5 - cfg.s2x2
  x21, _ = dev.sbend(xstart, y + cfg.ch * 5, 30, dy2x2 + dy)
  x31, y31, y32 = psw.device(x21, y + cfg.ch * 5.5 + dy)
  x33, y33 = dev.sbend(x31, y32, angle, -dy2x2)
  x34, y34 = dev.bends(x31, y31, 180, 0, 1, 1)
  dev.bends(x21, y31, 5, 0, -1, 1)

  # delay line
  xp, yp = delay(x10, y34, 5000, 200, 6)

  # 광 스위치 to delay line
  io_angle = 30
  x35, y35 = dev.sline(x33, y33, 100)
  x36, y36 = dev.sbend(x35, y35, io_angle, y34 - y35)

  # 출력단 2x2 MMI
  angle, dl = 10, cfg.dr * 0.5
  x51, _ = dev.sbend(xstart, y + cfg.ch * 3, angle, dy2x2)
  x51, _ = dev.sbend(xstart, y + cfg.ch * 4, angle, -dy2x2)
  x52, y51, y52 = y2x2.device(x51, y + cfg.ch * 3.5)
  x53, y53 = dev.sbend(x52, y51, angle, dy2x2)
  x53, y54 = dev.sbend(x52, y52, angle, -dy2x2)
  x54, _ = dev.sline(x53, y53, x33 - x53)
  x55, _ = dev.sline(x53, y54, x33 - x53)
  x56, y56 = dev.sbend(x54, y53, io_angle, yp[0] - y53 - dl)
  x57, y57 = dev.sbend(x55, y54, io_angle, yp[0] - y54 - dl * 2)
  dev.electrode((x57 + xp[0] - cfg.lpad) * 0.5, y57, -1)

  # 정렬 도파로
  df = dev.euler(cfg.wg, cfg.radius, 90)
  x61, y61 = xp[4] - df.dx, y
  x62, y62 = dev.bends(x61, y61, 90, 0, 1, 1)
  dev.sline(xstart, y61, x61 - xstart)
  dev.tline(x62, y62, yp[4] - y62)

  # 연결 도파로
  dev.sline(x36, y36, xp[0] - x36)
  dev.sline(x34, y34, xp[1] - x34)
  dev.sline(x56, y56, xp[2] - x56)
  dev.sline(x57, y57, xp[3] - x57)
  dev.tline(x10, y10, yp[4] - y10)

  # 입출력 도파로
  tip.sline(xstart, y + cfg.ch * 3, x, '')
  tip.sline(xstart, y + cfg.ch * 4, x, 'Outputs')
  tip.sline(xstart, y + cfg.ch * 5, x, 'Input')
  tip.sline(xstart, y, x, 'Align')
  tip.sline(xstart, y + cfg.ch * 6, x, 'Align')

  return x, y


def test_voa(x, y):
  dy = cfg.ch * 3
  x1, y1 = x + 3000, y
  x2, y2 = dev.sbend(x1, y1, 30, -dy)
  x3, y3 = voa.device(x2, y2)
  x4, y4 = dev.sbend(x3, y3, 30, dy)

  tip.sline(x1, y1, x, 'VOA')
  tip.sline(x4, y1, x + cfg.lchip, 'VOA')


def test_chips(x, y):
  voa.chip(x, y, x + 2000, 10)
  psw.chip(x, y + cfg.ch * 4, x + 3000, 10)
  pbs.chip(x, y + cfg.ch * 8, cfg.lchip)
  dev.sline(x, y + cfg.ch * 9, cfg.lchip)
  tip.chip(x, y + cfg.ch * 10, cfg.lchip)


if __name__ == '__main__':
  # delay(0, 0, 5000, 200, 6)
  device(0, 0)
  dev.saveas(f'delay_{cfg.draft}')
