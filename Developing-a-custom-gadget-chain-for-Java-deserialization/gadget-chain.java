import data.productcatalog.ProductTemplate;

import java.io.*;
import java.util.Base64;

class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        ProductTemplate template = new ProductTemplate(args[0]);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(outputStream);
        objectOutputStream.writeObject(template);
        objectOutputStream.flush();
        objectOutputStream.close();
        String newCookie = Base64.getEncoder().encodeToString(outputStream.toByteArray());
        System.out.print(newCookie);
    }
}
