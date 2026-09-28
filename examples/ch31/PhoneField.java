// @where Java: cw/PhoneField.java, in carewell_beans.jar
package cw;

import java.awt.Color;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import oracle.forms.ui.VTextField;

/**
 * A pluggable Java component for phone numbers: the text item accepts only digits,
 * '+' and spaces as the user types, and turns amber until the number has ten digits.
 */
public class PhoneField extends VTextField {
  private static final Color INCOMPLETE = new Color(0xff, 0xe8, 0xb0);

  public PhoneField() {
    super();
    addKeyListener(new KeyAdapter() {
      public void keyTyped(KeyEvent e) {
        char c = e.getKeyChar();
        if (!Character.isDigit(c) && c != '+' && c != ' ' && !Character.isISOControl(c)) {
          e.consume();                                   // never reaches the server
        }
      }
      public void keyReleased(KeyEvent e) {
        String digits = getText().replaceAll("[^0-9]", "");
        if (digits.startsWith("91")) digits = digits.substring(2);
        setBackground(digits.length() == 10 ? Color.white : INCOMPLETE);
      }
    });
  }
}
