// @where FormInventory.java: lists the blocks, items, and triggers of forms (Chapter 38)
import oracle.forms.jdapi.*;

public class FormInventory {
  public static void main(String[] args) {
    Jdapi.setFailLibraryLoad(false);                 // report, even if a library is missing
    Jdapi.setFailSubclassLoad(false);
    for (String file : args) {
      FormModule form = FormModule.open(file);
      int triggers = count(form.getTriggers());
      System.out.println(form.getName() + "  (" + triggers + " form-level triggers)");
      JdapiIterator blocks = form.getBlocks();
      while (blocks.hasNext()) {
        Block block = (Block) blocks.next();
        int items = 0, itemTriggers = 0;
        JdapiIterator it = block.getItems();
        while (it.hasNext()) {
          itemTriggers += count(((Item) it.next()).getTriggers());
          items++;
        }
        String source = block.getQueryDataSourceName();
        System.out.printf("  %-14s %-14s %3d items %3d triggers%n", block.getName(),
            source == null || source.isEmpty() ? "-" : source, items, count(block.getTriggers()) + itemTriggers);
      }
      form.destroy();
    }
    Jdapi.shutdown();
  }

  static int count(JdapiIterator objects) {
    int n = 0;
    while (objects.hasNext()) { objects.next(); n++; }
    return n;
  }
}
