// @where Java: cw/BarChart.java, in carewell_beans.jar
package cw;

import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import oracle.forms.handler.IHandler;
import oracle.forms.properties.ID;
import oracle.forms.ui.CustomEvent;
import oracle.forms.ui.VBean;

/**
 * A bar chart for a bean area of Oracle Forms.
 *   set_custom_property(item, 1, 'TITLE', 'Bookings in November');
 *   set_custom_property(item, 1, 'DATA',  'Wilson=15;Pillai=12;Menon=9');
 * A click on a bar raises the event BAR_CLICKED, with the parameter BAR_LABEL.
 */
public class BarChart extends VBean {
  private static final ID TITLE       = ID.registerProperty("TITLE");
  private static final ID DATA        = ID.registerProperty("DATA");
  private static final ID BAR_CLICKED = ID.registerProperty("BAR_CLICKED");
  private static final ID BAR_LABEL   = ID.registerProperty("BAR_LABEL");
  private static final Color BAR = new Color(0x28, 0x56, 0xb0);

  private IHandler handler;
  private String title = "";
  private String[] labels = new String[0];
  private double[] values = new double[0];
  private Rectangle[] bars = new Rectangle[0];

  public BarChart() {
    addMouseListener(new MouseAdapter() {
      public void mouseClicked(MouseEvent e) {
        for (int i = 0; i < bars.length; i++) {
          if (bars[i] != null && bars[i].contains(e.getPoint())) {
            try {
              handler.setProperty(BAR_LABEL, labels[i]);   // the event's parameter
            } catch (Exception ignored) { }
            dispatchCustomEvent(new CustomEvent(handler, BAR_CLICKED));
          }
        }
      }
    });
  }

  public void init(IHandler h) {
    super.init(h);
    handler = h;
  }

  public boolean setProperty(ID id, Object value) {
    if (id == TITLE) {
      title = String.valueOf(value);
      repaint();
      return true;
    }
    if (id == DATA) {                                      // label=value;label=value
      String[] pairs = String.valueOf(value).split(";");
      labels = new String[pairs.length];
      values = new double[pairs.length];
      for (int i = 0; i < pairs.length; i++) {
        String[] lv = pairs[i].split("=");
        labels[i] = lv[0];
        values[i] = lv.length > 1 ? Double.parseDouble(lv[1]) : 0;
      }
      repaint();
      return true;
    }
    return super.setProperty(id, value);
  }

  public void paint(Graphics g0) {
    Graphics2D g = (Graphics2D) g0;
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    int w = getWidth(), h = getHeight();
    g.setColor(Color.white);
    g.fillRect(0, 0, w, h);
    g.setColor(Color.darkGray);
    g.setFont(new Font("Dialog", Font.BOLD, 12));
    g.drawString(title, 10, 18);
    double max = 1;
    for (double v : values) max = Math.max(max, v);
    int n = values.length, left = 10, top = 30, bottom = h - 22;
    bars = new Rectangle[n];
    if (n == 0) return;
    int slot = (w - 2 * left) / n;
    g.setFont(new Font("Dialog", Font.PLAIN, 10));
    for (int i = 0; i < n; i++) {
      int bh = (int) ((bottom - top) * values[i] / max);
      bars[i] = new Rectangle(left + i * slot + 4, bottom - bh, slot - 8, bh);
      g.setColor(BAR);
      g.fill(bars[i]);
      g.setColor(Color.darkGray);
      FontMetrics fm = g.getFontMetrics();
      String v = String.valueOf((long) values[i]);
      g.drawString(v, bars[i].x + (bars[i].width - fm.stringWidth(v)) / 2, bars[i].y - 3);
      int lx = bars[i].x + (bars[i].width - fm.stringWidth(labels[i])) / 2;
      g.drawString(labels[i], lx, h - 8);
    }
  }
}
