// @where DateMasks.java: gives every date item without a format mask the clinic's format (Chapter 38)
import oracle.forms.jdapi.*;

public class DateMasks {
  public static void main(String[] args) {
    for (String file : args) {
      FormModule form = FormModule.open(file);
      int changed = 0;
      JdapiIterator blocks = form.getBlocks();
      while (blocks.hasNext()) {
        Block block = (Block) blocks.next();
        JdapiIterator items = block.getItems();
        while (items.hasNext()) {
          Item item = (Item) items.next();
          boolean isDate = item.getDataType() == JdapiTypes.DATY_DATE_CTID;
          String mask = item.getFormatMask();
          if (isDate && (mask == null || mask.isEmpty())) {
            item.setFormatMask("DD-MON-YYYY");
            System.out.println("  " + block.getName() + "." + item.getName());
            changed++;
          }
        }
      }
      if (changed > 0) form.save(file);           // compile the form afterwards
      System.out.println(file + ": " + changed + " items changed");
      form.destroy();
    }
    Jdapi.shutdown();
  }
}
